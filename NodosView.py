import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QFrame, QTextEdit, QListWidget
import networkx as nx
import matplotlib.pyplot as plt
import json

class NodosView(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)
        Safe_Graph = nx.DiGraph()

        with open("datos.json") as file:
            self.data = json.load(file)

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
        for barrio in self.data["lugares"]:
            nombre = barrio["nombre"]
            Safe_Graph.add_node(nombre, color="blue")
            nodos.append(nombre)

        # Crear las conexiones en base a la información del archivo JSON
        for conexion in self.data["conexiones"]:
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
        self.lbSafes = self.findChild(QTextEdit, "lbSafes")
        self.lbSafes.setReadOnly(True) 
        self.lbShort = self.findChild(QTextEdit, "lbShort")
        self.lbShort.setReadOnly(True) 
        self.listOrigin = self.findChild(QListWidget, "listOrigin")
        self.listDestination = self.findChild(QListWidget, "listDestination")

        self.lbImagen = self.findChild(QLabel, "lbImagen")
        self.lbImagen.setScaledContents(True)

    def obtener_incidentes(self,lugar):
        homicidios = 0
        robos = 0
        residencial = 0

        for conexion in self.data['conexiones']:
            origen = conexion['origen']
            destino = conexion['destino']

            if origen == lugar or destino == lugar:
                if 'incidentes' in conexion:
                    if 'Homicidio' in conexion['incidentes']:
                        homicidios += conexion['incidentes']['Homicidio']
                    if 'Robo' in conexion['incidentes']:
                        robos += conexion['incidentes']['Robo']
                    if 'Residencial' in conexion['incidentes']:
                        residencial += conexion['incidentes']['Residencial']

        return homicidios, robos, residencial

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

    def isKeyList(self, key, lista):
        for i in lista:
            if i == key:
                return True
        return False
 
    def calculateRoute(self):
        source = self.comboOrigin.currentText()  
        self.uploadListOrigin(source)

        target = self.comboDestination.currentText()
        self.uploadListDestination(target)
        
        safe_path = nx.dijkstra_path(self.Safe_Graph, source=source, target=target, weight='weight')
        self.lbSafes.setText(' -> '.join(safe_path))
        short_path = nx.dijkstra_path(self.Safe_Graph, source=source, target=target, weight=True)
        self.lbShort.setText(' -> '.join(short_path))
        color_map = nx.get_node_attributes(self.Safe_Graph, "color")

        for key in color_map:
            if self.isKeyList(key, safe_path):
                color_map[key] = "green"

        danger_colors = [color_map.get(node) for node in self.Safe_Graph.nodes()]

        pos = nx.layout.fruchterman_reingold_layout(self.Safe_Graph)
        plt.close('all')
        nx.draw_networkx(self.Safe_Graph, pos, node_color=danger_colors)
        labels = nx.get_edge_attributes(self.Safe_Graph, 'weight')
        nx.draw_networkx_edge_labels(self.Safe_Graph, pos, edge_labels=labels)
        plt.savefig("graph.png") 
        self.refreshFrame()
    
    def uploadListOrigin(self,source):
        homicidios, robos, residencial = self.obtener_incidentes(source)
        self.listOrigin.clear()
        self.listOrigin.addItem(f"Número de homicidios={homicidios}")
        self.listOrigin.addItem(f"Número de robos={robos}")
        self.listOrigin.addItem(f"Número urto residencial={residencial}")
    
    def uploadListDestination(self,target):
        homicidios, robos, residencial = self.obtener_incidentes(target)
        self.listDestination.clear()
        self.listDestination.addItem(f"Número de homicidios={homicidios}")
        self.listDestination.addItem(f"Número de robos={robos}")
        self.listDestination.addItem(f"Número urto residencial={residencial}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    View = NodosView()
    View.show()
    View.drawGraph()  
    View.refreshFrame()
    sys.exit(app.exec_())
