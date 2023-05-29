import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QLabel, QComboBox
import networkx as nx
import matplotlib.pyplot as plt

class NodosView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    View = NodosView()
    View.show()
    #View.drawGraph()  
    sys.exit(app.exec_())