#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import argparse
parser = argparse.ArgumentParser(description='Process args.')
parser.add_argument('src', type=str,
                    help='an integer for the accumulator')
parser.add_argument('dst', type=str,
                    help='an integer for the accumulator')
parser.add_argument('filename', type=str,
                    help='an integer for the accumulator')


class browser(QWebView):
    def __init__(self, parent=None):
        super(browser, self).__init__(parent)

        self.timerScreen = QTimer()
        self.timerScreen.setInterval(2000)
        self.timerScreen.setSingleShot(True)
        self.timerScreen.timeout.connect(self.takeScreenshot)

        self.loadFinished.connect(self.timerScreen.start)
        global parser
        args = parser.parse_args()
        print args
        self.filename = args.filename
        url = "http://107.170.246.247:8081/get_map?src=" + args.src \
            + "&dest=" + args.dst
        self.load(QUrl(url))

    def takeScreenshot(self):
        image = QImage(self.page().mainFrame().contentsSize(),
                       QImage.Format_ARGB32)
        painter = QPainter(image)

        self.page().mainFrame().render(painter)

        painter.end()
        image.save(self.filename + ".png")

        sys.exit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = browser()
    app.exec_()
