#!/bin/python

import subprocess
import os
import shutil
import glob
import time

def backup(SD_NAME=None, session=None, erase=False):
	if not os.path.exists('raw'):
		os.makedirs('raw')
	SD_NAME = 'test' 
	SD_ROOT = '/media/' + os.getusername() + '/' + SD_NAME
	DATE = time.strftime('%Y-%m-%d_%H-%M-%S')
	if not session:
		BACKUP_DIR = 'video_' + DATE
	else:
		BACKUP_DIR = session
	os.chdir('raw')
	if not os.path.exists(BACKUP_DIR):
		os.makedirs(BACKUP_DIR)
	os.chdir(BACKUP_DIR)
	command = ['rsync', '-a', '-r', '--stats', '--progress', SD_ROOT+'/PRIVATE/AVCHD/BDMV/STREAM', '.']
	if subprocess.check_call(command) == 0:
		if erase:
			shutil.rmtree(SD_ROOT)
		print("Done")
	else:
		print("Error while running rsync")
	for filename in glob.glob('00*.MTS'):
		os.rename(filename,DATE+filename)
	os.chdir('../..')