import os
import sys
import subprocess
import zipfile
import requests
import shutil
import ctypes
import win32com.client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSettings, QVariantAnimation, pyqtSignal, pyqtProperty

# Pfad zum SysinternalsSuite-Ordner
SUITE_FOLDER = "SysinternalsSuite2"
ZIP_URL = "https://download.sysinternals.com/files/SysinternalsSuite.zip"
ZIP_NAME = "SysinternalsSuite.zip"

# Einstellungen: Sprache, Theme und weitere Checkbox-Einstellungen werden mittels QSettings gespeichert.
SETTINGS = QSettings("SysinternalsGUI", "Language")

# Übersetzungen (beide Sprachen inkl. neuer Schlüssel)
TRANSLATIONS = {
    'de': {
        'title': "Sysinternals Suite GUI",
        'search_placeholder': "Suche nach Programmen oder Beschreibungen...",
        'start_button': "Starten",
        'other_programs': "Andere Programme",
        'language_label': "Sprache:",
        'theme_label': "Dunkelmodus",
        'error_file_not_found': "Die Datei existiert nicht:\n{}",
        'error_program_start': "Beim Starten des Programms ist ein Fehler aufgetreten:\n{}",
        'shortcut_created': "Shortcut erstellt:\n{}",
        'error_shortcut': "Fehler beim Erstellen des Shortcuts:\n{}",
        'add_additional_programs': "Zusätzliche Programme hinzufügen",
        'add_additional_programs_tooltip': "WizTree, Windhawk, ...",
        'always_run_as_admin': "Mit Administratorrechten starten",
        'always_run_as_admin_tooltip': "Programme immer mit Windows Administrator-Rechten starten",
        'wiztree_desc': "Portables Festplattenscan-Tool für die schnelle Ansicht von Verzeichnissen und Dateien.",
        'wiztree64_desc': "WizTree 64-Bit Version – optimiert für 64‑Bit Systeme.",
        'windhawk_desc': (
            "Windhawk zielt darauf ab, die Anpassung von Windows-Programmen zu erleichtern. "
            "Es ermöglicht die Installation und Konfiguration von Mods (Anpassungsmodulen) mit nur wenigen Klicks. "
            "Für Entwickler bietet es eine bequeme Plattform zum Entwickeln und Teilen solcher Mods. "
            "Weitere Details und den Download finden Sie auf der offiziellen Website."
        ),
        'powertoys_desc': "Microsoft Powertoys – Eine Sammlung nützlicher Dienstprogramme zur Optimierung und Erweiterung von Windows.",
        'wireshark_desc': "Wireshark – Netzwerkprotokoll-Analysetool zur detaillierten Untersuchung des Datenverkehrs.",
        'recuva_desc': "Recuva – Wiederherstellungsprogramm zur Wiederherstellung gelöschter Dateien.",
        'fileshredder_desc': "File Shredder – Sicheres Löschen von Dateien, um Daten unwiederbringlich zu entfernen.",
        # Neue Schlüssel für die System32-Checkbox
        'system32_programs': "System32-Programme anzeigen",
        'system32_programs_tooltip': "Alle .exe und .msc Programme aus dem System32 Ordner anzeigen (automatisch ermittelt)."
    },
    'en': {
        'title': "Sysinternals Suite GUI",
        'search_placeholder': "Search for programs or descriptions...",
        'start_button': "Start",
        'other_programs': "Other Programs",
        'language_label': "Language:",
        'theme_label': "Dark Mode",
        'error_file_not_found': "File not found:\n{}",
        'error_program_start': "Error starting program:\n{}",
        'shortcut_created': "Shortcut created:\n{}",
        'error_shortcut': "Error creating shortcut:\n{}",
        'add_additional_programs': "Add Additional Programs",
        'add_additional_programs_tooltip': "WizTree, Windhawk, ...",
        'always_run_as_admin': "Always run as admin",
        'always_run_as_admin_tooltip': "Always start programs with Windows Administrator privileges",
        'wiztree_desc': "Portable disk scanning tool for quick folder and file viewing.",
        'wiztree64_desc': "WizTree 64-bit version – optimized for 64-bit systems.",
        'windhawk_desc': (
            "Windhawk aims to make it easier to customize Windows programs. It allows installing "
            "and configuring mods with just a couple of clicks. More details and the download are available on the official website."
        ),
        'powertoys_desc': "Microsoft Powertoys – A set of utilities to optimize and enhance Windows.",
        'wireshark_desc': "Wireshark – A network protocol analyzer for detailed traffic inspection.",
        'recuva_desc': "Recuva – A file recovery tool to restore deleted files.",
        'fileshredder_desc': "File Shredder – Secure file deletion to permanently remove data.",
        # Neue Schlüssel für die System32-Checkbox
        'system32_programs': "Show System32 Programs",
        'system32_programs_tooltip': "Display all .exe and .msc programs from the System32 folder (automatically determined)."
    }
}

