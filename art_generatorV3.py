#!/usr/bin/env python

#ideas:
#piet mondrian style pattern
#stroke function
#adjust calculate_pointNr function
#swirls
#angled rectangles
#circular gradient
#auswahlbox für art des kunstwerks (pattern, symmetry, mandala, comic, ...)
#custom color sets (farben eingeben die dann ausschließlich verwendet werden)
#punktwolke nach normalverteilung in artgen (mehr punkte in der mitte, als am rand -> Haufen in der Mitte)

#anmerkung für nächste version:
#parameter als array übergeben statt einzeln
#bei jeder funktion erst seed generieren, daraus bild malen, seed abspeichern (evtl auf dem bild als text)
#standard methoden in eigenes modul und dann importierenfs

#https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Shapes



#canvas.find_all() to get handles of all objects on canvas
#canvas.coords(<object handle>) to get coordinates of object



import tkinter as tk
import random as rn
import math

canvas_width = 900
canvas_height = canvas_width

default_background = '\n<rect fill="#ffffff" stroke="none" width="'+str(canvas_width)+'" height="'+str(canvas_height)+'" x="'+str(0)+'" y="'+str(0)+'" />' # clean background (white rectangle) to reset svg output

global svg
svg = default_background

def draw_image(event): #draw random amount of shapes with background
	bg = rn.randint(1,5)
	if bg == 0: #background
		pass #draw_gradient()
	elif bg == 1:
		draw_colorwall('')
	elif bg == 2:
		draw_perspective('')
	elif bg == 3:
		draw_patch('')
	elif bg == 4:
		draw_bubbles('')
	else:
		draw_color('')
	amount = rn.randint(5,12)
	for i in range(amount): #shapes
		shape = rn.randint(0,5)
		if shape == 0:
			draw_rectangle('','','')
		elif shape == 1:
			draw_line('','','')
		elif shape == 2:
			draw_polyline('','', '')
		elif shape == 3:
			draw_ellipse('','','')
		elif shape == 4:
			draw_polygon('','','')
		elif shape == 5:
			if rn.randint(0,4) == 0: #additional lower probability for radial
				draw_radial('')
			else:
				draw_polygon('','','')

def save(event):
    output = get_svg()
    with open('artwork_number.txt','r') as _file_: #get number of already existing artworks
    	content = _file_.read().split('\n')
    if test_mode.get() != 1:
        with open('artwork_number.txt','w') as _file_: #raise number of artworks by 1
            _file_.write(str(int(content[0])+1))
    with open('kunstwerk'+str(int(content[0])+1)+'.svg','w') as _file_: #write svg
    	_file_.write(output)
    	_file_.close()

def save_previous(event): #prints previous drawing on console for manual saving
    print(prev_drawing) #prev_drawing is defined at end of code as previous drawing

def get_svg(): #format svg data from svg variable into proper output string
    docinfo = '<svg width="'+str(canvas_width)+'px" height="'+str(canvas_height)+'px" docname="svgoutput.svg">'
    content = '\n<g>'+svg+'\n</g>'
    output = docinfo+content+'\n</svg>'
    return output

def collect_output(output, overwrite): #called at end of each basic shape to set output
    global svg
    if overwrite == 'overwrite':
        svg = output
    else:
        svg = svg + output

def delete_canvas(event): #event is given when bound keyboard key is pressed
    global prev_drawing
    prev_drawing = get_svg() #save what is on screen in prev_drawing
    canvas.delete('all')
    canvas.configure(bg='white')
    collect_output(default_background, 'overwrite')

