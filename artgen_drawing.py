import random, artgen, artgen_tools, math, hsl_colors

cwidth, cheight = artgen.cwidth, artgen.cheight
output_width, output_height = artgen.output_width, artgen.output_height
xborder, yborder = artgen.xborder, artgen.yborder

#parameters
width_min, width_max = 2, cwidth/10 #for outlines and lines

######complex shapes
####################
def draw_perspective(canvas):
	amount = random.randint(3,7)
	max_radius = random.randint(int(cwidth/10),int(cwidth/4))
	centers = artgen_tools.get_coordinates(2)
	perspective_factor = random.randint(60,140)/100
	coords1, coords2 = [], []
	for i in range(amount):
		angle = 2*math.pi*i/amount
		radius = max_radius*random.randint(20,100)/100
		x = centers[0]+math.cos(angle)*radius
		y = centers[1]+math.sin(angle)*radius
		coords1 += [x,y]
		radius = radius*perspective_factor
		x = centers[2]+math.cos(angle)*radius
		y = centers[3]+math.sin(angle)*radius
		coords2 += [x,y]
	color = artgen_tools.get_color()
	width = random.randint(2,int(cwidth/60))
	output = ""
	canvas, string = draw_polygon(canvas, coords=coords1, outline=color, width=width)
	output += string
	for i in range(amount):
		coords = [coords1[2*i],coords1[2*i+1],coords2[2*i],coords2[2*i+1]]
		canvas, string = draw_line(canvas,coords=coords,color=color,width=width)
		output += string
	canvas, string = draw_polygon(canvas, coords=coords2, outline=color, width=width)
	output += string
	return canvas, output

def draw_flow(canvas):
	amount = random.randint(5,36)
	gradient = hsl_colors.get_gradient(artgen_tools.get_color(),artgen_tools.get_color(),amount)
	output = ""
	line_coords = artgen_tools.get_coordinates(2)
	radius1, radius2 = random.randint(2,int(cwidth/4)), random.randint(4,int(cwidth/4))
	shape_number = random.randint(0,1)
	for i in range(amount):
		radius = radius1+(radius2-radius1)*i/amount
		x = line_coords[0]+(line_coords[2]-line_coords[0])*i/amount
		y = line_coords[1]+(line_coords[3]-line_coords[1])*i/amount
		coords = [x,y]
		if shape_number == 0:
			canvas, string = draw_circle(canvas, coords=coords, fill=gradient[i], radius=radius)
		elif shape_number == 1:
			coords = [coords[0]-radius,coords[1]-radius,coords[0]+radius,coords[1]+radius]
			canvas, string = draw_rectangle(canvas, coords=coords, fill=gradient[i])
		output += string
	return canvas, output

def draw_spray(canvas):
	amount = random.randint(5,36)
	gradient = hsl_colors.get_gradient(artgen_tools.get_color(),artgen_tools.get_color(),amount)
	output = ""
	for i in range(amount):
		radius = 10+i*4
		canvas, string = draw_circle(canvas, fill=gradient[i], radius=radius)
		output += string
	return canvas, output

def draw_circular_pattern(canvas):
	symmetry = random.randint(3,7) #number of symmetry axes
	amount = random.randint(3,6) #number of points in polygon
	coords = artgen_tools.get_coordinates(amount)
	max_radius = cwidth-xborder if cwidth-xborder < cheight-yborder else cheight-yborder
	for i in range(amount):
		radius = math.sqrt((coords[2*i]-cwidth/2-xborder)**2+(coords[2*i+1]-cheight/2-yborder)**2)
		if radius>max_radius:
			angle = math.asin((coords[2*i+1]-cheight/2-xborder)/radius)
			x = cwidth/2+(2*max_radius-radius)*math.cos(angle)
			y = cheight/2+(2*max_radius-radius)-math.sin(angle)
			coords[2*i], coords[2*i+1] = x, y
	color = artgen_tools.get_color()
	canvas, string = draw_polygon(canvas, coords, color)
	for i in range(1,symmetry):
		new_coords = []
		for j in range(amount):
			radius = math.sqrt((coords[2*j]-cwidth/2-xborder)**2+(coords[2*j+1]-cheight/2-yborder)**2)
			angle = math.asin((coords[2*j+1]-cheight/2-xborder)/radius)+i*2*math.pi/symmetry
			x, y = cwidth/2+radius*math.cos(angle), cheight/2-radius*math.sin(angle)
			new_coords += [x,y]
		canvas, new_string = draw_polygon(canvas, new_coords, color)
		string += new_string
	return canvas, string

def draw_symmetry(canvas):
	amount = random.randint(3,6)
	coords = artgen_tools.get_coordinates(amount)
	mirrored_coords = []
	for i in range(amount):
		mirrored_coords += [cwidth/2-(coords[2*i]-cwidth/2), coords[2*i+1]]
	color = artgen_tools.get_color()
	canvas, string1 = draw_polygon(canvas,coords,color)
	canvas, string2 = draw_polygon(canvas,mirrored_coords,color)
	string = string1+string2
	return canvas, string