# Hier sind die Übersetzungen (Beschreibungen) für bekannte System32-Programme
SYSTEM32_DESCRIPTIONS = {
    # .msc Dateien (Microsoft Management Console)
    "adsiedit.msc": {
        "de": "Verwaltet und bearbeitet Active Directory-Objekte.",
        "en": "Manages and edits Active Directory objects."
    },
    "azman.msc": {
        "de": "Verwaltet die Autorisierungsverwaltung in Windows.",
        "en": "Manages Authorization Manager in Windows."
    },
    "certlm.msc": {
        "de": "Verwaltet Zertifikate auf lokalen Computern.",
        "en": "Manages certificates on local computers."
    },
    "certmgr.msc": {
        "de": "Verwaltet Zertifikate für Benutzerkonten.",
        "en": "Manages certificates for user accounts."
    },
    "comexp.msc": {
        "de": "Verwaltet COM+-Anwendungen und -Komponenten.",
        "en": "Manages COM+ applications and components."
    },
    "compmgmt.msc": {
        "de": "Zentrale Verwaltung von Systemtools, Speicher und Diensten.",
        "en": "Central management of system tools, storage, and services."
    },
    "devmgmt.msc": {
        "de": "Verwaltet und konfiguriert Hardwaregeräte.",
        "en": "Manages and configures hardware devices."
    },
    "devmoderunasuserconfig.msc": {
        "de": "Konfiguriert den Entwicklermodus für Benutzerkonten.",
        "en": "Configures developer mode for user accounts."
    },
    "diskmgmt.msc": {
        "de": "Verwaltet Festplatten und Partitionen.",
        "en": "Manages disks and partitions."
    },
    "dssite.msc": {
        "de": "Verwaltet Active Directory-Standorte und -Dienste.",
        "en": "Manages Active Directory sites and services."
    },
    "eventvwr.msc": {
        "de": "Zeigt und analysiert System- und Anwendungsprotokolle.",
        "en": "Displays and analyzes system and application logs."
    },
    "fsmgmt.msc": {
        "de": "Verwaltet freigegebene Ordner und Dateien.",
        "en": "Manages shared folders and files."
    },
    "gpedit.msc": {
        "de": "Konfiguriert Gruppenrichtlinien auf dem lokalen Computer.",
        "en": "Configures Group Policy on the local computer."
    },
    "lusrmgr.msc": {
        "de": "Verwaltet lokale Benutzer und Gruppen.",
        "en": "Manages local users and groups."
    },
    "perfmon.msc": {
        "de": "Überwacht und analysiert Systemleistung.",
        "en": "Monitors and analyzes system performance."
    },
    "printmanagement.msc": {
        "de": "Verwaltet Drucker und Druckaufträge.",
        "en": "Manages printers and print jobs."
    },
    "rsop.msc": {
        "de": "Zeigt die resultierenden Gruppenrichtlinien an.",
        "en": "Displays the Resultant Set of Policy."
    },
    "secpol.msc": {
        "de": "Konfiguriert lokale Sicherheitsrichtlinien.",
        "en": "Configures local security policies."
    },
    "services.msc": {
        "de": "Verwaltet Systemdienste und -prozesse.",
        "en": "Manages system services and processes."
    },
    "taskschd.msc": {
        "de": "Plant und verwaltet geplante Aufgaben.",
        "en": "Schedules and manages tasks."
    },
    "tpm.msc": {
        "de": "Verwaltet das Trusted Platform Module (TPM).",
        "en": "Manages the Trusted Platform Module (TPM)."
    },
    "virtmgmt.msc": {
        "de": "Verwaltet virtuelle Maschinen und Hyper-V.",
        "en": "Manages virtual machines and Hyper-V."
    },
    "wf.msc": {
        "de": "Konfiguriert die Windows-Firewall.",
        "en": "Configures Windows Firewall."
    },
    "wmimgmt.msc": {
        "de": "Verwaltet WMI (Windows Management Instrumentation).",
        "en": "Manages WMI (Windows Management Instrumentation)."
    },
    # .exe Dateien
    "agentactivationruntimestarter.exe": {
        "de": "Startet den Agent Activation Runtime-Dienst.",
        "en": "Starts the Agent Activation Runtime service."
    },
    "alg.exe": {
        "de": "Bietet Unterstützung für Drittanbieter-Protokolle.",
        "en": "Provides support for third-party protocols."
    },
    "appidcertstorecheck.exe": {
        "de": "Überprüft den Zertifikatspeicher für Anwendungs-IDs.",
        "en": "Checks the certificate store for application IDs."
    },
    "arp.exe": {
        "de": "Zeigt und ändert die ARP-Tabelle (Address Resolution Protocol).",
        "en": "Displays and modifies the ARP table."
    },
    "at.exe": {
        "de": "Plant Befehle und Skripte zur Ausführung zu einem bestimmten Zeitpunkt.",
        "en": "Schedules commands and scripts to run at a specified time."
    },
    "attrib.exe": {
        "de": "Ändert Dateiattribute (z. B. schreibgeschützt, versteckt).",
        "en": "Changes file attributes (e.g., read-only, hidden)."
    },
    "auditpol.exe": {
        "de": "Konfiguriert die Überwachungsrichtlinien.",
        "en": "Configures audit policies."
    },
    "autochk.exe": {
        "de": "Überprüft Dateisysteme auf Fehler.",
        "en": "Checks file systems for errors."
    },
    "calc.exe": {
        "de": "Ein einfacher Taschenrechner.",
        "en": "A simple calculator."
    },
    "cmd.exe": {
        "de": "Startet die Windows-Eingabeaufforderung.",
        "en": "Starts the Windows Command Prompt."
    },
    "comp.exe": {
        "de": "Vergleicht den Inhalt von Dateien oder Ordnern.",
        "en": "Compares the contents of files or folders."
    },
    "control.exe": {
        "de": "Öffnet die Systemsteuerung.",
        "en": "Opens the Control Panel."
    },
    "defrag.exe": {
        "de": "Defragmentiert Festplatten.",
        "en": "Defragments hard drives."
    },
    "diskpart.exe": {
        "de": "Verwaltet Festplattenpartitionen.",
        "en": "Manages disk partitions."
    },
    "dxdiag.exe": {
        "de": "Zeigt Informationen zu DirectX und Systemhardware an.",
        "en": "Displays information about DirectX and system hardware."
    },
    "eventcreate.exe": {
        "de": "Erstellt benutzerdefinierte Ereignisse in Ereignisprotokollen.",
        "en": "Creates custom events in event logs."
    },
    "explorer.exe": {
        "de": "Startet den Windows Explorer.",
        "en": "Starts Windows Explorer."
    },
    "findstr.exe": {
        "de": "Durchsucht Dateien nach bestimmten Zeichenfolgen.",
        "en": "Searches files for specific strings."
    },
    "gpupdate.exe": {
        "de": "Aktualisiert Gruppenrichtlinien.",
        "en": "Updates Group Policies."
    },
    "ipconfig.exe": {
        "de": "Zeigt Netzwerkkonfigurationen an.",
        "en": "Displays network configurations."
    },
    "mmc.exe": {
        "de": "Startet die Microsoft Management Console.",
        "en": "Starts the Microsoft Management Console."
    },
    "mstsc.exe": {
        "de": "Startet den Remote Desktop Client.",
        "en": "Starts the Remote Desktop Client."
    },
    "notepad.exe": {
        "de": "Startet den Editor.",
        "en": "Starts Notepad."
    },
    "ping.exe": {
        "de": "Überprüft die Netzwerkverbindung zu einem anderen Computer.",
        "en": "Checks network connectivity to another computer."
    },
    "regedit.exe": {
        "de": "Startet den Registrierungseditor.",
        "en": "Starts the Registry Editor."
    },
    "sfc.exe": {
        "de": "Überprüft und repariert Systemdateien.",
        "en": "Scans and repairs system files."
    },
    "shutdown.exe": {
        "de": "Fährt den Computer herunter oder startet ihn neu.",
        "en": "Shuts down or restarts the computer."
    },
    "taskmgr.exe": {
        "de": "Startet den Task-Manager.",
        "en": "Starts the Task Manager."
    },
    "xcopy.exe": {
        "de": "Kopiert Dateien und Verzeichnisse.",
        "en": "Copies files and directories."
    }
}