def get_color():
	#color_mode = 1
	#https://matplotlib.org/stable/gallery/color/named_colors.html
	#'gold' 'cyan' 'dodgerblue' 'royalblue' 'orange' 'deeppink' 'darkviolet'
	if baldessari_mode.get() == 1:
		#baldessari_colors = ['red', 'yellow', 'limegreen', 'dodgerblue']
		colors = ['#ff0000', '#ffff00', '#32cd32', '#1e90ff']
		color = colors[rn.randint(0,len(colors)-1)]
	elif base_mode.get() == 1:
		#base_colors = ['red','yellow','lime','blue']
		colors = ['#ff0000', '#ffff00', '#00ff00', '#0000ff']
		color = colors[rn.randint(0,len(colors)-1)]
	elif piet_mode.get() == 1:
		colors = ['#FFFFFF', '#000000', '#FFC0C0', '#FFFFC0', '#C0FFC0', '#C0FFFF', '#C0C0FF', '#FFC0FF', '#FF0000', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#FF00FF', '#C00000', '#C0C000', '#00C000', '#00C0C0', '#0000C0', '#C000C0']
		color = colors[rn.randint(0,len(colors)-1)]
	elif grayscale_mode.get() == 1:
		gray = rn.randint(0,255)
		color = '#'+str(hex(gray).lstrip('0x'))+str(hex(gray).lstrip('0x'))+str(hex(gray).lstrip('0x'))
	elif custom_mode.get() == 1:
		colors = []
		if b_color1['bg'] != '#000001':
			colors.append(b_color1['bg'])
		if b_color2['bg'] != '#000001':
			colors.append(b_color2['bg'])
		if b_color3['bg'] != '#000001':
			colors.append(b_color3['bg'])
		if b_color4['bg'] != '#000001':
			colors.append(b_color4['bg'])
		if b_color5['bg'] != '#000001':
			colors.append(b_color5['bg'])
		color = colors[rn.randint(0,len(colors)-1)] if len(colors)>0 else '#ffffff'
	else: #random color
		color = '#'+hex(rn.randint(0,16777215)).lstrip('0x')
	if len(color) < 7:
		color = '#ffffff' if rn.randint(0,1) == 0 else '#000000'
	return color

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

def is_color(_input_):
    try:
        split_input = _input_.split('#') #returns array ['', 'abcdef']
        test_object = int(split_input[1],16)
        if test_object >= 0 and test_object <= 16777215:
            return True
        else:
            return False
    except:
        return False

def get_coordinates(n): #return n number of coordinate pairs
    border = int(e_border.get())
    coordinates = []
    for i in range(n):
        x, y = round(rn.randint(border, canvas_width-border), 2), round(rn.randint(border, canvas_height-border), 2)
        coordinates.append(x)
        coordinates.append(y)
    return coordinates

def sort_coordinates(coordinates): #used in rectangle and ellipse to get correct width and height
    x1,y1,x2,y2 = coordinates[0], coordinates[1], coordinates[2], coordinates[3]
    if x1 > x2: #sort coordinates
            x2, x1 = coordinates[0], coordinates[2]
    if y1 > y2:
            y2, y1 = coordinates[1], coordinates[3]
    return x1,y1,x2,y2

def draw_color(color): #draw full screen of one color as background
    global prev_drawing
    prev_drawing = get_svg()
    canvas.delete('all')
    color = color if is_color(color) else get_color()
    canvas.create_rectangle(0,0,canvas_width,canvas_height, fill=color, outline='')
    output = '\n<rect x="0" y="0" width="'+str(canvas_width)+'" height="'+str(canvas_height)+'" fill="'+color+'" stroke="none"/>'
    collect_output(output, 'overwrite')

def draw_gradient(color1,color2):
	global prev_drawing
	prev_drawing = get_svg()
	canvas.delete('all')
	orientation = rn.randint(0,0)
	test_mode = 1 #testing
	if orientation == 0: #horizontal gradient
		gradient = get_gradient(color1,color2,canvas_height)
		for i in range(0,len(gradient),3):
			coords = [0,i,canvas_width,i]
			draw_line(coords,gradient[i],3)
	else: #vertical gradient
		gradient = get_gradient(color1,color2,canvas_width)
	#save('') #testing
	#at the end erase svg memory from all lines and insert one rectangle with gradient fill
	#svg = '<defs>\n  <linearGradient\n    <stop offset=0/>\n  </linearGradient>\n</defs>'

def draw_rectangle(coordinates, color, mode): #inputs can be left blank to get random values
    coordinates = coordinates if len(coordinates) == 4 else get_coordinates(2) #if no coordinates are given, get random ones
    x1, y1, x2, y2 = sort_coordinates(coordinates)
    width = round(x2-x1,2) #width for svg output
    height = round(y2-y1,2) #height for svg output
    color = color if is_color(color) else get_color()
    modes = ['filled','outline']
    mode = mode if mode in modes else modes[rn.randint(0,len(modes)-1)]
    if mode == 'filled': #filled
        canvas.create_rectangle(coordinates, fill=color, outline='')
        output = '\n<rect x="'+str(x1)+'" y="'+str(y1)+'" width="'+str(width)+'" height="'+str(height)+'" fill="'+color+'" stroke="none"/>'
    else: #outlined
    	stroke_width = round(width*0.01*rn.randint(4,6), 0)
    	canvas.create_rectangle(coordinates, outline=color, width=stroke_width)
    	output = '\n<rect x="'+str(x1)+'" y="'+str(y1)+'" width="'+str(width)+'" height="'+str(height)+'" fill="none" stroke="'+color+'" stroke-width="'+str(stroke_width)+'"/>'
    collect_output(output,'')

def draw_line(coordinates, color, width): #straight line with start and end point
    coordinates = coordinates if len(coordinates) == 4 else get_coordinates(2)
    color = color if is_color(color) else get_color()
    width = round(canvas_width*0.02, 2) if width == '' else width
    canvas.create_line(coordinates, fill=color, width=width, capstyle='projecting')
    output = '\n<line x1="'+str(coordinates[0])+'" y1="'+str(coordinates[1])+'" x2="'+str(coordinates[2])+'" y2="'+str(coordinates[3])+'" stroke="'+color+'" stroke-width="'+str(width)+'"  stroke-linecap="square"/>'
    collect_output(output,'')

def draw_ellipse(coordinates, color, mode):
    coordinates = coordinates if len(coordinates) == 4 else get_coordinates(2) #if no coordinates are given, get random ones
    x1, y1, x2, y2 = sort_coordinates(coordinates)
    cx, cy = (x1+x2)*0.5, (y1+y2)*0.5  #for svg output
    rx, ry = (x2-x1)*0.5, (y2-y1)*0.5
    color = color if is_color(color) else get_color()
    if mode == 'filled':
        __mode__ = 0
    elif mode == 'outline':
        __mode__ = 1
    else:
        __mode__ = rn.randint(0,1)
    if __mode__ == 0: #filled
        canvas.create_oval(coordinates, fill=color, outline='')
        output = '\n<ellipse cx="'+str(cx)+'" cy="'+str(cy)+'" rx="'+str(rx)+'" ry="'+str(ry)+'" fill="'+color+'" stroke="none"/>'
    else: #outlined
    	stroke_width = round(rx*2*0.01*rn.randint(4,6), 2)
    	canvas.create_oval(coordinates, outline=color, width=stroke_width)
    	output = '\n<ellipse cx="'+str(cx)+'" cy="'+str(cy)+'" rx="'+str(rx)+'" ry="'+str(ry)+'" fill="none" stroke="'+color+'" stroke-width="'+str(stroke_width)+'"/>'
    collect_output(output,'')

def draw_polyline(coordinates, color, width): #path with multiple points
    length = rn.randint(4,8)
    coordinates = coordinates if len(coordinates) != 0 and len(coordinates)%2 == 0 else get_coordinates(length)
    color = color if is_color(color) else get_color()
    stroke_width = round(canvas_width*0.02, 2) if width == '' else width
    canvas.create_line(coordinates, fill=color, width=stroke_width, joinstyle='miter', capstyle='projecting')
    text_coordinates = str(coordinates[0])+' '+str(coordinates[1])
    for i in range(1,int(len(coordinates)*0.5)):
        text_coordinates = text_coordinates +' '+str(coordinates[2*i])+' '+str(coordinates[2*i+1])
    output = '\n<polyline points="'+text_coordinates+'" stroke="'+color+'" stroke-width="'+str(stroke_width)+'" stroke-linecap="square" stroke-linejoin="miter" fill="none"/>'
    collect_output(output,'')

def draw_polygon(coordinates, color, mode): #mode can also be number, to set outline width
    coordinates = coordinates if coordinates != '' else get_coordinates(rn.randint(3,5)) #if no coordinates are given, get random ones
    output = '\n<polygon points="' #svg output
    for i in range(len(coordinates)): #add coordinates to svg output
        output = output + str(coordinates[i])+' '
    color = color if is_color(color) else get_color()
    modes = ['filled','outline']
    mode = modes[rn.randint(0,len(modes)-1)] if mode == '' else mode
    if mode == 'filled': #filled
        canvas.create_polygon(coordinates, fill=color, outline='', joinstyle='miter')
        output = output + '" fill="'+color+'" stroke="none" stroke-linecap="butt" stroke-linejoin="miter"/>'
    else: #outline
        try:
            stroke_width = int(mode) #check if a number is given
        except: #else set random width
            stroke_width = round(rn.randint(10,30))
        canvas.create_polygon(coordinates, fill='', outline=color, width=stroke_width, joinstyle='miter')
        output = output + '" fill="none" stroke="'+color+'" stroke-width="'+str(stroke_width)+'" stroke-linecap="butt" stroke-linejoin="miter stroke-miterlimit:12"/>'
    collect_output(output,'')

def draw_comic(event): #polygon with shadow
    coordinates = get_coordinates(rn.randint(5,10))
    offset = rn.randint(4,19)
    shadow_coordinates = []
    for i in coordinates:
        shadow_coordinates.append(i+offset)
    color = get_color()
    draw_polygon(shadow_coordinates, '#000000', 'filled')
    draw_polygon(coordinates, color, 'filled')

def draw_blacknwhite(event):
    if rn.randint(0,1) == 0:
        draw_color('#ffffff')
    else:
        draw_color('#000000')
    amount = rn.randint(3,12)
    for i in range(amount):
        if rn.randint(0,1) == 0:
            draw_polygon('', '#ffffff', '')
        else:
            draw_polygon('', '#000000', '')

def draw_monocolor(event): #random amount of shapes and background using just two colors
    bg = get_color()
    draw_color(bg)
    color = get_color()
    amount = rn.randint(3,12)
    for i in range(amount):
        if rn.randint(0,1) == 0:
            draw_polygon('', color, '')
        else:
            draw_polygon('', bg, '')

def draw_threecolors(event): #random amount of shapes and background using just three colors
    bg = get_color()
    draw_color(bg)
    color1 = get_color()
    color2 = get_color()
    amount = rn.randint(3,12)
    draw_polygon('', color1, '') #have at least one polygon of each color
    draw_polygon('', color2, '')
    for i in range(amount-2):
        if rn.randint(0,2) == 0:
            draw_polygon('', color1, '')
        elif rn.randint(0,2) == 0:
            draw_polygon('', color2, '')
        else:
            draw_polygon('', bg, '')

def draw_radial(event): #orb shape
    revolutions = rn.randint(3,9) #how many time to go around
    resolution = rn.randint(5,20) #how many points per revolution
    border = int(e_border.get())
    r_min = rn.randint(int((canvas_height-2*border)*0.5*0.04), int((canvas_height-2*border)*0.5*0.4))
    r_max = rn.randint(int((canvas_height-2*border)*0.5*0.6), int((canvas_height-2*border)*0.5))
    coordinates = []
    angle_offset = rn.randint(0,360)
    for i in range(revolutions):
        for j in range(resolution):
            percentage = (i+j/resolution)/revolutions #[0,1]
            #print(percentage)
            r = (r_min+(r_max-r_min)*math.sin(percentage*math.pi))*rn.randint(93,107)*0.01
            phi = j*(360/resolution)+angle_offset
            x = int(round(canvas_width*0.5+math.cos(phi/180*math.pi)*r, 0))
            y = int(round(canvas_height*0.5+math.sin(phi/180*math.pi)*r, 0))
            coordinates.append(x)
            coordinates.append(y)
    color = get_color()
    width = (r_max-r_min)*rn.randint(3,10)*0.01
    canvas.create_polygon(coordinates, fill='', outline=color, width=width)
    output = '\n<polygon points="'
    for i in coordinates: #add coordinates to output
        output = output + str(i)+' '
    output = output + '" fill="none" stroke="'+color+'" stroke-width="'+str(width)+'" stroke-linecap="butt" stroke-linejoin="miter"/>'
    #l_output['text'] = l_output['text'] + output
    collect_output(output,'')

def draw_paper(event):
    draw_color(get_color()) #background
    amount = rn.randint(5,12) #how many paper shapes
    overlap = 5 #amount of pixels outside of the canvas size
    outside_length = (canvas_width+2*overlap)*2+(canvas_height+2*overlap)*2 #ring of the outer paper sheet coordinates, clockwise
    outside_points = []
    for i in range(amount*2): #append outer ring coordinates, two for each paper shape
            outside_points.append(rn.randint(0,outside_length))
    inside_coordinates = get_coordinates(amount)
    area1 = canvas_width+2*overlap
    area2 = canvas_width+canvas_height+4*overlap
    area3 = 2*canvas_width+canvas_height+6*overlap
    for i in range(amount):
        if outside_points[2*i] < area1: #check if first point of paper shape is in top area
            x1 = -overlap+outside_points[2*i]
            y1 = -overlap
        elif outside_points[2*i] < area2: #right area
            x1 = canvas_width+overlap
            y1 = -overlap+outside_points[2*i]-area1
        elif outside_points[2*i] < area3: #bottom area
            x1 = -outside_points[2*i]+area2+area1
            y1 = canvas_height+overlap
        else: #left area
            x1 = -overlap
            y1 = -outside_points[2*i]+area3+area2
        if outside_points[2*i+1] < area1: #check if second point of paper shape is in top area
            x2 = -overlap+outside_points[2*i+1]
            y2 = -overlap
        elif outside_points[2*i+1] < area2: #right area
            x2 = canvas_width+overlap
            y2 = outside_points[2*i+1]-area1
        elif outside_points[2*i+1] < area3: #bottom area
            x2 = -outside_points[2*i+1]+area2+area1
            y2 = canvas_height+overlap
        else: #left area
            x2 = -overlap
            y2 = canvas_height+2*canvas_width+6*overlap+outside_points[2*i]-area3
        x3, y3 = inside_coordinates[2*i], inside_coordinates[2*i+1]
        color = get_color()
        coordinates = [x1,y1,x2,y2,x3,y3]
        draw_polygon(coordinates, color, 'filled')

def draw_pixels(event):
    border = int(e_border.get())
    bg_color = get_color()
    draw_color(bg_color)
    colors = [get_color(),get_color()]
    pixels = rn.randint(5,42)
    mode = rn.randint(0,2) #mode 0: random colors, mode 1: fg and bg colors, mode 2: two fg colors
    if mode == 1:
        colors = [bg_color, get_color()]
    elif mode == 2:
        colors = [bg_color, get_color(), get_color()]
    for j in range(pixels): #lines of pixels
        for i in range(pixels): #columns of pixels
            coordinates = []
            x1 = round(border + i*(canvas_width-2*border)/pixels,2)
            y1 = round(border + j*(canvas_height-2*border)/pixels,2)
            x2 = round(x1 + (canvas_width-2*border)/pixels,2)
            y2 = round(y1 + (canvas_height-2*border)/pixels,2)
            coordinates.append(x1)
            coordinates.append(y1)
            coordinates.append(x2)
            coordinates.append(y2)
            if mode == 0:
                draw_rectangle(coordinates, get_color(), 'filled')
            else:
                draw_rectangle(coordinates, colors[rn.randint(0,len(colors)-1)], 'filled')

def draw_symmetry(event):
    amount = rn.randint(3,9)
    coordinates = get_coordinates(amount)
##    for i in range(amount): #put all x coordinates to the left side of canvas
##        dist = abs(canvas_width*0.5-coordinates[2*i])
##        coordinates[2*i] = canvas_width*0.5-dist
    mirrored_coordinates = []
    for i in range(amount): #create mirrored coordinates
##        dist = abs(canvas_width*0.5-coordinates[2*i])
        dist = -(coordinates[2*i]-canvas_width*0.5)
        mirrored_coordinates.append(canvas_width*0.5+dist) #mirror x coordinate
        mirrored_coordinates.append(coordinates[2*i+1])
    color = get_color()
    if rn.randint(0,0) == 0:
        mode = 'filled'
    else:
        mode = 'outline'
    draw_polygon(coordinates, color, mode)
    draw_polygon(mirrored_coordinates, color, mode)

def draw_triangle(event,color):
    coordinates = get_coordinates(3)
    draw_polygon(coordinates, color, '')

def draw_spectrum(event):
    points = rn.randint(4,8)
    number_of_lines = rn.randint(points*2,points*3)*1
    divisions = 18+rn.randint(-4,4)#12+rn.randint(-2,2) #number of points in each line
    height_variety = int(round(200/number_of_lines,0))
    width = 100/number_of_lines+rn.randint(int(-50/number_of_lines),int(50/number_of_lines)) #line width
    draw_color('') #background
    linecolor = get_color()
    offset_table = [] #saves all offsets for each point in each line
    coordinates = []
    border = int(e_border.get())
    if rn.randint(0,1) == 0: #horizontal
        x_step = (canvas_width-2*border)/divisions
        for j in range(divisions+1): #first line
            offset = rn.randint(-height_variety,height_variety)*2
            offset_table.append(offset)
            x, y = border+j*x_step, border+offset*math.sin(0/number_of_lines*math.pi)
            coordinates.append(x)
            coordinates.append(y)
        draw_polyline(coordinates, linecolor, width)
        for i in range(1,number_of_lines+1): #following lines
            coordinates = []
            y_height = i*(canvas_height-2*border)/number_of_lines
            for j in range(divisions+1):
                offset = offset_table[len(offset_table)-1-divisions]+rn.randint(-height_variety,height_variety)*1
                offset_table.append(offset)
                x, y = border+j*x_step, border+y_height+offset*math.sin(i/number_of_lines*math.pi)*math.sin(j/divisions*math.pi)
                coordinates.append(x)
                coordinates.append(y)
            draw_polyline(coordinates, linecolor, width)
    else: #vertical
        y_step = (canvas_height-2*border)/divisions
        for j in range(divisions+1): #first line
            offset = rn.randint(-height_variety,height_variety)*2
            offset_table.append(offset)
            x, y = border+offset*math.sin(0/number_of_lines*math.pi), border+j*y_step
            coordinates.append(x)
            coordinates.append(y)
        draw_polyline(coordinates, linecolor, width)
        for i in range(1,number_of_lines+1): #following lines
            coordinates = []
            x_height = i*(canvas_width-2*border)/number_of_lines
            for j in range(divisions+1):
                offset = offset_table[len(offset_table)-1-divisions]+rn.randint(-height_variety,height_variety)*1
                offset_table.append(offset)
                x, y = border+x_height+offset*math.sin(i/number_of_lines*math.pi)*math.sin(j/divisions*math.pi), border+j*y_step
                coordinates.append(x)
                coordinates.append(y)
            draw_polyline(coordinates, linecolor, width)

def draw_colorwall(event):
    amount = rn.randint(3,10) #number of lines
    height_variety = 600/amount#400/amount
    walltype = rn.randint(0,1) #random or gradient colors
    colors = []
    if walltype == 0: #random colors
        bg = get_color()
        colors.append(bg)
        for i in range(amount):
        	colors.append(get_color())
    else: #gradient colors
        color1 = get_color()
        color2 = get_color()
        colors = get_gradient(color1,color2,amount+1)
    draw_color(colors[0])
    x_left, x_right = -1, canvas_width+1 #bottom coordinates overhanging canvas, shared by all polygons
    y_bottom = canvas_height+1
    for i in range(amount):
        coordinates = [x_right,y_bottom,x_left,y_bottom]
        y_line = (i+0.5)*(canvas_height/(amount))
        coordinates.append(x_left)
        coordinates.append(y_line)
        for j in range(6):
            x_new = x_left+(j+1)*(canvas_width/5.5)
            y_new = y_line+rn.randint(int(-height_variety),int(height_variety))
            coordinates.append(x_new)
            coordinates.append(y_new)
        coordinates.append(x_right) #top right corner of polygon
        coordinates.append(y_line)
        draw_polygon(coordinates, colors[i+1], 'filled')

def draw_pattern(event):
    border = int(e_border.get())
    bgtype = rn.randint(1,2)
    if bgtype == 0:
        draw_gradient('')
    elif bgtype == 1:
        draw_patch('')
    else:
        draw_color('')
    pattern_amount_x = rn.randint(5,15) #how many pattern elements are drawn per line
    pattern_amount_y = int(round(pattern_amount_x*(canvas_height/canvas_width),0))
    pattern_width = (canvas_width-2*border)/pattern_amount_x #pixel size of each tile
    line_width = 195/pattern_amount_x #line_width = 95/pattern_amount_x*rn.randint(90,110)*0.01
    color = get_color()
    pattern_nr = rn.randint(6,6) #which pattern to draw
    if pattern_nr == 0: #slash pattern
        for i in range(pattern_amount_y):
            for j in range(pattern_amount_x):
                if rn.randint(0,1) == 0:
                    x1, y1 = border+pattern_width*j, border+pattern_width*i
                    x2, y2 = border+pattern_width*(j+1), border+pattern_width*(i+1)
                else:
                    x1, y1 = border+pattern_width*(j+1), border+pattern_width*i
                    x2, y2 = border+pattern_width*j, border+pattern_width*(i+1)
                #canvas.create_line(x1,y1,x2,y2,fill=color,width=line_width,capstyle='round')
                coordinates = [x1,y1,x2,y2]
                draw_line(coordinates, color, line_width)
##    elif pattern_nr == 1 or pattern_nr == 2: #rounded pattern
##        for i in range(pattern_amount_y):
##            for j in range(pattern_amount_x):
##                if pattern_nr == 1:
##                	tile_type = rn.randint(0,1)
##                else:
##                	tile_type = rn.randint(2,3)
##                if tile_type == 0: #tile 1 (more pointy)
##                    x1_1, y1_1 = border+pattern_width*j, border+pattern_width*i+pattern_width*0.5
##                    x2_1, y2_1 = border+pattern_width*j+pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*i+pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_1, y3_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i
##                    x1_2, y1_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)
##                    x2_2, y2_2 = border+pattern_width*(j+1)-pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*(i+1)-pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_2, y3_2 = border+pattern_width*(j+1), border+pattern_width*i+pattern_width*0.5
##                elif tile_type == 1: #tile 2 (more pointy)
##                    x1_1, y1_1 = border+pattern_width*(j+1), border+pattern_width*i+pattern_width*0.5
##                    x2_1, y2_1 = border+pattern_width*(j+1)-pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*i+pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_1, y3_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i
##                    x1_2, y1_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)
##                    x2_2, y2_2 = border+pattern_width*j+pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*(i+1)-pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_2, y3_2 = border+pattern_width*j, border+pattern_width*i+pattern_width*0.5
##                elif tile_type == 2: #tile 3 (fully round)
##                    x1_1, y1_1 = border+pattern_width*j, border+pattern_width*i+pattern_width*0.5
##                    x2_1, y2_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i+pattern_width*0.5
##                    x3_1, y3_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i
##                    x1_2, y1_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)
##                    x2_2, y2_2 = border+pattern_width*(j+1)-pattern_width*0.5, border+pattern_width*(i+1)-pattern_width*0.5
##                    x3_2, y3_2 = border+pattern_width*(j+1), border+pattern_width*i+pattern_width*0.5
##                elif tile_type == 3: #tile 4 (fully round)
##                    x1_1, y1_1 = border+pattern_width*(j+1), border+pattern_width*i+pattern_width*0.5
##                    x2_1, y2_1 = border+pattern_width*(j+1)-pattern_width*0.5, border+pattern_width*i+pattern_width*0.5
##                    x3_1, y3_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i
##                    x1_2, y1_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)
##                    x2_2, y2_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)-pattern_width*0.5
##                    x3_2, y3_2 = border+pattern_width*j, border+pattern_width*i+pattern_width*0.5
##                else: #old tile
##                    x1_1, y1_1 = border+pattern_width*(j+1), border+pattern_width*i+pattern_width*0.5
##                    x2_1, y2_1 = border+pattern_width*j+pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*i+pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_1, y3_1 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*i
##                    x1_2, y1_2 = border+pattern_width*j+pattern_width*0.5, border+pattern_width*(i+1)
##                    x2_2, y2_2 = border+pattern_width*(j+1)-pattern_width*0.5*math.sin(math.pi*0.25), border+pattern_width*(i+1)-pattern_width*0.5*math.cos(math.pi*0.25)
##                    x3_2, y3_2 = border+pattern_width*j, border+pattern_width*i+pattern_width*0.5
##                if pattern_nr == 1 or pattern_nr == 2:
##                	canvas.create_line(x1_1,y1_1,x2_1,y2_1,x3_1,y3_1,fill=color,width=line_width,capstyle='round',smooth=1)
##                	canvas.create_line(x1_2,y1_2,x2_2,y2_2,x3_2,y3_2,fill=color,width=line_width,capstyle='round',smooth=1)
    elif pattern_nr == 3: #bar pattern
        bar_type = rn.randint(0,1)
        for i in range(pattern_amount_y):
            for j in range(pattern_amount_x):
                tile_type = rn.randint(0,1)
                if tile_type == 0: #horizontal bar
                    x1, y1 = border+pattern_width*(j+0.05), border+pattern_width*(i+0.05)
                    x2, y2 = border+pattern_width*(j+0.95), border+pattern_width*(i+0.45)
                    x3, y3 = border+pattern_width*(j+0.05), border+pattern_width*(i+0.55)
                    x4, y4 = border+pattern_width*(j+0.95), border+pattern_width*(i+0.95)
                else: #vertical bar
                    x1, y1 = border+pattern_width*(j+0.05), border+pattern_width*(i+0.05)
                    x2, y2 = border+pattern_width*(j+0.45), border+pattern_width*(i+0.95)
                    x3, y3 = border+pattern_width*(j+0.55), border+pattern_width*(i+0.05)
                    x4, y4 = border+pattern_width*(j+0.95), border+pattern_width*(i+0.95)
                if bar_type == 0:
                    coordinates1 = [x1,y1,x2,y2]
                    draw_rectangle(coordinates1, color, 'filled')
                    coordinates2 = [x3,y3,x4,y4]
                    draw_rectangle(coordinates2, color, 'filled')
                else:
                    coordinates1 = [x1,y1,x2,y2]
                    draw_rectangle(coordinates1, color, '')
                    coordinates2 = [x3,y3,x4,y4]
                    draw_rectangle(coordinates2, color, '')
    elif pattern_nr == 4: #L-pattern
        for i in range(pattern_amount_y):
            for j in range(pattern_amount_x):
                orientation = rn.randint(1,4)
                x_offset = border + j*pattern_width
                y_offset = border + i*pattern_width
                if orientation == 1: #|'
                    x1, y1 = x_offset + 0.25*pattern_width, y_offset + 0.75*pattern_width
                    x2, y2 = x_offset + 0.25*pattern_width, y_offset + 0.25*pattern_width
                    x3, y3 = x_offset + 0.75*pattern_width, y_offset + 0.25*pattern_width
                elif orientation == 2: #'|
                    x1, y1 = x_offset + 0.25*pattern_width, y_offset + 0.25*pattern_width
                    x2, y2 = x_offset + 0.75*pattern_width, y_offset + 0.25*pattern_width
                    x3, y3 = x_offset + 0.75*pattern_width, y_offset + 0.75*pattern_width
                elif orientation == 3: #|_
                    x1, y1 = x_offset + 0.25*pattern_width, y_offset + 0.25*pattern_width
                    x2, y2 = x_offset + 0.25*pattern_width, y_offset + 0.75*pattern_width
                    x3, y3 = x_offset + 0.75*pattern_width, y_offset + 0.75*pattern_width
                else: #_|
                    x1, y1 = x_offset + 0.25*pattern_width, y_offset + 0.75*pattern_width
                    x2, y2 = x_offset + 0.75*pattern_width, y_offset + 0.75*pattern_width
                    x3, y3 = x_offset + 0.75*pattern_width, y_offset + 0.25*pattern_width
                coordinates = [x1,y1,x2,y2,x3,y3]
                width = pattern_width*0.45
                draw_polyline(coordinates, color, width)
    elif pattern_nr == 5: #t-pattern
        for i in range(pattern_amount_y):
            for j in range(pattern_amount_x):
                tile_type = rn.randint(1,4)
                if tile_type == 1: #-'-
                    x1, y1 = border+pattern_width*(j+0.15), border+pattern_width*(i+0.5)
                    x2, y2 = border+pattern_width*(j+0.85), border+pattern_width*(i+0.5)
                    x3, y3 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.15)
                    x4, y4 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.5)
                elif tile_type == 2: #-,-
                    x1, y1 = border+pattern_width*(j+0.15), border+pattern_width*(i+0.5)
                    x2, y2 = border+pattern_width*(j+0.85), border+pattern_width*(i+0.5)
                    x3, y3 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.5)
                    x4, y4 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.85)
                elif tile_type == 3: #|-
                    x1, y1 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.15)
                    x2, y2 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.85)
                    x3, y3 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.5)
                    x4, y4 = border+pattern_width*(j+0.85), border+pattern_width*(i+0.5)
                else: #-|
                    x1, y1 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.15)
                    x2, y2 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.85)
                    x3, y3 = border+pattern_width*(j+0.15), border+pattern_width*(i+0.5)
                    x4, y4 = border+pattern_width*(j+0.5), border+pattern_width*(i+0.5)
                coordinates1 = [x1,y1,x2,y2]
                draw_line(coordinates1, color, line_width)
                coordinates2 = [x3,y3,x4,y4]
                draw_line(coordinates2, color, line_width)
    else: #random pattern 1
        amount = rn.randint(1,6)
        width = line_width*0.4/(0.5*amount)
        og_coords = []
        measurements = []
        x_midpoint = border+pattern_width*0.5
        y_midpoint = x_midpoint
        for i in range(amount):
            x1, y1 = rn.randint(border,int(border+pattern_width)), rn.randint(border,int(border+pattern_width))
            x2, y2 = rn.randint(border,int(border+pattern_width)), rn.randint(border,int(border+pattern_width))
            og_coords.append(x1)
            og_coords.append(y1)
            og_coords.append(x2)
            og_coords.append(y2)
            #new rotation part
            angle1 = math.atan((y_midpoint-y1)/(x1-x_midpoint))
            angle2 = math.atan((y_midpoint-y2)/(x2-x_midpoint))
            measurements.append(angle1)
            measurements.append(angle2)
            d1 = math.sqrt((x1-x_midpoint)**2+(y1-y_midpoint)**2)
            d2 = math.sqrt((x2-x_midpoint)**2+(y2-y_midpoint)**2)
            measurements.append(d1)
            measurements.append(d2)
        color = get_color()
        for i in range(pattern_amount_y):
            for j in range(pattern_amount_x):
                rotation = rn.randint(0,3) #how many pi/2 times to rotate current tile
                for k in range(amount):
                    x1 = og_coords[4*k]+j*pattern_width+math.cos(measurements[4*k]+rotation*math.pi)*measurements[4*k+2]
                    y1 = og_coords[4*k+1]+i*pattern_width+math.sin(measurements[4*k]+rotation*math.pi)*measurements[4*k+2]
                    x2 = og_coords[4*k+2]+j*pattern_width+math.cos(measurements[4*k+1]+rotation*math.pi)*measurements[4*k+3]
                    y2 = og_coords[4*k+3]+i*pattern_width+math.sin(measurements[4*k+1]+rotation*math.pi)*measurements[4*k+3]
                    coords = [x1, y1, x2, y2]
                    draw_line(coords, color, width)

