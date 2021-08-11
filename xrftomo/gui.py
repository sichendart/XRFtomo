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


from PyQt5 import QtGui, QtWidgets, QtCore
# from matplotlib.figure import Figure
import xrftomo
import xrftomo.config as config
from scipy import stats
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import matplotlib
from os.path import expanduser
from skimage import measure
from matplotlib.pyplot import *
from scipy import ndimage as ndi
from skimage.morphology import remove_small_objects



STR_CONFIG_THETA_STRS = 'theta_pv_strs'

class xrftomoGui(QtGui.QMainWindow):
    def __init__(self, app, params):
        super(QtGui.QMainWindow, self).__init__()
        self.params = params
        self.param_list = {}
        self.app = app
        # self.get_values_from_params()
        self.initUI()

    def initUI(self):
        exitAction = QtGui.QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        exitAction.setShortcut('Ctrl+Q')

        closeAction = QtGui.QAction('Quit', self)
        closeAction.triggered.connect(sys.exit)
        closeAction.setShortcut('Ctrl+X')

        openH5Action = QtGui.QAction('open h5 file', self)
        openH5Action.triggered.connect(self.openH5)

        openExchangeAction = QtGui.QAction('open exchange file', self)
        openExchangeAction.triggered.connect(self.openExchange)

        openTiffAction = QtGui.QAction('open tiff files', self)
        openTiffAction.triggered.connect(self.openTiffs)

        openThetaAction = QtGui.QAction('open thetas file', self)
        openThetaAction.triggered.connect(self.openThetas)

        #openTiffFolderAction = QtGui.QAction("Open Tiff Folder", self)
        #openTiffFolderAction.triggered.connect(self.openTiffFolder)

        saveProjectionAction = QtGui.QAction('Projections', self)
        saveProjectionAction.triggered.connect(self.saveProjections)

        # saveHotSpotPosAction = QtGui.QAction('save hotspot positions',self)
        # saveHotSpotPosAction.triggered.connect(self.save_hotspot_positions)

        saveSinogramAction = QtGui.QAction('Sinogram', self)
        saveSinogramAction.triggered.connect(self.saveSinogram)

        saveSinogram2Action = QtGui.QAction('Sinogram stack', self)
        saveSinogram2Action.triggered.connect(self.saveSinogram2)

        saveReconstructionAction = QtGui.QAction('Reconstruction', self)
        saveReconstructionAction.triggered.connect(self.saveReconstruction)

        saveRecon2npyAction = QtGui.QAction("recon as npy", self)
        saveRecon2npyAction.triggered.connect(self.saveRecon2npy)

        saveReconArray2npyAction = QtGui.QAction("reconArr as npy", self)
        saveReconArray2npyAction.triggered.connect(self.saveReconArray2npy)

        saveToHDFAction = QtGui.QAction('as HDF file', self)
        saveToHDFAction.triggered.connect(self.saveToHDF)

        saveThetasAction = QtGui.QAction('Angle information to .txt', self)
        saveThetasAction.triggered.connect(self.saveThetas)

        saveToNumpyAction = QtGui.QAction("as Numpy file", self)
        saveToNumpyAction.triggered.connect(self.saveToNumpy)

        saveAlignemtInfoAction = QtGui.QAction("Alignment", self)
        saveAlignemtInfoAction.triggered.connect(self.saveAlignemnt)

        saveCorrAnalysisAction = QtGui.QAction("Corelation Analysis", self)
        saveCorrAnalysisAction.triggered.connect(self.saveCorrAlsys)



        runTransRecAction = QtGui.QAction("Transmission Recon", self)
        #runTransRecAction.triggered.connect(self.runTransReconstruct)

        # selectImageTagAction = QtGui.QAction("Select Image Tag", self)
        #selectImageTagAction.triggered.connect(self.selectImageTag)

        undoAction = QtGui.QAction('Undo (Ctrl+Z)', self)
        undoAction.triggered.connect(self.undo)
        undoAction.setShortcut('Ctrl+Z')

        preferencesAction = QtGui.QAction("exit preferences")

        setAspectratio = QtGui.QAction("lock aspect ratio",self)
        setAspectratio.setCheckable(True)
        setAspectratio.triggered.connect(self.toggle_aspect_ratio)

        restoreAction = QtGui.QAction("Restore", self)
        restoreAction.triggered.connect(self.restore)

        keyMapAction = QtGui.QAction('key map settings', self)
        keyMapAction.triggered.connect(self.keyMapSettings)

        configAction = QtGui.QAction('load configuration settings', self)
        configAction.triggered.connect(self.configSettings)


        self.forceLegacy = QtGui.QAction("force legacy mode", self)
        self.forceLegacy.setCheckable(True)


        # matcherAction = QtGui.QAction("match template", self)
        #matcherAction.triggered.connect(self.match_window)

        # saveHotSpotPosAction = QtGui.QAction("Save Hot Spot Pos", self)
        #saveHotSpotPosAction.triggered.connect(self.saveHotSpotPos)

        wienerAction = QtGui.QAction("Wiener", self)
        #wienerAction.triggered.connect(self.ipWiener)

        # externalImageRegAction = QtGui.QAction("External Image Registaration", self)
        #externalImageRegAction.triggered.connect(self.externalImageReg)

        ###
        self.frame = QtWidgets.QFrame()
        self.vl = QtWidgets.QVBoxLayout()

        # theta_auto_completes = seshowImgProcesslf.config.get(STR_CONFIG_THETA_STRS)
        # theta_auto_completes = self.params.theta_pv
        # if theta_auto_completes is None:
        #     theta_auto_completes = []
        self.fileTableWidget = xrftomo.FileTableWidget(self)
        self.imageProcessWidget = xrftomo.ImageProcessWidget()
        self.sinogramWidget = xrftomo.SinogramWidget()
        self.reconstructionWidget = xrftomo.ReconstructionWidget()
        self.scatterWidget = xrftomo.ScatterView()
        self.scatterWidgetRecon = xrftomo.ScatterView()
        self.miniReconWidget = xrftomo.MiniReconView()

        self.writer = xrftomo.SaveOptions()

        #refresh UI
        self.imageProcessWidget.refreshSig.connect(self.refreshUI)

        #sinogram changed
        self.sinogramWidget.sinoChangedSig.connect(self.update_sino)

        #slider change
        self.imageProcessWidget.sliderChangedSig.connect(self.imageProcessWidget.updateSliderSlot)

        #element dropdown change
        self.imageProcessWidget.elementChangedSig.connect(self.sinogramWidget.updateElementSlot)
        self.sinogramWidget.elementChangedSig.connect(self.reconstructionWidget.updateElementSlot)
        self.reconstructionWidget.elementChangedSig.connect(self.imageProcessWidget.updateElementSlot)

        # data update
        self.imageProcessWidget.dataChangedSig.connect(self.update_history)
        self.sinogramWidget.dataChangedSig.connect(self.update_history)

        # theta update
        self.imageProcessWidget.thetaChangedSig.connect(self.update_theta)
        self.imageProcessWidget.thetaChangedSig.connect(self.sinogramWidget.updateImgSldRange)

        #data dimensions changed
        self.imageProcessWidget.ySizeChangedSig.connect(self.sinogramWidget.ySizeChanged)
        self.imageProcessWidget.ySizeChangedSig.connect(self.reconstructionWidget.ySizeChanged)
        self.imageProcessWidget.xSizeChangedSig.connect(self.reconstructionWidget.xSizeChanged)
        self.imageProcessWidget.padSig.connect(self.update_padding)
        #alignment changed
        self.imageProcessWidget.alignmentChangedSig.connect(self.update_alignment)
        self.sinogramWidget.alignmentChangedSig.connect(self.update_alignment)
        self.sinogramWidget.restoreSig.connect(self.restore)

        #fnames changed 
        self.imageProcessWidget.fnamesChanged.connect(self.update_filenames)
        self.imageProcessWidget.fnamesChanged.connect(self.sinogramWidget.update_filenames)


        #update_reconstructed_data
        self.reconstructionWidget.reconChangedSig.connect(self.update_recon)
        self.reconstructionWidget.reconArrChangedSig.connect(self.update_recon_array)

        self.prevTab = 0
        self.TAB_FILE = 0
        self.TAB_IMAGE_PROC = 1
        self.TAB_SINOGRAM = 2
        self.TAB_RECONSTRUCTION = 3

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.fileTableWidget, 'Files')
        self.tab_widget.addTab(self.imageProcessWidget, "Pre Processing")
        self.tab_widget.addTab(self.sinogramWidget, "Alignment")
        self.tab_widget.addTab(self.reconstructionWidget, "Reconstruction")
        self.tab_widget.setTabEnabled(1,False)
        self.tab_widget.setTabEnabled(2,False)
        self.tab_widget.setTabEnabled(3,False)

        self.tab_widget.currentChanged.connect(self.onTabChanged)
        self.fileTableWidget.saveDataBtn.clicked.connect(self.updateImages)

        self.vl.addWidget(self.tab_widget)
        #self.vl.addWidget(self.createMessageWidget())

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        ## Top menu bar [file   Convert Option    Alignment   After saving in memory]
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        self.fileMenu = menubar.addMenu('&File')
        self.fileMenu.addAction(openH5Action)
        self.fileMenu.addAction(openExchangeAction)
        self.fileMenu.addAction(openTiffAction)
        self.fileMenu.addAction(openThetaAction)
        ##self.fileMenu.addAction(openFileAction)
        #self.fileMenu.addAction(openFolderAction)
        #self.fileMenu.addAction(openTiffFolderAction)
        self.fileMenu.addAction(exitAction)
        self.fileMenu.addAction(closeAction)

        self.editMenu = menubar.addMenu("Edit")
        self.editMenu.addAction(undoAction)
        self.editMenu.addAction(preferencesAction)
        # self.editMenu.addAction(matcherAction)
        # self.editMenu.addAction(saveHotSpotPosAction)
        # self.editMenu.addAction(alignHotSpotPosAction)
        # self.editMenu.addAction(externalImageRegAction)
        self.editMenu.addAction(restoreAction)
        self.editMenu.setDisabled(True)

        analysis = QtGui.QMenu('Analysis', self)
        corrElemAction = QtGui.QAction('Correlate Elements', self)
        analysis.addAction(corrElemAction)
        corrElemAction.triggered.connect(self.corrElem)

        scatterPlotAction = QtGui.QAction('Scatter Plot', self)
        analysis.addAction(scatterPlotAction)
        scatterPlotAction.triggered.connect(self.scatterPlot)

        scatterPlotReconAction = QtGui.QAction('Scatter Plot Recon', self)
        analysis.addAction(scatterPlotReconAction)
        scatterPlotReconAction.triggered.connect(self.scatterPlotRecon)

        projWinAction = QtGui.QAction('reprojection', self)
        analysis.addAction(projWinAction)
        projWinAction.triggered.connect(self.projWindow)

        pixelDistanceAction = QtGui.QAction('spatial analysis', self)
        analysis.addAction(pixelDistanceAction)
        pixelDistanceAction.triggered.connect(self.pixDistanceWindow)

        layerDensityAction = QtGui.QAction('onion analysis', self)
        analysis.addAction(layerDensityAction)
        layerDensityAction.triggered.connect(self.onionWindow)

        subPixShift = QtGui.QMenu("Sub pixel shift", self)
        ag = QtGui.QActionGroup(subPixShift)
        ag.setExclusive(True)
        self.subPix_1 = ag.addAction(QtGui.QAction('1', subPixShift, checkable=True))
        subPixShift.addAction(self.subPix_1)
        self.subPix_1.setChecked(True)
        self.subPix_1.triggered.connect(self.subPixShiftChanged)

        self.subPix_05 = ag.addAction(QtGui.QAction('2', subPixShift, checkable=True))
        subPixShift.addAction(self.subPix_05)
        self.subPix_05.triggered.connect(self.subPixShiftChanged)

        self.subPix_025 = ag.addAction(QtGui.QAction('5', subPixShift, checkable=True))
        subPixShift.addAction(self.subPix_025)
        self.subPix_025.triggered.connect(self.subPixShiftChanged)

        self.subPix_01 = ag.addAction(QtGui.QAction('10', subPixShift, checkable=True))
        subPixShift.addAction(self.subPix_01)
        self.subPix_01.triggered.connect(self.subPixShiftChanged)

        #
        # viewStatAct = QAction('View statusbar', self, checkable=True)
        # viewStatAct.setStatusTip('View statusbar')
        # viewStatAct.setChecked(True)
        # viewStatAct.triggered.connect(self.toggle_sps)

        self.toolsMenu = menubar.addMenu("Tools")
        self.toolsMenu.addMenu(analysis)
        self.toolsMenu.addMenu(subPixShift)
        self.toolsMenu.setDisabled(True)

        self.settingsMenu = menubar.addMenu("Settings")
        self.settingsMenu.addAction(self.forceLegacy)

        self.viewMenu = menubar.addMenu("View")
        self.viewMenu.addAction(setAspectratio)
        self.viewMenu.setDisabled(True)

        self.afterConversionMenu = menubar.addMenu('Save')
        self.afterConversionMenu.addAction(saveProjectionAction)
        # self.afterConversionMenu.addAction(saveHotSpotPosAction)
        self.afterConversionMenu.addAction(saveReconstructionAction)
        self.afterConversionMenu.addAction(saveRecon2npyAction)
        self.afterConversionMenu.addAction(saveReconArray2npyAction)
        self.afterConversionMenu.addAction(saveAlignemtInfoAction)
        self.afterConversionMenu.addAction(saveSinogramAction)
        self.afterConversionMenu.addAction(saveSinogram2Action)
        self.afterConversionMenu.addAction(saveThetasAction)
        self.afterConversionMenu.addAction(saveToHDFAction)
        self.afterConversionMenu.addAction(saveToNumpyAction)
        self.afterConversionMenu.addAction(saveCorrAnalysisAction)

        self.helpMenu = menubar.addMenu('&Help')
        self.helpMenu.addAction(keyMapAction)
        self.helpMenu.addAction(configAction)

        self.afterConversionMenu.setDisabled(True)
        version = "1.0.7"
        add = 0
        if sys.platform == "win32":
            add = 50
        self.setGeometry(add, add, 1100 + add, 500 + add)
        self.setWindowTitle('XRFtomo v{}'.format(version))
        self.show()

        #_______________________Help/config_options______________________
        self.config_options = QtWidgets.QWidget()
        self.config_options.resize(300,400)
        self.config_options.setWindowTitle('config options')
        self.legacy_chbx = QtWidgets.QCheckBox("Load as legacy data")
        self.directory_chbx = QtWidgets.QCheckBox("Load last directory")
        self.element_chbx = QtWidgets.QCheckBox("Load last elements")
        self.image_tag_chbx = QtWidgets.QCheckBox("Load last image_tag")
        self.data_tag_chbx= QtWidgets.QCheckBox("Load last data_tag")
        self.alingmen_chbx = QtWidgets.QCheckBox("Load alignment information")
        self.iter_align_param_chbx = QtWidgets.QCheckBox("Load last iter-align parameters")
        self.recon_method_chbx = QtWidgets.QCheckBox("Load last-used reconstruction method")

        self.checkbox_states = eval(self.params.load_settings)
        self.legacy_chbx.setChecked(self.checkbox_states[0])
        self.directory_chbx.setChecked(self.checkbox_states[1])
        self.element_chbx.setChecked(self.checkbox_states[2])
        self.image_tag_chbx.setChecked(self.checkbox_states[3])
        self.data_tag_chbx.setChecked(self.checkbox_states[4])

        self.alingmen_chbx.setChecked(self.checkbox_states[5])
        self.iter_align_param_chbx.setChecked(self.checkbox_states[6])
        self.recon_method_chbx.setChecked(self.checkbox_states[7])

        self.toggleDebugMode()

        self.legacy_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.legacy_chbx.stateChanged.connect(self.refresh_filetable)
        self.directory_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.element_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.image_tag_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.data_tag_chbx.stateChanged.connect(self.loadSettingsChanged)

        self.alingmen_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.iter_align_param_chbx.stateChanged.connect(self.loadSettingsChanged)
        self.recon_method_chbx.stateChanged.connect(self.loadSettingsChanged)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.legacy_chbx)
        vbox.addWidget(self.directory_chbx)
        vbox.addWidget(self.element_chbx)
        vbox.addWidget(self.image_tag_chbx)
        vbox.addWidget(self.data_tag_chbx)
        vbox.addWidget(self.alingmen_chbx)
        vbox.addWidget(self.iter_align_param_chbx)
        vbox.addWidget(self.recon_method_chbx)

        self.config_options.setLayout(vbox)



        #_______________________Help/keymap_options______________________
        self.keymap_options = QtWidgets.QWidget()
        self.keymap_options.resize(600,400)
        self.keymap_options.setWindowTitle('key map')
        text = QtWidgets.QLabel("Undo: \t\t Ctr+Z \t\t previous image: \t A \n\n" 
                    "shift image up: \t up \t\t next image: \t D \n\n" 
                    "shift image down: \t down  \t\t skip (hotspot): \t S \n\n"
                    "shift image left: \t left \t\t next (hotspot): \t N \n\n"
                    "shift image right: \t right  \n\n"
                    "shift stack up: \t Shift + up \n\n"
                    "shift stack down: \t Shift + down \n\n"
                    "shift stack left: \t Shift + left \n\n"
                    "shift stack right: \t Shift + right \n\n"
                    "exclude image: \t Delete \n\n"
                    "copy background: \t Ctrl + C \n\npaste background:  Ctrl + V"
                    )

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(text)
        self.keymap_options.setLayout(vbox)


        #_______________________ scatter plot window ______________________ win 1
        self.scatter_window = QtWidgets.QWidget()
        self.scatter_window.resize(1000,500)
        self.scatter_window.setWindowTitle('scatter')

        self.elem1_options = QtWidgets.QComboBox()
        self.elem1_options.setFixedWidth(100)
        self.elem2_options = QtWidgets.QComboBox()
        self.elem2_options.setFixedWidth(100)

        self.projection_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.projection_lcd = QtWidgets.QLCDNumber(self)
        projection_lbl = QtWidgets.QLabel("Projection index")
        # self.width_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        # self.width_lcd = QtWidgets.QLCDNumber(self)
        width_lbl = QtWidgets.QLabel("curve width")
        slope_lbl = QtWidgets.QLabel("Slope: ")
        self.slope_value = QtWidgets.QLineEdit("")



        self.apply_globally = QtWidgets.QPushButton("set red region to zero")

        ##_____ left blok: scatter view _____
        hboxA1 = QtWidgets.QHBoxLayout()
        hboxA1.addWidget(self.elem1_options)
        hboxA1.addWidget(self.elem2_options)
        hboxA1.addWidget(self.apply_globally)

        hboxA2 = QtWidgets.QHBoxLayout()
        hboxA2.addWidget(projection_lbl)
        hboxA2.addWidget(self.projection_lcd)
        hboxA2.addWidget(self.projection_sld)

        # hboxA3 = QtWidgets.QHBoxLayout()
        # hboxA3.addWidget(width_lbl)
        # hboxA3.addWidget(self.width_lcd)
        # hboxA3.addWidget(self.width_sld)

        hboxA4 = QtWidgets.QHBoxLayout()
        hboxA4.addWidget(slope_lbl)
        hboxA4.addWidget(self.slope_value)

        vboxA1 = QtWidgets.QVBoxLayout()
        vboxA1.addWidget(self.scatterWidget)
        vboxA1.addLayout(hboxA1)
        vboxA1.addLayout(hboxA2)
        # vboxA1.addLayout(hboxA3)
        vboxA1.addLayout(hboxA4)

        ##_____ right block: recon_view _____
        self.recon_views = QtWidgets.QComboBox()
        views = ["recon #1", "recon #2", "difference:#2 - #1"]
        for k in range(len(views)):
            self.recon_views.addItem(views[k])

        self.recon_method = QtWidgets.QComboBox()
        methodname = ["mlem", "gridrec", "art", "pml_hybrid", "pml_quad", "fbp", "sirt", "tv"]
        for k in range(len(methodname)):
            self.recon_method.addItem(methodname[k])

        self.recon_button = QtWidgets.QPushButton("reconstruct")
        self.recon_button.clicked.connect(self.updateMiniRecon)

        spacer = QtWidgets.QLabel("")

        hboxB1 = QtWidgets.QHBoxLayout()
        hboxB1.addWidget(self.recon_views)
        hboxB1.addWidget(self.recon_method)
        hboxB1.addWidget(self.recon_button)

        vboxB1 = QtWidgets.QVBoxLayout()
        vboxB1.addWidget(self.miniReconWidget)
        vboxB1.addLayout(hboxB1)
        vboxB1.addWidget(spacer)
        vboxB1.addWidget(spacer)
        vboxB1.addWidget(spacer)


        hboxC1 = QtWidgets.QHBoxLayout()
        hboxC1.addLayout(vboxA1)
        hboxC1.addLayout(vboxB1)

        self.scatter_window.setLayout(hboxC1)

        self.elem1_options.currentIndexChanged.connect(self.updateScatter)
        self.elem2_options.currentIndexChanged.connect(self.updateScatter)
        self.projection_sld.valueChanged.connect(self.updateScatter)
        # self.width_sld.valueChanged.connect(self.updateWidth)
        # self.width_sld.valueChanged.connect(self.updateInnerScatter)
        self.scatterWidget.mousePressSig.connect(self.updateInnerScatter)
        self.scatterWidget.roiDraggedSig.connect(self.updateInnerScatter)
        self.apply_globally.clicked.connect(self.sendData)
        self.slope_value.returnPressed.connect(self.slopeEntered)
        self.first_run = True


        #_______________________ scatter plot window Recon ______________________ win 2
        self.scatter_window_recon = QtWidgets.QWidget()
        self.scatter_window_recon.resize(1000,500)
        self.scatter_window_recon.setWindowTitle('scatter')

        self.elem1_options_recon = QtWidgets.QComboBox()
        self.elem1_options_recon.setFixedWidth(100)
        self.elem2_options_recon = QtWidgets.QComboBox()
        self.elem2_options_recon.setFixedWidth(100)

        self.recon_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.recon_lcd = QtWidgets.QLCDNumber(self)
        recon_lbl = QtWidgets.QLabel("Projection index")
        # self.width_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        # self.width_lcd = QtWidgets.QLCDNumber(self)
        width_lbl_recon = QtWidgets.QLabel("curve width")
        slope_lbl_recon = QtWidgets.QLabel("Slope: ")
        self.slope_value_recon = QtWidgets.QLineEdit("")



        self.apply_globally_recon = QtWidgets.QPushButton("set red region to zero")

        ##_____ left blok: scatter view _____
        hboxA1_recon = QtWidgets.QHBoxLayout()
        hboxA1_recon.addWidget(self.elem1_options_recon)
        hboxA1_recon.addWidget(self.elem2_options_recon)
        hboxA1_recon.addWidget(self.apply_globally_recon)

        hboxA2_recon = QtWidgets.QHBoxLayout()
        hboxA2_recon.addWidget(recon_lbl)
        hboxA2_recon.addWidget(self.recon_lcd)
        hboxA2_recon.addWidget(self.recon_sld)

        # hboxA3 = QtWidgets.QHBoxLayout()
        # hboxA3.addWidget(width_lbl)
        # hboxA3.addWidget(self.width_lcd)
        # hboxA3.addWidget(self.width_sld)

        hboxA4_recon = QtWidgets.QHBoxLayout()
        hboxA4_recon.addWidget(slope_lbl_recon)
        hboxA4_recon.addWidget(self.slope_value_recon)

        vboxA1_recon = QtWidgets.QVBoxLayout()
        vboxA1_recon.addWidget(self.scatterWidgetRecon)
        vboxA1_recon.addLayout(hboxA1_recon)
        vboxA1_recon.addLayout(hboxA2_recon)
        # vboxA1.addLayout(hboxA3)
        vboxA1_recon.addLayout(hboxA4_recon)



        hboxC1_recon = QtWidgets.QHBoxLayout()
        hboxC1_recon.addLayout(vboxA1_recon)

        self.scatter_window_recon.setLayout(hboxC1_recon)

        self.elem1_options_recon.currentIndexChanged.connect(self.updateScatterRecon)
        self.elem2_options_recon.currentIndexChanged.connect(self.updateScatterRecon)
        self.recon_sld.valueChanged.connect(self.updateScatterRecon)
        # self.width_sld.valueChanged.connect(self.updateWidth)
        # self.width_sld.valueChanged.connect(self.updateInnerScatter)
        self.scatterWidgetRecon.mousePressSig.connect(self.updateInnerScatterRecon)
        self.scatterWidgetRecon.roiDraggedSig.connect(self.updateInnerScatterRecon)
        self.apply_globally_recon.clicked.connect(self.sendRecon)
        self.slope_value_recon.returnPressed.connect(self.slopeEnteredRecon)
        self.first_run_recon = True




        #_______________________ projecion compare window ______________________ win 3
        self.projection_window = QtWidgets.QWidget()
        self.projection_window.resize(1000,500)
        self.projection_window.setWindowTitle('reprojection tools')

        self.miniProjectionWidget1 = xrftomo.MiniReconView()
        self.miniProjectionWidget2 = xrftomo.MiniReconView()

        self.elem_options = QtWidgets.QComboBox()
        self.elem_options.setFixedWidth(100)
        spacer = QtWidgets.QLabel("")

        ##_____ left blok: scatter view _____
        hboxA1 = QtWidgets.QHBoxLayout()
        hboxA1.addWidget(self.elem_options)

        vboxA1 = QtWidgets.QVBoxLayout()
        vboxA1.addWidget(self.miniProjectionWidget1)
        vboxA1.addLayout(hboxA1)
        vboxA1.addWidget(spacer)
        

        ##_____ right block: recon_view _____
        self.compare_metric = QtWidgets.QComboBox()
        metric = ["MSE", "SSM", "pearson", "adaptive"]
        for k in range(len(metric)):
            self.compare_metric.addItem(metric[k])

        self.compare_button = QtWidgets.QPushButton("compare")
        self.compare_button.clicked.connect(self.updateMiniReproj)

        self.compare_results = QtWidgets.QLabel("-1")

        sf_lbl = QtWidgets.QLabel("scale factor")
        self.sf_txt = QtWidgets.QLabel("-1")
        # [recon#][method][recon]
        # [start_lbl][start_txt]
        # [end_lbl][end_txt]
        # [compare_metric][compare result lbl]

        spacer = QtWidgets.QLabel("")

        hboxB4 = QtWidgets.QHBoxLayout()
        hboxB4.addWidget(self.compare_metric)
        hboxB4.addWidget(self.compare_results)
        hboxB4.addWidget(self.compare_button)

        hboxB5 = QtWidgets.QHBoxLayout()
        hboxB5.addWidget(sf_lbl)
        hboxB5.addWidget(self.sf_txt)

        vboxB1 = QtWidgets.QVBoxLayout()
        vboxB1.addWidget(self.miniProjectionWidget2)
        vboxB1.addLayout(hboxB4)
        vboxB1.addLayout(hboxB5)

        hboxC1 = QtWidgets.QHBoxLayout()
        hboxC1.addLayout(vboxA1)
        hboxC1.addLayout(vboxB1)

        self.projection_window.setLayout(hboxC1)

        self.elem_options.currentIndexChanged.connect(self.updateMiniProj)
        self.first_run_a = True








  #_______________________ pixel distance window ______________________ win4
        self.pixel_distance_window = QtWidgets.QWidget()
        self.pixel_distance_window.resize(1000,500)
        self.pixel_distance_window.setWindowTitle('spatial analysis')

        self.miniReconWidget_w4 = xrftomo.MiniReconView()
        self.miniHisto_w4 = xrftomo.MiniReconView()

        self.recon_sld_w4 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)

        recons_list_lbl = QtWidgets.QLabel("recons list")
        self.recons_list_w4 = QtWidgets.QComboBox()
        self.recons_list_w4.setFixedWidth(100)

        numbins_lbl_w4 = QtWidgets.QLabel("number of bins")
        self.numbins_box_w4 = QtWidgets.QLineEdit("100")

        stack_range1_lbl_w4 = QtWidgets.QLabel("lower slice index")
        stack_range2_lbl_w4 = QtWidgets.QLabel("upper slice index")
        self.stack_range1_w4 = QtWidgets.QLineEdit("0")
        self.stack_range2_w4 = QtWidgets.QLineEdit("1")


        ##_____ left blok: recon view _____
        hboxA_w4 = QtWidgets.QHBoxLayout()
        hboxA_w4.addWidget(recons_list_lbl)
        hboxA_w4.addWidget(self.recons_list_w4)

        hboxB_w4 = QtWidgets.QHBoxLayout()
        hboxB_w4.addWidget(numbins_lbl_w4)
        hboxB_w4.addWidget(self.numbins_box_w4)

        hboxC_w4 = QtWidgets.QHBoxLayout()
        hboxC_w4.addWidget(stack_range1_lbl_w4)
        hboxC_w4.addWidget(self.stack_range1_w4)

        hboxD_w4 = QtWidgets.QHBoxLayout()
        hboxD_w4.addWidget(stack_range2_lbl_w4)
        hboxD_w4.addWidget(self.stack_range2_w4) 

        hboxA1 = QtWidgets.QHBoxLayout()
        hboxA1.addWidget(recons_list_lbl)
        hboxA1.addWidget(self.recons_list_w4)


        vboxA1 = QtWidgets.QVBoxLayout()
        vboxA1.addWidget(self.miniReconWidget_w4)
        vboxA1.addLayout(hboxA1)
        vboxA1.addWidget(spacer)
        

        ##_____ right block: pixel distance analysis _____
        vboxB1 = QtWidgets.QVBoxLayout()
        vboxB1.addWidget(self.miniHisto_w4)

        hboxC1 = QtWidgets.QHBoxLayout()
        hboxC1.addLayout(hboxA_w4)
        hboxC1.addLayout(vboxB1)

        self.pixel_distance_window.setLayout(hboxC1)

        self.recons_list_w4.currentIndexChanged.connect(self.updateDistanceHisto)
        # self.recon_sld_w4.valueChanged.connect(self.updateDistanceHisto)
        self.first_run_w4 = True

  #_______________________ onion window ______________________ win5

        self.onion_window = QtWidgets.QWidget()
        self.onion_window.resize(1000,500)
        self.onion_window.setWindowTitle('onion analysis')

        self.miniReconWidget_w5 = xrftomo.MiniReconView()
        self.miniHisto_w5 = xrftomo.MiniReconView()

        elem1_list_lbl = QtWidgets.QLabel("recons list")
        self.elem1_list_w5 = QtWidgets.QComboBox()
        self.elem1_list_w5.setFixedWidth(100)

        elem2_list_lbl = QtWidgets.QLabel("recons list")
        self.elem2_list_w5 = QtWidgets.QComboBox()
        self.elem2_list_w5.setFixedWidth(100)

        self.recon_sld_w5 = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.recon_lcd_w5 = QtWidgets.QLCDNumber(self)
        recon_lbl_w5 = QtWidgets.QLabel("recon index")

        layer_depth_lbl_w5 = QtWidgets.QLabel("layer depth (micron)")
        elem1_thresh_lbl_w5 = QtWidgets.QLabel("element1 threshold 0-1")
        self.layer_depth_w5 = QtWidgets.QLineEdit("50")
        self.elem1_thresh_w5 = QtWidgets.QLineEdit("0.25")

        self.create_onion_button = QtWidgets.QPushButton("create onion")
        self.create_onion_button.clicked.connect(self.createOnion)

        self.run_layer_analysis = QtWidgets.QPushButton("run analysis")
        self.run_layer_analysis.clicked.connect(self.updateOnionHisto)

        ##_____ left blok: recon view _____
        hboxA_w5 = QtWidgets.QHBoxLayout()
        hboxA_w5.addWidget(elem1_list_lbl)
        hboxA_w5.addWidget(self.elem1_list_w5)
        hboxA_w5.addWidget(self.create_onion_button)

        hboxB_w5 = QtWidgets.QHBoxLayout()
        hboxB_w5.addWidget(layer_depth_lbl_w5)
        hboxB_w5.addWidget(self.layer_depth_w5)

        hboxC_w5 = QtWidgets.QHBoxLayout()
        hboxC_w5.addWidget(elem1_thresh_lbl_w5)
        hboxC_w5.addWidget(self.elem1_thresh_w5)

        hboxD_w5 = QtWidgets.QHBoxLayout()
        hboxD_w5.addWidget(recon_lbl_w5)
        hboxD_w5.addWidget(self.recon_lcd_w5)
        hboxD_w5.addWidget(self.recon_sld_w5)

        vboxA1 = QtWidgets.QVBoxLayout()
        vboxA1.addWidget(self.miniReconWidget_w5)
        vboxA1.addLayout(hboxA_w5)
        vboxA1.addLayout(hboxD_w5)
        vboxA1.addLayout(hboxB_w5)
        vboxA1.addLayout(hboxC_w5)

        ##_____ right block: pixel distance analysis _____
        hboxE_w5 = QtWidgets.QHBoxLayout()
        hboxE_w5.addWidget(elem2_list_lbl)
        hboxE_w5.addWidget(self.elem2_list_w5)
        hboxE_w5.addWidget(self.run_layer_analysis)

        vboxB1 = QtWidgets.QVBoxLayout()
        vboxB1.addWidget(self.miniHisto_w5)
        vboxB1.addLayout(hboxE_w5)

        hboxC1 = QtWidgets.QHBoxLayout()
        hboxC1.addLayout(vboxA1)
        hboxC1.addLayout(vboxB1)

        self.onion_window.setLayout(hboxC1)

        self.first_run_w5 = True
        self.onion_layers = None





    def updateOnion(self):
        if self.first_run_w5:
            e1 = 0
            self.first_run_w5 = False

        else:
            e1 = self.elem1_list_w5.currentIndex()

        self.elem1_list_w5.clear()
        self.elem2_list_w5.clear()
        try:
            self.recon_sld_w5.setRange(0, len(self.recon_array[0])-1)
        except TypeError:
            print("run reconstruction first")
            return


        for i in self.elements:
            self.elem1_list_w5.addItem(i)
            self.elem2_list_w5.addItem(i)
        try:
            self.elem1_list_w5.setCurrentIndex(e1)
            self.elem2_list_w5.setCurrentIndex(e1)
            self.elem1_list_w5.setCurrentText(self.elements[e1])
            self.elem2_list_w5.setCurrentText(self.elements[e1])
        except:
            self.elem1_list_w5.setCurrentIndex(0)
            self.elem2_list_w5.setCurrentIndex(0)

        recon_indx_w5 = self.recon_sld_w5.value()
        self.recon_lcd_w5.display(recon_indx_w5)
        return

    def updateOnionHisto(self):

        if self.onion_layers.any() == None:
            print('create onion first')
            return

        num_layers = self.onion_layers.max()
        total_signal = np.zeros(num_layers)
        img = self.recon_array[self.elem2_list_w5.currentIndex(), self.recon_sld_w5.value()]

        for i in range(num_layers):
            depth_mask = self.onion_layers == (i+1)
            total_signal[i] = np.sum(img*depth_mask)


        #generate histogram
        # Creating histogram 
        # fig, axs = plt.subplots(1, 1, figsize =(10, 7), tight_layout = True)
        # #calculate number of bins based on max value
        x = (np.arange(num_layers)+1)*eval(self.layer_depth_w5.text())
        # axs.bar(x, total_signal,width=10)
        # axs.set_title("Desnity as a function of depth")
        # axs.set_xlabel("distance (micron)")
        # axs.set_ylabel("total signal ug/cm^3")
        #    Show plot
        # fig.show()
        self.miniHisto_w5.barView.setOpts(x=x,height=total_signal, width=9)

        return

    def createOnion(self):

        layer_depth = eval(self.layer_depth_w5.text())
        threshold = eval(self.elem1_thresh_w5.text())
        img = self.recon_array[self.elem1_list_w5.currentIndex(), self.recon_sld_w5.value()]
        self.onion_slice, self.onion_layers = self.peel_onion(img,threshold,layer_depth)

        self.miniReconWidget_w5.reconView.setImage(self.onion_slice)

        pass

    def peel_onion(self, data, data_thresh, layer_depth):
        reached_core = False
        #establish surface aka first layer
        layer_0 = self.create_mask(data, data_thresh)      #bool array xy
        msk = np.ones_like(layer_0)*layer_0*1     #uint8 array xy
        msks = msk.copy()
        i = 0
        #peel away layers find out how many layers there are first
        while not reached_core:
            print("current layer: {}".format(i))
            i+=1
            try:
                msk = ndi.binary_erosion(msk, structure=np.ones((layer_depth*2, layer_depth*2)))
                msks = msk+msks
                if msk.max()==0:
                    reached_core = True

            except: 
                reached_core = True
        mask_incremental = msks.copy()
        msks = msks*255//i
        superimposed = (msks + data/np.max(data)*layer_0*255*0.6)
        superimposed_img = superimposed//(superimposed.max()/255)
        
        return superimposed_img, mask_incremental, 


    def create_mask(self, data, mask_thresh=None, scale=.8):
        # Remove nan values
        mask_nan = np.isfinite(data)
        data[~np.isfinite(data)] = 0
        #     data /= data.max()
        # Median filter with disk structuring element to preserve cell edges.
        data = ndi.median_filter(data, size=int(data.size ** .5 * .05), mode='nearest')
        #     data = rank.median(data, disk(int(size**.5*.05)))
        # Threshold
        if mask_thresh == None:
            mask_thresh = np.nanmean(data) * scale / np.nanmax(data)
        mask = np.isfinite(data)
        mask[data / np.nanmax(data) < mask_thresh] = False
        # Remove small spots
        mask = remove_small_objects(mask, data.size // 100)
        # Remove small holes
        mask = ndi.binary_fill_holes(mask)
        return mask * mask_nan






    def updateMiniReproj(self):

        e1 = self.elem_options.currentIndex()

        data = self.data
        element= e1

        try:
            recon = self.recon
        except:
            return 0,0
        self.reprojection = self.reproject(recon)
        dummy, sf = self.compare_projections(self.compare_metric.currentIndex(), self.proj, self.reprojection)
        
        self.reprojection /= sf
        results, dummy = self.compare_projections(self.compare_metric.currentIndex(), self.proj, self.reprojection)

        self.compare_results.setText(str(results))
        self.sf_txt.setText(str(sf))

        self.miniProjectionWidget2.reconView.setImage(self.reprojection)
        return


    def reproject(self, recon):
        try:
            num_slices = recon.shape[0]
        except:
            return

        width = recon.shape[1]
        reprojection = np.zeros([num_slices, width])
        tmp = np.zeros([num_slices, width])

        for i in range(num_slices):
            reprojection[i] = np.sum(recon[i], axis=0)

        return reprojection

    def compare_projections(self, metric, projA, projB):
        d = len(projA)
        if d < 2:
            return 0, 0

        if metric == 0: #MSE
            err = projA - projB
            #mean squared error
            result = (np.square(err)).mean(axis=None)
            sf = np.sum(projB)/np.sum(projA)

        elif metric == 1: #SSM
            errMat = np.zeros(projA.shape[0])
            simMat = np.zeros(projA.shape[0])

            for i in range(projA.shape[0]):
                err = np.sum((projA[i].astype("float") - projB[i].astype("float")) ** 2)
                err /= float(projA[i].shape[0] * projA[i].shape[1])
                sim = measure.compare_ssim(projA[i], projB[i])

                errMat[i] = err
                simMat[i] = sim
                errVal = np.sum(errMat)/len(errMat)
                simVal = np.sum(simMat)/len(simMat)
            result = simVal
            sf = np.sum(projB)/np.sum(projA)


        elif metric == 2: #pearson
            result, p = stats.pearsonr(projA.flatten(), projB.flatten())

            sf = np.sum(projB)/np.sum(projA)


        elif metric == 3:
            scaler_arr = np.zeros(projA.shape[0])
            for i in range(projA.shape[0]):

                if projA[i].max() == 0:
                    projA[i] = np.zeros(projA.shape[1])
                else:
                    scaler_arr[i] = projB[i].max()/projA[i].max()
            new_reprojection = np.asarray([projB[i]*scaler_arr[i] for i in range(len(scaler_arr))])
            sf = np.mean(scaler_arr[scaler_arr> scaler_arr.max()*.5])
            #mean squared error
            result = (np.square(projA - new_reprojection)).mean(axis=None)

        else:
            result = -1
            sf = -1

        return result, sf
        


    def updateMiniProj(self):
        thetas = self.thetas
        if self.first_run_a:
            e1 = 0
            self.first_run_a = False

        else:
            e1 = self.elem_options.currentIndex()

        self.elem_options.currentIndexChanged.disconnect(self.updateMiniProj)
        self.elem_options.clear()

        for i in self.elements:
            self.elem_options.addItem(i)
        try:
            self.elem_options.setCurrentIndex(e1)
            self.elem_options.setCurrentText(self.elements[e1])
        except:
            self.elem_options.setCurrentIndex(0)

        #find where proj index angle ==0:
        zero_index = np.where(abs(thetas)==abs(thetas).min())[0][0]
        self.proj = self.data[e1,zero_index]

        self.elem_options.currentIndexChanged.connect(self.updateMiniProj)
        self.miniProjectionWidget1.reconView.setImage(self.proj)
        return

    def updateDistanceHisto(self):
        if self.first_run_w4:
            e1 = 0
            self.first_run_w4 = False

        else:
            e1 = self.recons_list_w4.currentIndex()

        self.recons_list_w4.currentIndexChanged.disconnect(self.updateDistanceHisto)
        self.recons_list_w4.clear()
        try:
            self.recon_sld_w4.setRange(0, len(self.recon_array[0])-1)
        except TypeError:
            print("run reconstruction first")
            return

        elem_indx_w4 = self.recons_list_w4.currentIndex()
        recon_indx_w4 = self.recon_sld_w4.value()

        for i in self.elements:
            self.recons_list_w4.addItem(i)
        try:
            self.recons_list_w4.setCurrentIndex(e1)
            self.recons_list_w4.setCurrentText(self.elements[e1])
        except:
            self.recons_list_w4.setCurrentIndex(0)

        self.recons_list_w4.currentIndexChanged.connect(self.updateDistanceHisto)

        ##calculate distance_array
        recon_element = self.recons_list_w4.currentIndex()
        recon_indx = self.recon_sld_w4.value()

        # distance_array = self.calculate_pixel_distance(self.recon_array[recon_element,recon_indx])
        distance_array = self.calculate_all_distances(self.recon_array[recon_element])
        
        #generate histogram
        # Creating histogram 
        fig, axs = plt.subplots(1, 1, figsize =(10, 7), tight_layout = True)
        #whole numbers
        distance_array = distance_array.round()
        #cutoff max distance
        # distance_array[distance_array < 100]
        #calculate number of bins based on max value
        num_bins = int(distance_array.max())

        axs.hist(distance_array, bins = num_bins,  density = True)
        axs.set_title(self.fileTableWidget.dirLineEdit.text())
        axs.set_xlabel("distance (micron)")
        #    Show plot
        plt.show()

        return

    def calculate_pixel_distance(self,img):

        point_arr = []


        #filter image so there arent so many points to calculate distances for,
        img[img<img.max()*0.05] = 0
        #then downsample the image to 50% or variable.

        #find non-zero pixels in image
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i,j]>0:
                    point_arr.append([i,j])

        #find pixel distances using permutations of points array
        point_arr = np.asanyarray(point_arr)
        num_points = len(point_arr)
        sub_points = list(np.arange(1, num_points))
        distance_arr = []
        for i in range(num_points-1):
            if len(sub_points)==0:
                break
            for j in sub_points:
                distance_arr.append(np.sqrt( (point_arr[i,0]-point_arr[j,0])**2 +
                                             (point_arr[i,1]-point_arr[j,1])**2  ))
            del sub_points[0]

        print(distance_arr)
        return distance_arr

    def calculate_all_distances(self,img_stack):
        #remove slices in stack where values all zero
        num_slices = img_stack.shape[0]
        non_zero_slices = []
        for i in range(num_slices):
            if img_stack[i].max()>0:
                non_zero_slices.append(i)

        slice_arr = [img_stack[i] for i in non_zero_slices]
        num_images = len(slice_arr)
        distance_arr = np.asarray(self.calculate_pixel_distance(slice_arr[0]))


        for i in range(1, num_images):
            distance_arr = np.append(distance_arr, np.asarray(self.calculate_pixel_distance(slice_arr[i])))

        return distance_arr

    def update_padding(self, x,y):
        self.sinogramWidget.x_padding_hist.append(x)
        self.sinogramWidget.y_padding_hist.append(y)


    def subPixShiftChanged(self):

        shift_size_arr = np.array([1,2,5,10])
        bool_arr = [self.subPix_1.isChecked(), self.subPix_05.isChecked(), self.subPix_025.isChecked(),self.subPix_01.isChecked()]
        shift_size = shift_size_arr[bool_arr.index(True)]
        print(str(shift_size))

        self.sinogramWidget.sub_pixel_shift = shift_size
        self.imageProcessWidget.sub_pixel_shift = shift_size

        return

    def updateScatter(self):
        if self.first_run:
            self.scatterWidget.ROI.endpoints[1].setPos(self.data[0,0].max(), self.data[0,0].max())
            e1 = 0
            e2 = 0

            self.first_run = False

        else:
            e1 = self.elem1_options.currentIndex()
            e2 = self.elem2_options.currentIndex()

        self.projection_sld.setRange(0, self.data.shape[1]-1)
        self.elem1_options.currentIndexChanged.disconnect(self.updateScatter)
        self.elem2_options.currentIndexChanged.disconnect(self.updateScatter)

        proj_indx = self.projection_sld.value()
        self.elem1_options.clear()
        self.elem2_options.clear()

        for i in self.elements:
            self.elem1_options.addItem(i)
            self.elem2_options.addItem(i)
        try:
            self.elem1_options.setCurrentIndex(e1)
            self.elem1_options.setCurrentText(self.elements[e1])
            self.elem2_options.setCurrentIndex(e2)
            self.elem2_options.setCurrentText(self.elements[e2])
            self.scatterWidget.p1.setLabel(axis='left', text=self.elements[e1])
            self.scatterWidget.p1.setLabel(axis='bottom', text=self.elements[e2])

        except:
            self.elem1_options.setCurrentIndex(0)
            self.elem2_options.setCurrentIndex(0)

        elem1 = self.data[e1,proj_indx]
        elem1 = elem1.flatten()
        elem2 = self.data[e2, proj_indx]
        elem2 = elem2.flatten()

        #update projection index LCD
        self.projection_lcd.display(self.projection_sld.value())

        self.elem1_options.currentIndexChanged.connect(self.updateScatter)
        self.elem2_options.currentIndexChanged.connect(self.updateScatter)
        # self.elem1_options.currentIndexChanged.connect(self.updateInnerScatter)
        # self.elem2_options.currentIndexChanged.connect(self.updateInnerScatter)

        self.scatterWidget.plotView.setData(elem2, elem1)
        self.scatterWidget.p1.setLabel(axis='left', text=self.elements[e1])
        self.scatterWidget.p1.setLabel(axis='bottom', text=self.elements[e2])
        self.updateInnerScatter()
        return




    # def updateWidth(self):

    #     # self.width_lcd.display(self.width_sld.value())
    #     width_values = np.linspace(0,1,101)
    #     self.width_sld.setRange(0, len(width_values)-1)
    #     self.width_lcd.display(width_values[self.width_sld.value()])
    #     return

    def updateInnerScatter(self,*dummy):
        self.scatterWidget.mousePressSig.disconnect(self.updateInnerScatter)
        self.scatterWidget.roiDraggedSig.disconnect(self.updateInnerScatter)
        e1 = self.elem1_options.currentIndex()
        e2 = self.elem2_options.currentIndex()

        #Normalizeself.projection_sld.currentIndex()
        elem1 = self.data[self.elem1_options.currentIndex(),self.projection_sld.value()]
        elem1 = elem1.flatten()
        elem2 = self.data[self.elem2_options.currentIndex(), self.projection_sld.value()]
        elem2 = elem2.flatten()

        # get slope then calculate new handle pos
        x_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().x()
        y_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().y()
        try:
            slope = y_pos/x_pos
        except ZeroDivisionError:
            slope = 1


        x_pos = 1/slope
        y_pos = x_pos*slope

        if elem2.max()*slope < elem1.max():
            x_pos = elem2.max()
            y_pos = x_pos*slope
        if elem2.max()*slope > elem1.max():
            x_pos = elem1.max()/slope
            y_pos = x_pos*slope

        self.scatterWidget.ROI.endpoints[1].setPos(x_pos,y_pos)
        self.slope_value.setText(str(round(slope,4)))

        tmp_arr = [(slope*elem2) <= elem1]
        tmp_elem1 = elem1[tmp_arr[0]]
        tmp_elem2 = elem2[tmp_arr[0]]
        self.scatterWidget.plotView2.setData(tmp_elem2, tmp_elem1, brush='r')

        self.scatterWidget.mousePressSig.connect(self.updateInnerScatter)
        self.scatterWidget.roiDraggedSig.connect(self.updateInnerScatter)

        return

    def slopeEntered(self):
        slope = eval(self.slope_value.text())
        if slope < 0 :
            return
        self.scatterWidget.mousePressSig.disconnect(self.updateInnerScatter)
        self.scatterWidget.roiDraggedSig.disconnect(self.updateInnerScatter)


        e1 = self.elem1_options.currentIndex()
        e2 = self.elem2_options.currentIndex()

        #Normalizeself.projection_sld.currentIndex()
        elem1 = self.data[self.elem1_options.currentIndex(),self.projection_sld.value()]
        elem1 = elem1.flatten()
        elem2 = self.data[self.elem2_options.currentIndex(), self.projection_sld.value()]
        elem2 = elem2.flatten()
        x_pos = 1/slope
        y_pos = x_pos*slope

        if elem2.max()*slope < elem1.max():
            x_pos = elem2.max()
            y_pos = x_pos*slope
        if elem2.max()*slope > elem1.max():
            x_pos = elem1.max()/slope
            y_pos = x_pos*slope

        self.scatterWidget.ROI.endpoints[1].setPos(x_pos,y_pos)
        self.slope_value.setText(str(round(slope,4)))

        tmp_arr = [(slope*elem2) <= elem1]
        tmp_elem1 = elem1[tmp_arr]
        tmp_elem2 = elem2[tmp_arr]
        self.scatterWidget.plotView2.setData(tmp_elem2, tmp_elem1, brush='r')

        self.scatterWidget.mousePressSig.connect(self.updateInnerScatter)
        self.scatterWidget.roiDraggedSig.connect(self.updateInnerScatter)


    def updateScatterRecon(self):
        if self.first_run_recon:
            try:
                self.scatterWidget.ROI.endpoints[1].setPos(self.recon[0,0].max(), self.recon[0,0].max())
                e1 = 0
                e2 = 0

                self.first_run_recon = False
            except TypeError:
                print("run reconstruction first")
                return
        else:
            e1 = self.elem1_options_recon.currentIndex()
            e2 = self.elem2_options_recon.currentIndex()

        self.recon_sld.setRange(0, self.recon_array.shape[1]-1)
        self.elem1_options_recon.currentIndexChanged.disconnect(self.updateScatterRecon)
        self.elem2_options_recon.currentIndexChanged.disconnect(self.updateScatterRecon)
        recon_indx = self.recon_sld.value()
        self.elem1_options_recon.clear()
        self.elem2_options_recon.clear()

        for i in self.elements:
            self.elem1_options_recon.addItem(i)
            self.elem2_options_recon.addItem(i)
        try:
            self.elem1_options_recon.setCurrentIndex(e1)
            self.elem1_options_recon.setCurrentText(self.elements[e1])
            self.elem2_options_recon.setCurrentIndex(e2)
            self.elem2_options_recon.setCurrentText(self.elements[e2])
            self.scatterWidgetRecon.p1.setLabel(axis='left', text=self.elements[e1])
            self.scatterWidgetRecon.p1.setLabel(axis='bottom', text=self.elements[e2])

        except:
            self.elem1_options_recon.setCurrentIndex(0)
            self.elem2_options_recon.setCurrentIndex(0)

        elem1 = self.recon_array[e1, recon_indx]
        elem1 = elem1.flatten()
        elem2 = self.recon_array[e2,recon_indx]
        elem2 = elem2.flatten()

        #update projection index LCD
        self.recon_lcd.display(self.recon_sld.value())

        self.elem1_options_recon.currentIndexChanged.connect(self.updateScatterRecon)
        self.elem2_options_recon.currentIndexChanged.connect(self.updateScatterRecon)
        # self.elem1_options.currentIndexChanged.connect(self.updateInnerScatter)
        # self.elem2_options.currentIndexChanged.connect(self.updateInnerScatter)

        self.scatterWidgetRecon.plotView.setData(elem2, elem1)
        self.scatterWidgetRecon.p1.setLabel(axis='left', text=self.elements[e1])
        self.scatterWidgetRecon.p1.setLabel(axis='bottom', text=self.elements[e2])
        self.updateInnerScatterRecon()
        return


    def updateInnerScatterRecon(self,*dummy):
        self.scatterWidgetRecon.mousePressSig.disconnect(self.updateInnerScatterRecon)
        self.scatterWidgetRecon.roiDraggedSig.disconnect(self.updateInnerScatterRecon)
        e1 = self.elem1_options_recon.currentIndex()
        e2 = self.elem2_options_recon.currentIndex()

        #Normalizeself.projection_sld.currentIndex()

        elem1 = self.reconstructionWidget.recon_array[e1,self.recon_sld.value()]
        elem1 = elem1.flatten()
        elem2 = self.reconstructionWidget.recon_array[e2, self.recon_sld.value()]
        elem2 = elem2.flatten()

        # get slope then calculate new handle pos
        x_pos = self.scatterWidgetRecon.p1.items[3].getHandles()[1].pos().x()
        y_pos = self.scatterWidgetRecon.p1.items[3].getHandles()[1].pos().y()
        try:
            slope = y_pos/x_pos
        except ZeroDivisionError:
            slope = 1


        x_pos = 1/slope
        y_pos = x_pos*slope

        if elem2.max()*slope < elem1.max():
            x_pos = elem2.max()
            y_pos = x_pos*slope
        if elem2.max()*slope > elem1.max():
            x_pos = elem1.max()/slope
            y_pos = x_pos*slope

        self.scatterWidgetRecon.ROI.endpoints[1].setPos(x_pos,y_pos)
        self.slope_value_recon.setText(str(round(slope,4)))

        tmp_arr = [(slope*elem2) <= elem1]
        tmp_elem1 = elem1[tmp_arr[0]]
        tmp_elem2 = elem2[tmp_arr[0]]
        self.scatterWidgetRecon.plotView2.setData(tmp_elem2, tmp_elem1, brush='r')

        self.scatterWidgetRecon.mousePressSig.connect(self.updateInnerScatterRecon)
        self.scatterWidgetRecon.roiDraggedSig.connect(self.updateInnerScatterRecon)

        return

    def slopeEnteredRecon(self):
        slope = eval(self.slope_value_recon.text())
        if slope < 0 :
            return
        self.scatterWidgetRecon.mousePressSig.disconnect(self.updateInnerScatterRecon)
        self.scatterWidgetRecon.roiDraggedSig.disconnect(self.updateInnerScatterRecon)


        e1 = self.elem1_options_recon.currentIndex()
        e2 = self.elem2_options_recon.currentIndex()
        elem1 = self.reconstructionWidget.recon_array[e1,self.recon_sld.value()]
        elem1 = elem1.flatten()
        elem2 = self.reconstructionWidget.recon_array[e2, self.recon_sld.value()]
        elem2 = elem2.flatten()

        x_pos = 1/slope
        y_pos = x_pos*slope

        if elem2.max()*slope < elem1.max():
            x_pos = elem2.max()
            y_pos = x_pos*slope
        if elem2.max()*slope > elem1.max():
            x_pos = elem1.max()/slope
            y_pos = x_pos*slope

        self.scatterWidgetRecon.ROI.endpoints[1].setPos(x_pos,y_pos)
        self.slope_value_recon.setText(str(round(slope,4)))

        tmp_arr = [(slope*elem2) <= elem1]
        tmp_elem1 = elem1[tmp_arr]
        tmp_elem2 = elem2[tmp_arr]
        self.scatterWidgetRecon.plotView2.setData(tmp_elem2, tmp_elem1, brush='r')

        self.scatterWidgetRecon.mousePressSig.connect(self.updateInnerScatterRecon)
        self.scatterWidgetRecon.roiDraggedSig.connect(self.updateInnerScatterRecon)


    def updateMiniRecon(self):
        
        e1 = self.elem1_options.currentIndex()
        e2 = self.elem2_options.currentIndex()

        data2 = self.data.copy()
        element= e2
        original_shape = data2[element,0].shape
        tmp_data = np.zeros_like(data2[element])


        #_____ calculate points within bounded region _____
        #get handle pos
        x_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().x()
        y_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().y()
        slope = y_pos/x_pos

        for i in range(data2.shape[1]):
            #Normalizeself.projection_sld.currentIndex()
            elem1 = self.data[e1,i] 
            elem1 = elem1.flatten()

            elem2 = self.data[e2, i]
            elem2 = elem2.flatten()

            tmp_arr = [(slope * elem2) < elem1]
            bounded_index = np.where(tmp_arr)[1]

            tmp = data2[e2, i].flatten()
            tmp[bounded_index] = 0
            tmp_data[i] = tmp.reshape(original_shape)


        data2[element] = tmp_data
        center = self.data.shape[3]//2
        beta = 1
        delta = 0.01
        iters = 10
        thetas = self.thetas
        mid_indx = data2.shape[2]//2
        tmp_data2 = data2.copy()
        tmp_data2[element] = tmp_data
        tmp_data2 = tmp_data2[:, :, mid_indx:mid_indx + 1, :]

        #TODO: unresolved method
        recon = self.reconstructionWidget.actions.reconstruct(tmp_data2, element, center, beta, delta, iters, thetas, 0, show_stats=False)

        self.miniReconWidget.reconView.setImage(recon[0])
        return

    def sendData(self):

        e1 = self.elem1_options.currentIndex()
        e2 = self.elem2_options.currentIndex()
        proj_indx = self.projection_sld.value()

        data2 = self.data.copy()
        element= e2
        original_shape = data2[element,0].shape
        tmp_data = np.zeros_like(data2[element])

        #get handle pos
        x_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().x()
        y_pos = self.scatterWidget.p1.items[3].getHandles()[1].pos().y()
        slope = y_pos/x_pos

        for i in range(data2.shape[1]):
            #Normalizeself.projection_sld.currentIndex()
            elem1 = self.data[e1,i] 
            elem1 = elem1.flatten()
            data1 = self.data[e1,i].flatten()

            elem2 = self.data[e2, i]
            elem2 = elem2.flatten()

            tmp_arr = [(slope * elem2) < elem1]
            bounded_index = np.where(tmp_arr)[1]

            tmp = data2[e2, i].flatten()
            tmp[bounded_index] = 0
            tmp_data[i] = tmp.reshape(original_shape)

        data2[element] = tmp_data

        self.data = data2.copy()
        self.update_data(self.data)


    def sendRecon(self):

        e1 = self.elem1_options_recon.currentIndex()
        e2 = self.elem2_options_recon.currentIndex()
        # recon_indx = self.recon_sld.value()

        recon2 = self.recon_array[e2].copy()
        element= e2
        original_shape = recon2[0].shape
        tmp_data = np.zeros_like(recon2)

        #get handle pos
        x_pos = self.scatterWidgetRecon.p1.items[3].getHandles()[1].pos().x()
        y_pos = self.scatterWidgetRecon.p1.items[3].getHandles()[1].pos().y()
        slope = y_pos/x_pos

        for i in range(recon2.shape[0]-1):
            #Normalizeself.projection_sld.currentIndex()
            elem1 = self.recon_array[e1,i].flatten()
            elem2 = self.recon_array[e2,i].flatten()

            tmp_arr = [(slope * elem2) < elem1]
            bounded_index = np.where(tmp_arr)[1]

            tmp = recon2[i].flatten()
            tmp[bounded_index] = 0
            tmp_data[i] = tmp.reshape(original_shape)

        recon2 = tmp_data

        self.recon = recon2.copy()
        self.recon_array[e2] = recon2.copy()
        self.update_recon(self.recon)
        self.update_recon_array(self.recon_array)

    def refresh_filetable(self):
        self.fileTableWidget.onLoadDirectory()
        return

    def toggleDebugMode(self):
        if self.params.experimental:
            self.debugMode()
            self.params.experimental = False

    def toggle_aspect_ratio(self, checkbox_state):
        if checkbox_state:
            self.imageProcessWidget.imageView.p1.vb.setAspectLocked(True)
            self.sinogramWidget.sinoView.p1.vb.setAspectLocked(True)
            self.sinogramWidget.imageView.p1.vb.setAspectLocked(True)
            self.sinogramWidget.diffView.p1.vb.setAspectLocked(True)
            self.reconstructionWidget.ReconView.p1.vb.setAspectLocked(True)
        else:
            self.imageProcessWidget.imageView.p1.vb.setAspectLocked(False)
            self.sinogramWidget.sinoView.p1.vb.setAspectLocked(False)
            self.sinogramWidget.imageView.p1.vb.setAspectLocked(False)
            self.sinogramWidget.diffView.p1.vb.setAspectLocked(False)
            self.reconstructionWidget.ReconView.p1.vb.setAspectLocked(False)

    def loadSettingsChanged(self):
        load_settings = [self.legacy_chbx.isChecked(),
                    self.directory_chbx.isChecked(),
                    self.element_chbx.isChecked(),
                    self.image_tag_chbx.isChecked(),
                    self.data_tag_chbx.isChecked(),
                    self.alingmen_chbx.isChecked(),
                    self.iter_align_param_chbx.isChecked(),
                    self.recon_method_chbx.isChecked()]
        self.params.load_settings = str(load_settings)
        # return
    def debugMode(self):
        self.fileTableWidget.thetaLabel.setVisible(True)
        self.fileTableWidget.thetaLineEdit.setVisible(True)
        self.fileTableWidget.elementTag.setVisible(True)
        self.fileTableWidget.elementTag_label.setVisible(True)
        self.imageProcessWidget.ViewControl.Equalize.setVisible(True)
        self.imageProcessWidget.ViewControl.invert.setVisible(True)
        self.imageProcessWidget.ViewControl.reshapeBtn.setVisible(True)
        # self.imageProcessWidget.ViewControl.btn2.setVisible(True)

        self.sinogramWidget.ViewControl.btn1.setVisible(True)
        self.sinogramWidget.ViewControl.btn3.setVisible(True)
        self.sinogramWidget.ViewControl.btn5.setVisible(True)
        self.sinogramWidget.ViewControl.btn6.setVisible(True)
        return

    def openFolder(self):
        try:
            folderName = QtGui.QFileDialog.getExistingDirectory(self, "Open Folder", QtCore.QDir.currentPath())
        except IndexError:
            print("no folder has been selected")
        except OSError:
            print("no folder has been selected")
        return folderName

    def openH5(self):
        currentDir = self.fileTableWidget.dirLineEdit.text()
        files = QtGui.QFileDialog.getOpenFileNames(self, "Open h5", QtCore.QDir.currentPath(), "h5 (*.h5)" )
        if files[0] == '' or files[0] == []:
            return

        # dir_ending_index = files[0][0].split(".")[0][::-1].find("/")+1
        dir_ending_index = files[0][0].rfind("/")
        path = files[0][0][:dir_ending_index]
        ext = "*."+files[0][0].split(".")[-1]
        self.fileTableWidget.dirLineEdit.setText(path)
        self.fileTableWidget.extLineEdit.setText(ext)
        self.fileTableWidget.onLoadDirectory()
        self.clear_all()
        #disable preprocessing, alignment, reconstructions, save, tools and edit, 
        #Clear self.data, history and reset everytihng prior to loading. 

        self.tab_widget.setTabEnabled(1,False)
        self.tab_widget.setTabEnabled(2,False)
        self.tab_widget.setTabEnabled(3,False)
        self.afterConversionMenu.setDisabled(True)
        self.editMenu.setDisabled(True)
        self.toolsMenu.setDisabled(True)

    def openExchange(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, "Open Folder", QtCore.QDir.currentPath())
        if fname[0] == '':
            return
        data, self.elements, thetas = xrftomo.read_exchange_file(fname)

        sort_angle_index = np.argsort(thetas)
        self.thetas= thetas[sort_angle_index]
        self.data = data[:,sort_angle_index,:,:]
        self.fnames = ["projection {}".format(x) for x in self.thetas]
        self.updateImages(True)
        return

    def openTiffs(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "Open Tiffs", QtCore.QDir.currentPath(), "TIFF (*.tiff *.tif)" )
        if files[0] == '' or files[0] == []:
            return

        dir_ending_index = files[0][0].split(".")[0][::-1].find("/")+1
        path = files[0][0].split(".")[0][:-dir_ending_index]
        ext = "*."+files[0][0].split(".")[-1]
        self.fileTableWidget.dirLineEdit.setText(path)
        self.fileTableWidget.extLineEdit.setText(ext)
        # self.clear_all()
        self.fileTableWidget.onLoadDirectory()

        #disable preprocessing, alignment, reconstructions, save, tools and edit, 
        #Clear self.data, history and reset everytihng prior to loading. 

        self.data = xrftomo.read_tiffs(files[0])
        self.fnames = [files[0][i].split("/")[-1] for i in range(len(files[0]))]
        self.tab_widget.setTabEnabled(1, False)
        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)
        self.afterConversionMenu.setDisabled(True)
        self.editMenu.setDisabled(True)
        self.toolsMenu.setDisabled(True)
        # update images seems to have dissappeare.
        return

    def openThetas(self):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open Theta.txt", QtCore.QDir.currentPath(), "text (*.txt)" )
        if file[0] == '':
            return

        try:
            tmp = self.data
            if tmp.all() == None:
                raise AttributeError
            data_loaded = True
            num_projections = self.data.shape[1]
        except ValueError:
            pass
        except AttributeError:
            # checking that number of projections is the same as the number of angles being loaded from text file,
            # but in the case that thetas are loaded before loading projections, then self.data will not be defined.
            # 1) check if fnames are loaded in filetable: if yes, compare against those.
            # 2) if not, insert message to select a directory with valid h5 files or load tiffs first.
            data_loaded = False
            try:
                #case 1 is true, check for number of fnames and create a list of these fnames as self.fnames
                num_projections = len(self.fileTableWidget.fileTableModel.arrayData)
                self.fnames = [self.fileTableWidget.fileTableModel.arrayData[x].filename for x in range(num_projections)]

            except AttributeError:
                # case 1 is false:
                # show message asking user to load data first or select valid directory.
                self.fileTableWidget.message.setText("select valid directory or load data first. ")
                return
        try:
            fnames, thetas = xrftomo.load_thetas_file(file[0])
        except:
            return
        if not len(thetas)==num_projections:
            self.fileTableWidget.message.setText("nummber of angles different than number of loaded images. ")
            return

        if thetas == []:
            print("No angle information loaded")
            return

        if fnames == []:
            print("No filenames in .txt. Assuming Tiff order corresponds to loaded theta order")
            sorted_index = np.argsort(thetas)
            thetas = np.asarray(thetas)[sorted_index]
            self.fnames = np.asarray(self.fnames)[sorted_index]

        #compare list size first:
        if len(fnames) != len(self.fnames):
            print("number of projections differ from number of loaded angles")
            return

        #filenames from textfile and file from filetable may be similar but not idential. compare only the numberic values
        fname_set1 = self.peel_string(fnames)
        fname_set2 = self.peel_string(self.fnames)

        if set(fname_set1) == set(fname_set2): #if list of fnames from theta.txt have containst same fnames as from the tiffs..
            sorted_index = [fname_set2.index(i) for i in fname_set1]
            self.fnames = np.asarray(self.fnames)[sorted_index]

        if set(fname_set1) != set(fname_set2) and fnames != []: #fnames from tiffs and thetas.txt do not match
            print("fnames from tiffs and thetas.txt do not match. Assuming fnames from table correspond to the same order as the loaded angles.")
            sorted_index = np.argsort(thetas)
            thetas = np.asarray(thetas)[sorted_index]
            self.fnames = np.asarray(self.fnames)[sorted_index]

        self.thetas = [float(list(thetas)[i]) for i in range(len(thetas))]
        self.fnames = [str(list(self.fnames)[i]) for i in range(len(self.fnames))]
        sorted_index = np.argsort(self.thetas)
        self.thetas = np.asarray(self.thetas)[sorted_index]
        self.fnames = np.asarray(self.fnames)[sorted_index]

        for i in range(len(self.thetas)):
            self.fileTableWidget.fileTableModel.arrayData[i].theta = self.thetas[i]
            self.fileTableWidget.fileTableModel.arrayData[i].filename = self.fnames[i]

        #check elementtable if there any elements, if not then manually set a single element
        if len(self.fileTableWidget.elementTableModel.arrayData) == 0 or len(self.fileTableWidget.elementTableModel.arrayData) == 1:
            self.elements = ["Channel_1"]

        self.thetas = np.asarray(self.thetas)

        if data_loaded:
            self.data = self.data[:, sorted_index]
            self.updateImages(True)
            self.tab_widget.setTabEnabled(1, True)
            self.tab_widget.setTabEnabled(2, True)
            self.tab_widget.setTabEnabled(3, True)
            self.afterConversionMenu.setDisabled(False)
            self.editMenu.setDisabled(False)
            self.toolsMenu.setDisabled(False)
            self.viewMenu.setDisabled(False)
            self.fileTableWidget.message.setText("Angle information loaded.")

        return

    def peel_string(self, string_list):
        peel_back = True
        peel_front = True
        while peel_back:
            if len(set([string_list[x][0] for x in range(len(string_list))])) == 1:
                string_list = [string_list[x][1:] for x in range(len(string_list))]
            else:
                peel_back = False
        while peel_front:
            if len(set([string_list[x][-1] for x in range(len(string_list))])) == 1:
                string_list = [string_list[x][:-1] for x in range(len(string_list))]
            else:
                peel_front = False
        return string_list


    def onTabChanged(self, index):
        if self.prevTab == self.TAB_FILE:
            self.loadImages()
        elif self.prevTab == self.TAB_IMAGE_PROC:
            pass
        elif self.prevTab == self.TAB_SINOGRAM:
            pass
        elif self.prevTab == self.TAB_RECONSTRUCTION:
            pass
        self.prevTab = index

    # def saveScatterPlot(self):
    #     try:
    #         self.writer.save_scatter_plot(self.figure)
    #     except AttributeError:
    #         print("Run correlation analysis first")
    #     return

    def saveCorrAlsys(self):
        try:
            self.writer.save_correlation_analysis(self.elements, self.rMat)
        except AttributeError:
            print("Run correlation analysis first")
        return

    def saveAlignemnt(self):
        try:
            self.writer.save_alignemnt_information(self.fnames, self.x_shifts, self.y_shifts, self.centers)
        except AttributeError:
            print("Alignment data does not exist.")
        return

    def saveProjections(self):
        try:
            self.writer.save_projections(self.fnames, self.data, self.elements)
        except AttributeError:
            print("projection data do not exist")
        return

    def saveSinogram(self):
        try:
            self.writer.save_sinogram(self.sino)
        except AttributeError:
            print("sinogram data do not exist")
        return

    def saveSinogram2(self):
        try:
            self.writer.save_sinogram2(self.data, self.elements)
        except AttributeError:
            print("sinogram data do not exist")
        return

    def saveReconstruction(self, recon):
        try:
            self.writer.save_reconstruction(self.recon)
        except AttributeError:
            print("reconstructed data do not exist")
        return
    def saveRecon2npy(self, recon):
        try:
            self.writer.save_recon_2npy(self.recon)
        except AttributeError:
            print("reconstructed data does not exist")
        return

    def saveReconArray2npy(self, recon):
        try:
            self.writer.save_recon_array_2npy(self.recon_array)
        except AttributeError:
            print("reconstructed data does not exist")
        return

    def saveToHDF(self):
        try:
            self.writer.save_dxhdf(self.data, self.elements, self.thetas)
        except AttributeError:
            print("projection data do not exist")
        return 

    def saveThetas(self):
        try:
            files = [i.filename for i in self.fileTableWidget.fileTableModel.arrayData]
            k = np.arange(len(files))
            thetas = [i.theta for i in self.fileTableWidget.fileTableModel.arrayData]
            files_bool = [i.use for i in self.fileTableWidget.fileTableModel.arrayData]
            self.fnames = [files[j] for j in k if files_bool[j]==True]
            self.thetas = np.asarray([thetas[j] for j in k if files_bool[j]==True])
            self.writer.save_thetas(self.fnames, self.thetas)
        except AttributeError:
            print("filename or angle information does not exist")
        return 

    def saveToNumpy(self):
        try:
            self.writer.save_numpy_array(self.data, self.thetas, self.elements)
        except AttributeError:
            print("data has not been imported first")
        return

    def loadImages(self):
        file_array = self.fileTableWidget.fileTableModel.arrayData
        self.element_array = self.fileTableWidget.elementTableModel.arrayData
        #for fidx in range(len(file_array)):

    # def reset_widgets(self):

    def updateImages(self, from_open=False):
        self.data_history = []
        self.x_shifts_history = []
        self.y_shifts_history = []
        self.theta_history = []
        self.fname_history = []
        # self.centers_history = []

        if not from_open:
            self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.data, self.elements, self.thetas, self.fnames = self.fileTableWidget.onSaveDataInMemory()
            #populate scatter plot combo box windows
            self.first_run = True

            self.app.restoreOverrideCursor()

            if len(self.data) == 0:
                return
            if len(self.elements) == 0:
                return
            if len(self.thetas) == 0:
                return
            if len(self.fnames) == 0:
                return
            self.updateScatter()

        self.centers = [100,100,self.data.shape[3]//2]
        self.x_shifts = np.zeros(self.data.shape[1], dtype=np.int)
        self.y_shifts = np.zeros(self.data.shape[1], dtype=np.int)
        self.original_data = self.data.copy()
        self.original_fnames = self.fnames.copy()
        self.original_thetas = self.thetas.copy()

        self.init_widgets()
        self.imageProcessWidget.showImgProcess()
        self.imageProcessWidget.imageView.setAspectLocked(True)

        self.sinogramWidget.showSinogram()
        self.sinogramWidget.showImgProcess()
        self.sinogramWidget.showDiffProcess()
        self.reconstructionWidget.showReconstruct()
        # self.reset_widgets()

        self.tab_widget.setTabEnabled(1,True)
        self.tab_widget.setTabEnabled(2,True)
        self.tab_widget.setTabEnabled(3,True)
        self.afterConversionMenu.setDisabled(False)
        self.editMenu.setDisabled(False)
        self.toolsMenu.setDisabled(False)
        self.viewMenu.setDisabled(False)
        self.update_history(self.data)
        self.update_alignment(self.x_shifts, self.y_shifts)
        self.refreshUI()

    def refreshUI(self):
        self.tab_widget.removeTab(1)
        self.tab_widget.removeTab(2)
        self.tab_widget.removeTab(3)
        self.tab_widget.insertTab(1, self.imageProcessWidget, "Pre Processing")
        self.tab_widget.insertTab(2, self.sinogramWidget, "Alignment")
        self.tab_widget.insertTab(3, self.reconstructionWidget, "Reconstruction")

    def init_widgets(self):
        self.imageProcessWidget.data = self.data
        self.imageProcessWidget.elements = self.elements
        self.imageProcessWidget.thetas = self.thetas
        self.imageProcessWidget.fnames = self.fnames
        self.imageProcessWidget.x_shifts = self.x_shifts
        self.imageProcessWidget.y_shifts = self.y_shifts
        self.imageProcessWidget.centers = self.centers
        self.imageProcessWidget.ViewControl.combo1.setCurrentIndex(0)
        self.imageProcessWidget.sld.setValue(0)

        self.sinogramWidget.data = self.data 
        self.sinogramWidget.elements = self.elements 
        self.sinogramWidget.thetas = self.thetas 
        self.sinogramWidget.fnames = self.fnames 
        self.sinogramWidget.x_shifts = self.x_shifts 
        self.sinogramWidget.y_shifts = self.y_shifts 
        self.sinogramWidget.centers = self.centers 
        self.sinogramWidget.ViewControl.combo1.setCurrentIndex(0)
        self.sinogramWidget.sld.setValue(0)

        self.reconstructionWidget.data_original = self.original_data
        self.reconstructionWidget.data = self.data 
        self.reconstructionWidget.elements = self.elements 
        self.reconstructionWidget.thetas = self.thetas 
        self.reconstructionWidget.fnames = self.fnames
        self.reconstructionWidget.x_shifts = self.x_shifts
        self.reconstructionWidget.y_shifts = self.y_shifts
        self.reconstructionWidget.centers = self.centers
        self.reconstructionWidget.ViewControl.combo1.setCurrentIndex(0)

        self.imageProcessWidget.sld.setValue(0)
        self.reconstructionWidget.sld.setValue(0)
        self.imageProcessWidget.lcd.display(str(self.thetas[0]))
        self.reconstructionWidget.recon = []
        self.sinogramWidget.sld.setValue(1)

    def update_history(self, data):
        index = self.imageProcessWidget.sld.value()
        self.update_data(data)
        self.update_theta(index, self.thetas)
        self.update_filenames(self.fnames, index)
        self.update_alignment(self.x_shifts, self.y_shifts)

        self.data_history.append(data.copy())
        self.theta_history.append(self.thetas.copy())
        self.x_shifts_history.append(self.x_shifts.copy())
        self.y_shifts_history.append(self.y_shifts.copy())
        # self.centers_history.append(self.centers.copy())
        self.fname_history.append(self.fnames.copy())
        print('history save event: ', len(self.data_history))

        if len(self.data_history) > 10:
            del self.data_history[0]
            del self.theta_history[0]
            del self.x_shifts_history[0]
            del self.y_shifts_history[0]
            # del self.centers[0]
            del self.fname_history[0]
        return

    def update_recon(self, recon):
        self.recon = recon
        self.reconstructionWidget.recon = recon
        self.reconstructionWidget.update_recon_image()
        return


    def update_recon_array(self, recon_array):
        self.recon_array = recon_array
        self.reconstructionWidget.recon_array = recon_array
        self.reconstructionWidget.update_recon_image()
        return

    def update_sino(self, sino):
        self.sino = sino.copy()
        return

    def update_data(self, data):
        self.data = data 
        self.imageProcessWidget.data = self.data
        self.imageProcessWidget.imageChanged()
        self.sinogramWidget.data = self.data
        self.sinogramWidget.imageChanged()
        self.reconstructionWidget.data = self.data
        return

    def update_theta(self, index, thetas):
        self.thetas = thetas
        self.imageProcessWidget.thetas = self.thetas
        self.sinogramWidget.thetas = self.thetas
        return

    def update_alignment(self, x_shifts, y_shifts):
        self.x_shifts = x_shifts
        self.y_shifts = y_shifts
        # self.centers = centers 
        self.imageProcessWidget.x_shifts = self.x_shifts
        self.imageProcessWidget.y_shifts = self.y_shifts
        self.imageProcessWidget.actions.x_shifts = self.x_shifts
        self.imageProcessWidget.actions.y_shifts = self.y_shifts
        self.sinogramWidget.x_shifts = self.x_shifts
        self.sinogramWidget.y_shifts = self.y_shifts
        self.sinogramWidget.actions.x_shifts = self.x_shifts
        self.sinogramWidget.actions.y_shifts = self.y_shifts
        self.reconstructionWidget.x_shifts = self.x_shifts
        self.reconstructionWidget.y_shifts = self.y_shifts

        # self.sinogramWidget.actions.centers = self.centers
        return
        
    def update_filenames(self, fnames, index):
        self.fnames = fnames 
        self.imageProcessWidget.fnames = fnames
        self.imageProcessWidget.updateFileDisplay(fnames, index)
        return

    def update_slider_range(self, thetas):
        index = self.imageProcessWidget.sld.value()
        self.imageProcessWidget.updateSldRange(index, thetas)
        self.sinogramWidget.updateImgSldRange(index, thetas)
        self.sinogramWidget.updateDiffSldRange(index, thetas)
        return

    def clear_all(self):
        self.data_history = []
        self.x_shifts_history = []
        self.y_shifts_history = []
        self.fname_history = []
        self.update_alignment([],[])

        self.imageProcessWidget.sld.setValue(0)
        self.imageProcessWidget.sld.setRange(0,0)
        self.imageProcessWidget.lcd.display(0)
        self.sinogramWidget.sld.setRange(0,0)
        self.sinogramWidget.sld.setRange(0,0)
        self.reconstructionWidget.sld.setValue(0)
        self.reconstructionWidget.sld.setRange(0,0)
        
        # self.imageProcessWidget.ViewControl.x_sld.setValue(1)
        # self.imageProcessWidget.ViewControl.x_sld.setRange(1,10)
        # self.imageProcessWidget.ViewControl.y_sld.setValue(1)
        # self.imageProcessWidget.ViewControl.y_sld.setRange(1,10)

        self.imageProcessWidget.imageView.projView.clear()
        self.sinogramWidget.sinoView.projView.clear()
        self.reconstructionWidget.ReconView.projView.clear()

        self.data = None
        self.recon = None
        self.recon_array = None
        self.imageProcessWidget.data = None
        self.sinogramWidget.data = None
        self.sinogramWidget.sinogramData = None
        self.reconstructionWidget.data = None
        self.reconstructionWidget.recon = None

        #move focus to first tab
        
        self.refreshUI()

        #clear element drowpdown
        #clear slice index under reconstruction (maye harmless to leave alone)        

        # self.update_sino([])

        return

    def undo(self):
        try:
            if len(self.data_history) <=1:
                print("maximum history stplt.imshow(self.data_history[1][0])ate reached, cannot undo further")
            else:
                del self.data_history[-1]
                del self.x_shifts_history[-1]
                del self.y_shifts_history[-1]
                del self.theta_history[-1]
                del self.fname_history[-1]
                # del self.centers_history[-1]
                self.data = self.data_history[-1].copy()
                self.x_shifts = self.x_shifts_history[-1].copy()
                self.y_shifts = self.y_shifts_history[-1].copy()
                self.thetas = self.theta_history[-1].copy()
                self.fnames = self.fname_history[-1].copy()
                # self.centers = self.centers_history[-1]

                self.update_alignment(self.x_shifts, self.y_shifts)
                self.update_slider_range(self.thetas)
                # self.update_y_slider_range(self.data.shape[2])
                self.sinogramWidget.ySizeChanged(self.data.shape[2])
                index = self.imageProcessWidget.sld.value()
                self.update_theta(index, self.thetas)
                self.update_filenames(self.fnames, index)
                self.update_data(self.data)

        except AttributeError:
            print("Load dataset first")
            return
        print(len(self.data_history))
        return

    def restore(self):
        try:
            num_projections = self.original_data.shape[1]
            self.data = self.original_data.copy()
            self.thetas = self.original_thetas.copy()
            self.fnames = self.original_fnames.copy()
            self.x_shifts = np.zeros(self.data.shape[1], dtype=np.int)
            self.y_shifts = np.zeros(self.data.shape[1], dtype=np.int)
            self.centers = [100,100,self.data.shape[3]//2]
            self.sinogramWidget.x_padding_hist = [0]
            self.sinogramWidget.y_padding_hist = [0]
            self.update_history(self.data)
            self.update_slider_range(self.thetas)

        except AttributeError:
            print("Load dataset first")
            return

    def projWindow(self):
        self.projection_window.show()
        self.updateMiniProj()

    def scatterPlot(self):
        self.scatter_window.show()
        self.updateScatter()

    def scatterPlotRecon(self):
        self.scatter_window_recon.show()
        self.updateScatterRecon()

    def pixDistanceWindow(self):
        self.pixel_distance_window.show()
        self.updateDistanceHisto()

        # self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        #create window, create two drop-down menus (for element selection)
        #load data[element1], load data2[element2], normalize the two,
        #assign elem1 to x axis, assign elem2 to y axis
        #divide data[elem2] by data[elem1], plot this.

    def onionWindow(self):
        self.onion_window.show()
        self.updateOnion()




    def xy_power(self):

        # dc=pylab.average(ti)
        # dc_img=ti-dc #substract dc value
        # x_axis=f1['MAPS']['x_axis'] #Get the array of x_axis
        # n_x=len(x_axis) #get the number of steps in x direction
        # x_delta_um=abs(x_axis[n_x-1]-x_axis[0])/n_x  #calculate the stepsize in x direction

        # f1=h5py.File(input_path)#read the HDF5 file
        # a=f1['MAPS']['mca_arr']
        # ti=a[channel,:,:] # select the channel associated with Ti fluorescence peak from XRF dectector 0
        # #for i in range(19):
        #    # ti+=a[channel+i,:,:]

        # fft_img=fft2(dc_img)
        # Fc_img=fftshift(fft_img)
        # abs_img=abs(Fc_img)
        # log_img=pylab.log(1+abs_img)
        # power_img=(abs_img)**2# power imaging

        # npiy, npix=power_img.shape
        # x1=np.arange(npix/2)
        # y1=np.arange(npiy/2)
        # f_x1=x1*(1./(n_x*x_delta_um))
        # f_y1=y1*(1./(n_x*x_delta_um))

        # x_power=np.array([0 for i in range(npix/2)], dtype=np.float32)
        # for i in range(npix/2):
        #     x_power[i]=power_img[npiy/2][npix/2+i-1]
        # y_power=np.array([0 for i in range(npiy/2)], dtype=np.float32)
        # for j in range(npiy/2):
        #     y_power[j]=power_img[npiy/2+j-1][npix/2]
            
        # #display fluorescence imaging
        # plt.subplot(221)
        # plt.imshow(ti)
        # plt.title('Fluorescence Imaging')

        # #display 2D-FFT
        # plt.subplot(223)
        # plt.imshow(log_img)
        # plt.title('2D-FFT')

        # #x direction power spectrum
        # plt.subplot(222)
        # plt.loglog(f_x1, x_power)
        # plt.xlim((1,10))
        # plt.title('X direction power spectrum')
        # plt.xlabel('Spatial frequency f(um^-1)')
        # plt.ylabel('Intensity(arb.units)')

        # #y direction power spectrum
        # plt.subplot(224)
        # plt.loglog(f_y1, y_power)
        # plt.xlim((1,10))
        # plt.title('Y direction power spectrum')
        # plt.xlabel('Spatial frequency f(um^-1)')
        # plt.ylabel('Intensity(arb.units)')

        # output_path= '/pf/esafs/edu/northwestern/k-brister/93940/data_analysed/bnp_power_spec_output/'+ os.path.splitext(filename)[0]+'_xy_directions.png'
        # print("output_path= "+output_path) 
        # plt.savefig(output_path)
        # plt.show()


        pass

    def corrElem(self):
        self.app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        
        data = self.data
        #normalize data
        # nom_data = self.normData(data)
        # errMat = np.zeros((data.shape[0],data.shape[0]))
        # simMat = np.zeros((data.shape[0],data.shape[0]))
        self.rMat = np.zeros((data.shape[0],data.shape[0]))
        for i in range(data.shape[0]):      #elemA
            for j in range(data.shape[0]):  #elemB
                elemA = data[i]
                elemB = data[j]
                # corr = np.mean(signal.correlate(elemA, elemB, method='direct', mode='same') / (data.shape[1]*data.shape[2]*data.shape[3]))
                rval = self.compare(elemA, elemB)
                # errMat[i,j]= err
                # simMat[i,j]= sim
                self.rMat[i,j]= rval

        sns.set(style="white")

        # Generate a mask for the upper triangle
        mask = np.zeros_like(self.rMat, dtype=np.bool)
        mask[np.triu_indices_from(mask,1)] = True

        # Set up the matplotlib figure
        self.analysis_figure, ax = plt.subplots(figsize=(11, 9))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        d = pd.DataFrame(data=self.rMat, columns=self.elements, index=self.elements)
        sns.heatmap(d, mask=mask, annot=True, cmap=cmap, vmax=self.rMat.max(), center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})
        self.analysis_figure.show()

        self.app.restoreOverrideCursor()
        return self.rMat

    # def normData(self,data):
    #     norm = np.zeros_like(data)
    #     for i in range(data.shape[0]):
    #         data_mean = np.mean(data[i])
    #         data_std = np.std(data[i])
    #         data_med = np.median(data[i])
    #         data_max = np.max(data[i])
    #         new_max = data_mean+10*data_std
    #         current_elem = data[i]
    #         current_elem[data[i] >= new_max] = new_max
    #         data[i] = current_elem

    #     return data 

    def compare(self, imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;

        d = len(imageA)
        # d2 = len(imageB)
        # errMat = np.zeros(imageA.shape[0])
        # simMat = np.zeros(imageA.shape[0])
        rMat = np.zeros(imageA.shape[0])


        if d > 2:
            for i in range(imageA.shape[0]):
                # err = np.sum((imageA[i].astype("float") - imageB[i].astype("float")) ** 2)
                # err /= float(imageA[i].shape[0] * imageA[i].shape[1])
                # sim = measure.compare_ssim(imageA[i], imageB[i])
                r, p = stats.pearsonr(imageA[i].flatten(), imageB[i].flatten())

                # errMat[i] = err
                # simMat[i] = sim
                rMat[i] = r
                # errVal = np.sum(errMat)/len(errMat)
                # simVal = np.sum(simMat)/len(simMat)
            rVal = np.sum(rMat)/len(rMat)
        else:
            # err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
            # err /= float(imageA.shape[0] * imageA.shape[1])
            # sim  = measure.compare_ssim(imageA, imageB)
            # errVal = err
            # simVal = sim
            r, p = stats.pearsonr(imageA.flatten(), imageB.flatten())

            rVal = r

        # return the MSE, the lower the error, the more "similar"
        return rVal


    def keyMapSettings(self):
        self.keymap_options.show()
        return

    def configSettings(self):
        self.config_options.show()
        return

    def closeEvent(self, event):
        print("here I am")
        try:
            sections = config.TOMO_PARAMS + ('gui', )
            home = expanduser("~")
            config.write('{}/xrftomo.conf'.format(home), args=self.params, sections=sections)
            self.sinogramWidget.ViewControl.iter_parameters.close()
            self.sinogramWidget.ViewControl.center_parameters.close()
            self.sinogramWidget.ViewControl.move2edge.close()
            self.sinogramWidget.ViewControl.sino_manip.close()
            self.imageProcessWidget.ViewControl.reshape_options.close()
            self.config_options.close()
            self.keymap_options.close()
            matplotlib.pyplot.close()

        except IOError as e:
            self.gui_warn(str(e))
            self.on_save_as()

def main(params):
    app = QtGui.QApplication(sys.argv)
    mainWindow = xrftomoGui(app, params)
    sys.exit(app.exec_())
