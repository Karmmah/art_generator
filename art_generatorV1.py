#TO-DO:
#-implement random text input from some database of words

#gute farben: #3dde99,#320fc4

try: # Python2
    import Tkinter as tk
except ImportError: # Python3
    import tkinter as tk
import random
import math
import threading as th

program_width = 800
program_height = 800

def give_color():    
    if e_color.get() != '':
        string = e_color.get()
        root.focus()
    else:
        string = give_random_color()
    
    return string

def give_random_color():
    color = [0]*6
    for i in range(len(color)):
        value = random.sample(range(16), 1)[0]
        if hex(value).lstrip('0x') == '':
            color[i] = '0'
        else:
            color[i] = hex(value).lstrip('0x')
    string = '#'+str(color[0])+str(color[1])+str(color[2])+str(color[3])+str(color[4])+str(color[5])
    return string

def save_imageinfo(event):
    file = open('kunstwerkXXX.txt', 'w')
    print(l_imageinfo['text'])
    file.write(l_imageinfo['text'])
    file.close()
    
def delete_canvas(event):
    canvas.delete('all')
    l_imageinfo['text'] = 'bg:white'

def draw_color(event):
    canvas.delete('all')

    color = give_color()
    canvas.create_rectangle(0,0,program_width,program_height, fill=color, outline='')
    l_imageinfo['text'] = 'bg:' + color

def draw_line(event):
    color = give_color()
    width = random.sample(range(40),1)[0]
    x1, y1 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
    x2, y2 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    l_imageinfo['text'] = l_imageinfo['text'] + '\nline:' + color + ' width:' + str(width) + ' x1:'+str(x1)+' y1:'+str(y1)+' x2:'+str(x2)+' y2:'+str(y2)

def draw_oval(event):
    color = give_random_color()
    width = random.sample(range(2,25),1)[0]
    x1, y1 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
    x2, y2 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10,
    if random.sample(range(10),1)[0] < 7:
        fill = 'None'
        canvas.create_oval(x1,y1,x2,y2, fill='', outline=color, width=width)
    else:
        fill = give_color()
        canvas.create_oval(x1,y1,x2,y2, fill=fill, outline='', width=width)
    l_imageinfo['text'] = l_imageinfo['text'] + '\noval:'+color+' fill:'+fill+' width:'+str(width)+' x1:'+str(x1)+' y1:'+str(y1)+' x2:'+str(x2)+' y2:'+str(y2)

def draw_point(event):
    color = give_color()
    width = random.sample(range(20),1)[0]
    x = random.sample(range(program_width-20),1)[0]+10
    y = random.sample(range(program_height-20),1)[0]+10
        
    canvas.create_oval(x-width,y-width,x+width,y+width, fill=color, outline='')
    l_imageinfo['text'] = l_imageinfo['text']+'\npoint:'+color+' x1:'+str(x-width)+' y1:'+str(y-width)+' x2:'+str(x+width)+' y2:'+str(y+width)

def draw_arc(event):
    color = give_color()
    width = random.sample(range(25),1)[0]
    x1, y1 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10,
    x2, y2 = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
    start = random.sample(range(360),1)[0]
    extent = random.sample(range(360),1)[0]
    canvas.create_arc(x1,y1,x2,y2, start=start, extent=extent, outline=color, width=width, style='arc')
    l_imageinfo['text'] = l_imageinfo['text']+'\narc:'+color+' width:'+str(width)+' start: '+str(start)+' extent: '+str(extent)+' x1:'+str(x1)+' y1:'+str(y1)+' x2:'+str(x2)+' y2:'+str(y2)

def draw_figure(event): #random nummer von zusammenhängenden strichen
    length = int(round(s_colorvariation.get()/8,0))+random.sample(range(1,3),1)[0]
    color = give_color()
    width = random.sample(range(25),1)[0]
    smooth = random.sample(range(2),1)[0]
    coords = []
    start = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_width-20),1)[0]+10
    coords.append(start)
    l_imageinfo['text'] = l_imageinfo['text']+'\nfigure:'+color+' width:'+str(width)+' smooth:'+str(smooth)+'\n     coords:'+str(start)
    
    for i in range(length):
##        form = random.sample(range(5)) #line, arc, circle, rectangle usw möglich
        nextcoord = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
        coords.append(nextcoord)

        l_imageinfo['text'] = l_imageinfo['text']+'\n     coords:'+str(nextcoord)

    canvas.create_line(coords, fill=color, width=width, smooth=smooth)