def draw_mandala(event):
    amount = rn.randint(7,13) #how many objects to draw
    length = rn.randint(3,7) #how many points for the object
    coordinates = get_coordinates(length)
    sizes = [] #array with size and angle for each original point
    for i in range(length):
        gk = coordinates[2*i+1]-canvas_height*0.5
        ak = coordinates[2*i]-canvas_width*0.5
        try:
            angle = math.atan(gk/ak)
        except: #error when ak=0 
            angle = 90
        size = math.sqrt(gk**2+ak**2)
        sizes.append([size, angle])
    color = get_color()
    width = 1/(amount*amount*0.001)
    _type_ = rn.randint(0,1)
    for i in range(0, amount):
        for j in range(length):
            angle = sizes[j][1] + i*2*math.pi/amount
            coordinates[2*j] = round(canvas_width*0.5 + math.cos(angle)*sizes[j][0], 2)
            coordinates[2*j+1] = round(canvas_height*0.5 + math.sin(angle)*sizes[j][0], 2)
        if _type_ == 0:
            draw_polyline(coordinates, color, width)
        else:
            draw_polygon(coordinates, color, 'filled')

def draw_colorline(event):
    amount = rn.randint(3,9)
    coordinates = get_coordinates(amount)
    width = rn.randint(10,30)
    draw_polyline(coordinates, get_color(), width*2)
    draw_polyline(coordinates, get_color(), width*1.5)
    draw_polyline(coordinates, get_color(), width)

