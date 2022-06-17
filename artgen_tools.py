import random, math, artgen, hsl_colors

#parameters
cwidth, cheight = artgen.cwidth, artgen.cheight
output_width, output_height = artgen.output_width, artgen.output_height
xborder, yborder = artgen.xborder, artgen.yborder

def artwork_number(mode): #mode is "normal" or "test"
	with open("artwork_number.txt","r") as _file_:
		number = int(_file_.read())+1
	if mode == "normal":
		with open("artwork_number.txt","w") as _file_:
			_file_.write(str(number))
	return number

def scale_to_output(coords): #scale coordinates from canvas to output svg file dimensions
	for i in range(int(len(coords)/2)):
		coords[2*i] = coords[2*i]*output_width/cwidth
		coords[2*i+1] = coords[2*i+1]*output_height/cheight
	return coords

def get_coordinates(amount=1): #coordinates format: [x1,y1,...,xn,yn]
	coordinates = []
	for i in range(amount):
		x = random.randint(xborder,cwidth-xborder)
		y = random.randint(yborder,cheight-yborder)
		coordinates += [x,y]
	return coordinates

def get_color():
	hue, saturation, luminance = random.randint(0,360), random.randint(0,100), random.randint(0,100)
	return hsl_colors.get_color(hue, saturation, luminance)
