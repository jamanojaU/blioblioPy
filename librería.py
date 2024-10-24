import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QStackedWidget, QPushButton, QTableWidget, QTableWidgetItem, 
                             QListWidget, QHeaderView)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet  # Importamos solo lo necesario de qt_material


class LibraryManager(QWidget):
    def __init__(self):
        super().__init__()

        # Usamos QLineEdit y QPushButton normales
        self.title_entry = QLineEdit()
        self.author_entry = QLineEdit()
        self.year_entry = QLineEdit()
        self.editor_entry = QLineEdit()
        self.pages_entry = QLineEdit()
        self.genre_entry = QLineEdit()
        self.ubication_entry = QLineEdit()

        # Tabla para mostrar los libros
        self.table = QTableWidget()

        # Inicializa la UI
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        #Reducir los márgenes del layout
        layout.setContentsMargins(10, 10, 10, 10)

        # Crear el título para el menú
        menu_title = QLabel("Menú")
        menu_title.setStyleSheet("font-size: 30px; color: #000")
        layout.addWidget(menu_title)

        # Crear el menú
        self.menu = QListWidget()
        self.menu.addItem("Añadir libro")
        self.menu.addItem("Biblioteca")
        self.menu.currentItemChanged.connect(self.change_section)

        # Estilo para hacer el texto más grande
        self.menu.setStyleSheet("""
            QListWidget {
                font-size: 20px;  /* Cambiar el tamaño del texto */
                font-weight: bold; /* Hacer el texto en negrita */
                background-color: #FFFFFF;
                color: #212121;
            }
            QListWidget::item {
                padding: 10px;  /* Añadir espacio alrededor del texto */
            }
            QListWidget::item:selected {
                background-color: #2196F3;  /* Cambiar el color de fondo al seleccionar */
                color: #FFFFFF;
            }
        """)

        # Ajustar el tamaño del QListWidget
        self.menu.setMaximumSize(400, 120)
        #self.menu.setItemAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.menu)

        # Crear las secciones
        self.sections = QStackedWidget()


        # Sección de añadir libro
        add_book_section = QWidget()
        add_book_layout = QVBoxLayout()
        add_book_layout.setSpacing(5)
        add_book_section.setLayout(add_book_layout)

        # Cambiar el estilo de los campos de texto para que la letra se vea mejor
        text_field_style = """
            QLineEdit {
                font-size: 24px;  /* Tamaño de fuente más grande */
                padding: 8px;     /* Espaciado interno más amplio */
                border: 2px solid #ccc;
                border-radius: 10px;
            }
        """

        # Añadir campos de texto con estilo
        title_label = QLabel("TÍTULO")
        title_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(title_label)
        self.title_entry.setPlaceholderText("Título")
        self.title_entry.setStyleSheet(text_field_style)
        self.title_entry.setFixedWidth(800)
        add_book_layout.addWidget(self.title_entry)

        author_label = QLabel("AUTOR")
        author_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(author_label)
        self.author_entry.setPlaceholderText("Autor")
        self.author_entry.setStyleSheet(text_field_style)
        self.author_entry.setFixedWidth(500)
        add_book_layout.addWidget(self.author_entry)

        year_label = QLabel("AÑO")
        year_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(year_label)
        self.year_entry.setPlaceholderText("Año")
        self.year_entry.setStyleSheet(text_field_style)
        self.year_entry.setFixedWidth(100)
        add_book_layout.addWidget(self.year_entry)

        editor_label = QLabel("EDITORIAL")
        editor_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(editor_label)
        self.editor_entry.setPlaceholderText("Editorial")
        self.editor_entry.setStyleSheet(text_field_style)
        self.editor_entry.setFixedWidth(500)
        add_book_layout.addWidget(self.editor_entry)

        pages_label = QLabel("Nº DE PÁGINAS")
        pages_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(pages_label)
        self.pages_entry.setPlaceholderText("Nº de páginas")
        self.pages_entry.setStyleSheet(text_field_style)
        self.pages_entry.setFixedWidth(100)
        add_book_layout.addWidget(self.pages_entry)

        genre_label = QLabel("GÉNERO")
        genre_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(genre_label)
        self.genre_entry.setPlaceholderText("Género")
        self.genre_entry.setStyleSheet(text_field_style)
        self.genre_entry.setFixedWidth(500)
        add_book_layout.addWidget(self.genre_entry)

        ubication_label = QLabel("UBICACIÓN")
        ubication_label.setStyleSheet("font-size: 30px; color: #000")
        add_book_layout.addWidget(ubication_label)
        self.ubication_entry.setPlaceholderText("Ubicación")
        self.ubication_entry.setStyleSheet(text_field_style)
        self.ubication_entry.setFixedWidth(300)
        add_book_layout.addWidget(self.ubication_entry)

        # Botón de añadir libro con estilo
        add_button = QPushButton('Añadir libro')
        add_button.setStyleSheet("""
            QPushButton {
                font-size: 30px;  /* Tamaño de fuente más grande */
                padding: 10px;    /* Espaciado interno más amplio */
                border: 2px solid #ccc;
                border-radius: 10px;
                background-color: #e3f2fd;  /* Color de fondo */
            }
            QPushButton:hover {
                background-color: #cbd6f9;  /* Cambiar el color de fondo al pasar el ratón */
            }
        """)
        add_button.clicked.connect(self.add_book)
        add_book_layout.addWidget(add_button)

        self.sections.addWidget(add_book_section)

        # Sección para ver los libros
        view_books_section = QWidget()
        view_books_layout = QVBoxLayout()
        view_books_section.setLayout(view_books_layout)

        # Crear buscador
        search_label = QLabel("Buscar libro:")
        search_label.setStyleSheet("font-size: 30px")
        self.search_entry = QLineEdit()
        self.search_entry.setStyleSheet("font-size: 25px")
        self.search_entry.textChanged.connect(self.filter_table)

        # Añadir buscador a la UI
        view_books_layout.addWidget(search_label)
        view_books_layout.addWidget(self.search_entry)

        # Configurar la tabla
        self.table.setColumnCount(7)  # Asegurarse de que las columnas coinciden con los datos
        self.table.setHorizontalHeaderLabels(["Título", "Autor", "Año", "Editorial", "Nº de páginas", "Género", "Ubicación"])

        # Habilitar la ordenación por columnas
        self.table.setSortingEnabled(True)

        # Estilo para los encabezados de las columnas
        header = self.table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0;  /* Color de fondo */
                font-weight: bold;           /* Negrita */
                font-size: 15px;             /* Tamaño de fuente */
                padding: 4px;                /* Espacio alrededor del texto */
                border: 1px solid #dcdcdc;   /* Bordes opcionales */
            }
        """)

        # Aumentar el tamaño del texto en las filas de la tabla
        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 20px;  /* Tamaño de texto de las filas */
            }
        """)

        # Personalizar la anchura de las columnas
        self.table.setColumnWidth(0, 400)  # Título - mayor anchura
        self.table.setColumnWidth(1, 200)  # Autor
        self.table.setColumnWidth(2, 100)  # Año
        self.table.setColumnWidth(3, 200)  # Editorial
        self.table.setColumnWidth(4, 140)  # Nº de páginas
        self.table.setColumnWidth(5, 150)  # Género
        self.table.setColumnWidth(6, 150)  # Ubicación

        view_books_layout.addWidget(self.table)

        # Botón de borrar libro seleccionado
        delete_button = QPushButton('Borrar libro seleccionado')
        delete_button.clicked.connect(self.delete_book)
        view_books_layout.addWidget(delete_button)

        self.sections.addWidget(view_books_section)

        # Añadir las secciones al layout pero alineadas arriba
        layout.addWidget(self.sections)
        self.setLayout(layout)


    def change_section(self):
        self.sections.setCurrentIndex(self.menu.currentRow())

    def filter_table(self):
        """Filtrar la tabla según el texto de búsqueda"""
        filter_text = self.search_entry.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
            self.table.setRowHidden(row, not match)

    def add_book(self):
        # Validar que todos los campos estén llenos
        if not all([self.title_entry.text(), self.author_entry.text(), self.year_entry.text(), 
            self.editor_entry.text(), self.pages_entry.text(), self.genre_entry.text(), 
            self.ubication_entry.text()]):
            # Mostrar mensaje de error si faltan campos con un QLabel
            error_label = QLabel("Por favor, rellene todos los campos")
            error_label.setStyleSheet("color: red")
            error_label.setFixedHeight(30)
            self.layout().addWidget(error_label)

            return

        title = self.title_entry.text()
        author = self.author_entry.text()
        year = self.year_entry.text()
        editor = self.editor_entry.text()
        pages = self.pages_entry.text()
        genre = self.genre_entry.text()
        ubication = self.ubication_entry.text()

        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        c.execute("INSERT INTO books (title, author, year, editor, pages, genre, ubication) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (title, author, year, editor, pages, genre, ubication))

        conn.commit()
        conn.close()

        self.load_data()

        # Limpiar los campos después de añadir
        self.title_entry.setText('')
        self.author_entry.setText('')
        self.year_entry.setText('')
        self.editor_entry.setText('')
        self.pages_entry.setText('')
        self.genre_entry.setText('')
        self.ubication_entry.setText('')

    def delete_book(self):
        selected_row = self.table.currentRow()
        title = self.table.item(selected_row, 0).text()
        author = self.table.item(selected_row, 1).text()
        year = self.table.item(selected_row, 2).text()
        editor = self.table.item(selected_row, 3).text()
        pages = self.table.item(selected_row, 4).text()
        genre = self.table.item(selected_row, 5).text()
        ubication = self.table.item(selected_row, 6).text()

        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        c.execute("DELETE FROM books WHERE title = ? AND author = ? AND year = ? AND editor = ? AND pages = ? AND genre = ? AND ubication = ?",
                  (title, author, year, editor, pages, genre, ubication))

        conn.commit()
        conn.close()

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        # Verificar si la tabla existe, si no, crearla
        c.execute('''CREATE TABLE IF NOT EXISTS books (
                        title TEXT, 
                        author TEXT, 
                        year TEXT, 
                        editor TEXT,
                        pages NUMERIC, 
                        genre TEXT, 
                        ubication TEXT
                    )''')

        # Ahora intenta seleccionar los datos
        result = c.execute("SELECT title, author, year, editor, pages, genre, ubication FROM books")
        
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                # Si estamos en la columna de páginas, establecer los datos numéricos
                if column_number == 4:  # Índice de la columna "Nº de páginas"
                    item.setData(Qt.DisplayRole, int(data))  # Asegura que los datos se traten como números
                self.table.setItem(row_number, column_number, item)

        conn.close()
