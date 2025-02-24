# #########################################################################
# Copyright © 2020, UChicago Argonne, LLC. All Rights Reserved.           #
#                                                                         #
#                       Software Name: XRFtomo                            #
#                                                                         #
#                   By: Argonne National Laboratory                       #
#                                                                         #
#                       OPEN SOURCE LICENSE                               #
#                                                                         #
# Redistribution and use in source and binary forms, with or without      #
# modification, are permitted provided that the following conditions      #
# are met:                                                                #
#                                                                         #
# 1. Redistributions of source code must retain the above copyright       #
#    notice, this list of conditions and the following disclaimer.        #
#                                                                         #
# 2. Redistributions in binary form must reproduce the above copyright    #
#    notice, this list of conditions and the following disclaimer in      #
#    the documentation and/or other materials provided with the           #
#    distribution.                                                        #
#                                                                         #
# 3. Neither the name of the copyright holder nor the names of its        #
#    contributors may be used to endorse or promote products derived      #
#    from this software without specific prior written permission.        #
#                                                                         #
#                               DISCLAIMER                                #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR   #
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT    #
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  #
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT        #
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,   #
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY   #
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT     #
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.    #
###########################################################################


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
# from matplotlib.figure import Figure
import pyqtgraph
import xrftomo

class ScatterView(pyqtgraph.GraphicsLayoutWidget):
    mouseMoveSig = pyqtSignal(int,int, name= 'mouseMoveSig')
    mousePressSig =pyqtSignal(name= 'mousePressSig')
    keyPressSig = pyqtSignal(str, name= 'keyPressSig')
    roiDraggedSig = pyqtSignal(name= 'roiSizeSig')


    def __init__(self):
    # def __init__(self, parent):
        super(ScatterView, self).__init__()
        self.keylist = []
        self.initUI()

    def initUI(self):
        custom_vb = xrftomo.CustomViewBox()
        # custom_vb.disableAutoRange(axis="xy")
        # custom_vb.setRange(xRange=(0,1), yRange=(0,1), padding=0)
        # custom_vb.invertY(True)

        #___________________ scatter view ___________________
        self.p1 = self.addPlot(viewBox = custom_vb, enableMouse = False)
        self.p1.setAutoPan(x=None, y=None)
        # self.p1.setYRange(0,1)
        # self.p1.setXRange(0,1)
        self.plotView = pyqtgraph.ScatterPlotItem()
        self.plotView2 = pyqtgraph.ScatterPlotItem()
        # self.ROI = pyqtgraph.LineSegmentROI(positions=([0,0],[1,1]), pos=[0,0], movable=False, maxBounds=QtCore.QRectF(0, 0, 1, 1))
        self.ROI = pyqtgraph.LineSegmentROI(positions=([0,0],[1000,1000]), pos=[0,0], movable=False)
        self.ROI.sigRegionChangeFinished.connect(self.roi_dragged)
        self.p1.addItem(self.plotView)
        self.p1.addItem(self.plotView2)
        self.p1.addItem(self.ROI)
        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)
        self.p1.scene().sigMouseClicked.connect(self.mouseClick)
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.vb = custom_vb

    def roi_dragged(self):

        try:
            x2_pos = self.ROI.getHandles()[1].pos().x()
            y2_pos = self.ROI.getHandles()[1].pos().y()
            self.ROI.endpoints[1].setPos(x2_pos, y2_pos)
            self.ROI.endpoints[0].setPos(0, 0)
            self.ROI.stateChanged(finish=False)
            self.roiDraggedSig.emit()
        except:
            self.ROI.stateChanged(finish=False)
            self.roiDraggedSig.emit()

        return
    def mouseMoved(self, evt):
        self.moving_x = round(self.p1.vb.mapSceneToView(evt).x(),3)
        self.moving_y = round(self.p1.vb.mapSceneToView(evt).y(),3)
        self.mouseMoveSig.emit(self.moving_x, self.moving_y)

    def mouseClick(self, evt):
        print(self.moving_x, self.moving_y)
        x2_pos = self.moving_x
        y2_pos = self.moving_y
        if evt.button() == 1:
            try:
                self.ROI.endpoints[1].setPos(x2_pos, y2_pos)
                self.ROI.endpoints[0].setPos(0, 0)
                self.ROI.stateChanged(finish=False)
                self.mousePressSig.emit()
            except:
                self.ROI.stateChanged(finish=False)
                self.mousePressSig.emit()

        if evt.button() == 2:
            pass

        return

    def wheelEvent(self, ev):
        #empty function, but leave it as it overrides some other unwanted functionality.
        pass

    def keyPressEvent(self, ev):
        self.firstrelease = True
        astr = ev.key()
        self.keylist.append(astr)

    def keyReleaseEvent(self, ev):
        if self.firstrelease == True:
            self.processMultipleKeys(self.keylist)

        self.firstrelease = False

        try:    #complains about an index error for some reason.
            del self.keylist[-1]
        except:
            pass
        return

    def processMultipleKeys(self, keyspressed):
        if len(keyspressed) ==1:
            pass

        if len(keyspressed) == 2:
            pass

        if len(keyspressed) >=3:
            self.keylist = []
            return
