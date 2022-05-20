import random, artgen, artgen_tools

#parameters
cwidth, cheight = artgen.cwidth, artgen.cheight
output_width, output_height = artgen.output_width, artgen.output_height
width_min, width_max = 2, 20

######shapes
############

def draw_triangle(canvas, coords=[], fill="", outline="", width=0):
	if coords == []:
		coords = artgen_tools.get_coordinates(3)
	if fill == "" and outline == "":
		fill = artgen_tools.get_color()
	if width == 0:
		width = random.randint(width_min,width_max)
	canvas.create_polygon(coords, fill=fill, outline=outline, width=width, joinstyle='miter')
	coords = artgen_tools.scale_to_output(coords) #scale the coordinates for proper size in output svg file
	string = '\n<polygon points="' #svg output
	for i in range(len(coords)): #add coordinates to svg output
		string = string + str(coords[i])+' '
	string = string + '" fill="'+fill+'" stroke="'+outline+'" stroke-width="'+str(width)+'" stroke-linecap="butt" stroke-linejoin="miter stroke-miterlimit:12"/>'
	return canvas, string

def draw_polygon(canvas, coords=[], fill="", outline="", width=0):
	amount = random.randint(3,6) #maybe adjust number with slider?
	if coords == []:
		coords = artgen_tools.get_coordinates(amount)
	if fill == "" and outline == "":
		fill = artgen_tools.get_color()
	if width == 0:
		width = random.randint(width_min,width_max)
	canvas.create_polygon(coords, fill=fill, outline=outline, width=width, joinstyle='miter')
	coords = artgen_tools.scale_to_output(coords) #scale the coordinates for proper size in output svg file
	string = '\n<polygon points="' #svg output
	for i in range(len(coords)): #add coordinates to svg output
		string = string + str(coords[i])+' '
	string = string + '" fill="'+fill+'" stroke="'+outline+'" stroke-width="'+str(width)+'" stroke-linecap="butt" stroke-linejoin="miter stroke-miterlimit:12"/>'
	return canvas, string

def draw_rectangle(canvas,coords=[],fill="",outline="",width=0):
	if coords == []:
		coords = artgen_tools.get_coordinates(2)
	if fill == "" and outline == "":
		fill = artgen_tools.get_color()
	if width == 0:
		width = random.randint(width_min,width_max)
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
		width = random.randint(width_min,width_max)
	canvas.create_line(coords,fill=color,width=width)
	coords = artgen_tools.scale_to_output(coords)
	string = '\n	<line x1="'+str(coords[0])+'" y1="'+str(coords[1])+'" x2="'+str(coords[2])+'" y2="'+str(coords[3])+'" stroke="'+color+'" stroke-width="'+str(width)+'" stroke-linecap="square"/>'
	return canvas,string

######backgrounds
#################

def draw_color(canvas, color=""): #draw full screen of one color as background
	color = color if color != "" else artgen_tools.get_color()
	canvas.create_rectangle(0,0,cwidth,cheight, fill=color, outline="")
	string = '\n	<rect x="0" y="0" width="'+str(output_width)+'" height="'+str(output_height)+'" fill="'+color+'" stroke=""/>'
	return canvas, string