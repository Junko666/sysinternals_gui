import os
import sys
import subprocess
import zipfile
import requests
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSettings

# Pfad zum SysinternalsSuite-Ordner
SUITE_FOLDER = "SysinternalsSuite"
ZIP_URL = "https://download.sysinternals.com/files/SysinternalsSuite.zip"
ZIP_NAME = "SysinternalsSuite.zip"

# Einstellungen
SETTINGS = QSettings("SysinternalsGUI", "Language")

# Übersetzungen
TRANSLATIONS = {
    'de': {
        'title': "Sysinternals Suite GUI",
        'search_placeholder': "Suche nach Programmen oder Beschreibungen...",
        'start_button': "Starten",
        'other_programs': "Andere Programme",
        'language_label': "Sprache:",
        'error_file_not_found': "Die Datei existiert nicht:\n{}",
        'error_program_start': "Beim Starten des Programms ist ein Fehler aufgetreten:\n{}"
    },
    'en': {
        'title': "Sysinternals Suite GUI",
        'search_placeholder': "Search for programs or descriptions...",
        'start_button': "Start",
        'other_programs': "Other Programs",
        'language_label': "Language:",
        'error_file_not_found': "File not found:\n{}",
        'error_program_start': "Error starting program:\n{}"
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
        "tcpview.exe": "Überwacht aktiven TCP- und UDP-Verbindungen auf dem System.",
        "vmmap.exe": "Visualisiert den virtuellen Speicherverbrauch von Prozessen.",
        "Volumeid.exe": "Ändert die Volume-Serial-Nummer von Laufwerken.",
        "whois.exe": "Abfrage von Whois-Informationen zu Domainnamen.",
        "Winobj.exe": "Zeigt eine grafische Darstellung der Windows-Objekt Managers an.",
        "ZoomIt.exe": "Bietet Bildschirmvergrößerung und Annotationen für Präsentationen.",
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
        "ZoomIt.exe": "Provides screen zoom and annotations for presentations.",
    }
}

def get_translated_programs(lang):
    return PROGRAMS_TRANSLATIONS.get(lang, PROGRAMS_TRANSLATIONS['de'])

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
        """Toggle the visibility of the content area."""
        is_checked = self.toggle_button.isChecked()
        self.content_area.setVisible(is_checked)

    def add_widget(self, widget):
        """Fügt ein Widget zum Inhalt hinzu."""
        self.content_layout.addWidget(widget)

class SysinternalsGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = SETTINGS.value("language", "de")
        self.translations = TRANSLATIONS[self.current_lang]
        self.programs = get_translated_programs(self.current_lang)
        
        self.init_ui()
        self.retranslate_ui()

    def init_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

        # Hauptlayout
        main_layout = QtWidgets.QVBoxLayout()

        # Sprachauswahl
        lang_layout = QtWidgets.QHBoxLayout()
        lang_label = QtWidgets.QLabel()
        self.lang_label = lang_label
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.addItem("Deutsch", "de")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setCurrentIndex(self.lang_combo.findData(self.current_lang))
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)

        # Suchleiste
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.search_bar.textChanged.connect(self.update_program_list)
        main_layout.addWidget(self.search_bar)

        # Scrollbereich
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        # Container-Widget für Programme
        self.container = QtWidgets.QWidget()
        self.scroll.setWidget(self.container)

        # Layout für Programme
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.container.setLayout(self.layout)

        # Hauptwidget setzen
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def change_language(self, index):
        self.current_lang = self.lang_combo.itemData(index)
        SETTINGS.setValue("language", self.current_lang)
        self.translations = TRANSLATIONS[self.current_lang]
        self.programs = get_translated_programs(self.current_lang)
        self.retranslate_ui()
        self.update_program_list()

    def retranslate_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.lang_label.setText(self.translations['language_label'])
        self.search_bar.setPlaceholderText(self.translations['search_placeholder'])
        self.update_program_list()

    def update_program_list(self):
        search_text = self.search_bar.text().lower()
        filtered_programs = {
            exe: desc for exe, desc in self.programs.items()
            if search_text in exe.lower() or search_text in desc.lower()
        }

        while self.layout.count() > 0:
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for exe, desc in filtered_programs.items():
            exe_path = os.path.join(SUITE_FOLDER, exe)
            if os.path.isfile(exe_path):
                text = f"<b>{exe}</b><br>{desc}"
                text_label = QtWidgets.QLabel(text)
                text_label.setWordWrap(True)
                text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                text_label.setStyleSheet("color: #FFFFFF;")

                btn = QtWidgets.QPushButton(self.translations['start_button'])
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #555555;
                        color: #FFFFFF;
                        border-radius: 10px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #777777;
                    }
                """)
                btn.clicked.connect(lambda checked, path=exe_path: self.run_program(path))

                prog_layout = QtWidgets.QHBoxLayout()
                prog_layout.addWidget(text_label)
                prog_layout.addWidget(btn)

                prog_widget = QtWidgets.QWidget()
                prog_widget.setLayout(prog_layout)
                prog_widget.setStyleSheet("""
                    QWidget {
                        background-color: #3C3C3C;
                        border-radius: 15px;
                        margin: 10px;
                        padding: 10px;
                    }
                """)
                self.layout.addWidget(prog_widget)

        all_exes = [f for f in os.listdir(SUITE_FOLDER) if f.lower().endswith('.exe')]
        other_exes = [f for f in all_exes if f not in self.programs]

        if other_exes:
            collapsible = CollapsibleWidget(self.translations['other_programs'])
            for exe in other_exes:
                exe_path = os.path.join(SUITE_FOLDER, exe)
                if os.path.isfile(exe_path):
                    text = f"<b>{exe}</b>"
                    text_label = QtWidgets.QLabel(text)
                    text_label.setWordWrap(True)
                    text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    text_label.setStyleSheet("color: #FFFFFF;")

                    btn = QtWidgets.QPushButton(self.translations['start_button'])
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #555555;
                            color: #FFFFFF;
                            border-radius: 10px;
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #777777;
                        }
                    """)
                    btn.clicked.connect(lambda checked, path=exe_path: self.run_program(path))

                    prog_layout = QtWidgets.QHBoxLayout()
                    prog_layout.addWidget(text_label)
                    prog_layout.addWidget(btn)

                    prog_widget = QtWidgets.QWidget()
                    prog_widget.setLayout(prog_layout)
                    prog_widget.setStyleSheet("""
                        QWidget {
                            background-color: #3C3C3C;
                            border-radius: 15px;
                            margin: 10px;
                            padding: 10px;
                        }
                    """)

                    collapsible.add_widget(prog_widget)
            self.layout.addWidget(collapsible)

    def run_program(self, exe_path):
        try:
            if not os.path.isfile(exe_path):
                QtWidgets.QMessageBox.critical(
                    self, 
                    self.translations['title'], 
                    self.translations['error_file_not_found'].format(exe_path)
                )
                return

            program_dir = os.path.dirname(exe_path)
            program_name = os.path.basename(exe_path)
            command = f'start cmd /k "cd /d {program_dir} && {program_name}"'
            subprocess.Popen(command, shell=True)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                self.translations['title'], 
                self.translations['error_program_start'].format(e)
            )

def main():
    check_suite()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#2E2E2E"))
    palette.setColor(QtGui.QPalette.WindowText, Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#3C3C3C"))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor("#3C3C3C"))
    palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
    palette.setColor(QtGui.QPalette.Text, Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#555555"))
    palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#5A5A5A"))
    palette.setColor(QtGui.QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    window = SysinternalsGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
