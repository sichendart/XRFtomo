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


from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import pyqtgraph
import xrftomo

class ImageView(pyqtgraph.GraphicsLayoutWidget):
    # shiftSig = pyqtSignal(str, name='sliderChangedSig')
    mouseMoveSig = pyqtSignal(int,int, name= 'mouseMoveSig')
    mousePressSig =pyqtSignal(int, name= 'mousePressSig')
    keyPressSig = pyqtSignal(str, name= 'keyPressSig')
    roiSizeSig = pyqtSignal(int, int, name= 'roiSizeSig')


    def __init__(self):
    # def __init__(self, parent):
        super(ImageView, self).__init__()
        # self.parent = parent
        self.hotSpotNumb = 0
        self.xSize = 10
        self.ySize = 10
        self.x_pos = 5
        self.y_pos = 5
        self.cross_pos_x = 5
        self.cross_pos_y = 5
        self.keylist = []
        self.firstrelease = False
        self.initUI()

    def initUI(self):
        custom_vb = xrftomo.CustomViewBox()
        # custom_vb.invertY(True)
        self.p1 = self.addPlot(viewBox = custom_vb, enableMouse = False)
        self.projView = pyqtgraph.ImageItem(axisOrder = "row-major")
        self.projView.rotate(0)
        self.projView.iniX = 0
        self.projView.iniY = 0
        self.ROI = pyqtgraph.ROI([self.projView.iniX, self.projView.iniY], [10, 10], scaleSnap = True)
        self.ROI.addScaleHandle(pos=(1, 1), center=(0,0))
        self.ROI.addScaleHandle(pos=(0,0), center=(1,1))
        self.ROI.addScaleHandle(pos=(0,1), center=(1,0))
        self.ROI.addScaleHandle(pos=(1,0), center=(0,1))
        # self.ROI.addFreeHandle()
        # self.cross_h = p1.pyqtgraph.PlotItem.addLine(x=10, y=10, z=0)
        self.p1.addItem(self.projView)
        self.p1.addItem(self.ROI)
        self.cross_v = self.p1.addLine(x=10)
        self.cross_h = self.p1.addLine(y=10)
        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)
        self.ROI.sigRegionChangeFinished.connect(self.roi_dragged)
        self.p1.scene().sigMouseClicked.connect(self.mouseClick)
        # self.p1.scene().sceneRectChanged.connect(self.windowResize)
        self.p1.setMouseEnabled(x=False, y=False)
        self.p1.vb = custom_vb

    # def windowResize(self, evt):
    #     pass

    def roi_dragged(self):
        x_pos = round(self.ROI.pos().x())
        y_pos = round(self.ROI.pos().y())
        xSize = int(self.ROI.size()[0])
        ySize = int(self.ROI.size()[1])
        frame_height = self.projView.height()
        frame_width = self.projView.width()
        self.x_pos, self.y_pos, self.xSize, self.ySize = self.update_roi(x_pos, y_pos, xSize, ySize, frame_height, frame_width)
        self.ROI.setPos([self.x_pos, self.y_pos], finish=False)

    def mouseMoved(self, evt):
        self.moving_x = int(round(self.p1.vb.mapSceneToView(evt).x()))
        self.moving_y = int(round(self.p1.vb.mapSceneToView(evt).y()))
        self.mouseMoveSig.emit(self.moving_x, self.moving_y)

    def mouseClick(self, evt):
        x_pos = self.moving_x
        y_pos = self.moving_y
        frame_height = self.projView.height()
        frame_width = self.projView.width()
        xSize = int(self.ROI.size()[0])
        ySize = int(self.ROI.size()[1])

        if evt.button() == 1:
            self.x_pos, self.y_pos, self.xSize, self.ySize = self.update_roi(x_pos-xSize//2, y_pos-ySize//2, xSize, ySize, frame_height, frame_width)
            self.ROI.setPos([self.x_pos, self.y_pos], finish=False)
            self.mousePressSig.emit(1)

        if evt.button() == 2:
            self.cross_pos_x, self.cross_pos_y = self.update_crosshair(x_pos, y_pos, frame_height, frame_width)
            try:

                self.p1.items[2].setValue(self.cross_pos_x)
                self.p1.items[3].setValue(self.cross_pos_y)
            except:
                try:
                    self.p1.items[3].setValue(self.cross_pos_x)
                    self.p1.items[4].setValue(self.cross_pos_y)
                except:
                    print("cant plot crosshair")


            self.mousePressSig.emit(2)


    def update_crosshair(self,x_pos, y_pos, frame_height, frame_width):
        cross_pos_x = x_pos
        cross_pos_y = y_pos
        max_y = frame_height
        max_x = frame_width

        ## if way far left
        if cross_pos_x <= 0 :
            cross_pos_x = 0
        ## if way far right
        if cross_pos_x >= max_x:
            cross_pos_x = max_x
        ## if way far above
        if cross_pos_y >= max_y :
            cross_pos_y = max_y
        ## if way far below
        if cross_pos_y <= 0:
            cross_pos_y = 0

        self.cross_pos_x = cross_pos_x
        self.cross_pos_y = cross_pos_y

        return cross_pos_x, cross_pos_y

    def update_roi(self, x_pos, y_pos, x_size, y_size, frame_height, frame_width):
        max_y = frame_height
        max_x = frame_width

        if x_size > max_x:
            x_size = max_x

        if y_size > max_y:
            y_size = max_y

        self.ROI.setSize([x_size, y_size], finish=False)

        if max_x == None or max_y == None:
             return 0, 0, 0, 0

        roi_left =x_pos
        roi_right = x_pos+x_size
        roi_top = y_pos+y_size
        roi_bottom = y_pos

        ## if way far left
        if roi_left <= 0:
            x_pos = 0
        ## if way far right
        if roi_right >= max_x:
            x_pos = max_x - x_size
        ## if way far above
        if roi_top >= max_y:
            y_pos = max_y-y_size
        ## if way far below
        if roi_bottom <= 0:
            y_pos = 0

        self.x_pos = x_pos
        self.y_pos = y_pos

        return x_pos, y_pos, x_size, y_size

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
            if keyspressed[0]== QtCore.Qt.Key_Left:
                self.keyPressSig.emit('left')
            if keyspressed[0] == QtCore.Qt.Key_Right:
                self.keyPressSig.emit('right')
            if keyspressed[0] == QtCore.Qt.Key_Up:
                self.keyPressSig.emit('up')
            if keyspressed[0] == QtCore.Qt.Key_Down:
                self.keyPressSig.emit('down')
            if keyspressed[0] == QtCore.Qt.Key_N:
                self.keyPressSig.emit('Next')
            if keyspressed[0] == QtCore.Qt.Key_S:
                self.keyPressSig.emit('Skip')
            if keyspressed[0] == QtCore.Qt.Key_Delete:
                self.keyPressSig.emit('Delete')
            if keyspressed[0] == QtCore.Qt.Key_A:
                self.keyPressSig.emit('A')
            if keyspressed[0] == QtCore.Qt.Key_D:
                self.keyPressSig.emit('D')

        if len(keyspressed) == 2:
            if keyspressed[0] == QtCore.Qt.Key_Shift and keyspressed[1] == QtCore.Qt.Key_Left:
                self.keyPressSig.emit('shiftLeft')
                return
            if keyspressed[0] == QtCore.Qt.Key_Shift and keyspressed[1] == QtCore.Qt.Key_Right:
                self.keyPressSig.emit('shiftRight')
                return
            if keyspressed[0] == QtCore.Qt.Key_Shift and keyspressed[1] == QtCore.Qt.Key_Up:
                self.keyPressSig.emit('shiftUp')
                return
            if keyspressed[0] == QtCore.Qt.Key_Shift and keyspressed[1] == QtCore.Qt.Key_Down:
                self.keyPressSig.emit('shiftDown')
                return
            if keyspressed[0] == QtCore.Qt.Key_Control and keyspressed[1] == QtCore.Qt.Key_C:
                self.keyPressSig.emit('Copy')
                return
            if keyspressed[0] == QtCore.Qt.Key_Control and keyspressed[1] == QtCore.Qt.Key_V:
                self.keyPressSig.emit('Paste')
                return
        if len(keyspressed) >=3:
            self.keylist = []
            return
