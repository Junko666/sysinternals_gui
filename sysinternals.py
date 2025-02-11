import os
import sys
import subprocess
import zipfile
import requests
import shutil
import win32com.client
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSettings, QVariantAnimation, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush

# Pfad zum SysinternalsSuite-Ordner
SUITE_FOLDER = "SysinternalsSuite"
ZIP_URL = "https://download.sysinternals.com/files/SysinternalsSuite.zip"
ZIP_NAME = "SysinternalsSuite.zip"

# Einstellungen (Sprache und Theme werden in denselben QSettings gespeichert)
SETTINGS = QSettings("SysinternalsGUI", "Language")

# Übersetzungen
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
        'error_shortcut': "Fehler beim Erstellen des Shortcuts:\n{}"
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
        'error_shortcut': "Error creating shortcut:\n{}"
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
        "Winobj.exe": "Zeigt eine grafische Darstellung des Windows-Objektmanagers an.",
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


# Custom ToggleSwitch Widget with a sliding circle
class ToggleSwitch(QtWidgets.QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, width=60, height=30):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._checked = False
        # The circle's horizontal position (start margin is 2)
        self._circle_position = 2
        self._animation = QtCore.QPropertyAnimation(self, b"circle_position")
        self._animation.setDuration(150)  # Faster and smoother
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw background (rounded rectangle)
        rect = self.rect()
        if self._checked:
            bg_color = QColor("#4cd964")
        else:
            bg_color = QColor("#CCCCCC")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)
        # Draw the circle
        circle_diameter = self.height() - 4
        circle_rect = QtCore.QRect(self._circle_position, 2, circle_diameter, circle_diameter)
        painter.setBrush(QBrush(QColor("white")))
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
        """Wechselt die Sichtbarkeit des Inhalts."""
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
        self.current_theme = SETTINGS.value("theme", "dark")
        self.init_ui()
        self.retranslate_ui()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("color: #FFFFFF;")

        # Hauptlayout
        main_layout = QtWidgets.QVBoxLayout()

        # Sprachauswahl
        lang_layout = QtWidgets.QHBoxLayout()
        self.lang_label = QtWidgets.QLabel()
        self.lang_label.setStyleSheet("color: #000000;")  # Sprache-Label in Schwarz
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.setStyleSheet("color: #000000;")  # Sprache-Combo in Schwarz
        self.lang_combo.addItem("Deutsch", "de")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setCurrentIndex(self.lang_combo.findData(self.current_lang))
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)

        # Suchleiste und ToggleSwitch (Switch rechts von der Suchleiste)
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.textChanged.connect(self.update_program_list)
        self.search_bar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.theme_switch = ToggleSwitch(width=60, height=30)
        # Setze Zustand anhand der gespeicherten Einstellung
        self.theme_switch.setChecked(self.current_theme == "dark")
        self.theme_switch.toggled.connect(self.change_theme)
        theme_search_layout = QtWidgets.QHBoxLayout()
        theme_search_layout.addWidget(self.search_bar)
        theme_search_layout.addWidget(self.theme_switch)
        main_layout.addLayout(theme_search_layout)

        # Scrollbereich für die Programm-Widgets
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

        # Übergangsanimation für den Theme-Wechsel (schneller & smoother)
        self.theme_animation = QVariantAnimation(
            self,
            duration=150,
            easingCurve=QtCore.QEasingCurve.InOutQuad
        )
        self.theme_animation.valueChanged.connect(self.on_theme_animate)

        self.update_searchbar_style()

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
        self.retranslate_ui()
        self.update_program_list()

    def retranslate_ui(self):
        self.setWindowTitle(self.translations['title'])
        self.lang_label.setText(self.translations['language_label'])
        self.search_bar.setPlaceholderText(self.translations['search_placeholder'])
        # Der ToggleSwitch selbst zeigt keinen Text, daher wird nur die Beschriftung im Sprachbereich gesetzt.
        self.update_program_list()

    def change_theme(self, checked):
        self.current_theme = "dark" if checked else "light"
        SETTINGS.setValue("theme", self.current_theme)
        self.apply_theme()

    def apply_theme(self):
        app = QtWidgets.QApplication.instance()
        if self.current_theme == "dark":
            dark_palette = QtGui.QPalette()
            dark_palette.setColor(QtGui.QPalette.Window, QColor("#2E2E2E"))
            dark_palette.setColor(QtGui.QPalette.WindowText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Base, QColor("#3C3C3C"))
            dark_palette.setColor(QtGui.QPalette.AlternateBase, QColor("#3C3C3C"))
            dark_palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Text, Qt.white)
            dark_palette.setColor(QtGui.QPalette.Button, QColor("#555555"))
            dark_palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QtGui.QPalette.BrightText, Qt.red)
            dark_palette.setColor(QtGui.QPalette.Highlight, QColor("#5A5A5A"))
            dark_palette.setColor(QtGui.QPalette.HighlightedText, Qt.white)
            app.setPalette(dark_palette)
            self.theme_animation.setStartValue(QColor("#E0E0E0"))
            self.theme_animation.setEndValue(QColor("#2E2E2E"))
        else:
            light_palette = QtGui.QPalette()
            light_palette.setColor(QtGui.QPalette.Window, QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.WindowText, QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.Base, QColor("#F0F0F0"))
            light_palette.setColor(QtGui.QPalette.AlternateBase, QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.black)
            light_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.black)
            light_palette.setColor(QtGui.QPalette.Text, QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.Button, QColor("#E0E0E0"))
            light_palette.setColor(QtGui.QPalette.ButtonText, QColor("#000000"))
            light_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
            light_palette.setColor(QtGui.QPalette.Highlight, QColor("#AAAAAA"))
            light_palette.setColor(QtGui.QPalette.HighlightedText, QColor("#000000"))
            app.setPalette(light_palette)
            self.theme_animation.setStartValue(QColor("#2E2E2E"))
            self.theme_animation.setEndValue(QColor("#E0E0E0"))
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

        # Programme aus der Übersetzungsliste anzeigen
        for exe, desc in filtered_programs.items():
            exe_path = os.path.join(SUITE_FOLDER, exe)
            if os.path.isfile(exe_path):
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
                self.layout.addWidget(prog_widget)

        # Andere EXE-Dateien, die nicht in der Übersetzungsliste enthalten sind
        all_exes = [f for f in os.listdir(SUITE_FOLDER) if f.lower().endswith('.exe')]
        other_exes = [f for f in all_exes if f not in self.programs]
        if search_text:
            other_exes = [exe for exe in other_exes if search_text in exe.lower()]
        if other_exes:
            collapsible = CollapsibleWidget(self.translations['other_programs'])
            for exe in other_exes:
                exe_path = os.path.join(SUITE_FOLDER, exe)
                if os.path.isfile(exe_path):
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

    def create_shortcut(self, exe_path):
        """Erstellt einen Shortcut des Programms auf dem Desktop."""
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

def main():
    check_suite()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SysinternalsGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
