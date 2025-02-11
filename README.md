# sysinternals_gui
Sysinternals Suite GUI


Precompiled executable .exe file for windows:
https://drive.google.com/file/d/1TwRe4EjaihnWGK397xvRIDd5Mr3TiE5B/view?usp=sharing
Dark-Mode:
![image](https://github.com/user-attachments/assets/398d0cfd-10d7-4500-8143-218dfbb945a6)

Light-Mode:
![image](https://github.com/user-attachments/assets/7d93ce7b-9f05-4b85-812d-d7f1b22a7c9a)


# Sysinternals Suite GUI

## Overview
The Sysinternals Suite GUI is a graphical user interface for the Sysinternals Suite, a collection of system utilities for Windows provided by Microsoft. This GUI allows users to easily browse, start, and manage the various tools in the Sysinternals Suite.

## Features
- **Download and Extract**: Automatically downloads and extracts the Sysinternals Suite if not already present.
- **Multilingual Support**: Supports both English and German, allowing users to switch languages via a dropdown menu.
- **Search Functionality**: Users can search for programs or descriptions to quickly find the desired tools.
- **Collapsible Widgets**: Uses collapsible widgets to keep the interface organized and display additional programs.

## Technical Details

### Dependencies
- `PyQt5`: For GUI development.
- `requests`: For downloading the Sysinternals Suite.
- `zipfile`: For extracting the downloaded ZIP file.
- `shutil`: For file operations.

### How It Works
- The program uses the `QSettings` class from PyQt5 to save user language settings.
- It implements a main class `SysinternalsGUI` that creates and manages the user interface.
- Programs are displayed in a scrollable list, and users can start them via buttons.

## Usage
To run the application, ensure you have the required dependencies installed and execute the script. The application will check for the Sysinternals Suite and download it if necessary.

# Sysinternals Suite GUI

## Übersicht
Die Sysinternals Suite GUI ist eine grafische Benutzeroberfläche für die Sysinternals Suite, eine Sammlung von Systemdienstprogrammen für Windows, die von Microsoft bereitgestellt werden. Diese GUI ermöglicht es Benutzern, die verschiedenen Tools der Sysinternals Suite einfach zu durchsuchen, zu starten und zu verwalten.

## Funktionen
- **Herunterladen und Entpacken**: Lädt die Sysinternals Suite automatisch herunter und entpackt sie, falls sie noch nicht vorhanden ist.
- **Mehrsprachige Unterstützung**: Unterstützt sowohl Deutsch als auch Englisch und ermöglicht es Benutzern, die Sprache über ein Dropdown-Menü zu wechseln.
- **Suchfunktion**: Benutzer können nach Programmen oder Beschreibungen suchen, um schnell die gewünschten Tools zu finden.
- **Kollabierbare Widgets**: Verwendet kollabierbare Widgets, um die Benutzeroberfläche übersichtlich zu gestalten und zusätzliche Programme anzuzeigen.

## Technische Details

### Abhängigkeiten
- `PyQt5`: Für die GUI-Entwicklung.
- `requests`: Zum Herunterladen der Sysinternals Suite.
- `zipfile`: Zum Entpacken der heruntergeladenen ZIP-Datei.
- `shutil`: Für Dateioperationen.

### Funktionsweise
- Das Programm verwendet die `QSettings`-Klasse von PyQt5, um die Spracheinstellungen des Benutzers zu speichern.
- Es implementiert eine Hauptklasse `SysinternalsGUI`, die die Benutzeroberfläche erstellt und verwaltet.
- Die Programme werden in einer scrollbaren Liste angezeigt, und Benutzer können sie über Schaltflächen starten.

## Verwendung
Um die Anwendung auszuführen, stellen Sie sicher, dass die erforderlichen Abhängigkeiten installiert sind, und führen Sie das Skript aus. Die Anwendung überprüft die Sysinternals Suite und lädt sie bei Bedarf herunter.