def draw_colorpolygon(event):
    amount = rn.randint(3,5)
    coordinates = get_coordinates(amount)
    width = rn.randint(10,30)
    draw_polygon(coordinates, get_color(), width*2)
    draw_polygon(coordinates, get_color(), width)
    draw_polygon(coordinates, get_color(), 'filled')

def draw_threedee(event):
    offset = rn.randint(8,14)
    amount = rn.randint(3,9)
    coordinates = get_coordinates(amount)
    cyan_coordinates = coordinates
    red_coordinates = coordinates
    for i in range(amount):
        cyan_coordinates[2*i] = cyan_coordinates[2*i]+offset
        red_coordinates[2*i] = red_coordinates[2*i]-offset
    draw_polygon(cyan_coordinates, '#00ffff', 'filled')
    draw_polygon(red_coordinates, '#ff0000', 'filled')
    draw_polygon(coordinates, '#000000', 'filled')

def draw_voronoi(event): #NOT FINISHED
    coords = get_coordinates(2) #get points p1 and p2
    draw_line(coords,'#000000',4) #draw line from p1 to p2
    distance = math.sqrt((coords[3]-coords[1])**2+(coords[2]-coords[0])**2) #calc distance from p2 to p1
    angle = math.atan((coords[3]-coords[1])/(coords[2]-coords[0])) #calc angle between line and horizontal
    #print(angle*180/math.pi)
    xintersect = coords[0]+math.cos(angle)*distance*0.5 #calc halfway point between points
    yintersect = coords[1]+math.sin(angle)*distance*0.5
    coords2 = [coords[0],coords[1],xintersect,yintersect] #new coords for line from p1 to halfway point
    draw_line(coords2,'#ff0000',4) #draw new coords line
    canvas.create_oval(coords[0]-distance*0.5,coords[1]-distance*0.5,coords[0]+distance*0.5,coords[1]+distance*0.5) #draw circle with halfway radius

