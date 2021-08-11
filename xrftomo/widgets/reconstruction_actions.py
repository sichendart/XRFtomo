# #########################################################################
# Copyright © 2020, UChicago Argonne, LLC. All Rights Reserved.        	  #
#    																	  #
#						Software Name: XRFtomo							  #
#																		  #
#					By: Argonne National Laboratory						  #
#																		  #
#						OPEN SOURCE LICENSE                               #
#                                                                         #
# Redistribution and use in source and binary forms, with or without      #
# modification, are permitted provided that the following conditions      #
# are met:                                                                #
#                                                                         #
# 1. Redistributions of source code must retain the above copyright       #
#    notice, this list of conditions and the following disclaimer.        #
#																		  #
# 2. Redistributions in binary form must reproduce the above copyright    #
#    notice, this list of conditions and the following disclaimer in      #
#    the documentation and/or other materials provided with the 		  #
#    distribution.														  #
# 									                                      #
# 3. Neither the name of the copyright holder nor the names of its 		  #
#    contributors may be used to endorse or promote products derived 	  #
#    from this software without specific prior written permission.		  #
#																		  #
#								DISCLAIMER								  #
#							  											  #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 	  #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 	  #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR   #
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 	  #
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  #
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 		  #
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,   #
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY   #
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 	  #
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.	  #
###########################################################################


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
import xrftomo
import tomopy
import os
from matplotlib.pyplot import *
import numpy as np
from skimage import exposure



