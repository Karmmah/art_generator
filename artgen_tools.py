import random, math

import artgen, hsl_colors
cwidth, cheight = artgen.get_canvas_dimensions()

def draw_line(canvas,coords=[],color="",width=0):
	if coords == []:
		coords = [random.randint(0,cwidth),random.randint(0,cheight),random.randint(0,cwidth),random.randint(0,cheight)]
	if color == "":
		color = get_color()
	if width == 0:
		width = random.randint(1,10)
	canvas.create_line(coords,fill=color,width=width)
	string = '\n	<line x1="'+str(coords[0])+'" y1="'+str(coords[1])+'" x2="'+str(coords[2])+'" y2="'+str(coords[3])+'" stroke="'+color+'" stroke-width="'+str(width)+'" stroke-linecap="square"/>'
	return canvas,string

def get_color():
	hue, saturation, luminance = random.randint(0,360), random.randint(0,100), random.randint(0,100)
	return hsl_colors.get_color(hue, saturation, luminance)
