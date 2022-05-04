# artgen in gui, random generation und drawing to canvas aufteilen
# separate modi für "filled" und "outline"
# auswahlfelder welche backgrounds und shapes für ganzes bild verwendet werden

import tkinter

#user parameters
pwidth = 1000 #program width
pheight = 500
cwidth = 1080 #canvas width
cheight = cwidth
default_border = 100
left_column_width = 250
right_column_width = left_column_width

def get_window_info(window): #get size and position of given window
	array = window.geometry().split("+")
	info = array[0].split("x")+array[1:3]
	print(info)
	return info

#gui
root = tkinter.Tk()
root.geometry(str(left_column_width+cwidth+right_column_width)+"x"+str(cheight))

#frame_left_width = left_column_width/(left_column_width+cwidth+right_column_width)
#frame_right_width = right_column_width/(left_column_width+cwidth+right_column_width)
#f_left = tkinter.Frame(root,bg="darkgrey")
#f_right = tkinter.Frame(root,bg="grey")
#f_left.place(anchor="nw",relwidth=frame_left_width,relheight=1)
#f_right.place(relx=1,anchor="ne",relwidth=frame_right_width,relheight=1)

canvas = tkinter.Canvas(root,width=cwidth,height=cheight,bg="black")
relheight = get_window_info(root)
canvas.place(relx=0.05,rely=0.12,relwidth=0.2)

canvas.create_line(0,0,cwidth,cheight,fill="red")
canvas.create_line(cwidth,0,0,cheight,fill="red")

root.mainloop()
