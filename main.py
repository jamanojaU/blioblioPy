import sys
from librería import LibraryManager
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

def main():
    app = QApplication([])
    library_manager = LibraryManager()
    library_manager.resize(1300, 900)
    library_manager.show()

    apply_stylesheet(app, theme='light_blue.xml')

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()