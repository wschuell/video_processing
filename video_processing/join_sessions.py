#!/bin/python

import subprocess
import os
import glob

def join_sessions(threads=1):
	if not os.path.exists('tmp'):
		os.makedirs('tmp')
	for session in next(os.walk('raw'))[1]: #listing direct child directories of ./raw
		out_file_name = "tmp/{}.mp4".format(session)
		if not os.path.isfile(out_file_name):
			subprocess.call(["avconv", "-i",
				"concat:" + "|".join(sorted([os.path.join("raw", session, f) for f in os.listdir(
					os.path.join("raw", session))])),
				"-acodec", "copy", "-vcodec", "libx264", "-crf", "21", "-r", "30000/1001",
				"-deinterlace", "-y", "-threads", str(threads), out_file_name])