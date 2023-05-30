import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox,QFrame
import networkx as nx
import matplotlib.pyplot as plt
import json

class NodosView(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)
        Safe_Graph = nx.DiGraph()

        json_file = "datos.json"

        with open(json_file) as file:
            data = json.load(file)

        def calculateWeight(array):
            names = []
            peso = 0
            #obtenemos nombres de los incidentes
            for name in array:
                names.append(name)
            #se suma el peso
            for i in range(len(names)):
                peso += array[names[i]]
            
            return peso
        def add_Connection(Graph, node1, node2, wei=1, di=False):
            Graph.add_edge(node1, node2, weight=wei)
            if not di:
                Graph.add_edge(node2, node1, weight=wei)

        nodos = []
        # Crear los nodos en base a la información del archivo JSON
        for barrio in data["lugares"]:
            nombre = barrio["nombre"]
            Safe_Graph.add_node(nombre, color="blue")
            nodos.append(nombre)

        # Crear las conexiones en base a la información del archivo JSON
        for conexion in data["conexiones"]:
            origen = conexion["origen"]
            destino = conexion["destino"]
            peso = calculateWeight(conexion["incidentes"])

            #se crea la conexion
            add_Connection(Safe_Graph, origen, destino, peso)

        self.comboOrigin = self.findChild(QComboBox, "comboOrigin")
        self.comboOrigin.clear()
        self.comboOrigin.addItems(nodos)

        self.comboDestination = self.findChild(QComboBox, "comboDestination")
        self.comboDestination.clear()
        self.comboDestination.addItems(nodos)

        self.Safe_Graph = Safe_Graph
        self.frame = self.findChild(QFrame, "frameSide")
        self.btn_CalculateRoute = self.frame.findChild(QPushButton, "btn_CalculateRoute")
        self.btn_CalculateRoute.clicked.connect(self.calculateRoute) 
        self.lbSafe = self.findChild(QLabel, "lbSafe")
        self.lbShort = self.findChild(QLabel, "lbShort")

        self.lbImagen = self.findChild(QLabel, "lbImagen")
        self.lbImagen.setScaledContents(True)

    def drawGraph(self):
        pos = nx.layout.fruchterman_reingold_layout(self.Safe_Graph)
        nx.draw_networkx(self.Safe_Graph, pos)
        #labels = nx.get_edge_attributes(self.Safe_Graph, 'weight')
        #nx.draw_networkx_edge_labels(self.Safe_Graph, pos, edge_labels=labels)
        plt.title("Looking for the Safe Way to Walk Graph")
        plt.savefig("graph.png")     

    def refreshFrame(self):
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

        pos = nx.layout.fruchterman_reingold_layout(self.Safe_Graph)
        plt.close('all')
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
