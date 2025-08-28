import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QResizeEvent, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListWidget, QPushButton, QGroupBox, QHBoxLayout, \
    QWidget, QVBoxLayout, QListWidgetItem, QDialog

from src.core.vocabulary_book import VocabularyBookInfo, VocabularyBook
from src.core.vocabulary_book_manager import VocabularyBookManager
from src.ui.ui_utils import MessageBox
from src.core.word_entry import WordEntry


class WordManagerUI(QMainWindow):
    def __init__(self, book_manager: VocabularyBookManager, book_name):
        super().__init__()
        self.book_manager = book_manager
        self.book: VocabularyBook = book_manager.get_book(book_name)
        if self.book is None:
            return
        # 标题图标和窗口大小
        self.setFixedSize(500, 700)
        self.setWindowTitle(book_name)
        self.setWindowIcon(QIcon("ico.ico"))
        # 窗口置中
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.space_label = QLabel()
# 功能---------------------------------------------------------------------------------------------
        self.widget_word_list = QListWidget()

        self.button_add_word = QPushButton("Add")
        self.button_add_word.clicked.connect(self.add_word)
        self.button_delete_word = QPushButton("Delete")
        self.button_delete_word.clicked.connect(self.delete_word)
# 布局---------------------------------------------------------------------------------------------
        # 功能
        group_function = QGroupBox()
        layout_function = QHBoxLayout(group_function)
        layout_function.addWidget(self.button_add_word)
        layout_function.addWidget(self.button_delete_word)
        # 测试
        group_book_list = QGroupBox("Word List")
        layout_book_list = QHBoxLayout(group_book_list)
        layout_book_list.addWidget(self.widget_word_list)
        self.init_word_list()

        # 全局
        widget_global = QWidget()
        layout_global = QVBoxLayout(widget_global)
        layout_global.addWidget(group_book_list)
        layout_global.addWidget(group_function)
        self.setCentralWidget(widget_global)

    def init_word_list(self):
        for word_entry in self.book.get_all_words().values():
            dict_word = word_entry.to_dict()
            dict_interpretations = dict_word["Interpretations"]
            first_interpretation = ""
            for value in dict_interpretations.values():
                if isinstance(value, str) and value.strip() != "":
                    first_interpretation = value
                    break
            self.add_word_to_ui(word_entry.word, first_interpretation)

    def add_word_to_ui(self, word: str, definition: str):
        item = QListWidgetItem()
        item_size = QSize(0, 100)
        item.setSizeHint(item_size)

        word_ui = WordUI(word, definition, item_size, self.widget_word_list, item, self.book)
        self.widget_word_list.addItem(item)
        self.widget_word_list.setItemWidget(item, word_ui)

    def add_word(self):
        pass

    def delete_word(self):
        pass

    # def create_word(self):
    #     dlg = NewWordDialog(self)
    #     if dlg.exec_() == QDialog.Accepted:
    #         name, desc = dlg.values()
    #         if not name or not name.strip():
    #             return
    #     else:
    #         return
    #     logger.INFO(f"Get create info: name: {name} description: {desc}")
    #
    #     book_info = VocabularyBookInfo(name, type=BookType.USER, description=desc)
    #     logger.INFO(f"Create vocabulary book.")
    #     if self.book_manager.create_vocabulary_book(book_info):
    #         logger.INFO(f"Create book success, name: {name} description: {desc}.")
    #         self.add_book_to_ui(name, desc, BookType.USER)
    #     else:
    #         MessageBox(f"\nCreate a new vocabulary book failed! \n\nThere is already a book called:\n\n{name}\n", "Error:")

    # def load_vocabulary_book(self):
    #     dlg = LoadBookDialog(self)
    #     if dlg.exec_() == QDialog.Accepted:
    #         name, desc, path = dlg.values()
    #         if not name or not name.strip():
    #             return
    #         if not path or not path.strip():
    #             return
    #     else:
    #         return
    #     logger.INFO(f"Get load info: name: {name} description: {desc} load path: {path}")
    #
    #     book_info = VocabularyBookInfo(name, type=BookType.USER, description=desc)
    #     logger.INFO(f"Load vocabulary book.")
    #
    #     if self.book_manager.create_vocabulary_book_from_data(book_info, path):
    #         logger.INFO(f"Load book success, name: {name} description: {desc}.")
    #         self.add_book_to_ui(name, desc, BookType.USER)
    #     else:
    #         MessageBox(f"\nCreate a new vocabulary book failed! \n\nThere is already a book called:\n\n{name}\n", "Error:")

    # def export_vocabulary_book(self):
    #     dlg = ExportBookDialog(self)
    #     if dlg.exec_() == QDialog.Accepted:
    #         name, export_type, path = dlg.values()
    #         if not name or not name.strip():
    #             return
    #         if not path or not path.strip():
    #             return
    #     else:
    #         return
    #     logger.INFO(f"Get export info: name: {name} export type: {export_type.lower()} output path: {path}")
    #     try:
    #         if self.book_manager.export_vocabulary_book(name, path, ExportType[export_type.upper()]):
    #             logger.INFO(f"Export book success, name: {name} .")
    #         else:
    #             MessageBox(f"\nExport vocabulary book failed!", "Error:")
    #     except Exception as e:
    #         MessageBox(f"\nExport vocabulary book failed! \n\n{e}", "Error:")

    def resizeEvent(self, event: QResizeEvent):
        # if not self.image_label.pixmap():
        #     return
        #
        # pixmap = self.image_label.pixmap()
        # scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        # self.image_label.setPixmap(scaled_pixmap)

        super().resizeEvent(event)

class WordUI(QWidget):
    def __init__(self, word, definition, size, list_widget, item, book):
        super().__init__()
        self.word = word
        self.list_widget = list_widget
        self.item = item
        self.book = book

        layout = QHBoxLayout(self)
        widget_info = QWidget()
        layout_info = QVBoxLayout(widget_info)
        self.label_word = QLabel(word)
        font_word = QFont()
        font_word.setFamily("Consolas")
        font_word.setPointSize(12)
        font_word.setBold(True)
        self.label_word.setFont(font_word)
        self.label_definition = QLabel(definition)
        self.label_definition.setStyleSheet("color: grey;")
        layout_info.addWidget(self.label_word)
        layout_info.addWidget(self.label_definition)
        layout.addWidget(widget_info, 1)

    def remove_self(self):
        if self.book.delete_vocabulary_book(self.word):
            row = self.list_widget.row(self.item)
            self.list_widget.takeItem(row)
        else:
            MessageBox("Delete vocabulary book failed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    vocabulary_book_manager = VocabularyBookManager("default")
    book_manager_ui = WordManagerUI(vocabulary_book_manager, "50_A")
    book_manager_ui.show()
    sys.exit(app.exec_())