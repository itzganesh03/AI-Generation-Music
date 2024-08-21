from PIL import Image
import os
from urllib.parse import unquote
import random
os.makedirs("/Audio/Temp",exist_ok=True)

def make_audio_list(l):
	with open("list.txt","w+") as file:
		for i in l:
			s="file '"+unquote(i['audioUrl']).strip("file:///")+"'"+"\n"
			file.write(s)

	try:
		os.system("ffmpeg.exe -f concat -safe 0 -i list.txt output.mp3")
	except:
		print("FFMPEG failed to merge audio")

def make_image_list(l):
	temp=[]
	for i in l:
		t=i['title']
		temp.append(f".\\Classifier_training_dataset\\{t}\\"+random.choice(os.listdir(f".\\Classifier_training_dataset\\{t}\\")))
	images = [Image.open(x) for x in temp]
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset, 0))
		x_offset += im.size[0]

	new_im.save('test.jpg')