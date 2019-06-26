#!/usr/bin/env python3
# Workload evenly distributed 
# for Jan and Maxi

from PyQt5 import QtGui, QtCore, QtWidgets
import wiimote
import sys
import time
import random


class WiiGame(QtWidgets.QWidget):

    def __init__(self, btAddr):
        super(WiiGame, self).__init__()
        self.connectingWiimote(btAddr)
        self.initUI()
        self.game_running = False
        self.text = "Press A for blue squares\n" + "And B for red squares\n\n" + "PRESS A or B to start"
        self.max_points = 25
        self.points = 0
        self.timer = QtCore.QTime()
        self.gameInterface()

    def gameInterface(self):
        while True:
            QtGui.QGuiApplication.processEvents()
            if self.wm.buttons["A"]:
                self.inputEvent("A")
            if self.wm.buttons["B"]:
                self.inputEvent("B")
            time.sleep(0.1)

    def inputEvent(self, ev):
        if not self.game_running:
            self.game_running = True
            self.text = ""
            self.current_target = random.getrandbits(1)
            self.timer.start()

        else:
            self.checkInput(ev)
            self.current_target = None
            self.update()

            QtGui.QGuiApplication.processEvents()
            time.sleep(0.3)
            self.current_target = random.getrandbits(1)

        self.update()

    def checkInput(self, ev):
        if (not self.current_target and ev == "A") or (self.current_target and ev == "B"):
            self.points += 1
        else:
            self.wm.rumble(0.2)
            self.points -= 1

        if self.points < 0:
            self.game_running = False
            self.text = "You LOOOOOSE"
            self.update()
            QtGui.QGuiApplication.processEvents()
            time.sleep(2)
            sys.exit(0)

        if self.points == self.max_points:
            self.game_running = False
            self.text = "Your time was: "+str(self.timer.elapsed()/1000)+" seconds"
            self.update()
            QtGui.QGuiApplication.processEvents()
            time.sleep(4)
            sys.exit(0)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawInfo(event, qp)
        self.drawTargets(event, qp)
        self.drawPoints(event, qp)
        qp.end()

    def drawInfo(self, event, qp):
        qp.setPen(QtGui.QColor(10, 10, 10))
        qp.setFont(QtGui.QFont("Decorative", 15))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

    def drawTargets(self, event, qp):
        if self.game_running:
            if self.current_target is None:
                qp.setBrush(QtGui.QColor(240, 240, 240))
                self.current_rect = QtCore.QRect(0, 0, 401, 401)
            elif not self.current_target:
                qp.setBrush(QtGui.QColor(34, 34, 200))
                self.current_rect = QtCore.QRect(150, 150, 100, 100)
            elif self.current_target:
                qp.setBrush(QtGui.QColor(200, 34, 34))
                self.current_rect = QtCore.QRect(150, 150, 100, 100)

            qp.drawRect(self.current_rect)

    def drawPoints(self, event, qp):
        qp.setPen(QtGui.QColor(255, 1, 1))
        qp.setFont(QtGui.QFont("Helvetiva", 15))
        qp.drawText(370, 20, str(self.points))

    def initUI(self):
        self.setGeometry(0, 0, 400, 400)
        self.setWindowTitle("WiiGame")
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setStyleSheet("QWidget {background: 'white',}")
        self.show()

    def connectingWiimote(self, btAddr):
        addr = btAddr
        name = None
        self.wm = wiimote.connect(addr, name)


def main():
    app = QtWidgets.QApplication(sys.argv)
    wii_game = WiiGame(sys.argv[1])
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