def draw_perspective(event):
	draw_color('')
	ybuffer = int(canvas_height*0.2) #so the focal point is not on the edge of the image
	point = [rn.randint(0,canvas_width), rn.randint(0+ybuffer,canvas_height)-ybuffer]
	if rn.randint(0,1) == 1: #option to draw walls in different color
		wall_color = get_color()
		coords = [0,0,point[0],point[1],0,canvas_height] #wall left
		draw_polygon(coords, wall_color, 'filled')
		coords = [canvas_width,0,point[0],point[1],canvas_width,canvas_height] #wall right
		draw_polygon(coords, wall_color, 'filled')
		coords = [0,canvas_height,point[0],point[1],canvas_width,canvas_height] #floor
		draw_polygon(coords, get_color(), 'filled')
		coords = [0,0,point[0],point[1],canvas_width,0] #ceiling
		draw_polygon(coords, get_color(), 'filled')
	line_color = '#000000' #get_color()
	coords = [0,0, point[0], point[1]]
	draw_line(coords, line_color, 3)
	coords = [canvas_width,0, point[0], point[1]]
	draw_line(coords, line_color, 3)
	coords = [0,canvas_height, point[0], point[1]]
	draw_line(coords, line_color, 3)
	coords = [canvas_width,canvas_height, point[0], point[1]]
	draw_line(coords, line_color, 3)