def draw_polygon(event): #random vieleck
    color = give_color()
    smooth = random.sample(range(2),1)[0]
    maxlines = 10
    coordinates = []
    str_coords = ''

    lines = random.sample(range(3, maxlines+1),1)[0]
    for i in range(lines):
        x, y = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
        coordinates += x, y
        str_coords = str_coords+' x'+str(i+1)+':'+str(x)+' y'+str(i+1)+':'+str(y)

    canvas.create_polygon(coordinates, fill=color, outline='', smooth=smooth)
    l_imageinfo['text'] = l_imageinfo['text']+'\npolygon:'+color+' smooth:'+str(smooth)+str_coords

def draw_comic(event): #random vieleck mit schatten
    color = give_color()
    smooth = random.sample(range(2),1)[0]
    shadow_offset = random.sample(range(5,15),1)[0]
    maxlines = 10
    coordinates = []
    shadow_coordinates = []
    str_coords = ''

    lines = random.sample(range(3, maxlines+1),1)[0]
    for i in range(lines):
        x, y = random.sample(range(program_width-20),1)[0]+10, random.sample(range(program_height-20),1)[0]+10
        coordinates += x, y
        shadow_coordinates += x+shadow_offset, y+shadow_offset
        str_coords = str_coords+' x'+str(i+1)+':'+str(x)+' y'+str(i+1)+':'+str(y)

    canvas.create_polygon(shadow_coordinates, fill='black', outline='', smooth=smooth)
    canvas.create_polygon(coordinates, fill=color, outline='', smooth=smooth)
    l_imageinfo['text'] = l_imageinfo['text']+'\npolygon:'+color+' smooth:'+str(smooth)+' shadow offset:'+str(shadow_offset)+str_coords

def draw_image(event):
    amount = int(round(s_colorvariation.get()/2,0))+1
    seed = []

    if random.sample(range(2),1)[0] == 0:
        draw_color('')
    else:
        draw_gradient('')
    for i in range(amount):
        seed += [random.sample(range(8),1)[0]] #range 6, da 6 sachen gezeichnet werden können

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
            draw_oval('')
        elif i == 5:
            draw_point('')
        elif i == 6:
            draw_arc('')
        elif i == 7:
            draw_stroke('')
##    canvas.create_rectangle(8,8,program_width-4,program_height-4, fill='', outline='white', width=16) #weißen rand um zeichenfläche

def draw_points(event):
    for i in range(s_colorvariation.get()*2):
        draw_point('')

def draw_symmetry(event): #mandala oder so, k.a.
    pass

def draw_stars(event):
    canvas.delete('all')
    color = '#11003f'
    l_imageinfo['text'] = 'bg: ' + color + '\nstars:'
    canvas.create_rectangle(0,0,program_width,program_height,fill=color,outline='')
    for i in range(random.sample(range(3,12),1)[0]*s_colorvariation.get()+1):
        width = random.sample(range(10),1)[0]
        x = random.sample(range(program_width-20),1)[0]+10
        y = random.sample(range(program_height-20),1)[0]+10            
        canvas.create_oval(x-int(width/2),y-int(width/2),x+int(width/2),y+int(width/2), fill='white', outline='')
        l_imageinfo['text'] = l_imageinfo['text']+'\n     x1:'+str(x-width/2)+' y1:'+str(y-width/2)+' x2:'+str(x+width/2)+' y2:'+str(y+width/2)

