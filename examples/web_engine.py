# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QHBoxLayout

from qframelesswindow import FramelessWindow, StandardTitleBar
from qframelesswindow.webengine import FramelessWebEngineView


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.set_title_bar(StandardTitleBar(self))

        self.hbox_layout = QHBoxLayout(self)

        # must replace QWebEngineView with FramelessWebEngineView
        self.web_engine = FramelessWebEngineView(self)

        self.hbox_layout.set_contents_margins(0, self.title_bar.height(), 0, 0)
        self.hbox_layout.add_widget(self.web_engine)

        # load web page
        self.web_engine.load("https://qfluentwidgets.com/")
        self.resize(1200, 800)

        self.title_bar.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
