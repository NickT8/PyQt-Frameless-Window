# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication

from qframelesswindow import AcrylicWindow

from __feature__ import snake_case  # isort: skip  # noqa: F401


class Window(AcrylicWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_window_title("Acrylic Window")
        self.title_bar.raise_()

        # customize acrylic effect
        # self.windowEffect.setAcrylicEffect(self.win_id(), "106EBE99")

        # you can also enable mica effect on Win11
        # self.windowEffect.setMicaEffect(self.win_id(), isDarkMode=False, isAlt=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
