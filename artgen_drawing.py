import random, artgen, artgen_tools

#parameters
cwidth, cheight = artgen.cwidth, artgen.cheight
output_width, output_height = artgen.output_width, artgen.output_height

def draw_rectangle(canvas,coords=[],fill="",outline="",width=0):
	if coords == []:
		coords = artgen_tools.get_coordinates(2)
	canvas.create_rectangle(coords,fill=fill,outline=outline,width=width)
	coords = artgen_tools.scale_to_output(coords) #scale the coordinates for proper size in output svg file
	x = coords[0] if coords[0]<coords[2] else coords[2]
	y = coords[1] if coords[1]<coords[3] else coords[3]
	width, height = str(int(round(abs(coords[0]-coords[2]),0))), str(int(round(abs(coords[1]-coords[3]),0)))
	string = '\n	<rect x="'+str(x)+'" y="'+str(y)+'" width="'+width+'" height="'+height+'" fill="'+fill+'" stroke="'+outline+'"/>'
	return canvas,string

def draw_line(canvas,coords=[],color="",width=0):
	if coords == []:
		coords = artgen_tools.get_coordinates(2)
	if color == "":
		color = artgen_tools.get_color()
	if width == 0:
		width = random.randint(1,10)
	canvas.create_line(coords,fill=color,width=width)
	coords = artgen_tools.scale_to_output(coords)
	string = '\n	<line x1="'+str(coords[0])+'" y1="'+str(coords[1])+'" x2="'+str(coords[2])+'" y2="'+str(coords[3])+'" stroke="'+color+'" stroke-width="'+str(width)+'" stroke-linecap="square"/>'
	return canvas,string