#to-do:
#-draw piet mondrian
#-adjust stroke line function
#-adjust calculate_pointNr function
#-fix image info output for all functions
#-fix mandala rotation center
#-fix monocolor
#-fix diamond

import tkinter as tk
import random as rn
import math

canvas_width = 800
canvas_height = canvas_width

def save_image(event):
    artgenfile = open('artgendata.txt','w')
    filecontent = list(map(str,artgenfile.split(' ')))
    number = filecontent[1]
    artgenfile.write('kunstwerke: '+str(number+1))
    artgenfile.close()
    file = open('kunstwerk'+str(number+1)+'.txt','w')
    print(l_output['text'])
    file.write(l_output['text'])
    file.close()
    
def delete_canvas(event):
    canvas.delete('all')
    canvas.configure(bg='white')
    l_output['text'] = 'bg: white'

def get_random_color():
    color = hex(rn.randint(0,16777215)).lstrip('0x')
    if len(color) < 6:
        while len(color) < 6:
            color = '0' + color
    color = '#'+color
    return color

def calculate_pointNr(): #return number of points in a polygon with crazyness; compensating for large crazyness numbers
    crazyness = s_crazyness.get()
    return int(1 + rn.randint(0,2) + abs(round(crazyness*0.3 - crazyness**2*(1/crazyness*0.5),0) ) )

def get_coordinates(length):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    coordinates = []
    for i in range(length):
        x, y = rn.randint(border, canvas_width-border), rn.randint(border, canvas_width-border)
        coordinates.append(x)
        coordinates.append(y)
    return coordinates

def draw_color(event): #event since assigned button press sends an event string
    canvas.delete('all')
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    color = get_random_color()
    canvas.create_rectangle(bgborder+2,bgborder+2,canvas_width-bgborder+2,canvas_height-bgborder+2, fill=color, outline='')
    l_output['text'] = 'bg:' + color

def draw_gradient(event):
    canvas.delete('all')
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    crazyness = int(round(s_crazyness.get()/3,0))
    colors = '' #for output of all colors to output field
    if s_crazyness.get() == 0:
        draw_color('')
    else:
        red = hex(rn.randint(0,255)).lstrip('0x') #first line
        if len(red) == 1:
            red = '0' + red
        elif red == '':
            red = '00'
        green = hex(rn.randint(0,255)).lstrip('0x')
        if len(green) == 1:
            green = '0' + green
        elif green == '':
            green = '00'
        blue = hex(rn.randint(0,255)).lstrip('0x')
        if len(blue) == 1:
            blue = '0' + blue
        elif blue == '':
            blue = '00'
        if rn.randint(0,1) == 1: #horizontal or vertical orientation
            orientation = 'v'
            length = canvas_width-bgborder*2
        else:
            orientation = 'h'
            length = canvas_height-bgborder*2
        for i in range(length): #following lines
            red = hex(int(red,16)+rn.randint(-int(round(crazyness/2,0)),int(round(crazyness/2,0)))).lstrip('0x')
            if len(red) == 1:
                red = '0' + red
            elif red == '':
                red = '00'
            elif int(red,16)<0:
                red = '00'
            elif int(red,16)>255:
                red = 'ff'                
            green = hex(int(green,16)+rn.randint(-int(round(crazyness/2,0)),int(round(crazyness/2,0)))).lstrip('0x')
            if len(green) == 1:
                green = '0' + green
            elif green == '':
                green = '00'
            elif int(green,16)<0:
                green = '00'
            elif int(green,16)>255:
                green = 'ff'                
            blue = hex(int(blue,16)+rn.randint(-int(round(crazyness/2,0)),int(round(crazyness/2,0)))).lstrip('0x')
            if len(blue) == 1:
                blue = '0' + blue
            elif blue == '':
                blue = '00'
            elif int(blue,16)<0:
                blue = '00'
            elif int(blue,16)>255:
                blue = 'ff'                
            color = '#'+red+green+blue
            if orientation == 'h':
                canvas.create_line(bgborder+2,bgborder+i+2,canvas_width-bgborder+2,bgborder+i+2, fill=color)
            else:
                canvas.create_line(bgborder+i+2,bgborder+2,bgborder+i+2,canvas_height-bgborder+2, fill=color)
            colors = colors+color
        l_output['text'] = 'bg: gradient crazyness:'+str(s_crazyness.get())+' colors:'+colors

