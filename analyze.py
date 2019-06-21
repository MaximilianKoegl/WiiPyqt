
from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import wiimote
import wiimote_node
import sys
# TODO read blutooth address and connect automatically

class NormalVectorNode(Node):
  
    nodeName = "NormalVector"

    def __init__(self, name):
        terminals = {
            'dataInX': dict(io='in'),
            'dataInY': dict(io='in'),
            'dataOut': dict(io='out'),
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        # TODO calculate rotation and return two points in tuple for direction of axis
        x = kwds['dataInX'][len(kwds['dataInX'])-1]-500
        y = kwds['dataInY'][len(kwds['dataInY'])-1]-500
        z = (0, 0, x*y)
       
        return {'dataOut': np.array([(10, 10), (x, y)])}

fclib.registerNodeType(NormalVectorNode, [('Data',)])


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

    pwX = pg.PlotWidget(title="X-Axis")
    layout.addWidget(pwX, 0, 1)
    pwX.setYRange(0, 1024)
    pwXNode = fc.createNode('PlotWidget', pos=(300, -150))
    pwXNode.rename("X-Axis")
    pwXNode.setPlot(pwX)

    pwY = pg.PlotWidget(title="Y-Axis")
    layout.addWidget(pwY, 0, 2)
    pwY.setYRange(0, 1024)
    pwYNode = fc.createNode('PlotWidget', pos=(300, 0))
    pwYNode.rename("Y-Axis")
    pwYNode.setPlot(pwY)

    pwZ = pg.PlotWidget(title="Z-Axis")
    layout.addWidget(pwZ, 0, 3)
    pwZ.setYRange(0, 1024)
    pwZNode = fc.createNode('PlotWidget', pos=(300, 150))
    pwZNode.rename("Z-Axis")
    pwZNode.setPlot(pwZ)

    pwNormal = pg.PlotWidget(title="Normal-Vector")
    layout.addWidget(pwNormal, 0, 4)
    pwNormal.setYRange(0, 1024)
    pwNormalNode = fc.createNode('PlotWidget', pos=(300, 300))
    pwNormalNode.rename("Normal Vector")
    pwNormalNode.setPlot(pwNormal)

    wiimoteNode = fc.createNode('Wiimote', pos=(0, 0), )
    bufferNodeX = fc.createNode('Buffer', pos=(150, -150))
    bufferNodeX.rename("Buffer-X")
    bufferNodeY = fc.createNode('Buffer', pos=(150, -0))
    bufferNodeY.rename("Buffer-Y")
    bufferNodeZ = fc.createNode('Buffer', pos=(150, 150))
    bufferNodeZ.rename("Buffer-Z")
    normalVectorNode = fc.createNode("NormalVector", pos=(150, 300))

    fc.connectTerminals(wiimoteNode['accelX'], bufferNodeX['dataIn'])
    fc.connectTerminals(bufferNodeX['dataOut'], pwXNode['In'])

    fc.connectTerminals(wiimoteNode['accelY'], bufferNodeY['dataIn'])
    fc.connectTerminals(bufferNodeY['dataOut'], pwYNode['In'])

    fc.connectTerminals(wiimoteNode['accelZ'], bufferNodeZ['dataIn'])
    fc.connectTerminals(bufferNodeZ['dataOut'], pwZNode['In'])

    fc.connectTerminals(bufferNodeX['dataOut'], normalVectorNode['dataInX'])
    fc.connectTerminals(bufferNodeY['dataOut'], normalVectorNode['dataInY'])
    fc.connectTerminals(normalVectorNode['dataOut'], pwNormalNode['In'])

    win.show()
    QtGui.QApplication.instance().exec()