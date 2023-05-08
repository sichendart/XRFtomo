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

class differenceView(pyqtgraph.GraphicsLayoutWidget):
    keyPressSig = pyqtSignal(str, name= 'keyPressSig')

    def __init__(self):
    # def __init__(self, parent):
        super(differenceView, self).__init__()
        self.keylist = []
        self.initUI()

    def initUI(self):
        custom_vb = xrftomo.CustomViewBox()
        self.p1 = self.addPlot(viewBox = custom_vb, enableMouse = False)
        self.projView = pyqtgraph.ImageItem()
        self.projView.rotate(-90)
        self.p1.addItem(self.projView)
        self.p1.vb = custom_vb

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
            if keyspressed[0] == QtCore.Qt.Key_A:
                self.keyPressSig.emit('A')
            if keyspressed[0] == QtCore.Qt.Key_D:
                self.keyPressSig.emit('D')
        if len(keyspressed) >=2:
            self.keylist = []
            return
