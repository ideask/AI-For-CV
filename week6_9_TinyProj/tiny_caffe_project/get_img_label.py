import numpy as np
import random
import os

process = ['Test','Train']
def doit(process):
	for phase in process:
		CurPwd = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
		file_name = CurPwd + '/src_data/' + phase + '/Label.TXT'
		file_write_name = CurPwd + '/' + phase + '.txt'
		#write_pre = CurPwd + '/src_data/' + phase + '/'
		with open(file_name) as f:
			lines = f.readlines()

		write_lines = []
		for line in lines:
			#write_line = write_pre + ' '.join(line.split(' ')[:-1]) + '\n'
			write_line = ' '.join(line.split(' ')[:-1]) + '\n'
			write_lines.append(write_line)
		random.shuffle(write_lines)

		with open(file_write_name, 'w') as wf:
			for wl in write_lines:
				wf.write(wl)

doit(process)

