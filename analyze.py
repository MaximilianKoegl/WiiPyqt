
from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import wiimote
from wiimote_node import WiimoteNode, BufferNode
import sys

# Workload evenly distributed
# for Jan and Maxi


class NormalVectorNode(Node):

    nodeName = "NormalVector"

    def __init__(self, name):
        terminals = {
            'dataInX': dict(io='in'),
            'dataInZ': dict(io='in'),
            'dataOut': dict(io='out'),
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        x = kwds['dataInX'][len(kwds['dataInX'])-1]-500
        z = kwds['dataInZ'][len(kwds['dataInZ'])-1]-500
        grad = np.arccos((x)/np.sqrt(x*x+z*z))
        new_x = np.cos(grad)*1000
        new_z = np.sin(grad)*1000
        if z < 0:
            new_z = -new_z
        return {'dataOut': np.array([(0, 0), (new_x, new_z)])}

fclib.registerNodeType(NormalVectorNode, [('Data',)])


class LogNode(Node):

    nodeName = "LogNode"

    def __init__(self, name):
        terminals = {
            'dataInX': dict(io='in'),
            'dataInY': dict(io='in'),
            'dataInZ': dict(io='in'),
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        x = kwds['dataInX'][len(kwds['dataInX'])-1]
        y = kwds['dataInY'][len(kwds['dataInZ'])-1]
        z = kwds['dataInZ'][len(kwds['dataInZ'])-1]

        print("X-Value: " + str(x))
        print("Y-Value: " + str(y))
        print("Z-Value: " + str(z)+"\n")

fclib.registerNodeType(LogNode, [('Data',)])


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle("AnalyzeWiimote")
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()
    cw.setLayout(layout)

    fc = Flowchart(terminals={
    })
    w = fc.widget()
    layout.addWidget(fc.widget(), 0, 0, 2, 1)

    # set plots and X-, Y-, Z-Nodes
    pwX = pg.PlotWidget(title="X-Axis")
    layout.addWidget(pwX, 0, 1)
    pwX.setYRange(0, 1024)
    pwXNode = fc.createNode('PlotWidget', pos=(500, -150))
    pwXNode.rename("X-Axis")
    pwXNode.setPlot(pwX)

    pwY = pg.PlotWidget(title="Y-Axis")
    layout.addWidget(pwY, 0, 2)
    pwY.setYRange(0, 1024)
    pwYNode = fc.createNode('PlotWidget', pos=(500, 0))
    pwYNode.rename("Y-Axis")
    pwYNode.setPlot(pwY)

    pwZ = pg.PlotWidget(title="Z-Axis")
    layout.addWidget(pwZ, 0, 3)
    pwZ.setYRange(0, 1024)
    pwZNode = fc.createNode('PlotWidget', pos=(500, 150))
    pwZNode.rename("Z-Axis")
    pwZNode.setPlot(pwZ)

    pwNormal = pg.PlotWidget(title="Normal-Vector")
    layout.addWidget(pwNormal, 0, 4)
    pwNormal.setYRange(-1024, 1024)
    pwNormal.setXRange(-1024, 1024)
    pwNormalNode = fc.createNode('PlotWidget', pos=(500, 300))
    pwNormalNode.rename("Normal Vector")
    pwNormalNode.setPlot(pwNormal)

    # connect Wiimote
    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0), )
    wiimoteNode.wiimote = wiimote.connect(sys.argv[1], None)
    wiimoteNode.set_update_rate(20.0)

    # create buffer- , log- and normalVector-Node
    logNode = fc.createNode("LogNode", pos=(300, 0))
    bufferNodeX = fc.createNode('Buffer', pos=(150, -150))
    bufferNodeX.rename("Buffer-X")
    bufferNodeY = fc.createNode('Buffer', pos=(150, -0))
    bufferNodeY.rename("Buffer-Y")
    bufferNodeZ = fc.createNode('Buffer', pos=(150, 150))
    bufferNodeZ.rename("Buffer-Z")
    normalVectorNode = fc.createNode("NormalVector", pos=(300, 300))

    # connect Nodes
    fc.connectTerminals(wiimoteNode['accelX'], bufferNodeX['dataIn'])
    fc.connectTerminals(bufferNodeX['dataOut'], pwXNode['In'])

    fc.connectTerminals(wiimoteNode['accelY'], bufferNodeY['dataIn'])
    fc.connectTerminals(bufferNodeY['dataOut'], pwYNode['In'])

    fc.connectTerminals(wiimoteNode['accelZ'], bufferNodeZ['dataIn'])
    fc.connectTerminals(bufferNodeZ['dataOut'], pwZNode['In'])

    fc.connectTerminals(bufferNodeX['dataOut'], normalVectorNode['dataInX'])
    fc.connectTerminals(bufferNodeZ['dataOut'], normalVectorNode['dataInZ'])
    fc.connectTerminals(normalVectorNode['dataOut'], pwNormalNode['In'])

    fc.connectTerminals(bufferNodeX['dataOut'], logNode['dataInX'])
    fc.connectTerminals(bufferNodeY['dataOut'], logNode['dataInY'])
    fc.connectTerminals(bufferNodeZ['dataOut'], logNode['dataInZ'])

    win.show()
    QtGui.QApplication.instance().exec()