class ReconstructionActions(QtWidgets.QWidget):
	dataSig = pyqtSignal(np.ndarray, name='dataSig')
	fnamesChanged = pyqtSignal(list,int, name="fnamesChanged")

	def __init__(self):
		super(ReconstructionActions, self).__init__()

	def reconstruct(self, data, element, center, method, beta, delta, iters, thetas, mid_indx, show_stats=False):
		'''
		load data for reconstruction and load variables for reconstruction
		make it sure that data doesn't have infinity or nan as one of
		entries
		'''
		recData = data[element, :, :, :]
		recData[recData == np.inf] = True
		recData[np.isnan(recData)] = True
		recCenter = np.array(center, dtype=np.float32)

		print("working fine")

		if method == 0:
			self.recon= tomopy.recon(recData, thetas * np.pi / 180, 
				algorithm='mlem', center=recCenter, num_iter=iters, accelerated=True, device='cpu')
			self.recon /= 0.0070430035033585735
		elif method == 1:
			# TODO: gridrec fails and cannot recover, all of python shuts down. consider removing.
			self.recon= tomopy.recon(recData, thetas * np.pi / 180,
				algorithm='gridrec')
			self.recon /= 0.9080359350734858
		elif method == 2:
			self.recon= tomopy.recon(recData, thetas * np.pi / 180, 
				algorithm='art', num_iter=iters)
			self.recon /= 0.9998318282790742
		elif method == 3:
			self.recon= tomopy.recon(recData, thetas * np.pi / 180, 
				algorithm='pml_hybrid', center=recCenter, 
				reg_par=np.array([beta, delta], dtype=np.float32), num_iter=iters)
			self.recon /= 0.9998791750170672
		elif method == 4:
			self.recon = tomopy.recon(recData, thetas * np.pi / 180,
				algorithm='pml_quad', center=recCenter,
				reg_par=np.array([beta, delta], dtype=np.float32), num_iter=iters)
			self.recon /= 0.9997819558282253
		elif method == 5:
			self.recon= tomopy.recon(recData, thetas * np.pi / 180,
				algorithm='fbp')
		elif method == 6:
			self.recon= tomopy.recon(recData, thetas * np.pi / 180, 
				algorithm='sirt', num_iter=iters)
		elif method == 7:
			self.recon = tomopy.recon(recData, thetas * np.pi / 180,
				algorithm='tv', center=recCenter,
				reg_par=np.array([beta, delta], dtype=np.float32), num_iter=iters)

		self.recon[self.recon<0] = 0
		#tomopy.remove_nan() does not remove inf values
		self.recon = tomopy.remove_nan(self.recon)

		if np.isinf(self.recon).max():
			print("WARNING: inf values found in reconstruction, consider reconstructing with less iterations")
			print("inf values replaced with 0.001")
			self.recon[self.recon == np.inf] = 0.001

		if show_stats:
			err, mse  = self.assessRecon(self.recon, recData, thetas, mid_indx, show_stats)
			print(mse)
		return self.recon

	def reconstructAll(self, data, element_names, center, method, beta, delta, iters, thetas):
		print("This will take a while")
		save_path = QtGui.QFileDialog.getExistingDirectory(self, "Open Folder", QtCore.QDir.currentPath())
		num_elements = data.shape[0]
		for i in range(num_elements):
			print("running reconstruction for:", element_names[i])
			#data, element, center, method, beta, delta, iters, thetas, mid_indx, show_stats=False
			recon = self.reconstruct(data, i, center, method, beta, delta, iters, thetas, 0, show_stats=False)
			#TODO: update recon_array with every new recon result. 
			savepath = save_path+'/'+element_names[i]
			savedir = savepath+'/'+element_names[i]
			os.makedirs(savepath)
			xrftomo.SaveOptions.save_reconstruction(self, recon, savedir)

		return recon

	def assessRecon(self,recon, data, thetas, mid_indx, show_plots=True):
		#TODO: make sure cros-section index does not exceed the data height
		#get index where projection angle is zero
		zero_index = np.where(abs(thetas)==abs(thetas).min())[0][0]
		num_slices = recon.shape[0]
		width = self.recon.shape[1]
		reprojection = np.zeros([num_slices, width])
		tmp = np.zeros([num_slices, width])

		# get recon reporjection for slice i and take the difference with data projection (at angle ~=0).
		for i in range(num_slices):
			reprojection[i] = np.sum(recon[i], axis=0)
			if data[zero_index, i].max() == 0:
				tmp[i] = np.zeros(width)
			else:
				#projection for 0 angle at row i / projection for angle 0 at row i, mximum value / maximum value of recon for row i
				#projection row / (proj max / reproj max)
				tmp[i] = data[zero_index, i] / (data[zero_index, i].max() / np.sum(recon[i], axis=0).max())
		#normalizing projectios against reconstruction side length, so plot appears withing image.
		projection = tmp*width/tmp.max()
		#normalizing reprojectios against reconstruction side length, so plot appears withing image.
		reprojection = reprojection*width/reprojection.max()

		projection_xSection = tmp[mid_indx]*width/tmp[mid_indx].max()
		reprojection_xSection = reprojection[mid_indx]*width/reprojection[mid_indx].max()
		#difference between reporjection and original projection at angle == 0
		# err = tmp - reprojection/reprojection
		err = projection - reprojection
		#mean squared error
		mse = (np.square(err)).mean(axis=None)
		figA = figure()
		imshow(recon[mid_indx], origin='lower'), plot(projection_xSection), plot(reprojection_xSection)
		legend(('projection', 'reprojection'), loc=1)
		title("MSE:{}".format(np.round(mse, 4)))
		figB = figure()
		imshow(projection)
		title("projection")
		figC = figure()
		imshow(reprojection)
		title("reprojection")

		if show_plots:
			figA.show()
			figB.show()
			figC.show()

		return err, mse

	def equalize_recon(self,recon):
		# Equalization
		global_mean = np.mean(recon)
		num_recons = recon.shape[0]
		for i in range(num_recons):
			local_mean = np.mean(recon[i])
			coeff = global_mean/local_mean
			recon[i] = recon[i]*coeff
			img = recon[i]
			# data[element,i] = exposure.equalize_hist(img)
			img *= 1/img.max()
			recon[i] = exposure.equalize_adapthist(img)
		return recon

	def setThreshold(self,threshold,recon):
		for i in range(recon.shape[0]):
			img = recon[i]
			img[img <= threshold] = 0
			recon[i] = img
		return recon

	def remove_hotspots(self, recon):
		max_val = np.max(recon)
		for i in range(recon.shape[0]):
			img = recon[i]
			img[img > 0.5*max_val] = 0.5*max_val
			recon[i] = img
		return recon

	def shiftProjection(self, data, x, y, index):
		X = int(x//1)
		Y = int(y//1)
		x = x - X
		y = y - Y 

		if x > 0: 
			x_dir = 1
		elif x < 0:
			x_dir = -1
		else:
			x_dir = 0

		if y > 0: 
			y_dir = 1
		elif x < 0:
			y_dir = -1
		else:
			y_dir = 0

		data[:,index] = np.roll(data[:,index], Y, axis=1)  #negative because image coordinates are flipped
		data[:,index] = np.roll(data[:,index], X, axis=2)

		if x_dir == 0 and y_dir == 0:
			return data

		else:
			data_a = data*x
			data_b = data*(1-x)
			data_b = self.shiftProjection(data_b,x_dir,0, index)
			data_c = data_a+data_b

			data_a = data_c*y
			data_b = data_c*(1-y)
			data_b = self.shiftProjection(data_b,0,y_dir, index)
			data = data_a+data_b

			return data

	def reconMultiply(self):
		'''
		multiply reconstruction by 10
		'''
		self.recon = self.recon * 10
		return self.recon

	def reconDivide(self, recon):
		'''
		divide reconstuction by 10
		'''
		self.recon = recon / 10
		return self.recon
