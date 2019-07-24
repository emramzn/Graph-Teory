
import sys
import PyQt5
import igraph 
import igraph.test
from igraph import *
import numpy as np
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot ,pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QPen,QFont
from PyQt5.QtWidgets import QMainWindow, QApplication,QVBoxLayout, QSizePolicy, QGridLayout, QWidget, QDesktopWidget, QPushButton, QAction, QLineEdit, QMessageBox ,QLabel

import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.image as mpimg






class graphPro():
    def __init__(self):
    
        
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight              

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)

    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node )
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


counter=0
NodeArr=[]
newGraph=graphPro()
liste=[]
listWeight=[]

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Teory of The Graph '
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 480
        self.initUI()
        
          

    def clearimg(self):
        global NodeArr
        global liste
        global listWeight
        global newGraph
        global counter

        del NodeArr[::]
        del liste[::]
        del listWeight[::]
        newGraph.edges.clear
        counter=0
        self.l1.setPixmap(QPixmap("clrimage.png"))
        self.text1.setText('')
        self.text2.setText('')
        self.textdst.setText('')
        self.textsrc.setText('')
        self.textRes.setText('')
        self.labelCount.setText('')

  
    def appendFunc(self):
        global counter
        global NodeArr
        global liste
        counter+1
        if len(NodeArr)>0:
            NodeArr.append(len(NodeArr))
        else:
            NodeArr.append(0)  

        print(len(NodeArr))
        print(NodeArr)

        self.labelCount.setText(str(len(NodeArr)))
        


    def creatNode(self,fromNode,ToNode,WightNode):

      
        global newGraph
        
        if newGraph.edges is None:
            newGraph.add_edge(0,0,0)

        newGraph.add_edge(str(fromNode),str(ToNode),int(WightNode))
        print(fromNode ," --> ", ToNode ," W : ", WightNode )

        if type(newGraph.edges)== tuple:
            self.visualGraph(0,0,0)

        else:
            self.visualGraph(fromNode,ToNode,WightNode)    
        
        self.imag()

   
    def imag(self):
        
        self.l1.setPixmap(QPixmap("NodesImages.png"))
    


    def visualGraph(self,fromNode,ToNode,WightNode):
        global NodeArr
        global liste
        global listWeight

        
        if not (fromNode is None) or not (ToNode is None) :    
            liste.append((int(fromNode),int(ToNode)))
    
        for i in liste:
            print("Liste : ",(i))
       
        g=Graph(liste)

        listWeight.append(WightNode)
        VertexSeq(g)["name"]=NodeArr
        visual_style={}

        visual_style["vertex_size"]=25
        visual_style["color"]="Black"
        visual_style["vertex_label"]=VertexSeq(g)["name"]
        visual_style["Layout"]=Layout
        visual_style["bbox"]=(400,400)
        visual_style["margin"]=20
        visual_style["edge_label"]=listWeight 

        plot(g,"NodesImages.png",**visual_style)


    @pyqtSlot()
    def shortestPath(self,fromNode,ToNode):
        global newGraph 
        a=str(fromNode)
        b=str(ToNode)

        print(dijsktra(newGraph,a,b))

        deger=dijsktra(newGraph,a,b)

        
        path=""
        for i in deger:
            
            path+=i+"-->"
            print("ss : ",i)
        
        self.textRes.setText(path[0:(len(path)-3)])
        # self.textRes.resize(len(path)+150,25)

    


    def initUI(self):
        global NodeArr
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.l1 =  QLabel(self)
        self.l1.setPixmap(QPixmap("NodesImages.png"))
        self.l1.setGeometry(10,10,400,400)
        
        self.labSet=QLabel(self)
        self.labSet.move(450,0)
        self.labSet.resize(200,100)
        self.labSet.setFont(QFont('SansSerif', 12))
        self.labSet.setText("Number Of Nodes :")


        self.labelCount=QLabel(self)
        self.labelCount.move(610,2)
        self.labelCount.resize(200,100)
        self.labelCount.setFont(QFont('SansSerif', 18))
        


        self.label=QLabel("Adjacency",self)
        self.label.move(550,150)
        self.label.resize(150,25)

        self.label=QLabel("Weigth",self)
        self.label.move(610,150)
        self.label.resize(150,25)

        self.text1=QLineEdit(self)
        self.text1.move(550,180)
        self.text1.resize(50,25)
        

        self.text2=QLineEdit(self)
        self.text2.move(610,180)
        self.text2.resize(50,25)

        self.label=QLabel("CONSTRUCT GRAPH",self)
        self.label.move(450,90)
        self.label.resize(150,25)
        
        
        self.btnadd = QPushButton('Add Node', self)
        self.btnadd.move(450,130)
        self.btnadd.resize(80,40)
        self.btnadd.clicked.connect(lambda:self.appendFunc())
        
        self.btnadd = QPushButton('Clear Screen', self)
        self.btnadd.move(450,370)
        self.btnadd.resize(220,40)
        self.btnadd.clicked.connect(lambda:self.clearimg())

        
        self.btnCreat = QPushButton('Connect Node', self)
        self.btnCreat.move(450,170)
        self.btnCreat.resize(80,40)
        self.btnCreat.clicked.connect(lambda:self.creatNode(self.text1.text(),NodeArr[-1],self.text2.text()))

      


        self.label=QLabel("THE SHORTEST PATH",self)
        self.label.move(450,220)
        self.label.resize(150,25)
        
        

        self.btnShort = QPushButton('RUN', self)
        self.btnShort.move(450,250)
        self.btnShort.resize(80,40)
        self.btnShort.clicked.connect(lambda:self.shortestPath(self.textsrc.text(),self.textdst.text()))
        
        self.label=QLabel("Source",self)
        self.label.move(550,240)
        self.label.resize(150,25)

        self.label=QLabel("Destination",self)
        self.label.move(610,240)
        self.label.resize(150,25)


        self.textsrc=QLineEdit(self)
        self.textsrc.move(550,260)
        self.textsrc.resize(50,25)

        self.textdst=QLineEdit(self)
        self.textdst.move(610,260)
        self.textdst.resize(50,25)

        self.label=QLabel("RESULTS",self)
        self.label.move(450,310)
        self.label.resize(250,25)
        
        self.textRes=QLineEdit(self)
        self.textRes.move(450,330)
        self.textRes.resize(220,25)
        

      
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())