def draw_line(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    coordinates = get_coordinates(2)
    width = rn.randint(1,30)
    color = get_random_color()
    canvas.create_line(coordinates, fill=color, width=width)
    l_output['text'] = l_output['text'] + '\nline: '+color+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_arc(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    coordinates = get_coordinates(3)
    width = rn.randint(1,40)
    color = get_random_color()
    canvas.create_line(coordinates, smooth=1, fill=color, width=width)
    l_output['text'] = l_output['text'] + '\narc: '+color+' width:'+str(width)+' coordinates:',str(coordinates)

def draw_rectangle(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    coordinates = get_coordinates(2)
    color = get_random_color()
    if rn.randint(0,1) == 0:
        canvas.create_rectangle(coordinates, fill=color, outline='')
        l_output['text'] = l_output['text'] + '\nrectangle (full): '+color+' coordinates:'+str(coordinates)
    else:
        width = rn.randint(1,40)
        canvas.create_rectangle(coordinates, outline=color, width=width)
        l_output['text'] = l_output['text'] + '\nrectangle (outline): '+color+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_oval(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    coordinates = get_coordinates(2)
    color = get_random_color()
    if rn.randint(0,1) == 0:
        canvas.create_oval(coordinates, fill=color, outline='')
        l_output['text'] = l_output['text'] + '\noval (full): '+color+' coordinates:'+str(coordinates)
    else:
        width = rn.randint(1,40)
        canvas.create_oval(coordinates, outline=color, width=width)
        l_output['text'] = l_output['text'] + '\noval (outline): '+color+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_figure(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(1,40)
    color = get_random_color()
    coordinates = get_coordinates(length)
    if rn.randint(0,1) == 0:
        canvas.create_line(coordinates, fill=color, width=width, joinstyle='miter')
    else:
        canvas.create_line(coordinates, smooth=1, capstyle='round', fill=color, width=width)
    l_output['text'] = l_output['text'] + '\nfigure: '+color+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_stroke(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(1,20)
    color = get_random_color()
    coordinates = []
##    maxstep = round(s_crazyness.get()/3,0) #max distance to next coordinate
    maxstep = s_crazyness.get()*5 #max distance to next coordinate
    start = rn.randint(0,canvas_width), rn.randint(0,canvas_height)
    coordinates.append(start)
    l_output['text'] = l_output['text']+'\nstroke:'+color+' width:'+str(width)+'\n     coords:'+str(start)
    for i in range(length):
        nextcoord = coordinates[i][0]+rn.randint(-maxstep,maxstep), coordinates[i][1]+rn.randint(-maxstep, maxstep)
        if nextcoord[0] < border:
            nextcoord = border, nextcoord[1]
        elif nextcoord[0] > canvas_width-border:
            nextcoord = ncanvas_width+border, nextcoord[1]
        coordinates.append(nextcoord)
        if nextcoord[1] < border:
            nextcoord = border, nextcoord[1]
        elif nextcoord[1] > canvas_width-border:
            nextcoord = canvas_height-border, nextcoord[1]
        coordinates.append(nextcoord)
        l_output['text'] = l_output['text']+'\n     coordinates:'+str(nextcoord)
    canvas.create_line(coordinates, smooth=1, fill=color, width=width)

def draw_threedee(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(1,40)
    effect_offset = rn.randint(10,16)
    coordinates = []
    redcoordinates = []
    bluecoordinates = []
    for i in range(length):
        x, y = rn.randint(border, canvas_width-border), rn.randint(border, canvas_width-border)
        coordinates.append(x)
        coordinates.append(y)
        redcoordinates.append(x-effect_offset)
        redcoordinates.append(y)
        bluecoordinates.append(x+effect_offset)
        bluecoordinates.append(y)
    if rn.randint(0,1) == 0:
        canvas.create_polygon(redcoordinates, fill='red', width=width)
        canvas.create_polygon(bluecoordinates, fill='cyan', width=width)
        canvas.create_polygon(coordinates, fill='black', width=width)
        l_output['text'] = l_output['text'] + '\n3D effect polygon: black effect_offset:'+str(effect_offset)+' width:'+str(width)+' coordinates:'+str(coordinates)
    else:
        canvas.create_polygon(redcoordinates, smooth=1, fill='red', width=width)
        canvas.create_polygon(bluecoordinates, smooth=1, fill='cyan', width=width)
        canvas.create_polygon(coordinates, smooth=1, fill='black', width=width)
        l_output['text'] = l_output['text'] + '\n3D effect polygon (smooth): black effect_offset: '+str(effect_offset)+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_rgb(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(1,40)
    effect_offset = rn.randint(6,11)
    effect_orientation = rn.randint(0,359)
    coordinates = []
    redcoordinates = []
##    yellowcoordinates = []
    greencoordinates = []
##    cyancoordinates = []
    bluecoordinates = []
    for i in range(length):
        x, y = rn.randint(border, canvas_width-border), rn.randint(border, canvas_width-border)
        coordinates.append(x)
        coordinates.append(y)
        redcoordinates.append(x-effect_offset*math.cos(math.pi*effect_offset/180))
        redcoordinates.append(y+effect_offset*math.sin(math.pi*effect_offset/180))
##        yellowcoordinates.append(x+effect_offset*math.cos(math.pi*(effect_offset+72)/180))
##        yellowcoordinates.append(y+effect_offset*math.sin(math.pi*(effect_offset+72)/180))
        greencoordinates.append(x+effect_offset*math.cos(math.pi*(effect_offset+120)/180))
        greencoordinates.append(y+effect_offset*math.sin(math.pi*(effect_offset+120)/180))
##        cyancoordinates.append(x+effect_offset*math.cos(math.pi*(effect_offset+216)/180))
##        cyancoordinates.append(y+effect_offset*math.sin(math.pi*(effect_offset+216)/180))
        bluecoordinates.append(x+effect_offset*math.cos(math.pi*(effect_offset+240)/180))
        bluecoordinates.append(y+effect_offset*math.sin(math.pi*(effect_offset+240)/180))
    if rn.randint(0,1) == 0:
        canvas.create_polygon(redcoordinates, fill='red', width=width)
##        canvas.create_polygon(yellowcoordinates, fill='yellow', width=width)
        canvas.create_polygon(greencoordinates, fill='lightgreen', width=width)
##        canvas.create_polygon(cyancoordinates, fill='cyan', width=width)
        canvas.create_polygon(bluecoordinates, fill='blue', width=width)
        canvas.create_polygon(coordinates, fill='black', width=width)
        l_output['text'] = l_output['text'] + '\nRGB effect polygon: black effect_offset:'+str(effect_offset)+' width:'+str(width)+' coordinates:'+str(coordinates)
    else:
        canvas.create_polygon(redcoordinates, smooth=1, fill='red', width=width)
##        canvas.create_polygon(yellowcoordinates, smooth=1, fill='yellow', width=width)
        canvas.create_polygon(greencoordinates, smooth=1, fill='lightgreen', width=width)
##        canvas.create_polygon(cyancoordinates, smooth=1, fill='cyan', width=width)
        canvas.create_polygon(bluecoordinates, smooth=1, fill='blue', width=width)
        canvas.create_polygon(coordinates, smooth=1, fill='black', width=width)
        l_output['text'] = l_output['text'] + '\nRGB effect polygon (smooth): black effect_offset: '+str(effect_offset)+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_polygon(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    color = get_random_color()
    coordinates = get_coordinates(length)
    if rn.randint(0,1) == 0:
        canvas.create_polygon(coordinates, fill=color)
        l_output['text'] = l_output['text'] + '\npolygon: '+color+' coordinates:'+str(coordinates)
    else:
        canvas.create_polygon(coordinates, smooth=1, fill=color)
        l_output['text'] = l_output['text'] + '\npolygon (smooth): '+color+' coordinates:'+str(coordinates)

def draw_comic(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(1,40)
    shadow_offset = rn.randint(7,20)
    color = get_random_color()
    coordinates = get_coordinates(length)
    shadow_coordinates = []
    for i in range(len(coordinates)):
        shadow_coordinates.append(coordinates[i]+shadow_offset)
    if rn.randint(0,1) == 0:
        canvas.create_polygon(shadow_coordinates, fill='black', width=width)
        canvas.create_polygon(coordinates, fill=color, width=width)
        l_output['text'] = l_output['text'] + '\ncomic: '+color+' width:'+str(width)+' shadow offset:'+str(shadow_offset)+' coordinates:'+str(coordinates)
    else:
        canvas.create_polygon(shadow_coordinates, smooth=1, fill='black', width=width)
        canvas.create_polygon(coordinates, smooth=1, fill=color, width=width)
        l_output['text'] = l_output['text'] + '\ncomic (smooth): '+color+' width:'+str(width)+' shadow offset:'+str(shadow_offset)+' coordinates:'+str(coordinates)


def draw_image(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    amount = int(round(s_crazyness.get()/5,0))+1
    seed = []
    if rn.randint(0,1) == 0:
        draw_color('')
    else:
        draw_gradient('')
    for i in range(amount):
        seed += [rn.randint(0,8)]
    for i in seed:
        if i == 0:
            draw_comic('')
        elif i == 1:
            draw_polygon('')
        elif i == 2:
            draw_figure('')
        elif i == 3:
            draw_line('')
        elif i == 4:
            draw_arc('')
        elif i == 5:
            draw_rectangle('')
        elif i == 6:
            draw_oval('')
##        elif i == 7:
##            draw_stroke('')

def draw_threecolors(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    draw_color('')
##    draw_polygon('') #second version with only polygons
##    draw_polygon('')
    seed = rn.randint(0,6), rn.randint(0,6)
    for i in seed:
        if i == 0:
            draw_comic('')
        elif i == 1:
            draw_polygon('')
        elif i == 2:
            draw_figure('')
        elif i == 3:
            draw_line('')
        elif i == 4:
            draw_arc('')
        elif i == 5:
            draw_rectangle('')
        elif i == 6:
            draw_oval('')

def draw_stars(event):
    canvas.delete('all')
    number = int(round(s_crazyness.get()*2+rn.randint(0,4),0))
    canvas.create_rectangle(0,0,canvas_width,canvas_height, fill='#141852', outline='')
    l_output['text'] = 'stars (bg: #141852): coordinates:'
    for i in range(number):
        size = rn.randint(3,12)
        x = rn.randint(-5,canvas_width-5)
        y = rn.randint(-5,canvas_width-5)
        canvas.create_oval(x-5,y-5,x-5+size,y-5+size, fill='white', outline='')
        l_output['text'] = l_output['text']+'\n'+str(x)+' '+str(y)

def draw_colorfigure(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(12,60)
    color1 = get_random_color()
    color2 = get_random_color()
    color3 = get_random_color()
    coordinates = get_coordinates(length)
    if rn.randint(0,1) == 0:
        canvas.create_line(coordinates, fill=color1, width=width*2.5, joinstyle='round', capstyle='round')
        canvas.create_line(coordinates, fill=color2, width=width*1.8, joinstyle='round', capstyle='round')
        canvas.create_line(coordinates, fill=color3, width=width, joinstyle='round', capstyle='round')
        l_output['text'] = l_output['text'] + '\ncolorfigure(width,width*1.8,width*2.5): '+color1+' '+' '+color2+' '+color3+' width:'+str(width)+' coordinates:'+str(coordinates)
    else:
        canvas.create_line(coordinates, smooth=1, fill=color1, width=width*2.5, capstyle='round')
        canvas.create_line(coordinates, smooth=1, fill=color2, width=width*1.8, capstyle='round')
        canvas.create_line(coordinates, smooth=1, fill=color3, width=width, capstyle='round')
        l_output['text'] = l_output['text'] + '\ncolorfigure(smooth, width,width*1.8,width*2.5): '+color1+' '+' '+color2+' '+color3+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_colorpolygon(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    length = calculate_pointNr()
    width = rn.randint(12,60)
    color1 = get_random_color()
    color2 = get_random_color()
    color3 = get_random_color()
    coordinates = get_coordinates(length)
    if rn.randint(0,1) == 0:
        canvas.create_polygon(coordinates, fill='', outline=color1, width=width*2.5)
        canvas.create_polygon(coordinates, fill='', outline=color2, width=width*1.8)
        canvas.create_polygon(coordinates, fill=color3, width=width)
        l_output['text'] = l_output['text'] + '\npolygon (width,width*1.8,width*2.5): '+color1+' '+' '+color2+' '+color3+' width:'+str(width)+' coordinates:'+str(coordinates)
    else:
        canvas.create_polygon(coordinates, smooth=1, fill='', outline=color1, width=width*2.5)
        canvas.create_polygon(coordinates, smooth=1, fill='', outline=color2, width=width*1.8)
        canvas.create_polygon(coordinates, smooth=1, fill=color3, width=width)
        l_output['text'] = l_output['text'] + '\ncolorpolygon (smooth, width,width*1.8,width*2.5): '+color1+' '+' '+color2+' '+color3+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_symmetry(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    width = rn.randint(12,40)
    length = calculate_pointNr()
    color = get_random_color()
    coordinates = []
    coordinates_mirrored = []
    for i in range(length):
    	xdistance = rn.randint(0,canvas_width/2-border)
    	x, y = canvas_width/2+xdistance, rn.randint(border,canvas_width-border)
    	x2, y2 = canvas_width/2-xdistance, y
    	coordinates.append(x)
    	coordinates.append(y)
    	coordinates_mirrored.append(x2)
    	coordinates_mirrored.append(y2)
    canvas.create_line(coordinates, fill=color, width=width, joinstyle='round', capstyle='round')
    canvas.create_line(coordinates_mirrored, fill=color, width=width, joinstyle='round', capstyle='round')
    l_output['text'] = l_output['text'] + '\nsymmetry: '+color+' width:'+str(width)+' coordinates:'+str(coordinates)
#    if rn.randint(0,1) == 0:
#        canvas.create_line(coordinates, fill=color, width=width, joinstyle='miter', capstyle='round')
#        canvas.create_line(coordinates_mirrored, fill=color, width=width, joinstyle='miter', capstyle='round')
#        l_output['text'] = l_output['text'] + '\nsymmetry: '+color+' width:'+str(width)+' coordinates:'+str(coordinates)
#    else:
#        canvas.create_line(coordinates, smooth=1, fill=color, width=width, capstyle='round')
#        canvas.create_line(coordinates_mirrored, smooth=1, fill=color, width=width, capstyle='round')
#        l_output['text'] = l_output['text'] + '\nsymmetry: '+color+' width:'+str(width)+' coordinates:'+str(coordinates)

def draw_mandala(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    width = rn.randint(12,30)
    length = calculate_pointNr()
    complexity = rn.randint(7,12)
    angle = 2*math.pi/complexity
    color = get_random_color()
    coordinates = []
    for i in range(3):#length):
        x, y = rn.randint(border, canvas_width-border), rn.randint(border, canvas_width-border)
        coordinates.append(x)
        coordinates.append(y)
    canvas.create_line(coordinates, fill=color, width=width, joinstyle='miter', capstyle='round')
    original_angle = math.atan(y/x)
    for i in range(complexity):
	    newcoordinates = []
	    for j in range(3):#length):
	    	radius = math.sqrt((coordinates[j]-canvas_width/2)**2+(coordinates[j+1]-canvas_height/2)**2)
	    	x = coordinates[j]+math.cos(original_angle+i*angle)*radius
    		y = coordinates[j+1]+math.sin(original_angle+i*angle)*radius
    		j += 1
    		newcoordinates.append(x)
    		newcoordinates.append(y)
	    canvas.create_line(newcoordinates, fill=color, width=width, joinstyle='miter', capstyle='round')

def draw_points(event):
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    amount = calculate_pointNr()*4
    for i in range(amount):
        x = rn.randint(border,canvas_width-border)
        y = rn.randint(border,canvas_height-border)
        size = rn.randint(4,16)
        color = get_random_color()
        canvas.create_oval(x-size/2,y-size/2,x+size/2,y+size/2, fill=color,outline='')
    l_output['text'] = l_output['text'] + '\npoint: '+color+' size:'+str(size)+' coordinates:'+str(x)+' '+str(y)

def draw_monocolor(event):
    delete_canvas(event)
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    color = get_random_color()
    amount = calculate_pointNr()*4
    for i in range(amount):
        if i % 2 != 0:
            fill = color
        else:
            fill = 'white'
        j = rn.randint(0,4)
        if j == 0:
            draw_rectangle(fill)
        elif j == 1:
            draw_oval(fill)
        elif j == 2:
            draw_figure(fill)
        elif j == 3:
            draw_polygon(fill)
        else:
            pass

def draw_pattern(event):
    draw_color('')
    border, bgborder = int(e_border.get()), int(e_bgborder.get())
    color = get_random_color()
    pattern_amount_x = rn.randint(6,35) #how many pattern elements are drawn per line
    pattern_amount_y = int(round(pattern_amount_x*(canvas_height/canvas_width),0))
    pattern_width = (canvas_width-2*border)/pattern_amount_x
    line_width = 60/pattern_amount_x
    for i in range(pattern_amount_y):
        for j in range(pattern_amount_x):
            if rn.randint(0,1) == 0:
                x1 = border+pattern_width*j
                y1 = border+pattern_width*i
                x2 = border+pattern_width*(j+1)
                y2 = border+pattern_width*(i+1)
            else:
                x1 = border+pattern_width*(j+1)
                y1 = border+pattern_width*i
                x2 = border+pattern_width*j
                y2 = border+pattern_width*(i+1)
            canvas.create_line(x1,y1,x2,y2,fill=color,width=line_width,capstyle='round')

def draw_triangle(event):
    coordinates = get_coordinates(3)
    color = get_random_color()
    if rn.randint(0,1) == 0:
        canvas.create_polygon(coordinates,fill=color,outline='')
    else:
        canvas.create_polygon(coordinates,fill='',outline=color,width=rn.randint(4,20),joinstyle='miter')

def draw_diamond(event):
    coordinates = get_coordinates(2) #get two coordinates for the location and direction
    angle = -math.atan((coordinates[3]-coordinates[1])/(coordinates[2]-coordinates[0]))#/math.pi*180
    length = math.sqrt((coordinates[3]-coordinates[1])**2+(coordinates[2]-coordinates[0])**2)
    print(angle,length) #testing
    width = rn.randint(20,70)*0.01*length #width ratio compared to height
    x3 = coordinates[0]+math.cos(angle)*length/2+math.cos(angle+math.pi*0.5)*width
    y3 = coordinates[1]+math.sin(angle)*length/2+math.sin(angle+math.pi*0.5)*width
    x4 = coordinates[0]+math.cos(angle)*length/2-math.cos(angle+math.pi*0.5)*width
    y4 = coordinates[1]+math.sin(angle)*length/2-math.sin(angle+math.pi*0.5)*width
    coordinates_new = [coordinates[0],coordinates[1],x3,y3,coordinates[2],coordinates[3],x4,y4]
    color = get_random_color()
    #canvas.create_polygon(coordinates_new,fill=color)
    canvas.create_line(coordinates,fill=color) #testing
    canvas.create_line(x3,y3,x4,y4,fill=color) #testing

def draw_longhole(event):
    pass#coordinates = get_coordinates(2)


root = tk.Tk()

background = '#666666'
bwidth = 14
bcolor = '#777777'
bborder = 5
brelief = 'raised'
bfont = 'Bahnschrift 9'
lfont = 'Bahnschrift 11'

geometry = str(canvas_width+520)+'x'+str(canvas_height+4)
root.geometry(geometry)
root.title('art_generator V1.1')
root.configure(bg=background)

f_left = tk.Frame(root, bg=background)
f_left.place(relx=0.01, rely=0.5, relwidth=0.174, relheight=0.96, anchor='w')

f_canvas = tk.Frame(root)
f_canvas.place(relx=0.5, anchor='n')

f_right = tk.Frame(root, bg=background)
f_right.place(relx=0.99, rely=0.5, anchor='e')

canvas = tk.Canvas(f_canvas, width=canvas_width, height=canvas_height, bg='white', bd=0, highlightbackground=background)
canvas.pack()

l_imageinfo = tk.Label(f_left, text='image info:', justify='left', font='Consolas 9', fg='white', bg=background)
l_imageinfo.pack(pady=5)
l_output = tk.Label(f_left, text='bg: white', justify='left', font='Consolas 9', fg='white', bg=bcolor)
l_output.pack(anchor='w')

f_buttons_top = tk.Frame(f_right, bg=background)
f_buttons_top.pack(anchor='n', pady=5)

f_buttons_midtop = tk.Frame(f_right, bg=background)
f_buttons_midtop.pack(anchor='c', pady=5)

f_buttons_midbot = tk.Frame(f_right, bg=background)
f_buttons_midbot.pack(anchor='c', pady=5)

f_buttons_bottom = tk.Frame(f_right, bg=background)
f_buttons_bottom.pack(anchor='s', pady=5)

b_image = tk.Button(f_buttons_top, command=lambda:draw_image(''), text='image (I)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_threecolors = tk.Button(f_buttons_top, command=lambda:draw_threecolors(''), text='threecolors (T)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_mandala = tk.Button(f_buttons_top, command=lambda:draw_mandala(''), text='mandala (M)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_symmetry = tk.Button(f_buttons_top, command=lambda:draw_symmetry(''), text='symmetry (H)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_area = tk.Button(f_buttons_top, state='disabled', command=lambda:draw_area(''), text='area (A)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_points = tk.Button(f_buttons_top, command=lambda:draw_points(''), text='points (.)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)
b_color = tk.Button(f_buttons_top, command=lambda:draw_color(''), text='color (B)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=0)
b_gradient = tk.Button(f_buttons_top, command=lambda:draw_gradient(''), text='gradient (G)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=1)
b_stars = tk.Button(f_buttons_top, command=lambda:draw_stars(''), text='stars (N)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=4,column=0)
b_monocolor = tk.Button(f_buttons_top, state='disabled', command=lambda:draw_monocolor(''), text='monocolor (W)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=4,column=1)
b_pattern = tk.Button(f_buttons_top, command=lambda:draw_pattern(''), text='pattern ()', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=5,column=0)

b_comic = tk.Button(f_buttons_midtop, command=lambda:draw_comic(''), text='comic (C)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_polygon = tk.Button(f_buttons_midtop, command=lambda:draw_polygon(''), text='polygon (P)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_figure = tk.Button(f_buttons_midtop, command=lambda:draw_figure(''), text='figure (F)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_stroke = tk.Button(f_buttons_midtop, state='disabled', command=lambda:draw_stroke(''), text='stroke (U)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_threedee = tk.Button(f_buttons_midtop, command=lambda:draw_threedee(''), text='3D (3)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_rgb = tk.Button(f_buttons_midtop, command=lambda:draw_rgb(''), text='RGB (Q)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)
b_colorfigure = tk.Button(f_buttons_midtop, command=lambda:draw_colorfigure(''), text='colorfigure (J)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=0)
b_colorpolygon = tk.Button(f_buttons_midtop, command=lambda:draw_colorpolygon(''), text='colorpolygon (K)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=1)

b_line = tk.Button(f_buttons_midbot, command=lambda:draw_line(''), text='line (L)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_arc = tk.Button(f_buttons_midbot, command=lambda:draw_arc(''), text='arc (A)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)
b_rectangle = tk.Button(f_buttons_midbot, command=lambda:draw_rectangle(''), text='rectangle (R)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=0)
b_oval = tk.Button(f_buttons_midbot, command=lambda:draw_oval(''), text='oval (O)', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=1)
b_triangle = tk.Button(f_buttons_midbot, command=lambda:draw_triangle(''), text='triangle ()', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_diamond = tk.Button(f_buttons_midbot, command=lambda:draw_diamond(''), text='diamond ()', width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=1)

b_save = tk.Button(f_buttons_bottom, command=lambda:save_image(''), text='save info (S)', width=bwidth, bg='gold', fg='black', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=0)
b_delete = tk.Button(f_buttons_bottom, command=lambda:delete_canvas(''), text='delete (D)', width=bwidth, bg='gray', fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=0,column=1)

s_crazyness = tk.Scale(f_right, orient='h', length=bwidth*15, from_=1, highlightbackground='white', troughcolor='red', bg=bcolor, fg='white', label='Crazyness', font=lfont, relief=brelief, bd=bborder)
s_crazyness.pack(pady=5)
s_crazyness.set(22)

f_border = tk.Frame(f_right, relief='raised', bd=bborder, highlightcolor='white', bg=bcolor)
f_border.pack(pady=5, ipady=1)
l_border = tk.Label(f_border, text='Border:', font=bfont, fg='white', bg=bcolor)
l_border.grid(row=0,column=0, padx=10)
l_bgborder = tk.Label(f_border, text='BG Border:', font=bfont, fg='white', bg=bcolor)
l_bgborder.grid(row=1,column=0, padx=10)
e_border = tk.Entry(f_border, width=5, font=bfont, justify='right')
e_border.grid(row=0,column=1, padx=10)
e_border.insert('end', 60)
e_bgborder = tk.Entry(f_border, width=5, font=bfont, justify='right')
e_bgborder.grid(row=1,column=1, padx=10)
e_bgborder.insert('end', 1) #1 for white border to make using snipping tool easier

l_info = tk.Label(f_right, text='Shortcuts: Ctrl + Button', font=lfont, bg='white', fg='black')
l_info.pack(anchor='s', pady=15)

root.bind('<Control-i>', draw_image)
root.bind('<Control-t>', draw_threecolors)
root.bind('<Control-m>', draw_mandala)
root.bind('<Control-h>', draw_symmetry)

#root.bind('<Control-.>', draw_points)
root.bind('<Control-b>', draw_color)
root.bind('<Control-g>', draw_gradient)
root.bind('<Control-n>', draw_stars)
root.bind('<Control-w>', draw_monocolor)

root.bind('<Control-c>', draw_comic)
root.bind('<Control-p>', draw_polygon)
root.bind('<Control-f>', draw_figure)
root.bind('<Control-u>', draw_stroke)
root.bind('<Control-Key-3>', draw_threedee)
root.bind('<Control-q>', draw_rgb)
root.bind('<Control-j>', draw_colorfigure)
root.bind('<Control-k>', draw_colorpolygon)

root.bind('<Control-l>', draw_line)
root.bind('<Control-a>', draw_arc)
root.bind('<Control-r>', draw_rectangle)
root.bind('<Control-o>', draw_oval)

root.bind('<Control-s>', save_image)
root.bind('<Control-d>', delete_canvas)

root.mainloop()