PROGRAMS_TRANSLATIONS = {
    'de': {
        "accesschk.exe": "Zeigt die Zugriffsrechte von Benutzern oder Gruppen auf Dateien, Ordner und Registry-Schlüssel an.",
        "AccessEnum.exe": "Ermöglicht die einfache Anzeige von Berechtigungen für Dateien und Registrierungsschlüssel.",
        "ADExplorer.exe": "Ein Active Directory-Browsing-Tool zum Durchsuchen und Analysieren von AD-Strukturen.",
        "ADInsight.exe": "Echtzeit-Überwachung und Analyse von Active Directory-Anfragen.",
        "adrestore.exe": "Stellt gelöschte Active Directory-Objekte wieder her.",
        "Autologon.exe": "Ermöglicht das Konfigurieren eines automatischen Logins für Benutzerkonten.",
        "Autoruns.exe": "Zeigt alle Programme an, die beim Systemstart oder Benutzeranmeldung automatisch gestartet werden.",
        "Bginfo.exe": "Zeigt relevante Systeminformationen auf dem Desktop-Hintergrund an.",
        "Cacheset.exe": "Ermöglicht die Anpassung der Systemcache-Einstellungen.",
        "Clockres.exe": "Misst die Auflösung der Systemuhr.",
        "Contig.exe": "Defragmentiert einzelne Dateien auf der Festplatte.",
        "Coreinfo.exe": "Zeigt Informationen über die Prozessor-Architektur und Caching.",
        "CPUSTRES.EXE": "Belastungstest-Tool für CPU-Temperaturen und Leistung.",
        "Dbgview.exe": "Zeigt Debug-Ausgaben von Anwendungen und Treibern in Echtzeit an.",
        "Desktops.exe": "Erlaubt die Nutzung mehrerer virtueller Desktops.",
        "disk2vhd.exe": "Erstellt VHD-Dateien aus physischen Festplatten.",
        "Diskmon.exe": "Überwacht und protokolliert Festplattenaktivitäten in Echtzeit.",
        "DiskView.exe": "Visualisiert die physische Speicherzuordnung auf der Festplatte.",
        "du.exe": "Analysiert den Festplattenplatzverbrauch von Verzeichnissen.",
        "efsdump.exe": "Extrahiert und analysiert EFS-verschlüsselte Dateien.",
        "FindLinks.exe": "Zeigt symbolische Verknüpfungen und Hardlinks für Dateien an.",
        "handle.exe": "Listet alle offenen Handles auf dem System auf.",
        "junction.exe": "Erstellt oder entfernt symbolische Verknüpfungen (Junctions) für Verzeichnisse.",
        "Listdlls.exe": "Listet alle geladenen DLLs eines Prozesses auf.",
        "procexp.exe": "Erweitertes Task-Manager-Tool zur Prozessüberwachung und -verwaltung.",
        "Procmon.exe": "Echtzeit-Überwachung von Dateisystem-, Registry- und Prozessaktivitäten.",
        "PsExec.exe": "Führt Prozesse remote auf anderen Systemen aus.",
        "PsInfo.exe": "Zeigt detaillierte Systeminformationen an.",
        "pskill.exe": "Beendet Prozesse auf lokalen oder entfernten Systemen.",
        "psservice.exe": "Verwalten und Überwachen von Windows-Diensten.",
        "RAMMap.exe": "Detaillierte Analyse der RAM-Nutzung im System.",
        "RegDelNull.exe": "Löscht Registrierungseinträge mit null-Bytes.",
        "Sysmon.exe": "Erweiterte Überwachung und Protokollierung von Systemaktivitäten.",
        "tcpview.exe": "Überwacht aktive TCP- und UDP-Verbindungen auf dem System.",
        "vmmap.exe": "Visualisiert den virtuellen Speicherverbrauch von Prozessen.",
        "Volumeid.exe": "Ändert die Volume-Serial-Nummer von Laufwerken.",
        "whois.exe": "Abfrage von Whois-Informationen zu Domainnamen.",
        "Winobj.exe": "Zeigt eine grafische Darstellung des Windows-Objektmanagers an.",
        "ZoomIt.exe": "Bietet Bildschirmvergrößerung und Annotationen für Präsentationen."
    },
    'en': {
        "accesschk.exe": "Displays the access rights of users or groups to files, folders, and registry keys.",
        "AccessEnum.exe": "Provides a simple view of permissions for files and registry keys.",
        "ADExplorer.exe": "An Active Directory browsing tool for exploring and analyzing AD structures.",
        "ADInsight.exe": "Real-time monitoring and analysis of Active Directory requests.",
        "adrestore.exe": "Restores deleted Active Directory objects.",
        "Autologon.exe": "Allows configuration of automatic login for user accounts.",
        "Autoruns.exe": "Displays all programs that start automatically during system startup or user login.",
        "Bginfo.exe": "Displays relevant system information on the desktop background.",
        "Cacheset.exe": "Allows adjustment of system cache settings.",
        "Clockres.exe": "Measures the resolution of the system clock.",
        "Contig.exe": "Defragments individual files on the hard drive.",
        "Coreinfo.exe": "Displays information about processor architecture and caching.",
        "CPUSTRES.EXE": "Stress test tool for CPU temperatures and performance.",
        "Dbgview.exe": "Displays debug outputs from applications and drivers in real-time.",
        "Desktops.exe": "Allows the use of multiple virtual desktops.",
        "disk2vhd.exe": "Creates VHD files from physical hard drives.",
        "Diskmon.exe": "Monitors and logs hard drive activity in real-time.",
        "DiskView.exe": "Visualizes the physical storage mapping on the hard drive.",
        "du.exe": "Analyzes disk space usage of directories.",
        "efsdump.exe": "Extracts and analyzes EFS-encrypted files.",
        "FindLinks.exe": "Displays symbolic links and hard links for files.",
        "handle.exe": "Lists all open handles on the system.",
        "junction.exe": "Creates or removes symbolic links (junctions) for directories.",
        "Listdlls.exe": "Lists all loaded DLLs of a process.",
        "procexp.exe": "Advanced Task Manager tool for process monitoring and management.",
        "Procmon.exe": "Real-time monitoring of file system, registry, and process activities.",
        "PsExec.exe": "Executes processes remotely on other systems.",
        "PsInfo.exe": "Displays detailed system information.",
        "pskill.exe": "Terminates processes on local or remote systems.",
        "psservice.exe": "Manages and monitors Windows services.",
        "RAMMap.exe": "Detailed analysis of RAM usage in the system.",
        "RegDelNull.exe": "Deletes registry entries with null bytes.",
        "Sysmon.exe": "Advanced monitoring and logging of system activities.",
        "tcpview.exe": "Monitors active TCP and UDP connections on the system.",
        "vmmap.exe": "Visualizes the virtual memory usage of processes.",
        "Volumeid.exe": "Changes the volume serial number of drives.",
        "whois.exe": "Queries Whois information for domain names.",
        "Winobj.exe": "Displays a graphical representation of the Windows Object Manager.",
        "ZoomIt.exe": "Provides screen zoom and annotations for presentations."
    }
}

