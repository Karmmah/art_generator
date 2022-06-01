#parameters
cwidth, cheight = 400, 400 #width and height of canvas
output_width, output_height = 1080, 1080 #dimensions of output svg file
xborder, yborder = 10, 10 #distance from canvas edge to keep free from shapes
frame_padding = 7 #distance between selector frames
default_background_color = "#fafafa"
default_background = '\n	<rect x="0" y="0" width="'+str(output_width)+'" height="'+str(output_height)+'" fill="'+default_background_color+'" stroke=""/>'

#button numbering
background_number = 1
single_number = 2
multiple_number = 3
delete_number = 9
save_number = 0

import random, artgen_tools, artgen_drawing #imported after parameter declaration because modules need these parameters

def draw_image(): #main method for drawing a whole random image by drawing a background and multiple shapes or some graphics
	pass

def add_single(event=""): #main method for adding one shape to the canvas
	global canvas,svg
	number = random.randint(1,30)
	if check_selection() == True: #check if at least one shape and one background are selected
		while number>=0:
			if line_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_line(canvas)
					break
				number -= 1
			if rectangle_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_rectangle(canvas)
					break
				number -= 1
			if polygon_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_polygon(canvas)
					break
				number -= 1
			if net_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_net(canvas)
					break
				number -= 1
			if symmetry_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_symmetry(canvas)
					break
				number -= 1
			if circular_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_circular_pattern(canvas)
					break
				number -= 1
		svg += string

def add_multiple(event=""): #main method for adding multiple shapes to canvas by calling the single method multiple times
	amount = random.randint(2,6)
	for i in range(amount):
		add_single()
	pass #a slider is needed to roughly specify how many shapes to add

def draw_background(event=""): #main method for drawing a background
	global canvas,svg
	canvas.delete('all')
	svg = ""
	number = random.randint(1,10)
	if check_selection() == True: #check if at least one shape and one background are selected
		while number>=0:
			if color_var.get() == True:
				if number<=0:
					canvas,string = artgen_drawing.draw_color(canvas)
					break
				number -= 1
#			if xxxxx_var.get() == True:
#				if number<=0:
#					canvas,string = artgen_drawing.draw_rectangle(canvas)
#					break
#				number -= 1
		svg += string

def reset_basic(): #reset checkmarks in basic shape section
	global rectangle_var,line_var,polygon_var
	rectangle_var.set(False)
	line_var.set(False)
	polygon_var.set(False)

def reset_complex():
	global net_var,symmetry_var
	net_var.set(False)
	symmetry_var.set(False)

def reset_graphics():
	pass

def reset_backgrounds():
	pass

def check_selection(): #check if at least one shape and one background is selected
	result_shapes = line_var.get()+rectangle_var.get()+polygon_var.get()
	result_background = color_var.get()
	result_complex = circular_var.get()+net_var.get()+symmetry_var.get()
	if result_background>0 and (result_shapes>0 or result_complex>0):
		return True
	else:
		print("Select at least one shape and one background")
		return False

def save(event=""):
	global mode_var
	number = artgen_tools.artwork_number(mode_var.get())
	name = "kunstwerk"+str(number)+".svg"
	with open(name,"w") as file:
		file.write(collect_svg(number))

def delete_canvas(event=""):
	canvas.delete("all")
	canvas.create_rectangle(0,0,cwidth,cheight,fill=default_background_color,outline="")
	global svg
	svg = default_background

#def get_canvas_objects(): #interesting method used for nothing
#	objects = canvas.find_all()
#	for item in objects:
#		print(canvas.coords(item))
#	return objects

def collect_svg(number): #format the saved svg information of all objects on canvas into proper svg file
	global svg
	docinfo = '<svg width="'+str(output_width)+'px" height="'+str(output_height)+'px" docname="kunstwerk'+str(number)+'.svg">'
	return docinfo+svg+'\n</svg>'

def main():
	import tkinter
	root = tkinter.Tk()

	f_creator = tkinter.Frame(root,bg="blue")
	f_selector = tkinter.Frame(root,bg="red",width=100,height=100)

	global canvas, svg
	svg = default_background #variable for saving info for each created shape on canvas for svg export

	canvas = tkinter.Canvas(f_creator, width=cwidth, height=cheight)
	canvas.create_rectangle(0,0,cwidth,cheight, fill=default_background_color, outline="")

