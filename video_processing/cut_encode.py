import subprocess
import os
from operator import sub
import glob

THREADS=3

# from https://gist.github.com/macu/9520902 (corrected!)
def duration(t0, t1):
    d = map(sub, list(map(int, t1.split(':'))), list(map(int, t0.split(':'))))
    print d
    if d[2] < 0:
        d[2] += 60
        d[1] -= 1
    if d[1] < 0:
        d[1] += 60
        d[0] -= 1
    print d
    return "%02d:%02d:%02d" % tuple(d)

test = {
	'session1':{'video1':[
	{'start':25145454, 'end': 54534543},
	]
}

def extract_mp4(filename,outdir,video_name,info,threads=1):
    out_file_name = "{}/{}.mp4".format(outdir,video_name)
    if not os.path.isfile(out_file_name):
        subprocess.call(["avconv", "-i", filename, "-ss", info["start"],
            "-t", duration(info["start"], info["end"]), "-acodec", "copy", "-vcodec", "libx264", "-threads", str(threads), out_file_name])

def extract_ts(filename,outdir,video_name,info,threads=1):
    out_file_name = "{}/{}.mp4".format(outdir,video_name)
    if not os.path.isfile(out_file_name):
        subprocess.call(["avconv", "-i", filename, 
            "-vcodec", "libx264", "-acodec", "copy", "-bsf:v", "h264_mp4toannexb", "-f", 
            "mpegts", "-ss", info["start"], "-t", duration(info["start"], info["end"]),
            "-strict", "experimental", "-threads", str(threads), "-y", out_file_name ])

def concat(part_files,outdir,video_name,threads=1):
    out_file_name = "{}/{}.{}".format(outdir,video_name,'.mp4')
    if not os.path.isfile(out_file_name):
        subprocess.call(["avconv", "-i",
            "concat:" + "|".join(sorted(part_files)),
            "-acodec", "copy", "-vcodec", "libx264", "-crf", "21", "-r", "30000/1001",
            "-deinterlace", "-threads", str(threads), "-y", out_file_name])

def cut_encode(cfg,threads=1):
    for session, value in cfg.items():
        for video_name, parts_info in value.items():
            if len(parts_info) == 1:
                extract_mp4(filename='tmp/{}.mp4'.format(session), outdir='output/'+session, video_name=video_name, info=parts_info[0], threads=threads)
            else:
                for part_nb in range(len(parts_info)):
                    extract_ts(filename='tmp/{}.mp4'.format(session), outdir='tmp', video_name=video_name + str(part_nb), info=parts_info[part_nb], threads=threads)
                part_files = ['tmp/{}{}.ts'.format(video_name,i) for i in range(len(parts_info))]
                concat(part_files=part_files, outdir='output', video_name, threads=threads)

