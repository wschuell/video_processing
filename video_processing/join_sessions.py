#!/bin/python

import subprocess
import os
from os.path import isfile, join


def join_sessions(threads=1, input_dir='raw', output_dir='tmp'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for session in next(os.walk(input_dir))[1]:
        print(session)
        out_file_name = "{}/{}.mp4".format(output_dir, session)
        if not os.path.isfile(out_file_name):
            path = join(input_dir, session)
            list_files = sorted(
                [join(path, f) for f in os.listdir(path) if isfile(join(path, f))])
            print list_files
            cmd = ["avconv", "-i", "concat:" + "|".join(list_files),
                   "-acodec", "copy", "-vcodec", "libx264", "-crf", "21", "-r", "30000/1001",
                   "-deinterlace", "-y", "-threads", str(threads), out_file_name]
            print(cmd)
            subprocess.call(cmd)
