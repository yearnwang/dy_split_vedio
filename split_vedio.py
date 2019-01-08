#!/usr/bin/env python
# coding=utf-8

import argparse
import ffmpeg
import os


# 分割的时间，单位：秒
g_per_s = 15;
# 字体的位置
g_font_path = '/Library/Fonts/Songti.ttc';
g_text_color = 'red'


def runBash(command):
	os.system(command)

def get_total_len(filename):
	probe = ffmpeg.probe(filename)
	video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
	print '[+]total time:%s s' % video_info['duration'];
	return video_info['duration'];
	pass;

def get_split_list(filename,total_num,per_ms,title_str):
	_list = [];
	_count = int(float(total_num)) / int(per_ms);

	_file_suffix = 'part';
	_out_part_file = filename;
	(pre_filename,extension) = os.path.splitext(_out_part_file);

	_start = 0;
	_end   = 0;

	for x in range(_count):
		_start = _end;
		_end   = _start + per_ms;
		_f_name = '%s_%s_%02d'%(pre_filename,_file_suffix,x+1);
		_f_title = '%s %d'%(title_str,x+1);
		_list.append({'start': _start, 'end': _end, 'f_name': _f_name ,'title':_f_title , 'ext':extension});
		pass;

	if int( float(total_num) % per_ms)  > 0 :
		_count = _count + 1;
		_start = _end;
		_end   = _start + int(float(total_num)) % per_ms;
		_f_name = '%s_%s_%02d'%(pre_filename,_file_suffix,_count);
		_f_title = '%s %d'%(title_str,_count);

		_list.append({'start': _start, 'end': _end, 'f_name': _f_name ,'title':_f_title,'ext':extension});

	return _list;

def crop(start,end,input,output):
	str  = 'ffmpeg -i %s -ss %d -to %d -acodec copy %s -y' % (input , start , end ,output);
	runBash(str);

def gen_bak_name(org_file_name,extension):
	_bak_file_name = '%s_bak%s'%(org_file_name,extension);
	return _bak_file_name;


def trim_vedio(filename,file_list):	
	for one_list in file_list:
		_start = int(one_list['start']);
		_end   = int(one_list['end']);
		_fname = one_list['f_name'];
		_ext   = one_list['ext'];
		_f_tmp_name =  gen_bak_name(_fname,_ext);
		crop(_start,_end,filename,_f_tmp_name);
	pass;

def addtext(input,output,text_str):
	#ffmpeg -i  test.mp4  -vf  drawtext="fontsize=80:fontfile=monaco.ttf:fontcolor=red:enable=lt(mod(t\,60)\,5):text='hahah!':x=(w-text_w)/2:y=(h-text_h)/2" test1.mp4 -y
	font_str = "\"fontsize=80:fontfile=%s:fontcolor=%s:enable=lt(mod(t\,60)\,5):text=%s:x=(w-text_w)/2:y=(h-text_h)/2:shadowy=2\"" % (g_font_path,g_text_color,text_str);
	str = "ffmpeg -i %s -vf drawtext=%s %s -y" %  (input , font_str, output);
	runBash(str);

def remove_file(filename):
	cmd_str = 'rm -rf %s' % filename;
	runBash(cmd_str);

def add_title_to_vedio(filename,file_list):

	for one_list in file_list:
		_start = int(one_list['start']);
		_end   = int(one_list['end']);
		_ext   = one_list['ext'];
		_fname = one_list['f_name'];
		_f_tmp_name =  gen_bak_name(_fname,_ext);
		_title = one_list['title'];
		_fname_new = '%s%s' % (_fname,_ext);
		addtext(_f_tmp_name , _fname_new, _title);
		remove_file(_f_tmp_name);
	pass;

def main():
	args = parser.parse_args();
	global g_text_color;

	mp4filename = args.filename;
	title_text = args.title;
	g_text_color = args.titlecolor;

	total_s = get_total_len(mp4filename);
	file_list = get_split_list(mp4filename,total_s,g_per_s,title_text);
	trim_vedio(mp4filename,file_list);
	add_title_to_vedio(mp4filename,file_list);
	pass;





if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='split vedio many and drawtext')
	parser.add_argument('filename', help='mp4 filename')
	parser.add_argument('title', help = 'drawtext title text')
	parser.add_argument('titlecolor', help = 'title text color')

	
	main();