def draw_patch(event): #background with three colors
	draw_color('')
	for i in range(2): #amount of shapes to draw
		edge1 = rn.randint(1,3)
		edge2 = rn.randint(edge1+1,4)
		if edge1 == 1 and edge2 == 2:
			coordinates = [rn.randint(0,canvas_width),0,canvas_width,rn.randint(0,canvas_height),canvas_width,0]
		elif edge1 == 1 and edge2 == 3:
			if rn.randint(0,1) == 0:
				coordinates = [rn.randint(0,canvas_width),0,0,0,0,canvas_height,rn.randint(0,canvas_width),canvas_height]
			else:
				coordinates = [rn.randint(0,canvas_width),0,canvas_width,0,canvas_width,canvas_height,rn.randint(0,canvas_width),canvas_height]
		elif edge1 == 1 and edge2 == 4:
			coordinates = [rn.randint(0,canvas_width),0,0,rn.randint(0,canvas_height),0,0]
		elif edge1 == 2 and edge2 == 3:
			coordinates = [canvas_width,rn.randint(0,canvas_height),rn.randint(0,canvas_width),canvas_height,canvas_width,canvas_height]
		elif edge1 == 2 and edge2 == 4:
			if rn.randint(0,1) == 0:
				coordinates = [canvas_width,rn.randint(0,canvas_height),canvas_width,0,0,0,0,rn.randint(0,canvas_height)]
			else:
				coordinates = [canvas_width,rn.randint(0,canvas_height),canvas_width,canvas_height,0,canvas_height,0,rn.randint(0,canvas_height)]
		elif edge1 == 3 and edge2 == 4:
			coordinates = [rn.randint(0,canvas_width),canvas_height,0,rn.randint(0,canvas_height),0,canvas_height]
		draw_polygon(coordinates,'','filled')

def draw_bubbles(event):
	draw_color('')
	references = rn.randint(2,7)
	amount = rn.randint(20,2000)
	coordinates = get_coordinates(amount)
	colors = []
	for i in range(references):
		colors.append(get_color())
	for i in range(references,amount-1): #draw colored circles colored according to nearest reference
		canvas_factor = 10*canvas_height*(1+amount/rn.randint(700,1300))/amount
		size = int(0.5*rn.randint(int(canvas_factor*0.7),int(canvas_factor*1.3)))
		x1,y1,x2,y2 = coordinates[2*i]-size, coordinates[2*i+1]-size, coordinates[2*i]+size, coordinates[2*i+1]+size
		coords = [x1,y1,x2,y2]
		distances = []
		for j in range(references): #calculate which reference is closest
			xref,yref = coordinates[2*j], coordinates[2*j+1]
			xpoint,ypoint = coordinates[2*i], coordinates[2*i+1]
			dist = math.sqrt((xpoint-xref)**2+(ypoint-yref)**2)
			distances.append(dist)
		min = 0
		for i in range(references): #get index of lowest distance to assign according color
			if distances[i] < distances[min]:
				min = i
		draw_ellipse(coords,colors[min],'filled')
	'''for i in range(references): #draw references on top of the other circles
		size = int(canvas_height/90)
		x1,y1 = coordinates[2*i]-size, coordinates[2*i+1]-size
		x2,y2 = coordinates[2*i]+size, coordinates[2*i+1]+size
		coords = [x1,y1,x2,y2]
		draw_ellipse(coords,'#000000','filled')'''

def draw_waveform(event):
	draw_color('')
	border = int(e_border.get())
	amount = rn.randint(42,100)#7,42)
	line_color = get_color()
	width = canvas_height/(amount*2.5)*1.3
	step = (canvas_height-2*border)/amount
	'''
	for i in range(amount):
		coords = [border+rn.randint(0,step*amount),border+i*step,canvas_height-border-rn.randint(0,step*amount),border+i*step]
		draw_line(coords,line_color,width)
	'''
	space = canvas_width*0.5-border
	variance = int(space*0.3)
	left = (space)*rn.randint(40,90)/100
	right = (space)*rn.randint(40,90)/100
	for i in range(1,amount):
		coords = [canvas_width*0.5-(left+rn.randint(-variance,variance))*math.sin(math.pi*0.15+math.pi*0.7*i/amount), border+i*step, canvas_width*0.5+(right+rn.randint(-variance,variance))*math.sin(math.pi*0.15+math.pi*0.7*i/amount), border+i*step]
		draw_line(coords,line_color,width)

def draw_separation(event): #shapes that are separated by an outline of the background color
	amount = rn.randint(10,30)
	#outline = rn.randint(10,70) #width of the outline around each shape
	bg_color = get_color()
	draw_color(bg_color)
	shape_color = get_color()
	for i in range(amount):
		coords = get_coordinates(rn.randint(3,7))
		if rn.randint(0,3) == 0:
			oval = get_coordinates(2)
			draw_ellipse(oval,bg_color,'outline')
			draw_ellipse(oval,shape_color,'filled')
		else:
			draw_polygon(coords,bg_color,'outline')
			draw_polygon(coords,shape_color,'filled')

def draw_paths(event):
	draw_color('')
	border = int(e_border.get())
	line_amount = rn.randint(5,20)
	div_amount = rn.randint(5,8)
	width = 20*6/line_amount
	color = get_color()
	if rn.randint(0,1) == 0: #horizontal
		x_step = (canvas_width-2*border)/div_amount
		for i in range(line_amount):
			coords = []
			for j in range(div_amount+1):
				offset = rn.randint(-int((canvas_height-2*border)*1/line_amount),int((canvas_height-2*border)*1/line_amount))
				y = border+i*(canvas_height-2*border)/line_amount+offset
				if y < border or y > canvas_height-border:
					y = border+i*(canvas_height-2*border)/line_amount-offset
				x = border+j*x_step
				coords.append(x)
				coords.append(y)
			draw_polyline(coords, color, width)
	else: #vertical
		y_step = (canvas_height-2*border)/div_amount
		for i in range(line_amount):
			coords = []
			for j in range(div_amount+1):
				offset = rn.randint(-int((canvas_width-2*border)*1/line_amount),int((canvas_width-2*border)*1/line_amount))
				x = border+i*(canvas_width-2*border)/line_amount+offset
				if x < border or x > canvas_width-border:
					x = border+i*(canvas_width-2*border)/line_amount-offset
				y = border+j*y_step
				coords.append(x)
				coords.append(y)
			draw_polyline(coords, color, width)

def draw_fractal(event):
	draw_color('')
	border = int(e_border.get())
	x_space = canvas_width-2*border
	y_space = canvas_height-2*border
	recursion_level = -1
	max_recursion_level = rn.randint(1,5)
	coordinates = [border,border,canvas_width-border,canvas_height-border]
	shape_mode = rn.randint(0,4)
	if shape_mode == 4:
		max_recursion_level = rn.randint(1,3)
	color_mode = rn.randint(0,1)
	if color_mode == 0:
		color = get_gradient(get_color(),get_color(),max_recursion_level+1)
	else:
		c = get_color()
		color = [c]*(max_recursion_level+1)
	fractal_recursion(coordinates,recursion_level,max_recursion_level,color,shape_mode,color_mode)

def fractal_recursion(coordinates,recursion_level,max_recursion_level,color,shape_mode,color_mode):
	x_length = coordinates[2]-coordinates[0]
	y_length = coordinates[3]-coordinates[1]
	if recursion_level < max_recursion_level:
		recursion_level += 1
		for i in range(4):
			x1 = coordinates[0]+i%2*x_length/2
			x2 = x1+x_length/2
			if i%4 < 2:
				y1, y2 = coordinates[1], coordinates[1]+y_length/2
			else:
				y1, y2 = coordinates[1]+y_length/2, coordinates[3]
			new_coordinates = [x1,y1,x2,y2]
			fractal_recursion(new_coordinates,recursion_level,max_recursion_level,color,shape_mode,color_mode)
	coords = [coordinates[0]+x_length/4,coordinates[1]+y_length/4,coordinates[2]-x_length/4,coordinates[3]-y_length/4]
	if shape_mode == 0:
		draw_rectangle(coords,color[recursion_level],'outline')
	elif shape_mode == 1:
		draw_rectangle(coords,color[recursion_level],'filled')
	elif shape_mode == 2:
		draw_ellipse(coords,color[recursion_level],'outline')
	elif shape_mode == 3:
		draw_ellipse(coords,color[recursion_level],'filled')
	else:
		width = 12/(recursion_level+1)
		draw_line(coords,color[recursion_level],width)
		mirrored_coords = [coords[2],coords[1],coords[0],coords[3]]
		draw_line(mirrored_coords,color[recursion_level],width)

def draw_spray(event):
	draw_color('')
	color1,color2 = get_color(),get_color()
	amount = rn.randint(200,500)
	cutoff = amount*rn.randint(75,92)/100
	for i in range(amount):
		center = get_coordinates(1)
		radius = rn.randint(10,20)
		coords = [center[0]-radius,center[1]-radius,center[0]+radius,center[1]+radius]
		if i > cutoff:
			draw_ellipse(coords,color1,'filled') #(coordinates, color, mode):
		else:
			draw_ellipse(coords,color2,'filled')