def get_translated_programs(lang):
    # Wir kopieren die Programme aus PROGRAMS_TRANSLATIONS
    return PROGRAMS_TRANSLATIONS.get(lang, PROGRAMS_TRANSLATIONS['de']).copy()

def download_and_extract():
    """Lädt die SysinternalsSuite herunter und entpackt sie."""
    try:
        print("Herunterladen der Sysinternals Suite...")
        with requests.get(ZIP_URL, stream=True) as r:
            r.raise_for_status()
            with open(ZIP_NAME, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print("Entpacken der Sysinternals Suite...")
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(SUITE_FOLDER)
        os.remove(ZIP_NAME)
        print("Download und Entpacken abgeschlossen.")
    except Exception as e:
        print(f"Beim Herunterladen oder Entpacken ist ein Fehler aufgetreten: {e}")
        sys.exit(1)

def check_suite():
    """Überprüft das Vorhandensein des SysinternalsSuite-Ordners und lädt bei Bedarf herunter."""
    if not os.path.isdir(SUITE_FOLDER):
        download_and_extract()

# Custom ToggleSwitch Widget with a sliding circle
class ToggleSwitch(QtWidgets.QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, width=60, height=30):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._checked = False
        self._circle_position = 2
        self._animation = QtCore.QPropertyAnimation(self, b"circle_position")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

    def getCirclePosition(self):
        return self._circle_position

    def setCirclePosition(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = pyqtProperty(int, fget=getCirclePosition, fset=setCirclePosition)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)
        start = self._circle_position
        if self._checked:
            end = self.width() - self.height() + 2
        else:
            end = 2
        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.start()
        super().mousePressEvent(event)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked
        if self._checked:
            self._circle_position = self.width() - self.height() + 2
        else:
            self._circle_position = 2
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        bg_color = QtGui.QColor("#4cd964") if self._checked else QtGui.QColor("#CCCCCC")
        painter.setBrush(QtGui.QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)
        circle_diameter = self.height() - 4
        circle_rect = QtCore.QRect(self._circle_position, 2, circle_diameter, circle_diameter)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("white")))
        painter.drawEllipse(circle_rect)
        painter.end()