def draw_gradient(event):
    canvas.delete('all')
    colorvariation = int(s_colorvariation.get())
    colors = ''
    
    if s_colorvariation.get() != 0: #if variation = 0, draw single color and skip lines
        red = hex(random.sample(range(256),1)[0]).lstrip('0x')
        if len(red) == 1:
            red = '0' + red
        green = hex(random.sample(range(256),1)[0]).lstrip('0x')
        if len(green) == 1:
            green = '0' + green
        blue = hex(random.sample(range(256),1)[0]).lstrip('0x')
        if len(blue) == 1:
            blue = '0' + blue
        
        if random.sample(range(2),1)[0]==1:
            orientation = 'v'
            length = program_width
        else:
            orientation = 'h'
            length = program_height

        for i in range(length):
            red = hex(int(red,16)+random.sample(range(-int(round(colorvariation/2,0)),int(round(colorvariation/2,0))+1),1)[0]).lstrip('0x')
            if len(red) == 1:
                red = '0' + red
            elif red == '':
                red = '00'
            elif int(red,16)<0:
                red = '00'
            elif int(red,16)>255:
                red = 'ff'
                
            green = hex(int(green,16)+random.sample(range(-int(round(colorvariation/2,0)),int(round(colorvariation/2,0))+1),1)[0]).lstrip('0x')
            if len(green) == 1:
                green = '0' + green
            elif green == '':
                green = '00'
            elif int(green,16)<0:
                green = '00'
            elif int(green,16)>255:
                green = 'ff'
                
            blue = hex(int(blue,16)+random.sample(range(-int(round(colorvariation/2,0)),int(round(colorvariation/2,0))+1),1)[0]).lstrip('0x')
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
                canvas.create_line(0,i,program_width,i, fill=color)
            else:
                canvas.create_line(i,0,i,program_height, fill=color)
            colors = colors+color
        l_imageinfo['text'] = 'bg:gradient, crazyness:'+str(s_colorvariation.get())+' colors:'+colors
    else:
        draw_color('')

def draw_area(event): #UNFINISHED
    canvas.delete('all')
    scaling_factor = 6 #factor for pixel size
    pixels = [0]*int(round(program_height/scaling_factor,0)), [0]*int(round(program_width/scaling_factor,0))
    colorvariation = s_colorvariation.get()

    #first row
    color = give_color()
    pixels[0][0] = color
    for i in range(1,int(program_width/6)):
        red = color[1]+color[2]
        green = color[3]+color[4]
        blue = color[5]+color[6]

        newred = hex(int(red,16)+int(round(random.sample(range(colorvariation*0.16),1)[0],0)))
        print('new red:',newred) #testing
        color = '#'+newred+newgreen+newblue
        pixel[0][i] = color

    #first column

    #following lines


