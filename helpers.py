from PIL import Image
import os
import random
os.makedirs("/Audio/Temp",exist_ok=True)
l=[{"Title": "Card 1", "Description": "Description for card 1", "AudioURL": "audio1.mp3", "ImageURL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr4_j6B_Rm1Om5WrQW6en163GJyhkE2awj9A&s"},
		{"Title": "Card 2", "Description": "Description for card 2", "AudioURL": "audio1.mp3", "ImageURL": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr4_j6B_Rm1Om5WrQW6en163GJyhkE2awj9A&s"}]
def make_audio_list(l):
	with open("list.txt","w+") as file:
		for i in l:
			print(i[1])
			file.write(i['AudioURL'])
	try:
		os.system("ffmpeg.exe -f concat -safe 0 -i list.txt output.mp3")
	except:
		print("FFMPEG failed to merge audio")

def make_image_list(l):
	temp=[]
	for i in l:
		t=i['Title']
		temp.append(random.choice(os.listdir(f".\\classified\\{t}\\")))
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




os.system("ffmpeg.exe -f concat -safe 0 -i list.txt output.mp3")