class CollapsibleWidget(QtWidgets.QWidget):
    """Ein einfaches kollabierbares Widget."""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.toggle_button = QtWidgets.QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: none;
                text-align: left;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton::checked {
                background-color: #777777;
            }
        """)
        self.toggle_button.clicked.connect(self.on_toggle)
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_area.setVisible(False)
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.content_area)

    def on_toggle(self):
        is_checked = self.toggle_button.isChecked()
        self.content_area.setVisible(is_checked)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

class SysinternalsGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = SETTINGS.value("language", "de")
        self.translations = TRANSLATIONS[self.current_lang]
        self.programs = get_translated_programs(self.current_lang)
        self.current_theme = SETTINGS.value("theme", "dark")
        self.additional_programs_downloaded = False  # Flag, ob zusätzliche Programme bereits geladen wurden
        self.special_programs = {}  # Für Programme, die nicht als Datei vorliegen (z. B. Powertoys)
        self.init_ui()
        self.retranslate_ui()
        self.apply_theme()
        # Prüfe, ob alle zusätzlichen Programme (außer Powertoys) bereits vorhanden sind.
        if self.check_all_additional_programs_installed():
            self.additional_programs_downloaded = True
            self.add_progs_checkbox.setChecked(True)
            self.programs["WizTree.exe"] = self.translations.get("wiztree_desc", "WizTree")
            self.programs["windhawk_setup.exe"] = self.translations.get("windhawk_desc", "Windhawk")
            self.programs["Powertoys"] = self.translations.get("powertoys_desc", "Powertoys")
            self.special_programs["Powertoys"] = {"url": "ms-windows-store://pdp/?ProductId=xp89dcgq3k6vld&ocid=sfw-fab-treatment&referrer=storeforweb&webId=1a77bb16-d2af-46b9-8b52-0c928d41a63c&webSessionId=987b1467-010c-4571-bfe8-dd3dc484e0e7"}
            self.programs["WiresharkPortable64.exe"] = self.translations.get("wireshark_desc", "Wireshark")
            self.programs["Recuva.exe"] = self.translations.get("recuva_desc", "Recuva")
            self.programs["FileShredder.exe"] = self.translations.get("fileshredder_desc", "File Shredder")
            self.update_program_list()

    def check_all_additional_programs_installed(self):
        """Überprüft, ob alle zusätzlichen Programme (außer Powertoys) bereits installiert sind."""
        required_files = ["WizTree.exe", "windhawk_setup.exe", "WiresharkPortable64.exe", "Recuva.exe", "FileShredder.exe"]
        for file in required_files:
            if not os.path.isfile(os.path.join(SUITE_FOLDER, file)):
                return False
        return True

    def init_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("color: #FFFFFF;")

        main_layout = QtWidgets.QVBoxLayout()

        # Sprachen, Additional Programs, Admin-Checkbox und neue System32-Checkbox
        lang_layout = QtWidgets.QHBoxLayout()
        self.lang_label = QtWidgets.QLabel()
        self.lang_label.setStyleSheet("color: #000000;")
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.setStyleSheet("color: #000000;")
        self.lang_combo.addItem("Deutsch", "de")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setCurrentIndex(self.lang_combo.findData(self.current_lang))
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)

        # Checkbox für zusätzliche Programme
        self.add_progs_checkbox = QtWidgets.QCheckBox()
        self.add_progs_checkbox.setStyleSheet("color: #000000;")
        self.add_progs_checkbox.setToolTip(self.translations['add_additional_programs_tooltip'])
        self.add_progs_checkbox.stateChanged.connect(self.handle_additional_programs_checkbox)
        lang_layout.addWidget(self.add_progs_checkbox)

        # Checkbox: Programme immer als Administrator starten
        self.admin_checkbox = QtWidgets.QCheckBox()
        self.admin_checkbox.setStyleSheet("color: #000000;")
        self.admin_checkbox.setToolTip(self.translations.get("always_run_as_admin_tooltip", ""))
        lang_layout.addWidget(self.admin_checkbox)

        # Neue Checkbox: System32-Programme anzeigen
        self.system32_checkbox = QtWidgets.QCheckBox()
        self.system32_checkbox.setStyleSheet("color: #000000;")
        # Lese den gespeicherten Zustand (Standard: False)
        self.system32_checkbox.setChecked(SETTINGS.value("show_system32_programs", False, type=bool))
        self.system32_checkbox.stateChanged.connect(self.handle_system32_checkbox)
        lang_layout.addWidget(self.system32_checkbox)

        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)

        # Suchleiste und ToggleSwitch
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.textChanged.connect(self.update_program_list)
        self.search_bar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.theme_switch = ToggleSwitch(width=60, height=30)
        self.theme_switch.setChecked(self.current_theme == "dark")
        self.theme_switch.toggled.connect(self.change_theme)
        theme_search_layout = QtWidgets.QHBoxLayout()
        theme_search_layout.addWidget(self.search_bar)
        theme_search_layout.addWidget(self.theme_switch)
        main_layout.addLayout(theme_search_layout)

        # Scrollbereich für Programme
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        self.container = QtWidgets.QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.container.setLayout(self.layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.theme_animation = QtCore.QVariantAnimation(
            self,
            duration=150,
            easingCurve=QtCore.QEasingCurve.InOutQuad
        )
        self.theme_animation.valueChanged.connect(self.on_theme_animate)

        self.update_searchbar_style()

    def handle_system32_checkbox(self, state):
        SETTINGS.setValue("show_system32_programs", state == Qt.Checked)
        self.update_program_list()

    def update_searchbar_style(self):
        if self.current_theme == "dark":
            style = """
                QLineEdit {
                    background-color: #3C3C3C;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    border-radius: 10px;
                    padding: 5px;
                }
            """
        else:
            style = """
                QLineEdit {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #AAAAAA;
                    border-radius: 10px;
                    padding: 5px;
                }
            """
        self.search_bar.setStyleSheet(style)

    def change_language(self, index):
        self.current_lang = self.lang_combo.itemData(index)
        SETTINGS.setValue("language", self.current_lang)
        self.translations = TRANSLATIONS[self.current_lang]
        self.programs = get_translated_programs(self.current_lang)
        # Falls zusätzliche Programme bereits geladen wurden, diese erneut hinzufügen:
        if self.additional_programs_downloaded:
            self.programs["WizTree.exe"] = self.translations.get("wiztree_desc", "WizTree")
            self.programs["windhawk_setup.exe"] = self.translations.get("windhawk_desc", "Windhawk")
            self.programs["Powertoys"] = self.translations.get("powertoys_desc", "Powertoys")
            self.programs["WiresharkPortable64.exe"] = self.translations.get("wireshark_desc", "Wireshark")
            self.programs["Recuva.exe"] = self.translations.get("recuva_desc", "Recuva")
            self.programs["FileShredder.exe"] = self.translations.get("fileshredder_desc", "File Shredder")
        self.retranslate_ui()
        self.update_program_list()

    def retranslate_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.lang_label.setText(self.translations['language_label'])
        self.search_bar.setPlaceholderText(self.translations['search_placeholder'])
        self.add_progs_checkbox.setText(self.translations['add_additional_programs'])
        self.add_progs_checkbox.setToolTip(self.translations['add_additional_programs_tooltip'])
        self.admin_checkbox.setText(self.translations['always_run_as_admin'])
        self.admin_checkbox.setToolTip(self.translations['always_run_as_admin_tooltip'])
        self.system32_checkbox.setText(self.translations['system32_programs'])
        self.system32_checkbox.setToolTip(self.translations['system32_programs_tooltip'])
        self.update_program_list()

    def change_theme(self, checked):
        self.current_theme = "dark" if checked else "light"
        SETTINGS.setValue("theme", self.current_theme)
        self.apply_theme()

    def apply_theme(self):
        app = QtWidgets.QApplication.instance()
        if self.current_theme == "dark":
            dark_palette = QtGui.QPalette()
            dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#2E2E2E"))
            dark_palette.setColor(QtGui.QPalette.WindowText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#3C3C3C"))
            dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#3C3C3C"))
            dark_palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Text, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#555555"))
            dark_palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.BrightText, Qt.red)
            dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#5A5A5A"))
            dark_palette.setColor(QtGui.QPalette.HighlightedText, Qt.white)
            app.setPalette(dark_palette)
            self.theme_animation.setStartValue(QtGui.QColor("#E0E0E0"))
            self.theme_animation.setEndValue(QtGui.QColor("#2E2E2E"))
        else:
            light_palette = QtGui.QPalette()
            light_palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#F0F0F0"))
            light_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
            light_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
            light_palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            light_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#AAAAAA"))
            light_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#000000"))
            app.setPalette(light_palette)
            self.theme_animation.setStartValue(QtGui.QColor("#2E2E2E"))
            self.theme_animation.setEndValue(QtGui.QColor("#E0E0E0"))
        self.theme_animation.start()
        self.update_searchbar_style()
        self.update_program_list()

    def on_theme_animate(self, value):
        color_name = value.name()
        self.centralWidget().setStyleSheet(f"background-color: {color_name};")

    def update_program_list(self):
        search_text = self.search_bar.text().lower()
        if self.current_theme == "dark":
            label_color = "#FFFFFF"
            widget_bg = "#3C3C3C"
            run_btn_bg = "#555555"
            run_btn_hover_bg = "#777777"
            shortcut_btn_bg = "#555555"
            shortcut_btn_hover_bg = "#777777"
        else:
            label_color = "#000000"
            widget_bg = "#F0F0F0"
            run_btn_bg = "#CCCCCC"
            run_btn_hover_bg = "#BBBBBB"
            shortcut_btn_bg = "#CCCCCC"
            shortcut_btn_hover_bg = "#BBBBBB"

        filtered_programs = {
            exe: desc for exe, desc in self.programs.items()
            if search_text in exe.lower() or search_text in desc.lower()
        }

        # Bestehende Widgets löschen
        while self.layout.count() > 0:
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Hauptprogramme (wobei "WizTree64.exe" ausgenommen wird)
        for exe, desc in filtered_programs.items():
            if exe == "WizTree64.exe":
                continue
            exe_path = os.path.join(SUITE_FOLDER, exe)
            if not (os.path.isfile(exe_path) or (exe in self.special_programs)):
                continue

            text = f"<b>{exe}</b><br>{desc}"
            text_label = QtWidgets.QLabel(text)
            text_label.setWordWrap(True)
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            text_label.setStyleSheet(f"color: {label_color};")

            run_btn = QtWidgets.QPushButton(self.translations['start_button'])
            run_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {run_btn_bg};
                    color: {label_color};
                    border-radius: 10px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {run_btn_hover_bg};
                }}
            """)
            run_btn.clicked.connect(lambda checked, path=exe_path: self.run_program(path))

            prog_layout = QtWidgets.QHBoxLayout()
            prog_layout.addWidget(text_label)
            prog_layout.addWidget(run_btn)
            if exe not in self.special_programs:
                shortcut_btn = QtWidgets.QPushButton("Shortcut")
                shortcut_btn.setToolTip("Shortcut zum Desktop hinzufügen")
                shortcut_btn.setFixedWidth(80)
                shortcut_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {shortcut_btn_bg};
                        color: {label_color};
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {shortcut_btn_hover_bg};
                    }}
                """)
                shortcut_btn.clicked.connect(lambda checked, path=exe_path: self.create_shortcut(path))
                prog_layout.addWidget(shortcut_btn)
            prog_widget = QtWidgets.QWidget()
            prog_widget.setLayout(prog_layout)
            prog_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {widget_bg};
                    border-radius: 15px;
                    margin: 10px;
                    padding: 10px;
                }}
            """)
            self.layout.addWidget(prog_widget)

        # Andere EXE-Dateien, die nicht in self.programs enthalten sind.
        all_exes = [f for f in os.listdir(SUITE_FOLDER) if f.lower().endswith('.exe')]
        other_exes = [f for f in all_exes if f not in self.programs]
        if search_text:
            other_exes = [exe for exe in other_exes if search_text in exe.lower()]
        if other_exes:
            collapsible = CollapsibleWidget(self.translations['other_programs'])
            for exe in other_exes:
                exe_path = os.path.join(SUITE_FOLDER, exe)
                if os.path.isfile(exe_path):
                    if exe == "WizTree64.exe":
                        desc = self.translations.get("wiztree64_desc", "")
                        text = f"<b>{exe}</b><br>{desc}"
                    else:
                        text = f"<b>{exe}</b>"
                    text_label = QtWidgets.QLabel(text)
                    text_label.setWordWrap(True)
                    text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    text_label.setStyleSheet(f"color: {label_color};")

                    run_btn = QtWidgets.QPushButton(self.translations['start_button'])
                    run_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {run_btn_bg};
                            color: {label_color};
                            border-radius: 10px;
                            padding: 5px;
                        }}
                        QPushButton:hover {{
                            background-color: {run_btn_hover_bg};
                        }}
                    """)
                    run_btn.clicked.connect(lambda checked, path=exe_path: self.run_program(path))

                    shortcut_btn = QtWidgets.QPushButton("Shortcut")
                    shortcut_btn.setToolTip("Shortcut zum Desktop hinzufügen")
                    shortcut_btn.setFixedWidth(30)
                    shortcut_btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {shortcut_btn_bg};
                            color: {label_color};
                            border-radius: 5px;
                            padding: 5px;
                            font-size: 12px;
                        }}
                        QPushButton:hover {{
                            background-color: {shortcut_btn_hover_bg};
                        }}
                    """)
                    shortcut_btn.clicked.connect(lambda checked, path=exe_path: self.create_shortcut(path))

                    prog_layout = QtWidgets.QHBoxLayout()
                    prog_layout.addWidget(text_label)
                    prog_layout.addWidget(run_btn)
                    prog_layout.addWidget(shortcut_btn)
                    prog_widget = QtWidgets.QWidget()
                    prog_widget.setLayout(prog_layout)
                    prog_widget.setStyleSheet(f"""
                        QWidget {{
                            background-color: {widget_bg};
                            border-radius: 15px;
                            margin: 10px;
                            padding: 10px;
                        }}
                    """)
                    collapsible.add_widget(prog_widget)
            if search_text:
                collapsible.toggle_button.setChecked(True)
                collapsible.content_area.setVisible(True)
            self.layout.addWidget(collapsible)

        # Neuer Bereich: System32-Programme (sowohl .exe als auch .msc)
        if self.system32_checkbox.isChecked():
            system32_folder = os.path.join(os.environ.get("windir", "C:\\Windows"), "System32")
            system32_files = [f for f in os.listdir(system32_folder)
                              if f.lower().endswith('.exe') or f.lower().endswith('.msc')]
            if search_text:
                system32_files = [f for f in system32_files if search_text in f.lower()]
            if system32_files:
                collapsible_sys32 = CollapsibleWidget(self.translations['system32_programs'])
                for file in sorted(system32_files):
                    exe_path = os.path.join(system32_folder, file)
                    if os.path.isfile(exe_path):
                        desc = SYSTEM32_DESCRIPTIONS.get(file.lower(), {}).get(self.current_lang, "")
                        if desc:
                            text = f"<b>{file}</b><br>{desc}"
                        else:
                            text = f"<b>{file}</b>"
                        text_label = QtWidgets.QLabel(text)
                        text_label.setWordWrap(True)
                        text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                        text_label.setStyleSheet(f"color: {label_color};")
                        run_btn = QtWidgets.QPushButton(self.translations['start_button'])
                        run_btn.setStyleSheet(f"""
                            QPushButton {{
                                background-color: {run_btn_bg};
                                color: {label_color};
                                border-radius: 10px;
                                padding: 5px;
                            }}
                            QPushButton:hover {{
                                background-color: {run_btn_hover_bg};
                            }}
                        """)
                        run_btn.clicked.connect(lambda checked, path=exe_path: self.run_program(path))

                        shortcut_btn = QtWidgets.QPushButton("Shortcut")
                        shortcut_btn.setToolTip("Shortcut zum Desktop hinzufügen")
                        shortcut_btn.setFixedWidth(80)
                        shortcut_btn.setStyleSheet(f"""
                            QPushButton {{
                                background-color: {shortcut_btn_bg};
                                color: {label_color};
                                border-radius: 5px;
                                padding: 5px;
                                font-size: 12px;
                            }}
                            QPushButton:hover {{
                                background-color: {shortcut_btn_hover_bg};
                            }}
                        """)
                        shortcut_btn.clicked.connect(lambda checked, path=exe_path: self.create_shortcut(path))

                        prog_layout = QtWidgets.QHBoxLayout()
                        prog_layout.addWidget(text_label)
                        prog_layout.addWidget(run_btn)
                        prog_layout.addWidget(shortcut_btn)

                        prog_widget = QtWidgets.QWidget()
                        prog_widget.setLayout(prog_layout)
                        prog_widget.setStyleSheet(f"""
                            QWidget {{
                                background-color: {widget_bg};
                                border-radius: 15px;
                                margin: 10px;
                                padding: 10px;
                            }}
                        """)
                        collapsible_sys32.add_widget(prog_widget)
                if search_text:
                    collapsible_sys32.toggle_button.setChecked(True)
                    collapsible_sys32.content_area.setVisible(True)
                self.layout.addWidget(collapsible_sys32)

    def run_program(self, exe_path):
        try:
            key = os.path.basename(exe_path)
            if key in self.special_programs:
                url = self.special_programs[key]["url"]
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
                return

            if not os.path.isfile(exe_path):
                QtWidgets.QMessageBox.critical(
                    self,
                    self.translations['title'],
                    self.translations['error_file_not_found'].format(exe_path)
                )
                return

            program_dir = os.path.dirname(exe_path)
            program_name = os.path.basename(exe_path)

            if self.admin_checkbox.isChecked():
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", os.path.abspath(exe_path), None, program_dir, 1
                )
            else:
                command = f'start cmd /k "cd /d {program_dir} && {program_name}"'
                subprocess.Popen(command, shell=True)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                self.translations['title'],
                self.translations['error_program_start'].format(e)
            )

    def create_shortcut(self, exe_path):
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            shortcut_name = os.path.splitext(os.path.basename(exe_path))[0] + ".lnk"
            shortcut_path = os.path.join(desktop, shortcut_name)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = os.path.abspath(exe_path)
            shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(exe_path))
            shortcut.IconLocation = os.path.abspath(exe_path)
            shortcut.save()
            QtWidgets.QMessageBox.information(
                self,
                self.translations['title'],
                self.translations['shortcut_created'].format(shortcut_path)
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                self.translations['title'],
                self.translations['error_shortcut'].format(e)
            )

    def handle_additional_programs_checkbox(self, state):
        if state == Qt.Checked and not self.additional_programs_downloaded:
            self.download_additional_programs()
            self.add_progs_checkbox.setEnabled(False)

    def download_additional_programs(self):
        QtWidgets.QMessageBox.information(
            self,
            self.translations['add_additional_programs'],
            "Zusätzliche Programme werden heruntergeladen. Bitte warten..."
        )
        try:
            downloaded = []
            wiztree_zip_path = os.path.join(SUITE_FOLDER, "wiztree_4_24_portable.zip")
            print("Herunterladen von WizTree...")
            with requests.get("https://diskanalyzer.com/files/wiztree_4_24_portable.zip", stream=True) as r:
                r.raise_for_status()
                with open(wiztree_zip_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            with zipfile.ZipFile(wiztree_zip_path, 'r') as zip_ref:
                zip_ref.extractall(SUITE_FOLDER)
            os.remove(wiztree_zip_path)
            print("WizTree heruntergeladen und entpackt.")
            downloaded.append("WizTree")

            windhawk_exe_path = os.path.join(SUITE_FOLDER, "windhawk_setup.exe")
            print("Herunterladen von Windhawk...")
            with requests.get("https://ramensoftware.com/downloads/windhawk_setup.exe", stream=True) as r:
                r.raise_for_status()
                with open(windhawk_exe_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print("Windhawk heruntergeladen.")
            downloaded.append("Windhawk")

            self.programs["Powertoys"] = self.translations.get("powertoys_desc", "Powertoys")
            self.special_programs["Powertoys"] = {
                "url": "ms-windows-store://pdp/?ProductId=xp89dcgq3k6vld&ocid=sfw-fab-treatment&referrer=storeforweb&webId=1a77bb16-d2af-46b9-8b52-0c928d41a63c&webSessionId=987b1467-010c-4571-bfe8-dd3dc484e0e7"
            }

            wireshark_path = os.path.join(SUITE_FOLDER, "WiresharkPortable64.exe")
            print("Herunterladen von Wireshark...")
            with requests.get("https://2.na.dl.wireshark.org/win64/WiresharkPortable64_4.2.10.paf.exe", stream=True) as r:
                r.raise_for_status()
                with open(wireshark_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print("Wireshark heruntergeladen.")
            downloaded.append("Wireshark")

            recuva_path = os.path.join(SUITE_FOLDER, "Recuva.exe")
            print("Herunterladen von Recuva...")
            with requests.get("https://portableapps.com/redir2/?a=rcvPortable&s=s&d=pa&f=rcvPortable_1.53.2096_online.paf.exe", stream=True) as r:
                r.raise_for_status()
                with open(recuva_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print("Recuva heruntergeladen.")
            downloaded.append("Recuva")

            fileshredder_path = os.path.join(SUITE_FOLDER, "FileShredder.exe")
            print("Herunterladen von File Shredder...")
            with requests.get("https://www.alternate-tools.com/files/FileShredder.exe", stream=True) as r:
                r.raise_for_status()
                with open(fileshredder_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print("File Shredder heruntergeladen.")
            downloaded.append("File Shredder")

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                self.translations['title'],
                f"Error downloading additional programs:\n{e}"
            )
            return

        self.programs["WizTree.exe"] = self.translations.get("wiztree_desc", "WizTree")
        self.programs["windhawk_setup.exe"] = self.translations.get("windhawk_desc", "Windhawk")
        self.programs["WiresharkPortable64.exe"] = self.translations.get("wireshark_desc", "Wireshark")
        self.programs["Recuva.exe"] = self.translations.get("recuva_desc", "Recuva")
        self.programs["FileShredder.exe"] = self.translations.get("fileshredder_desc", "File Shredder")
        self.additional_programs_downloaded = True
        self.update_program_list()
        QtWidgets.QMessageBox.information(
            self,
            self.translations['add_additional_programs'],
            f"Heruntergeladene Programme: {', '.join(downloaded)}"
        )

def main():
    check_suite()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SysinternalsGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
