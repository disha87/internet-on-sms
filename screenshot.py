#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *


class browser(QWebView):
    def __init__(self, parent=None):
        super(browser, self).__init__(parent)

        self.timerScreen = QTimer()
        self.timerScreen.setInterval(2000)
        self.timerScreen.setSingleShot(True)
        self.timerScreen.timeout.connect(self.takeScreenshot)

        self.loadFinished.connect(self.timerScreen.start)
        self.load(QUrl(
            "http://107.170.246.247:8081/get_map?src=37.3386884%2C-121.9770935&dest=37.3375716%2C-121.8897658"))

    def takeScreenshot(self):
        image = QImage(self.page().mainFrame().contentsSize(),
                       QImage.Format_ARGB32)
        painter = QPainter(image)

        self.page().mainFrame().render(painter)

        painter.end()
        image.save('map2' + ".png")

        sys.exit()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = browser()
    app.exec_()