##def draw_area(event):
##    canvas.delete('all')
##    scaling_factor = 6 #factor for pixel size
##    line_data = [0]*int(program_width/scaling_factor)
##    
##    if s_colorvariation.get() == '':
##        colorvariation = 20
##    else:
##        colorvariation = int(s_colorvariation.get())
##
##    #first line
##    red = hex(random.sample(range(256),1)[0]).lstrip('0x')
##    if len(red) == 1:
##        red = '0' + red
##    elif red == '':
##        red = '00'
##    green = hex(random.sample(range(256),1)[0]).lstrip('0x')
##    if len(green) == 1:
##        green = '0' + green
##    elif green == '':
##        green = '00'
##    blue = hex(random.sample(range(256),1)[0]).lstrip('0x')
##    if len(blue) == 1:
##        blue = '0' + blue
##    elif blue == '':
##        blue = '00'
##        
##    if e_color.get() != '':
##        color = e_color.get()
##    else:
##        color = '#'+red+green+blue
##    canvas.create_line(0,scaling_factor/2,1*scaling_factor,scaling_factor/2, fill=color, width=scaling_factor)
##    line_data[0] = red, green, blue
##
##    for i in range(1,len(line_data)):
##        red = hex(int(line_data[i-1][0],16)+random.sample(range(-colorvariation,colorvariation+1),1)[0]).lstrip('0x')
##        if len(red) == 1:
##            red = '0' + red
##        elif red == '':
##            red = '00'
##        elif int(red,16)<0:
##            red = '00'
##        elif int(red,16)>255:
##            red = 'ff'
##            
##        green = hex(int(line_data[i-1][1],16)+random.sample(range(-colorvariation,colorvariation+1),1)[0]).lstrip('0x')
##        if len(green) == 1:
##            green = '0' + green
##        elif green == '':
##            green = '00'
##        elif int(green,16)<0:
##            green = '00'
##        elif int(green,16)>255:
##            green = 'ff'
##        if len(green) < 2: #testing
##            print('len(green) after:', len(green))
##            
##        blue = hex(int(line_data[i-1][2],16)+random.sample(range(-colorvariation,colorvariation+1),1)[0]).lstrip('0x')
##        if len(blue) == 1:
##            blue = '0' + blue
##        elif blue == '':
##            blue = '00'
##        elif int(blue,16)<0:
##            blue = '00'
##        elif int(blue,16)>255:
##            blue = 'ff'
##            
##        color = '#'+red+green+blue
##        canvas.create_line(i*scaling_factor,scaling_factor/2,(i+1)*scaling_factor,scaling_factor/2, fill=color, width=scaling_factor)
##        line_data[i] = red, green, blue
##    
##    #following lines
##    for j in range(1,int(program_height/scaling_factor)+int(scaling_factor/2)):
##        i = 0
##        
##        for i in range(len(line_data)):
##            red = hex(int(line_data[i-len(line_data)][0],16)+int(random.sample(range(-colorvariation,colorvariation+1),1)[0]*random.sample(range(-colorvariation,colorvariation+1),1)[0]/colorvariation*2)).lstrip('0x')
##            if len(red) == 1:
##                red = '0' + red
##            elif red == '':
##                red = '00'
##            elif int(red,16)<0:
##                red = '00'
##            elif int(red,16)>255:
##                red = 'ff'
##                
##            green = hex(int(line_data[i-len(line_data)][1],16)+int(random.sample(range(-colorvariation,colorvariation+1),1)[0]*random.sample(range(-colorvariation,colorvariation+1),1)[0]/colorvariation*2)).lstrip('0x')
##            if len(green) == 1:
##                green = '0' + green
##            elif green == '':
##                green = '00'
##            elif int(green,16)<0:
##                green = '00'
##            elif int(green,16)>255:
##                green = 'ff'
##            if len(green) < 2: #testing
##                print('len(green) after:', len(green))
##                
##            blue = hex(int(line_data[i-len(line_data)][2],16)+int(random.sample(range(-colorvariation,colorvariation+1),1)[0]*random.sample(range(-colorvariation,colorvariation+1),1)[0]/colorvariation*2)).lstrip('0x')
##            if len(blue) == 1:
##                blue = '0' + blue
##            elif blue == '':
##                blue = '00'
##            elif int(blue,16)<0:
##                blue = '00'
##            elif int(blue,16)>255:
##                blue = 'ff'
##                
##            color = '#'+red+green+blue
##            canvas.create_line(i*scaling_factor,j*scaling_factor,(i+1)*scaling_factor,j*scaling_factor, fill=color, width=scaling_factor)
##            line_data[i] = red, green, blue
##    l_imageinfo['text'] = 'bg: custom area, crazyness:'+str(s_colorvariation.get())

###font styles: font="Times 20 italic bold"
##def draw_branding(event):
##    root.focus()
##    if e_color.get() == '':
##        canvas.create_text(program_width*0.2,program_height*0.9, text='human_machine_art', font='Bahnschrift 14', fill='white')
##    else:
##        canvas.create_text(program_width*0.2,program_height*0.9, text='human_machine_art', font='Bahnschrift 14', fill=e_color.get())

def draw_threecolors(event):
    draw_color('')
    draw_polygon('')
    draw_polygon('')

def draw_stroke(event):
    length = s_colorvariation.get()+random.sample(range(5),1)[0]
    width = random.sample(range(3,15),1)[0]
    color = give_color()
    maxstep = 100 #max distance to next coordinate
    coords = []
    start = random.sample(range(program_width),1)[0], random.sample(range(program_height),1)[0]
    coords.append(start)
    l_imageinfo['text'] = l_imageinfo['text']+'\nstroke:'+color+' width:'+str(width)+'\n     coords:'+str(start)

    for i in range(length):
        nextcoord = coords[i][0]+random.sample(range(-maxstep,maxstep),1)[0], coords[i][1]+random.sample(range(-maxstep, maxstep),1)[0]
        coords.append(nextcoord)

        l_imageinfo['text'] = l_imageinfo['text']+'\n     coords:'+str(nextcoord)

    canvas.create_line(coords, fill=color, width=width, smooth=1)


root = tk.Tk()
root.title('Art Generator')
root.configure(background='#666666')

background = tk.Canvas(root, width=program_width, height=program_height+100, bg='black').place(anchor='s')

canvas = tk.Canvas(root, width=program_width, height=program_height, bg='white')
canvas.grid(row=0,column=0,columnspan=8)
canvas.create_text(program_width/2, program_height/2, text='Shortcuts: Ctrl + Button', font='Consolas 24')

