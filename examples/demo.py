# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QLabel

from qframelesswindow import FramelessWindow, StandardTitleBar

from __feature__ import snake_case  # isort: skip  # noqa: F401


class CustomTitleBar(StandardTitleBar):
    """Custom title bar"""

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.min_btn.set_hover_color(Qt.white)
        self.min_btn.set_hover_background_color(QColor(0, 100, 182))
        self.min_btn.set_pressed_color(Qt.white)
        self.min_btn.set_pressed_background_color(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.max_btn.set_style_sheet(
            """
            TitleBarButton {
                qproperty-hover_color: white;
                qproperty-hover_background_color: rgb(0, 100, 182);
                qproperty-pressed_color: white;
                qproperty-pressed_background_color: rgb(54, 57, 65);
            }
        """
        )


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.set_title_bar(CustomTitleBar(self))

        self.label = QLabel(self)
        self.label.set_scaled_contents(True)
        self.label.set_pixmap(QPixmap("screenshot/shoko.png"))

        self.set_window_icon(QIcon("screenshot/logo.png"))
        self.set_window_title("PySide6-Frameless-Window")
        self.set_style_sheet("background:white")

        self.title_bar.raise_()

    def resize_event(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resize_event(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(self.width() // 2 - length // 2, self.height() // 2 - length // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
