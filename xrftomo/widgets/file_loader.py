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


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import xrftomo
import h5py
import numpy as np
import os
from xrftomo.file_io.reader import *

class FileTableWidget(QWidget):
    def __init__(self, parent):
        super(FileTableWidget, self).__init__()
        self.parent = parent
        self._num_cols = 4
        self._num_row = 4
        self.auto_load_settings = eval(self.parent.params.load_settings)
        self.auto_theta_pv = self.parent.params.theta_pv
        self.auto_input_path = self.parent.params.input_path
        self.auto_extension = self.parent.params.file_extension
        self.auto_element_tag = self.parent.params.element_tag
        self.auto_quant_tag = self.parent.params.quant_tag
        self.auto_scaler_tag = self.parent.params.scaler_tag
        self.auto_data_path = self.parent.params.data_path
        self.auto_sorted_angles = self.parent.params.sorted_angles
        self.auto_selected_elements = eval(self.parent.params.selected_elements)
        self.initUI()

    def initUI(self):
        self.fileTableModel = xrftomo.FileTableModel()
        self.fileTableView = QTableView()
        self.fileTableView.setModel(self.fileTableModel)
        self.fileTableView.setSortingEnabled(True)
        self.fileTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.fileTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTableView.customContextMenuRequested.connect(self.onFileTableContextMenu)

        self.elementTableModel = xrftomo.ElementTableModel()
        self.elementTableView = QTableView()
        self.elementTableView.setModel(self.elementTableModel)
        self.elementTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.elementTableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.elementTableView.customContextMenuRequested.connect(self.onElementTableContextMenu)

        dirLabel = QLabel('Directory:')
        self.dirLineEdit = QLineEdit(self.auto_input_path)
        self.dirLineEdit.returnPressed.connect(self.onLoadDirectory)
        self.extLineEdit = QLineEdit(self.auto_extension)
        self.extLineEdit.setMaximumSize(50, 30)
        self.extLineEdit.returnPressed.connect(self.onLoadDirectory)
        # self.dirBrowseBtn = QPushButton('Browse')
        # self.dirBrowseBtn.clicked.connect(self.onDirBrowse)

        self.thetaOptions = ['2xfm:m53.VAL', '2xfm:m36.VAL','2xfm:m58.VAL', '9idbTAU:SM:ST:ActPos']
        thetaCompleter = QCompleter(self.thetaOptions)
        self.thetaLabel = QLabel('Theta PV:')
        self.thetaLabel.setFixedWidth(90)
        self.thetaLabel.setVisible(False)
        self.thetaLineEdit = QLineEdit(self.auto_theta_pv)
        self.thetaLineEdit.setCompleter(thetaCompleter)
        # self.thetaLineEdit.textChanged.connect(self.onThetaPVChange)
        self.thetaLineEdit.returnPressed.connect(self.onThetaUpdate)
        self.thetaLineEdit.setFixedWidth(123)
        self.thetaLineEdit.setVisible(False)

        data_menu_lbl = QLabel("data tag")
        data_menu_lbl.setFixedWidth(90)
        self.data_menu = QMenu()
        self.data_menu.setFixedSize(123,25)
        self.data_menu.triggered.connect(self.data_menu.show)
        self.data_menu.show()

        element_menu_lbl = QLabel("element tag")
        element_menu_lbl.setFixedWidth(90)
        self.element_menu = QMenu()
        self.element_menu.setFixedSize(123,25)
        self.element_menu.triggered.connect(self.element_menu.show)
        self.element_menu.show()

        self.saveDataBtn = QPushButton('Save to Memory')
        # self.saveDataBtn.clicked.connect(self.onSaveDataInMemory)
        # self.saveDataBtn.setEnabled(False)
        self.saveDataBtn.setFixedWidth(221)

        message_label = QLabel('Messages:')
        self.message = QTextEdit()
        self.message.setReadOnly(True)
        self.message.setMaximumHeight(20)
        self.message.setText('')


        hBox0 = QHBoxLayout()
        hBox0.addWidget(data_menu_lbl)
        hBox0.addWidget(self.data_menu)
        hBox0.setAlignment(Qt.AlignLeft)

        hBox1 = QHBoxLayout()
        hBox1.addWidget(element_menu_lbl)
        hBox1.addWidget(self.element_menu)
        hBox1.setAlignment(Qt.AlignLeft)

        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.thetaLabel)
        hBox2.addWidget(self.thetaLineEdit)
        hBox2.setAlignment(Qt.AlignLeft)

        hBox7 = QHBoxLayout()
        hBox7.addWidget(self.saveDataBtn)
        hBox7.setAlignment(Qt.AlignLeft)

        vBox1 = QVBoxLayout()
        vBox1.addLayout(hBox0)
        vBox1.addLayout(hBox1)
        vBox1.addLayout(hBox2)
        vBox1.addLayout(hBox7)
        # vBox1.setFixedWidth(275)

        layout0 = QHBoxLayout()
        layout0.addWidget(dirLabel)
        layout0.addWidget(self.dirLineEdit)
        layout0.addWidget(self.extLineEdit)
        # layout0.addWidget(self.dirBrowseBtn)

        layout1 = QHBoxLayout()
        layout1.addLayout(vBox1)
        layout1.addWidget(self.fileTableView)
        layout1.addWidget(self.elementTableView)

        layout2 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(message_label)
        layout2.addWidget(self.message)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout0)
        mainLayout.addLayout(layout1)
        mainLayout.addLayout(layout2)

        self.setLayout(mainLayout)
        try:
            self.onLoadDirectory()
        except:
            print("Invalid directory or file; Try a new folder or remove problematic files.")
        self.onThetaUpdate()

    def onLoadDirectory(self, files = None):
        self.version = 0
        ext = self.extLineEdit.text()
        self.fileTableModel.loadDirectory(self.dirLineEdit.text(), self.extLineEdit.text())
        fpath = self.fileTableModel.getFirstCheckedFilePath()

        if fpath == None:
            self.message.setText('Invalid directory')
            return
        self.fileTableModel.setAllChecked(True)

        if ".h5" in ext:
            try:
                fpath = self.fileTableModel.getFirstCheckedFilePath()
                self.img = h5py.File(fpath, "r")
                self.data_menu_name = self.data_menu.addMenu("data")
                self.populate_data_menu(self.img, self.data_menu_name)
                self.data_menu_name.setTitle(self.auto_data_path)

                self.element_menu_name = self.element_menu.addMenu("element")
                self.populate_element_menu(self.img, self.element_menu_name)
                self.element_menu_name.setTitle(self.auto_element_tag)

                self.element_tag_changed()
                # self.setup_scaler_list()
                self.onThetaUpdate()

                try: #set auto_load options here:

                    elem_indx = self.elementTags[self.imageTag.currentIndex()].index(self.auto_element_tag)
                    self.elementTag.setCurrentIndex(elem_indx)
                    self.element_tag = self.elementTag.currentText()
                    self.element_tag_changed()

                    quant_indx = self.quantTags.index(self.auto_quant_tag)
                    self.quantTag.setCurrentIndex(quant_indx)

                    scaler_indx = self.scalerTags.index(self.auto_scaler_tag)
                    self.scalerTag.setCurrentIndex(scaler_indx)

                except:
                    pass
                self.elementTag.currentIndexChanged.connect(self.element_tag_changed)
                # self.scalerTag.currentIndexChanged.connect(self.scaler_tag_changed)

            except KeyError:
                pass

        if ext == '*.tiff' or ext == ".tiff" or ext == ".tif" or ext == "*.tif":
            # TODO: when loading from filemenu, check only files which were selected
            if not self.elementTableModel.arrayData == []:

                for i in range(1,len(self.elementTableModel.arrayData)):
                    self.elementTableModel.arrayData.pop()
                self.elementTableModel.arrayData[0].element_name = "Channel_1"
                self.elementTableModel.arrayData[0].use = True
            else:
                pass

            self.imageTag.setEnabled(False)
            self.dataTag.setEnabled(False)
            self.scalerTag.setEnabled(False)
            self.message.setText("Load angle information using txt or csv file")
            pass
        return

    def rename_menu(self):
        name = self.sender().text()
        self.data_menu_name.setTitle(name)
        self.data_menu_name.setFixedSize(123,25)
        self.data_menu_name.show()
        return

    def populate_data_menu(self, obj, menu):
        keys = obj.keys()
        for key in keys:
            if isinstance(obj[key],h5py.Group):
                sub_menu = menu.addMenu(key)
                self.populate_data_menu(obj[key], sub_menu)
            elif isinstance(obj[key],h5py.Dataset):
                sub_action = QAction(key,self)
                menu.addAction(sub_action)
                sub_action.triggered.connect(self.update_data_path)
        return menu

    def populate_element_menu(self, obj, menu):
        keys = obj.keys()
        for key in keys:
            if isinstance(obj[key],h5py.Group):
                sub_menu = menu.addMenu(key)
                self.populate_element_menu(obj[key], sub_menu)
            elif isinstance(obj[key],h5py.Dataset):
                sub_action = QAction(key,self)
                menu.addAction(sub_action)
                sub_action.triggered.connect(self.update_element_tag)
        return menu

    def update_data_path(self):
        name0 = self.sender().associatedWidgets()[0].title()
        name1 = ""
        if isinstance(self.sender(), QAction):
            name1 = self.sender().text()
        elif isinstance(self.sender(), QMenu):
            name1 = self.sender().title()
        print("{}/{}".format(name0,name1))
        self.data_path = "{}/{}".format(name0,name1)
        self.data_menu_name.setTitle(self.data_path)
        self.data_menu.setFixedSize(123,25)
        self.data_menu.show()

    def update_element_tag(self):
        name0 = self.sender().associatedWidgets()[0].title()
        name1 = ""
        if isinstance(self.sender(), QAction):
            name1 = self.sender().text()
        elif isinstance(self.sender(), QMenu):
            name1 = self.sender().title()
        print("{}/{}".format(name0,name1))
        self.element_tag = "{}/{}".format(name0,name1)
        self.element_menu_name.setTitle(self.element_tag)
        self.element_menu.setFixedSize(123,25)
        self.element_menu.show()

    def getElements(self):
        #TODO: do not ise img_tags
        # img_tag = self.imageTag.currentText()
        element_tag = self.element_tag
        element_list = list(self.img[element_tag])
        element_list = [x.decode("utf-8") for x in element_list]
        element_idxs = []
        element_names = []
        for i in range(len(element_list)):
            if self.elementTableModel.arrayData[i].use:
                element_names.append(self.elementTableModel.arrayData[i].element_name)
                element_idxs.append(i)

        return element_names, element_idxs


    def element_tag_changed(self):
        element_tag = self.element_tag
        element_list = list(self.img[element_tag])
        elements = [x.decode("utf-8") for x in element_list]
        self.elementTableModel.loadElementNames(elements)
        self.elementTableModel.setAllChecked(False)
        self.elementTableModel.setChecked(self.auto_selected_elements, (True))
        return

    def normalizeData(self, data, scalers, quants):
        #normalize
        num_files = data.shape[1]
        num_elements= data.shape[0]
        for i in range(num_elements):
            for j in range(num_files):
                data[i,j] = data[i,j]/quants[i,j]
            data[i] = data[i]/scalers
        data[np.isnan(data)] = 0.0001
        data[data == np.inf] = 0.0001
        # for i in range(num_elements):
        #     norm_median = np.median(data[i, :, :, :])
        #     norm_mean = np.mean(data[i, :, :, :])
        #     norm_std = np.std(data[i, :, :, :])
        #     elem_max = np.max(data[i, :, :, :])
        #     norm_max = 3*norm_std + norm_mean
        #     for j in range(num_files):
        #         median_arr = np.ones_like(data[i,j])*norm_mean
        #         data[i,j] = [data[i,j] <= norm_max]*data[i,j,:,:]
        #         data[i,j] = data[i,j] + [data[i,j] == 1]*np.ones_like(data[i,j])*norm_max
        return data

    def checkVersion(self):
        #temporary definition of 'version'
        exchange_bool = list(self.img)

        try:
            theta_exists = self.img[list(self.img)[0]]["theta"][()]
            self.version = 1
        except:
            print("checking file version... No version info available")
            self.version = 0

        # if self.parent.forceLegacy.isChecked():
        #     self.version=0

        #Temporary hardcode version to 0 (legacy import mode)
        #self.version = 0

        # TODO: the auto_load_settings line will override non-legacy version, not good.
        # if self.auto_load_settings[0]:
        #     self.version = 0
        # try:
            # TODO: there may no longer be a legacy checkbox
            # if self.parent.legacy_chbx.isChecked():
            #     self.version = 0
            # if not self.parent.legacy_chbx.isChecked():
            #     self.version = 1
        # except:
        #     #checkboxes not yet defined
        #     pass
        return self.version

    def onThetaUpdate(self):
        # version defines file format and how to read thetas from it.
        path_files = self.fileTableModel.getAllFiles()
        #get path_files list
        thetaPV = self.thetaLineEdit.text()
        #TODO: check to see if thetas is available under exchange tag, if not, load in
        #legacy mode or just check under MAPS, or throw a warning (prompt user to enable
        #debug tools and enter PV otherweise load thetas file.
        try:
            thetas = load_thetas(path_files, self.imgTags[self.imageTag.currentIndex()], self.version, thetaPV)
        except:
            thetas=[]
            self.message.setText("directory probably not mounted.")
        if len(thetas) == 0:
            for i in self.thetaOptions:
                try:
                    thetas = load_thetas(path_files, self.imgTags[self.imageTag.currentIndex()], self.version, i)
                except:
                    print("trying theta PV {}".format(i))
                if len(thetas) >0:
                    if len(set(thetas)) > 1:
                        self.thetaLineEdit.setText(i)
                        break
                else:
                    thetas = np.ones(len(path_files))

        self.fileTableModel.update_thetas(thetas)
        if self.parent.params.sorted_angles == True:
            self.fileTableView.sortByColumn(1, 0)
        return

    def onFileTableContextMenu(self, pos):
        if self.fileTableView.selectionModel().selection().indexes():
            rows = []
            for i in self.fileTableView.selectionModel().selection().indexes():
                rows += [i.row()]
            menu = QMenu()
            check_action = menu.addAction("Check")
            uncheck_action = menu.addAction("Uncheck")
            action = menu.exec_(self.fileTableView.mapToGlobal(pos))
            if action == check_action or action == uncheck_action:
                self.fileTableModel.setChecked(rows, (check_action == action))

    def onElementTableContextMenu(self, pos):
        if self.elementTableView.selectionModel().selection().indexes():
            rows = []
            for i in self.elementTableView.selectionModel().selection().indexes():
                rows += [i.row()]
            menu = QMenu()
            check_action = menu.addAction("Check")
            uncheck_action = menu.addAction("Uncheck")
            action = menu.exec_(self.elementTableView.mapToGlobal(pos))
            if action == check_action or action == uncheck_action:
                self.elementTableModel.setChecked(rows, (check_action == action))

    def reset_widgets(self):
        self.parent.imageProcessWidget.sld.setValue(0)
        self.parent.reconstructionWidget.sld.setValue(0)
        self.parent.reconstructionWidget.recon = []
        self.parent.sinogramWidget.sld.setValue(0)

    def onSaveDataInMemory(self):
        files = [i.filename for i in self.fileTableModel.arrayData]
        if len(files) == 0:
            self.message.setText('Directory probably not mounted')
            return [], [] , [], []
        thetas = [i.theta for i in self.fileTableModel.arrayData]
        elements = [i.element_name for i in self.elementTableModel.arrayData]
        files_bool = [i.use for i in self.fileTableModel.arrayData]
        elements_bool = [i.use for i in self.elementTableModel.arrayData]
        element_tag = self.element_tag
        k = np.arange(len(files))
        l = np.arange(len(elements))
        files = [files[j] for j in k if files_bool[j]==True]
        path_files = [self.fileTableModel.directory + '/' + s for s in files]
        thetas = np.asarray([thetas[j] for j in k if files_bool[j]==True])
        elements = [elements[j] for j in l if elements_bool[j]==True]

        #update auto-load parameters
        self.parent.params.input_path = self.dirLineEdit.text()
        self.parent.params.file_extension = self.extLineEdit.text()
        self.parent.params.theta_pv = self.thetaLineEdit.text()
        self.parent.params.data_path = self.data_path
        self.parent.params.element_tag = self.element_tag
        self.parent.params.selected_elements = str(list(np.where(elements_bool)[0]))

        if len(elements) == 0:
            self.message.setText('no element selected.')
            return [], [] , [], []
        else:
            self.message.setText('loading files...')
        if all(x==thetas[0] for x in thetas):           #check if all values in thetas are the same: no theta info.
            self.message.setText('WARNING: No unique angle information. Double check Theta PV or current directory')
            # return [], [] , [], []

        self.parent.clear_all()
        try:
            data, quants, scalers = xrftomo.read_mic_xrf(path_files, elements, hdf_tag, data_tag, element_tag, quant_tag, scaler_tag, scaler_idx)
        except:
            self.message.setText("invalid image/data/element tag combination. Load failed")
            return [], [], [], []

        if data is None or scalers is None:
            return [], [], [], []
        if self.scalerTag.currentText() != 'None':
            elements, element_idxs = self.getElements()
        self.message.setText('finished loading')

        data[np.isnan(data)] = 0.0001
        data[data == np.inf] = 0.0001

        return data, elements, thetas, files