####
bwidth = 14
bcolor = '#777777'
bborder = 5
#brelief must be flat, groove, raised, ridge, solid, or sunken
brelief = 'raised'
bfont = 'Bahnschrift 9'
####

l_colorvariation = tk.Label(root, text='Crazyness:', bg='#666666', fg='white', font='Bahnschrift 9').grid(row=1, column=0)

#bg='white', highlightthickness=0, sliderlength=40
s_colorvariation = tk.Scale(root, orient='horizontal', sliderrelief='raised', troughcolor='lightgray', bg='#888888', fg='white', bd=3, font='Times, 6', width=5)
s_colorvariation.grid(row=1, column=1)
s_colorvariation.set(9)

l_color = tk.Label(root, text='Color (hex):', bg='#666666', fg='white', font='Bahnschrift 9').grid(row=1, column=2)

##entryText = tk.StringVar() #input a color
e_color = tk.Entry(root,width=21, bg=bcolor, fg='white')
e_color.grid(row=1,column=2, columnspan=3)

l_imageinfo = tk.Label(root, text='bg: white', width=32, height=1, bg='#666666', fg='white', font='Consolas 8')
l_imageinfo.grid(row=1, column=4, columnspan=3)

b_color = tk.Button(root, text='color (1)', command=lambda:draw_color(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=0)
b_area = tk.Button(root, state='disabled', text='area (2)', command=lambda:th.Thread(target=draw_area).start(), width=bwidth, font=bfont, bg=bcolor, fg='white', bd=bborder, relief=brelief).grid(row=2,column=1)
b_gradient = tk.Button(root, text='gradient (3)', command=lambda:draw_gradient(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=2)
b_stars = tk.Button(root, text='stars (4)', command=lambda:draw_stars(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=3)
b_image = tk.Button(root, text='image (5)', command=lambda:draw_image(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=4)
b_points = tk.Button(root, text='points (6)', command=lambda:draw_points(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=5)
b_threecolors = tk.Button(root, text='three colors (7)', command=lambda:draw_threecolors(''), relief=brelief, width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder).grid(row=2, column=6)

b_comic = tk.Button(root, text='comic (Q)', command=lambda:draw_comic(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=0)
b_polygon = tk.Button(root, text='polygon (W)', command=lambda:draw_polygon(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=1)
b_figure = tk.Button(root, text='figure (E)', command=lambda:draw_figure(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=2)
b_line = tk.Button(root, text='line (R)', command=lambda:draw_line(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=3)
b_oval = tk.Button(root, text='oval (T)', command=lambda:draw_oval(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=4)
b_arc = tk.Button(root, text='arc (Z)', command=lambda:draw_arc(''), width=bwidth, bg=bcolor, fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=3,column=5)
b_stroke = tk.Button(root, text='stroke (U)', relief=brelief, command=lambda:draw_stroke(''), width=bwidth, bg=bcolor, fg='white', bd=bborder).grid(row=3, column=6)

b_erase = tk.Button(root, text='erase (D)', command= lambda: delete_canvas(''), width=bwidth, bg='gray', fg='white', font=bfont, bd=bborder, relief=brelief).grid(row=1,column=7)
b_save = tk.Button(root, text='save (S)', command =lambda:save_imageinfo(''), width=bwidth, bg='gold', font=bfont, bd=bborder, relief=brelief).grid(row=2,column=7)

root.bind('<Motion>', root.focus())

root.bind('<Control-d>', delete_canvas)
root.bind('<Control-s>', save_imageinfo)
root.bind('<Control-Key-1>', draw_color)
root.bind('<Control-Key-2>', draw_area)
root.bind('<Control-Key-3>', draw_gradient)
root.bind('<Control-Key-4>', draw_stars)
root.bind('<Control-Key-5>', draw_image)
root.bind('<Control-Key-6>', draw_points)
root.bind('<Control-Key-7>', draw_threecolors)
root.bind('<Control-q>', draw_comic)
root.bind('<Control-w>', draw_polygon)
root.bind('<Control-e>', draw_figure)
root.bind('<Control-r>', draw_line)
root.bind('<Control-t>', draw_oval)
root.bind('<Control-z>', draw_arc)
root.bind('<Control-u>', draw_stroke)

l_creator = tk.Label(root, text='by Karmmah', font='Consolas 10 ', bg='#666666', fg='#888888')
l_creator.grid(row=3, column=7)

root.mainloop()
