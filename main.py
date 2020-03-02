#!/usr/bin/python3

from main_window import Umbrella_samping_Main_Window
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


if __name__ == '__main__':
    umbrella_sampling_app = QApplication(sys.argv)

    window = Umbrella_samping_Main_Window()
    window.show()

    sys.exit(umbrella_sampling_app.exec_())
