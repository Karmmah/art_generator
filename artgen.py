#parameters
cwidth, cheight = 300, 300 #width and height of canvas
output_width, output_height = 1080, 1080 #dimensions of output svg file
xborder, yborder = 10, 10 #distance from canvas edge to keep free from shapes
frame_padding = 7 #distance between selector frames
default_background_color = "#fafafa"
default_background = '\n	<rect x="0" y="0" width="'+str(output_width)+'" height="'+str(output_height)+'" fill="'+default_background_color+'" stroke=""/>'

import artgen_tools, artgen_drawing #imported after parameter declaration because modules need these parameters

def test_output():
	print(collect_svg())

def test(): #delete after testing
	global canvas,svg
#	canvas = artgen_tools.draw_line(canvas,[coords])
	canvas,string = artgen_drawing.draw_rectangle(canvas,fill=artgen_tools.get_color(),width=2)#,color="#fedcba")
	svg += string
	return canvas

def draw_image(): #main method for drawing a whole random image by drawing a background and multiple shapes
	pass

def add_single(): #main method for adding one shape to the canvas
	pass

def add_multi(): #main method for adding multiple shapes to canvas by calling the single method multiple times
	pass #a slider is needed to roughly specify how many shapes to add

def draw_background(): #main method for drawing a background
	pass

def reset_basic(): #reset checkmarks in basic shape section
	global rect_var,line_var
	rect_var.set(False)
	line_var.set(False)

def reset_complex():
	pass

def reset_graphics():
	pass

def reset_backgrounds():
	pass

def save():
	name = "kunstwerk"+str(artgen_tools.artwork_number())+".svg"
	with open(name) as file:
		file.write(collect_svg())

def delete_canvas():
	canvas.delete("all")
	canvas.create_rectangle(0,0,cwidth,cheight,fill=default_background_color,outline="")
	global svg
	svg = default_background

#def get_canvas_objects(): #interesting method used for nothing
#	objects = canvas.find_all()
#	for item in objects:
#		print(canvas.coords(item))
#	return objects

def collect_svg(): #format the saved svg information of all objects on canvas into proper svg file
	global svg
	number = artgen_tools.artwork_number()
	docinfo = '<svg width="'+str(output_width)+'px" height="'+str(output_height)+'px" docname="kunstwerk'+str(number)+'.svg">'
	output = docinfo+svg+'\n</svg>'
	return output

def main():
	import tkinter

	root = tkinter.Tk()

	f_creator = tkinter.Frame(root,bg="blue")
	f_selector = tkinter.Frame(root,bg="red",width=100,height=100)

	global canvas, svg
	svg = default_background #variable for saving info for each created shape on canvas for svg export

	canvas = tkinter.Canvas(f_creator, width=cwidth, height=cheight)
	canvas.create_rectangle(0,0,cwidth,cheight, fill=default_background_color, outline="")

	b_test = tkinter.Button(f_creator, text="test", command=test)
	b_output = tkinter.Button(f_creator, text="output", command=test_output)

#	l_seed = tkinter.Label(f_creator, text="Input Seed")
#	e_seed = tkinter.Entry(f_creator, state="disabled")

	f_backgrounds = tkinter.Frame(f_selector, bg="yellow", width=40, height=40)
	pass

	f_basic_shapes = tkinter.Frame(f_selector, bg="lightgreen", width=40, height=40)
	b_reset_basic = tkinter.Button(f_basic_shapes, text="reset", command=reset_basic)
	global rect_var,line_var
	rect_var = tkinter.BooleanVar()
	line_var = tkinter.BooleanVar()
	c_rectangle = tkinter.Checkbutton(f_basic_shapes, text="Rectangle", variable=rect_var)#, onvalue=1)
	c_line = tkinter.Checkbutton(f_basic_shapes, text="Line", variable=line_var)#, onvalue=1)

	f_complex_shapes = tkinter.Frame(f_selector, bg="skyblue", width=40, height=40)
	pass

	f_graphics = tkinter.Frame(f_selector, bg="orange", width=40, height=40)
	pass

	b_save = tkinter.Button(f_creator, text="save", command=save, bg="gold")
	b_delete = tkinter.Button(f_creator, text="delete", command=delete_canvas, bg="#ff4040")

	#alignment and grids
	#frames:
	f_creator.grid(row=0, column=0)
	f_selector.grid(row=0, column=1)
	#inside f_creator:
	canvas.grid(row=0, columnspan=2)
	b_test.grid(row=1, column=0)
	b_output.grid(row=1, column=1)
	b_save.grid(row=99, column=0)
	b_delete.grid(row=99, column=1)
	#inside f_selector:
	f_backgrounds.grid(row=0, column=0, padx=frame_padding, pady=frame_padding)
	f_basic_shapes.grid(row=0, column=1, padx=frame_padding, pady=frame_padding)
	f_complex_shapes.grid(row=1, column=0, padx=frame_padding, pady=frame_padding)
	f_graphics.grid(row=1, column=1, padx=frame_padding, pady=frame_padding)
	#inside f_backgrounds:
	pass
	#inside f_basic_shapes:
	b_reset_basic.pack()
	c_line.pack(anchor="nw")
	c_rectangle.pack(anchor="nw")
	#inside f_complex_shapes:
	pass
	#inside f_graphics:
	pass

	root.mainloop()

if __name__ == "__main__":
	main()