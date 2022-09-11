import json
import os
import sys
from ctypes import windll
from os.path import join as pjoin

# from PyQt5.QtGui import QPixmap
from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QFontDatabase, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)

AppID = "advik.desktop_launcher.1"
windll.shell32.SetCurrentProcessExplicitAppUserModelID(AppID)

from plyer import notification

notification.notify(
    title="testing",
    message="message",
    app_icon="assets/rocket.ico",
    timeout=10,
)


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Desktop Launcher")
        self.resize(1000, 600)
        self.backgroundimage = QLabel(self)
        self.backgroundimage_pixmap = QPixmap("macos.png")
        self.backgroundimage_pixmap_orignal = self.backgroundimage_pixmap
        self.backgroundimage.setPixmap(self.backgroundimage_pixmap)

        winT = Qt.WindowType

        self.setWindowFlags(
            # winT.WindowOverridesSystemGestures |
            # winT.NoDropShadowWindowHint |
            winT.WindowTitleHint
            | winT.CustomizeWindowHint
            | winT.WindowCloseButtonHint  # |
            # winT.WindowMaximizeButtonHint
        )
        del winT
        # Make the window fullscreen
        self.maxi = False
        Screen_s = QShortcut(self)
        Screen_s.setKey("F11")
        Screen_s.activated.connect(self.toggleScreen)
        self.show()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.backgroundimage.resize(self.size())
        self.backgroundimage_pixmap = self.backgroundimage_pixmap_orignal.scaled(
            self.size()
        )
        self.backgroundimage.setPixmap(self.backgroundimage_pixmap)

    def closeEvent(self, a0):
        confirmarion = QMessageBox.question(
            self,
            "Desktop Launcher - Confirm Exit",
            "Are you sure you want to exit Desktop Launcher?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmarion == QMessageBox.StandardButton.Yes:
            a0.accept()
        else:
            a0.ignore()

    def toggleScreen(self):
        if self.maxi:
            self.showNormal()
            self.maxi = False
        else:
            self.showMaximized()
            self.maxi = True


def main():
    global QFontDatabase
    app = QApplication(sys.argv)
    fontDB = QFontDatabase
    del QFontDatabase

    for root, dirs, files in os.walk("fonts"):
        for file in files:
            if file.endswith(".ttf") or file.endswith(".otf"):
                pth = pjoin(root, file).replace("\\", "/")
                fontDB.addApplicationFont(pth)
                del pth
    del root, dirs, files, file
    ui = UI()
    app.exec()


def create_settings():
    default_settings = {
        "window_flags": [
            "WindowTitleHint",
            "CustomizeWindowHint",
            "WindowCloseButtonHint"
        ],
        "current_theme": "dark",
        "wallpaper": "res://assets/PR-Demo.png",
    }
    with open("settings.json", "wb") as f:
        f.write(json.dumps(default_settings).encode("utf-8"))


if __name__ == "__main__":
    main()
