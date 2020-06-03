import os
import copy
import subprocess

# from .backup import backup
# from .join_sessions import join_sessions
# from .cut_encode import extract_mp4
# from .cut_encode import extract_ts
# from .cut_encode import concat
# from .cut_encode import cut_encode


class VideoProcessing(object):

	def __init__(self,global_dir='.',tmp_dir='tmp/',output_dir='output/',threads=1):
		self.global_dir = global_dir
		self.threads = threads
		self.tmp_dir = os.path.join(self.global_dir,tmp_dir)
		self.output_dir = os.path.join(self.global_dir,output_dir)
		self.create_dirs()
		
	def create_dirs(self):
		for d in [self.output_dir,self.tmp_dir]:
			if not os.path.exists(d):
				os.makedirs(d)

	def set_config(self,cfg):
		self.cfg = copy.deepcopy(cfg)

	def update_config(self,cfg):
		#TODO recursive update scheme
		self.cfg.update(cfg)

	def process(self):
		for session, value in self.cfg.items():
			for video_name, parts_info in value.items():
				filename = os.path.join(self.tmp_dir,'{}.mp4'.format(session))
				if len(parts_info) == 1:
					self.extract_mp4(filename=filename, outdir=os.path.join(self.output_dir,session), video_name=video_name, info=parts_info[0])
				else:
					for part_nb,part in enumerate(parts_info):
						self.extract_ts(filename=filename, outdir=os.path.join(self.tmp_dir,session), video_name=video_name,video_nb=str(part_nb), info=part)
					part_files = [ os.path.join(self.tmp_dir,session,video_name,'{}.ts'.format(i)) for i in range(len(parts_info))]
					self.concat(part_files=part_files, outdir=os.path.join(self.output_dir,session), video_name=video_name)


	def get_duration(self,start,end):
		if not isinstance(start,int):
			start = sum([60**(i)*int(r) for i,r in enumerate(reversed(start.split(':')))])
		if not isinstance(end,int):
			end = sum([60**(i)*int(r) for i,r in enumerate(reversed(end.split(':')))])
		t = end-start
		# d = tuple([t//60**i for i in (2,1,0)])
		# return d_end-d_start
		#TODO use datetime
		# d = map(sub, list(map(int, end.split(':'))), list(map(int, start.split(':'))))
		# print(d)
		# if d[2] < 0:
		# 	d[2] += 60
		# 	d[1] -= 1
		# if d[1] < 0:
		# 	d[1] += 60
		# 	d[0] -= 1
		# print(d)
		# return "%02d:%02d:%02d" % d
		return t

	def extract_mp4(self,filename,outdir,video_name,info):
		if not os.path.exists(outdir):
			os.makedirs(outdir)
		out_file_name = os.path.join(outdir,"{}.mp4".format(video_name))
		if not os.path.isfile(out_file_name):
			cmd = 'avconv -i {filename} -ss {start} -t {duration} -acodec copy -vcodec libx264 -threads {threads} {outfile}'.format(filename=filename,start=info[0],duration=self.get_duration(*info),threads=self.threads,outfile=out_file_name)
			print(cmd)
			subprocess.check_call(cmd.split(' '))

	def extract_ts(self,filename,outdir,video_name,video_nb,info):
		if not os.path.exists(os.path.join(outdir,video_name)):
			os.makedirs(os.path.join(outdir,video_name))
		out_file_name = os.path.join(outdir,video_name,"{}.ts".format(video_nb))
		if not os.path.isfile(out_file_name):
			cmd = 'avconv -i {filename} -acodec copy -vcodec libx264 -bsf:v h264_mp4toannexb -f mpegts -ss {start} -t {duration} -strict experimental -threads {threads} -y {outfile}'.format(filename=filename,start=info[0],duration=self.get_duration(*info),threads=self.threads,outfile=out_file_name)
			print(cmd)
			subprocess.check_call(cmd.split(' '))

	def concat(self,part_files,outdir,video_name):
		if not os.path.exists(outdir):
			os.makedirs(outdir)
		out_file_name = os.path.join(outdir,"{}.mp4".format(video_name))
		if not os.path.isfile(out_file_name):
			cmd = 'avconv -i concat:{file_list} -acodec copy -vcodec libx264 -crf 21 -r 30000/1001 -deinterlace -threads {threads} -y {outfile}'.format(file_list="|".join(sorted(part_files)),threads=self.threads,outfile=out_file_name)
			print(cmd)
			subprocess.check_call(cmd.split(' '))

if __name__ == '__main__':
	vp = VideoProcessing(global_dir='../../',threads=6)
	cfg = {'wednesday':
					{
					'introduction':[('00:10','00:20'),('00:25','01:30')],
					}
			,'thursday':
					{
					'introduction':[('00:15','00:20'),('00:25','01:30')],
					'introduction_2':[('02:10','02:20'),],
							
					}
			}

	vp.set_config(cfg)
	vp.process()