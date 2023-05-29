import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox,QFrame
import networkx as nx
import matplotlib.pyplot as plt

class NodosView(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)
        Safe_Graph = nx.DiGraph()
        nodos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "Z"]
        self.comboOrigin = self.findChild(QComboBox, "comboOrigin")
        self.comboOrigin.clear()
        self.comboOrigin.addItems(nodos)

        self.comboDestination = self.findChild(QComboBox, "comboDestination")
        self.comboDestination.clear()
        self.comboDestination.addItems(nodos)

        for nodo in nodos:
            Safe_Graph.add_node(nodo, color="blue")

        def add_Connection(Graph, node1, node2, wei=1, di=False):
            Graph.add_edge(node1, node2, weight=wei)
            if not di:
                Graph.add_edge(node2, node1, weight=wei)

        add_Connection(Safe_Graph, nodos[0], nodos[2], 1)
        add_Connection(Safe_Graph, nodos[11], nodos[2], 2)
        add_Connection(Safe_Graph, nodos[3], nodos[4])
        add_Connection(Safe_Graph, nodos[3], nodos[5], 4)
        add_Connection(Safe_Graph, nodos[4], nodos[5])
        add_Connection(Safe_Graph, nodos[2], nodos[6], 3)
        add_Connection(Safe_Graph, nodos[6], nodos[7], 10)
        add_Connection(Safe_Graph, nodos[7], nodos[8], 2)
        add_Connection(Safe_Graph, nodos[7], nodos[9], 6)
        add_Connection(Safe_Graph, nodos[7], nodos[0], 20)
        add_Connection(Safe_Graph, nodos[9], nodos[10], 4)
        add_Connection(Safe_Graph, nodos[6], nodos[5], 2)
        add_Connection(Safe_Graph, nodos[6], nodos[4], 2)
        add_Connection(Safe_Graph, nodos[9], nodos[3], 2)
        add_Connection(Safe_Graph, nodos[7], nodos[1], 1)
        add_Connection(Safe_Graph, nodos[11], nodos[1], 1)
       

        self.Safe_Graph = Safe_Graph
        self.frame = self.findChild(QFrame, "frameSide")
        self.btn_CalculateRoute = self.frame.findChild(QPushButton, "btn_CalculateRoute")
        self.btn_CalculateRoute.clicked.connect(self.calculateRoute) 
        self.lbSafe = self.findChild(QLabel, "lbSafe")
        self.lbShort = self.findChild(QLabel, "lbShort")

    def drawGraph(self):
        pos = nx.layout.planar_layout(self.Safe_Graph)
        nx.draw_networkx(self.Safe_Graph, pos)
        labels = nx.get_edge_attributes(self.Safe_Graph, 'weight')
        nx.draw_networkx_edge_labels(self.Safe_Graph, pos, edge_labels=labels)
        plt.title("Looking for the Safe Way to Walk Graph")
        plt.savefig("graph.png")     

    def refreshFrame(self):
        self.lbImagen.setScaledContents(True)
        self.lbImagen = self.findChild(QLabel, "lbImagen")
        pixmap = QPixmap('graph.png')  
        self.lbImagen.setPixmap(pixmap)
        self.frame.update()

    def isKeyList(self,key, lista):
        for i in lista:
            if i == key:
                return True
        return False
 
    def calculateRoute(self):
        source = self.comboOrigin.currentText()  
        target = self.comboDestination.currentText()
        safe_path = nx.dijkstra_path(self.Safe_Graph, source=source, target=target,weight='weight')
        self.lbSafe.setText(' -> '.join(safe_path))
        short_path = nx.dijkstra_path(self.Safe_Graph, source=source, target=target,weight=True)
        self.lbShort.setText(' -> '.join(short_path))
        color_map = nx.get_node_attributes(self.Safe_Graph, "color")

        for key in color_map:
            if self.isKeyList(key,safe_path):
                color_map[key] = "green"

        danger_colors = [color_map.get(node) for node in self.Safe_Graph.nodes()]

        pos = nx.layout.planar_layout(self.Safe_Graph)
        nx.draw_networkx(self.Safe_Graph,pos, node_color=danger_colors)
        labels = nx.get_edge_attributes(self.Safe_Graph, 'weight')
        nx.draw_networkx_edge_labels(self.Safe_Graph,pos, edge_labels=labels)
        plt.savefig("graph.png") 
        self.refreshFrame()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    View = NodosView()
    View.show()
    View.drawGraph()  
    View.refreshFrame()
    sys.exit(app.exec_())