def draw_gradient_image(event):
	draw_color('')
	amount = rn.randint(7,16) #how many shapes to draw
	gradient = get_gradient(get_color(),get_color(),amount)
#	draw_color(gradient[0])
	for i in range(amount):
		shape = rn.randint(0,1)
		if shape == 0:
			draw_triangle('',gradient[i])
		elif shape == 1:
			draw_rectangle('',gradient[i],'filled')

def draw_double_color(event):
	draw_paper('')
	bg = '#fafafa'
	border = int(e_border.get())
	offset = border/2
	draw_line([offset,offset,canvas_width-offset,offset],bg,border) #top edge of borderframe
	draw_line([offset,offset,offset,canvas_height-offset],bg,border) #left edge
	draw_line([canvas_width-offset,offset,canvas_width-offset,canvas_height-offset],bg,border) #right edge
	draw_line([offset,canvas_height-offset,canvas_width-offset,canvas_height-offset],bg,border) #bottom edge
	amount = rn.randint(2,5)
	for i in range(amount):
		coords = []
		edges = rn.randint(3,15)
		for j in range(edges):
			point = [rn.randint(0,canvas_width),rn.randint(0,canvas_height)]
			coords += point
		draw_polygon(coords,bg,'filled')
#	for i in range(amount):
#		if rn.randint(0,1) == 0:
#			coords1 = [rn.randint(0,canvas_width),0,rn.randint(0,canvas_width),canvas_height]
#			coords2 = [rn.randint(0,canvas_width),0,rn.randint(0,canvas_width),canvas_height]
#			coords = coords1+coords2
#		else:
#			coords1 = [0,rn.randint(0,canvas_height),canvas_width,rn.randint(0,canvas_height)]
#			coords2 = [0,rn.randint(0,canvas_height),canvas_width,rn.randint(0,canvas_height)]
#			coords = coords1+coords2
#		draw_polygon(coords,bg,'filled')

def draw_comet(color):
	r_min = 30
	r_max = 250
	center = get_coordinates(1)
	border = int(e_border.get())
	if center[0]-r_max < border:
		center = [center[0]+border,center[1]]
	elif center[0]+r_max > canvas_width-border:
		center = [center[0]-border,center[1]]
	if center[1]-r_max < border:
		center = [center[0],center[1]+border]
	elif center[1]+r_max > canvas_height-border:
		center = [center[0],center[1]-border]
	amount = rn.randint(4,6)
	coords = []
	angle_offset = rn.randint(0,100)/100*2*math.pi
	for i in range(amount):
		angle = angle_offset+i*2*math.pi/amount
		radius = rn.randint(r_min,r_max)
		point = [center[0]+radius*math.cos(angle),center[1]-radius*math.sin(angle)]
		coords += point
	if not is_color(color):
		color = get_color()
	draw_polygon(coords,'','outline')

'''
def draw_starlight(event):
	point = get_coordinates(1)
	number_of_rays = rn.randint(5,12)
	angle_offset = rn.randint(0,200)/100*math.pi
	for i in range(number_of_rays):
		#-for each ray calculate which border it intersects and where
		#-depending on the angle of the ray, just check borders in that direction
		angle = angle_offset+i*2*math.pi/number_of_rays
		if 0<=angle<=math.pi/2:
			x_intersection = (border-point[1])/angle+point[0] if angle != 0 else canvas_width
			if x_intersection >= canvas_width-border:
				x_intersection = canvas_width-border
				y_intersection = 
			else:
				pass
		elif math.pi/2<angle<=math.pi:
			pass
		elif math.pi<angle<=math.pi*3/2:
			pass
		else:
			pass
'''

background = '#777780' #program background color
bwidth = 14 #button width
bcolor = '#444455'
bfontcolor = '#ffffff'
bborder = 3
brelief = 'flat'
bfont = 'Nimbus 10' #Bahnschrift
lfont = 'Nimbus 12' #label font

root = tk.Tk()
geometry = str(canvas_width+700)+'x'+str(canvas_height+4) #size of the window
root.geometry(geometry)
root.title('Art Generator V3 - by Karmmah')
root.configure(bg=background)
img = tk.Image("photo", file="art_generator_logo2.gif") #program icon in window bar
root.tk.call('wm', 'iconphoto', root._w, img)

f_left = tk.Frame(root, bg=background)
f_left.place(relx=0.03, rely=0.5, anchor='w')

f_canvas = tk.Frame(root)
f_canvas.place(relx=0.5, anchor='n')

f_right = tk.Frame(root, bg=background)
f_right.place(relx=0.99, rely=0.5, anchor='e')

#input fields for borders
f_border = tk.Frame(f_left, relief='raised', bd=bborder, highlightcolor='white', bg=bcolor)
f_border.pack(pady=5, ipady=1)
l_border = tk.Label(f_border, text='Border:', font=bfont, fg='white', bg=bcolor)
l_border.grid(row=0,column=0, padx=10)
e_border = tk.Entry(f_border, width=5, font=bfont, justify='right')
e_border.grid(row=0,column=1, padx=10)
e_border.insert('end', 100)#int((canvas_height-canvas_height/1.618)*0.5))

canvas = tk.Canvas(f_canvas, width=canvas_width, height=canvas_height, bg='white', bd=0, highlightbackground=background)
canvas.pack()

#l_imageinfo = tk.Label(f_left, text='svg data:', justify='left', font='Consolas 9', fg='white', bg=background)
#l_imageinfo.pack(pady=5)
#l_output = tk.Label(f_left, text=default_background, font='Consolas 6', fg='white', bg=bcolor)
#l_output.pack(anchor='w')

f_buttons_top = tk.Frame(f_right, bg=background)
f_buttons_top.pack(anchor='n', pady=5)
f_buttons_midtop = tk.Frame(f_right, bg=background)
f_buttons_midtop.pack(anchor='c', pady=5)
f_buttons_midbot = tk.Frame(f_right, bg=background)
f_buttons_midbot.pack(anchor='c', pady=5)
f_buttons_bottom = tk.Frame(f_right, bg=background)
f_buttons_bottom.pack(anchor='s', pady=5)