#	l_seed = tkinter.Label(f_creator, text="Input Seed")
#	e_seed = tkinter.Entry(f_creator, state="disabled")

	#all variables for the checkbuttons
	global circular_var,symmetry_var,rectangle_var,line_var,color_var,polygon_var,net_var,mode_var

	b_background = tkinter.Button(f_creator, text="Background %i"%(background_number), command=draw_background)
	b_single = tkinter.Button(f_creator, text="Add One %i"%(single_number), command=add_single)
	b_multiple = tkinter.Button(f_creator, state="normal", text="Add Multiple %i"%(multiple_number), command=add_multiple)
	mode_var = tkinter.StringVar() #variable for changing the save mode to test (artwork number won't be increased on save)
	mode_var.set("normal")
	c_mode = tkinter.Checkbutton(f_creator, text="Test Export", variable=mode_var, onvalue="test", offvalue="normal")

	#backgrounds
	f_backgrounds = tkinter.Frame(f_selector, bg="yellow", width=40, height=40)
	b_reset_backgrounds = tkinter.Button(f_backgrounds, text="reset", command=reset_backgrounds)
	color_var = tkinter.IntVar()
	color_var.set(1)
	c_color = tkinter.Checkbutton(f_backgrounds, text="Color", variable=color_var)

	#basic shapes
	f_basic_shapes = tkinter.Frame(f_selector, bg="lightgreen", width=40, height=40)
	b_reset_basic = tkinter.Button(f_basic_shapes, text="reset", command=reset_basic)
	line_var = tkinter.BooleanVar()
	rectangle_var = tkinter.BooleanVar()
	rectangle_var.set(1)
	polygon_var = tkinter.BooleanVar()
	c_line = tkinter.Checkbutton(f_basic_shapes, text="Line", variable=line_var)
	c_rectangle = tkinter.Checkbutton(f_basic_shapes, text="Rectangle", variable=rectangle_var)
	c_polygon = tkinter.Checkbutton(f_basic_shapes, text="Polygon", variable=polygon_var)

	#complex shapes
	f_complex_shapes = tkinter.Frame(f_selector, bg="skyblue", width=40, height=40)
	b_reset_complex = tkinter.Button(f_complex_shapes, text="reset", command=reset_complex)
	net_var = tkinter.BooleanVar()
	symmetry_var = tkinter.BooleanVar()
	circular_var = tkinter.BooleanVar()
	c_net = tkinter.Checkbutton(f_complex_shapes, text="Net", variable=net_var)
	c_symmetry = tkinter.Checkbutton(f_complex_shapes, text="Symmetry", variable=symmetry_var)
	c_circular = tkinter.Checkbutton(f_complex_shapes, text="Circular Patter", variable=circular_var)

	#graphics
	f_graphics = tkinter.Frame(f_selector, bg="orange", width=40, height=40)
	pass

	#colorpalette
	f_colorpalette = tkinter.Frame(f_selector, bg="grey", width=40, height=40)
	pass

	b_save = tkinter.Button(f_creator, text="save %i"%(save_number), command=save, bg="gold")
	b_delete = tkinter.Button(f_creator, text="delete %i"%(delete_number), command=delete_canvas, bg="#ff4040")

	#alignment and grids
	#frames:
	f_creator.grid(row=0, column=0)
	f_selector.grid(row=0, column=1)
	#frames inside f_selector:
	f_backgrounds.grid(row=0, column=0, padx=frame_padding, pady=frame_padding)
	f_basic_shapes.grid(row=0, column=1, padx=frame_padding, pady=frame_padding)
	f_complex_shapes.grid(row=1, column=0, padx=frame_padding, pady=frame_padding)
	f_graphics.grid(row=1, column=1, padx=frame_padding, pady=frame_padding)
	f_colorpalette.grid(row=2, column=0, padx=frame_padding, pady=frame_padding)
	#inside f_creator:
	canvas.grid(row=0, columnspan=3)
	b_background.grid(row=1,column=0)
	b_single.grid(row=1, column=1)
	b_multiple.grid(row=1,column=2)
	b_save.grid(row=3, column=0)
	b_delete.grid(row=3, column=1)
	c_mode.grid(row=4,column=1)
	#inside f_backgrounds:
	b_reset_backgrounds.grid(row=0)
	c_color.grid(row=1,column=0)
	#inside f_basic_shapes:
	b_reset_basic.pack()
	c_line.pack(anchor="nw")
	c_rectangle.pack(anchor="nw")
	c_polygon.pack(anchor="nw")
	#inside f_complex_shapes:
	b_reset_complex.pack()
	c_net.pack(anchor="nw")
	c_symmetry.pack(anchor="nw")
	c_circular.pack(anchor="nw")
	#inside f_graphics:
	pass

	root.bind('<Key-%i>'%(background_number),draw_background)
	root.bind('<Key-%i>'%(single_number),add_single)
	root.bind('<Key-%i>'%(multiple_number),add_multiple)
	root.bind('<Key-%i>'%(delete_number),delete_canvas)

	root.mainloop()

if __name__ == "__main__":
	main()
