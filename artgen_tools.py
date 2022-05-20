import random, math, artgen, hsl_colors

#parameters
cwidth, cheight = artgen.cwidth, artgen.cheight
output_width, output_height = artgen.output_width, artgen.output_height
xborder, yborder = artgen.xborder, artgen.yborder

def get_gradient(color1,color2,steps):
    red1, green1, blue1 = int(color1[1:3],16), int(color1[3:5],16), int(color1[5:7],16)
    red2, green2, blue2 = int(color2[1:3],16), int(color2[3:5],16), int(color2[5:7],16)
    gradient = []
    for i in range(steps):
        red_new = hex(int(round(red1+(red2-red1)*i/steps,0))).lstrip('-0x')
        green_new = hex(int(round(green1+(green2-green1)*i/steps,0))).lstrip('-0x')
        blue_new = hex(int(round(blue1+(blue2-blue1)*i/steps,0))).lstrip('-0x')
        while len(red_new) < 2:
            red_new = '0'+red_new
        while len(green_new) < 2:
            green_new = '0'+green_new
        while len(blue_new) < 2:
            blue_new = '0'+blue_new
        gradient.append('#'+str(red_new)+str(green_new)+str(blue_new))
    return gradient

def artwork_number(mode="normal"):
####implement counting one up when test mode is not active
	with open("artwork_number.txt") as _file_:
		number = int(_file_.read())+1
		if mode == "test":
			_file_.write(str(number+1))
	return number

def scale_to_output(coords): #scale coordinates from canvas to output svg file dimensions
	for i in range(int(len(coords)/2)):
		coords[2*i] = coords[2*i]*output_width/cwidth
		coords[2*i+1] = coords[2*i+1]*output_height/cheight
	return coords

# [random.randint(0,cwidth),random.randint(0,cheight),random.randint(0,cwidth),random.randint(0,cheight)]
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
