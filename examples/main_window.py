# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMenuBar,
    QStatusBar,
    QTextEdit,
)

from qframelesswindow import FramelessDialog, FramelessMainWindow

from __feature__ import snake_case  # isort: skip  # noqa: F401


class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.set_window_title("Frameless Main Window")

        # add menu bar
        menu_bar = QMenuBar(self.title_bar)
        menu = QMenu("File(&F)", self)
        menu.add_action("open")
        menu.add_action("save")
        menu_bar.add_menu(menu)
        menu_bar.add_action("Edit(&E)")
        menu_bar.add_action("Select(&S)")
        menu_bar.add_action("Help(&H)", self.showHelpDialog)
        self.title_bar.layout().insert_widget(0, menu_bar, 0, Qt.AlignLeft)
        self.title_bar.layout().insert_stretch(1, 1)
        self.set_menu_widget(self.title_bar)

        # add status bar
        status_bar = QStatusBar(self)
        status_bar.add_widget(QLabel("row 1"))
        status_bar.add_widget(QLabel("column 1"))
        self.set_status_bar(status_bar)

        # set central widget
        self.text_edit = QTextEdit()
        self.set_central_widget(self.text_edit)

        self.set_style_sheet(
            """
            QMenuBar{background: #F0F0F0; padding: 5px 0}
            QTextEdit{border: none; font-size: 15px}
            QDialog > QLabel{font-size: 15px}
            """
        )

    def showHelpDialog(self):
        w = FramelessDialog(self)

        # add a label to dialog
        w.set_layout(QHBoxLayout())
        w.layout().add_widget(QLabel("Frameless Dialog"), 0, Qt.AlignCenter)

        # raise title bar
        w.title_bar.raise_()
        w.resize(300, 300)

        # disable resizing dialog
        w.set_resize_enabled(False)
        w.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # fix issue #50
    app.set_attribute(Qt.AA_DontCreateNativeWidgetSiblings)

    window = MainWindow()
    window.show()
    app.exec()