def draw_net(canvas):
	#generate some points; for each point find out which are two closest neighbours, draw triangle to these points
	#maybe check if the same triangles are drawn multiple times
	amount = random.randint(4,8)
	coords = artgen_tools.get_coordinates(amount)
	svg = ""
	for i in range(amount):
		closest = [-1,cwidth+cheight] #coord index and calculated distance
		second_closest = [-1,cwidth+cheight]
		for j in range(amount):
			if j != i:
				distance = math.sqrt((coords[2*j]-coords[2*i])**2+(coords[2*j+1]-coords[2*i+1])**2)
				if distance < second_closest[1]:
					if distance < closest[1]:
						second_closest = closest
						closest = [j, distance]
					else:
						second_closest = [j, distance]
		coordinates = [coords[2*i],coords[2*i+1],coords[2*closest[0]],coords[2*closest[0]+1],coords[2*second_closest[0]],coords[2*second_closest[0]+1]]
		canvas, string = draw_polygon(canvas, coords=coordinates)
		svg += string
	return canvas,svg

######basic shapes
##################
def draw_circle(canvas, coords=[], radius=0, fill="", outline="", width=0):
	if coords == [] or len(coords) != 2:
		coords = artgen_tools.get_coordinates(1)
	if radius == 0:
		if cwidth < cheight:
			radius = random(4,cwidth/2)
		else:
			radius = random.randint(4,cheight/2)
	if fill == "" and outline == "":
		fill = artgen_tools.get_color()
	if width == 0:
		width = random.randint(width_min,width_max)
	coords = [coords[0]-radius,coords[1]-radius,coords[0]+radius,coords[1]+radius]
	canvas.create_oval(coords, fill=fill, outline=outline, width=width)
	coords = artgen_tools.scale_to_output(coords)
	cx, cy = (coords[0]+coords[2])/2, (coords[1]+coords[3])/2
	rx, ry = abs((coords[0]-coords[2])/2), abs((coords[1]-coords[3])/2)
	string = '\n<ellipse cx="%f" cy="%f" rx="%f" ry="%f" fill="%s" stroke="%s" stroke-width="%f"/>'%(cx,cy,rx,ry,fill,outline,width)
	return canvas, string

def draw_polygon(canvas, coords=[], fill="", outline="", width=0):
	amount = random.randint(3,6) #maybe adjust number with slider?
	if coords == []:
		coords = artgen_tools.get_coordinates(amount)
	if fill == "" and outline == "":
		fill = artgen_tools.get_color()
	if width == 0:
		width = random.randint(width_min,width_max)
#	canvas.create_polygon(coords, fill=fill, outline=outline, width=width, joinstyle='miter')
	xavg, yavg = 0, 0 #calculate center of coordinates for ordering the coordinates around it
	amount = int(len(coords)/2) #number of points
	for i in range(amount):
		xavg += coords[2*i]
		yavg += coords[2*i+1]
	xavg, yavg = xavg/amount, yavg/amount
#	canvas.create_oval(xavg-3,yavg-3,xavg+3,yavg+3, fill="black")
	sorted_coords = []
	for i in range(amount):
		if coords[2*i]-xavg != 0:
			angle = math.atan((yavg-coords[2*i+1])/(coords[2*i]-xavg)) #calculate angle of point to avg relative to horizontal
		else:
			if yavg-coords[2*i+1] > 0:
				angle = math.pi/2
			else:
				angle = -math.pi/2
		angle = -angle
		if coords[2*i]-xavg < 1:
			angle += math.pi
		sorted_coords += [[angle,coords[2*i],coords[2*i+1]]]
	sorted_coords.sort()
	coords = []
	for i in range(amount):
		coords += sorted_coords[i][1:3]
#		canvas.create_text(sorted_coords[i][1:3], text=str(i), font="Arial 24", fill="#ff0000")
	canvas.create_polygon(coords, fill=fill, outline=outline, width=width, joinstyle='miter')
	coords = artgen_tools.scale_to_output(coords) #scale the coordinates for proper size in output svg file
	string = '\n	<polygon points="' #svg output
	for i in range(len(coords)): #add coordinates to svg output
		string = string + str(coords[i])+' '
	fill = "none" if fill=="" else fill
	string = string + '" fill="'+fill+'" stroke="'+outline+'" stroke-width="'+str(width)+'" stroke-linecap="butt" stroke-linejoin="miter stroke-miterlimit:12"/>'
	return canvas, string

#def draw_polygon_basic(canvas, coords=[], fill="", outline="", width=0):
#	amount = random.randint(3,6) #maybe adjust number with slider?
#	if coords == []:
#		coords = artgen_tools.get_coordinates(amount)
#	if fill == "" and outline == "":
#		fill = artgen_tools.get_color()
#	if width == 0:
#		width = random.randint(width_min,width_max)
#	canvas.create_polygon(coords, fill=fill, outline=outline, width=width, joinstyle='miter')
#	coords = artgen_tools.scale_to_output(coords) #scale the coordinates for proper size in output svg file
#	string = '\n	<polygon points="' #svg output
#	for i in range(len(coords)): #add coordinates to svg output
#		string = string + str(coords[i])+' '
#	string = string + '" fill="'+fill+'" stroke="'+outline+'" stroke-width="'+str(width)+'" stroke-linecap="butt" stroke-linejoin="miter stroke-miterlimit:12"/>'
#	return canvas, string

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