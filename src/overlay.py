from PyQt5 import QtWidgets, QtCore, QtGui
from pynput import keyboard
import sys

class OverlayWindow(QtWidgets.QWidget):
    toggle_signal = QtCore.pyqtSignal()
    def __init__(self, rectangles, screen_width=1920, screen_height=1080):
        super().__init__()
        self.rectangles = rectangles
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setGeometry(0, 0, screen_width, screen_height)
        ##
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.activateWindow()
        self.raise_()
        self.setFocus()
        ##
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        for rect, color in self.rectangles:
            pen = QtGui.QPen(QtGui.QColor(*color), 3)
            qp.setPen(pen)
            qp.drawRect(*rect)

    def toggle_vissibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.raise_()
            self.setFocus()

    def listen_for_hotkey(overlay):
        def on_press(key):
            # F8 key = Key.f8, Esc = Key.esc
            try:
                if key == keyboard.Key.f8:
                    overlay.toggle_signal.emit()
                elif key == keyboard.Key.esc:
                    QtWidgets.QApplication.quit()
                    listener.stop()
                    sys.exit(0)
            except Exception as e:
                print(e)

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()