b_image = tk.Button(f_buttons_top, state='normal', command=lambda:draw_image(''), text='image', width=bwidth, bg='yellow', fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_blacknwhite = tk.Button(f_buttons_top, state='normal', command=lambda:draw_blacknwhite(''), text='blacknwhite', width=bwidth, bg='green', fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_threecolors = tk.Button(f_buttons_top, state='normal', command=lambda:draw_threecolors(''), text='threecolors', width=bwidth, bg='blue', fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_pixels = tk.Button(f_buttons_top, state='normal', command=lambda:draw_pixels(''), text='pixels', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_color = tk.Button(f_buttons_top, state='normal', command=lambda:draw_color(''), text='color', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_gradient = tk.Button(f_buttons_top, state='normal', command=lambda:draw_gradient(get_color(),get_color()), text='gradient', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)
b_perspective = tk.Button(f_buttons_top, state='normal', command=lambda:draw_perspective(''), text='perspective', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=3,column=0)
b_monocolor = tk.Button(f_buttons_top, state='normal', command=lambda:draw_monocolor(''), text='monocolor', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=3,column=1)
b_pattern = tk.Button(f_buttons_top, state='normal', command=lambda:draw_pattern(''), text='pattern', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=4,column=0)
b_swirls = tk.Button(f_buttons_top, state='disabled', command=lambda:draw_swirls(''), text='swirls', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=4,column=1)
b_colorwall = tk.Button(f_buttons_top, state='normal', command=lambda:draw_colorwall(''), text='colorwall', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=5,column=0)
b_spectrum = tk.Button(f_buttons_top, state='normal', command=lambda:draw_spectrum(''), text='spectrum', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=5,column=1)
b_voronoi = tk.Button(f_buttons_top, state='normal', command=lambda:draw_voronoi(''), text='voronoi', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=6,column=0)
b_text = tk.Button(f_buttons_top, state='disabled', command=lambda:draw_text(''), text='text', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=6,column=1)
b_paper = tk.Button(f_buttons_top, state='normal', command=lambda:draw_paper(''), text='paper', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=7,column=0)
b_patch = tk.Button(f_buttons_top, state='normal', command=lambda:draw_patch(''), text='patch', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=7,column=1)
b_bubbles = tk.Button(f_buttons_top, state='normal', command=lambda:draw_bubbles(''), text='bubbles', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=8,column=0)
b_waveform = tk.Button(f_buttons_top, state='normal', command=lambda:draw_waveform(''), text='waveform', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=8,column=1)
b_separation = tk.Button(f_buttons_top, state='normal', command=lambda:draw_separation(''), text='separation', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=9,column=0)
b_paths = tk.Button(f_buttons_top, state='normal', command=lambda:draw_paths(''), text='paths', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=9,column=1)
b_fractal = tk.Button(f_buttons_top, state='normal', command=lambda:draw_fractal(''), text='fractal', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=10,column=0)
b_spray = tk.Button(f_buttons_top, state='normal', command=lambda:draw_spray(''), text='spray', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=10,column=1)
b_gradient_image = tk.Button(f_buttons_top, state='normal', command=lambda:draw_gradient_image(''), text='gradient image', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=11,column=0)
b_double_color = tk.Button(f_buttons_top, state='normal', command=lambda:draw_double_color(''), text='double color', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=11,column=1)

b_comic = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_comic(''), text='comic', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_polygon = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_polygon('', '', ''), text='polygon', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_polyline = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_polyline('', '', ''), text='polyline', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_stroke = tk.Button(f_buttons_midtop, state='disabled', command=lambda:draw_stroke(''), text='stroke', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_threedee = tk.Button(f_buttons_midtop, state='disabled', command=lambda:draw_threedee(''), text='3D', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_rgb = tk.Button(f_buttons_midtop, state='disabled', command=lambda:draw_rgb(''), text='RGB', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)
b_colorline = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_colorline(''), text='colorline', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=3,column=0)
b_colorpolygon = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_colorpolygon(''), text='colorpolygon', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=3,column=1)
b_radial = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_radial(''), text='radial', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=4,column=0)
b_symmetry = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_symmetry(''), text='symmetry', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=4,column=1)
b_mandala = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_mandala(''), text='mandala', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=5,column=0)
b_starlight = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_starlight(''), text='starlight', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=5,column=1)
b_comet = tk.Button(f_buttons_midtop, state='normal', command=lambda:draw_comet(''), text='comet', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=6,column=0)

b_line = tk.Button(f_buttons_midbot, state='normal', command=lambda:draw_line('', '', ''), text='line', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_arc = tk.Button(f_buttons_midbot, state='disabled', command=lambda:draw_arc(''), text='arc', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_rectangle = tk.Button(f_buttons_midbot, state='normal', command=lambda:draw_rectangle('','',''), text='rectangle', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_ellipse = tk.Button(f_buttons_midbot, state='normal', command=lambda:draw_ellipse('', '', ''), text='ellipse', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_triangle = tk.Button(f_buttons_midbot, state='normal', command=lambda:draw_triangle('',''), text='triangle', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_diamond = tk.Button(f_buttons_midbot, state='disabled', command=lambda:draw_diamond(''), text='diamond', width=bwidth, bg=bcolor, fg=bfontcolor, font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)

adj_b_width = int(round(bwidth*0.58,0)) #special width for save prev delete buttons
b_save = tk.Button(f_buttons_bottom, state='normal', command=lambda:save(''), text='save svg', width=adj_b_width, bg='gold', fg='black', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_previous = tk.Button(f_buttons_bottom, state='normal', command=lambda:save_previous(''), text='previous', width=adj_b_width, bg='#d4aa00', fg='black', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_delete = tk.Button(f_buttons_bottom, state='normal', command=lambda:delete_canvas(''), text='delete (D)', width=adj_b_width, bg='#d40000', fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=2)

l_info = tk.Label(f_right, text='Shortcuts: Ctrl+(Button)', font=lfont, bg='white', fg='black')
l_info.pack(anchor='s', pady=15)

#color backup: #00cc00
#s_crazyness = tk.Scale(f_left, state='disabled', orient='h', length=bwidth*15, from_=1, highlightbackground='white', troughcolor='#00d1a0', bg=bcolor, fg='white', label='Crazyness', font=lfont, relief=brelief, bd=bborder)
#s_crazyness.pack(pady=5)
#s_crazyness.set(22)

test_mode = tk.IntVar() #if test mode is selected, number of artworks in saved file is not increased after save
c_save = tk.Checkbutton(f_left, text='test export', variable=test_mode, font=bfont, bg=bcolor, fg='white')
c_save.pack()

f_colormodes = tk.Frame(f_left, relief='raised', bd=bborder, highlightcolor='white', bg=bcolor)
f_colormodes.pack(pady=5, ipady=1)
l_colormodes = tk.Label(f_colormodes, text='color modes', font=bfont, bg=bcolor, fg='white')
l_colormodes.pack()
base_mode = tk.IntVar()
c_base = tk.Checkbutton(f_colormodes, text='base', variable=base_mode, font=bfont, bg=bcolor, fg='white', borderwidth=0)
c_base.pack()
baldessari_mode = tk.IntVar()
c_baldessari = tk.Checkbutton(f_colormodes, text='baldessari', variable=baldessari_mode, font=bfont, bg=bcolor, fg='white')
c_baldessari.pack()
piet_mode = tk.IntVar()
c_piet = tk.Checkbutton(f_colormodes, text='piet', variable=piet_mode, font=bfont, bg=bcolor, fg='white')
c_piet.pack()
grayscale_mode = tk.IntVar()
c_grayscale = tk.Checkbutton(f_colormodes, text='grayscale', variable=grayscale_mode, font=bfont, bg=bcolor, fg='white')
c_grayscale.pack()

colorselection_width = bwidth*15

def colorselection(event):
	color = [hex(int(s_red.get())).lstrip('0x'), hex(int(s_green.get())).lstrip('0x'), hex(int(s_blue.get())).lstrip('0x')]
	for i in range(len(color)):
		while len(color[i])<2:
			 color[i] = '0'+color[i]
	l_color['bg'] = '#'+color[0]+color[1]+color[2]

f_colorselection = tk.Frame(f_left,relief='raised',bd=bborder,highlightcolor='white',bg=bcolor)
f_colorselection.pack(pady=5,ipady=1)
l_color = tk.Label(f_colorselection,width=26,height=2,bg='black')
l_color.grid(row=1,columnspan=5)
s_red = tk.Scale(f_colorselection,orient='h',length=colorselection_width,to=255,command=colorselection)
s_green = tk.Scale(f_colorselection,orient='h',length=colorselection_width,to=255,command=colorselection)
s_blue = tk.Scale(f_colorselection,orient='h',length=colorselection_width,to=255,command=colorselection)
s_red.grid(row=2,columnspan=5)
s_green.grid(row=3,columnspan=5)
s_blue.grid(row=4,columnspan=5)

def colorbuttons(button_number):
	if button_number == 1:
		b_color1['bg'] = l_color['bg']
	elif button_number == 2:
		b_color2['bg'] = l_color['bg']
	elif button_number == 3:
		b_color3['bg'] = l_color['bg']
	elif button_number == 4:
		b_color4['bg'] = l_color['bg']
	elif button_number == 5:
		b_color5['bg'] = l_color['bg']

b_color1 = tk.Button(f_colorselection,relief='flat',border=bborder,bg='#000001',command=lambda:colorbuttons(1))
b_color2 = tk.Button(f_colorselection,relief='flat',border=bborder,bg='#000001',command=lambda:colorbuttons(2))
b_color3 = tk.Button(f_colorselection,relief='flat',border=bborder,bg='#000001',command=lambda:colorbuttons(3))
b_color4 = tk.Button(f_colorselection,relief='flat',border=bborder,bg='#000001',command=lambda:colorbuttons(4))
b_color5 = tk.Button(f_colorselection,relief='flat',border=bborder,bg='#000001',command=lambda:colorbuttons(5))
b_color1.grid(row=0,column=0)
b_color2.grid(row=0,column=1)
b_color3.grid(row=0,column=2)
b_color4.grid(row=0,column=3)
b_color5.grid(row=0,column=4)

custom_mode = tk.IntVar() #color mode
c_custom = tk.Checkbutton(f_colorselection, text='custom colors', variable=custom_mode, font=bfont, bg=bcolor, fg='white', borderwidth=0)
c_custom.grid(row=5,columnspan=5)

root.bind('<Control-d>',delete_canvas)

global prev_drawing #save previous drawing for when skipping over one you like
prev_drawing = get_svg()

root.mainloop()
