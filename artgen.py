#parameters
cwidth, cheight = 300,300

import artgen_tools

def test_output(): #delete after testing
	print(collect_svg())

def test(): #delete after testing
	global canvas,svg
	import random
	coords = [random.randint(0,cwidth),random.randint(0,cheight),random.randint(0,cwidth),random.randint(0,cheight)]
#	canvas = artgen_tools.draw_line(canvas,[coords])
	canvas,string = artgen_tools.draw_line(canvas,width=2)#,color="#fedcba")
	svg += string
	return canvas

def collect_svg():
	global svg
	docinfo = '<svg width="'+str(cwidth)+'px" height="'+str(cheight)+'px" docname="svgoutput.svg">'
	content = '\n<g>'+svg+'\n</g>'
	output = docinfo+content+'\n</svg>'
	return output

def get_canvas_dimensions(): #method for external modules to receive canvas parameters
	return cwidth, cheight

def main():
	import tkinter

	root = tkinter.Tk()

	global canvas,svg
	svg = "" #variable for saving each created shape  on canvas for svg export
	canvas = tkinter.Canvas(width=cwidth,height=cheight)
	canvas.pack()

	b_test = tkinter.Button(root,text="test",command=test)
	b_test.pack()
	b_output = tkinter.Button(root,text="output",command=test_output)
	b_output.pack()

	root.mainloop()

if __name__ == "__main__":
	main()