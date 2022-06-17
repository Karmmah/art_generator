#start:FF0000-green'-red,-blue'-green,-red'-blue, (' goes up; , goes down)

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

def get_color(h,s,l): #hue in [0,360], value in [0,100], saturation in [0,100]
	color = calc_hue(h)
	color = calc_saturation(color,s)
	color = calc_luminance(color,l)
	return color

def get_monochromatic(hue,saturation,luminance):
	variation = 0.15
	color1 = get_color(hue*(1-variation),saturation,luminance)
	color2 = get_color(hue,saturation,luminance)
	color3 = get_color(hue*(1+variation),saturation,luminance)
	return [color1,color2,color3]

def get_analogous(hue,saturation,luminance):
	variation = 360/12
	hue2 = hue-variation if hue-variation>0 else hue+variation+360
	hue3 = hue+variation if hue+variation<360 else hue+variation-360
	color1 = get_color(hue,saturation,luminance)
	color2 = get_color(hue2,saturation,luminance)
	color3 = get_color(hue3,saturation,luminance)
	return [color1,color2,color3]

def get_complementary(hue,saturation,luminance):
	hue2 = hue+180 if hue+180<360 else hue+180-360
	color1 = get_color(hue,saturation,luminance)
	color2 = get_color(hue2,saturation,luminance)
	return [color1,color2]

def get_tetradic(hue,saturation,luminance):
	hue2 = hue+90 if hue+90<360 else hue+90-360
	hue3 = hue+180 if hue+180<360 else hue+180-360
	hue4 = hue+270 if hue+270<360 else hue+270-360
	color1 = get_color(hue,saturation,luminance)
	color2 = get_color(hue2,saturation,luminance)
	color3 = get_color(hue3,saturation,luminance)
	color4 = get_color(hue4,saturation,luminance)
	return [color1,color2,color3,color4]

def get_triadic(hue,saturation,luminance): #hue = 0 => red
	hue2 = hue+120 if hue+120 <= 360 else hue+120-360
	hue3 = hue+240 if hue+240 <= 360 else hue+240-360
	color1 = get_color(hue,saturation,luminance)
	color2 = get_color(hue2,saturation,luminance)
	color3 = get_color(hue3,saturation,luminance)
	return [color1,color2,color3]

def calc_luminance(color,luminance):
	red,green,blue = color[1:3],color[3:5],color[5:7]
	array = [int(red,16),int(green,16),int(blue,16)]
	for i in range(len(array)):
		change = (luminance-50)/50
		distance = array[i] if change<0 else 255-array[i]
		color = hex(int(round(array[i]+change*distance))).lstrip("0x")
		while len(color)<2:
			color = "0"+color
		array[i] = color
	return "#"+array[0]+array[1]+array[2]

def calc_saturation(color,saturation):
	red,green,blue = color[1:3],color[3:5],color[5:7]
	array = [int(red,16),int(green,16),int(blue,16)]
	for i in range(len(array)):
		distance = array[i]-127
		color = hex(int(round(127+distance*saturation/100))).lstrip("0x")
		while len(color)<2:
			color = "0"+color
		array[i] = color
	return "#"+array[0]+array[1]+array[2]

def calc_hue(angle):
	if angle > 300 or angle <= 60:
		red = 'ff'
	elif angle > 60 and angle <= 120:
		red = hex(int(255*(120-angle)/60)).lstrip('-0x')
	elif angle > 120 and angle <= 240:
		red = '00'
	else:
		red = hex(int(255*(angle-240)/60)).lstrip('-0x')
	while len(red)<2:
		red = '0'+red

	#green
	if angle <= 60:
		green = hex(int(255*angle/60)).lstrip('-0x')
	elif angle > 60 and angle <= 180:
		green = 'ff'
	elif angle > 180 and angle <= 240:
		green = hex(int(255*(240-angle)/60)).lstrip('-0x')
	else:
		green = '00'
	while len(green)<2:
		green = '0'+green

	#blue
	if angle <= 120:
		blue = '00'
	elif angle > 120 and angle <= 180:
		blue = hex(int(255*(angle-120)/60)).lstrip('-0x')
	elif angle > 180 and angle <= 300:
		blue = 'ff'
	else:
		blue = hex(int(255*(360-angle)/60)).lstrip('-0x')
	while len(blue)<2:
		blue = '0'+blue
	color = '#'+red+green+blue
	return color

def draw_colorcircle(radius,width,offset,saturation,luminance):
	border = 10+width/2
	for i in range(360):
		if i+offset > 360:
			angle = i+offset
			angle = angle-360
		else:
			angle = i+offset
		color = get_color(angle,saturation,luminance)
		try:
			canvas.create_arc(cwidth/2-radius,cheight/2-radius,cwidth/2+radius,cheight/2+radius, start=i, extent=1, fill='', outline=color, style='arc', width=width)
#			canvas.create_arc(border,border,cwidth-border,cheight-border, start=i, extent=1, fill='', outline=color, style='arc', width=width)
		except:
			print(angle,'canvas error')

import tkinter

def main2(): #draw static color circle fading to grey towards the middle
#	canvas.delete('all')
	global root,canvas,cwidth,cheight
	cwidth = 600
	cheight = cwidth
	root = tkinter.Tk()
	canvas = tkinter.Canvas(root, width=cwidth, height=cheight)
	canvas.pack()
	border = 10 #pixels from canvas edge

	amount = 40
	width = (cwidth-2*border)/2/amount
	for i in range(amount):
		radius = (width/2+(amount-1)*width)-i*width
		draw_colorcircle(radius,width+1,0,100-i*100/amount,50)

	root.mainloop()

def main(): #draw rotating color circle with additional color tiles
	global root,canvas,cwidth,cheight
	cwidth = 600
	cheight = cwidth

	root = tkinter.Tk()
	canvas = tkinter.Canvas(root, width=cwidth, height=cheight)
	canvas.pack()
	f_color1 = tkinter.Label(root)
	f_color2 = tkinter.Label(root)
	f_color3 = tkinter.Label(root)
	f_color1.place(relx=0.4,rely=0.5,relwidth=0.1,relheight=0.1,anchor="s")
	f_color2.place(relx=0.5,rely=0.5,relwidth=0.1,relheight=0.1,anchor="s")
	f_color3.place(relx=0.6,rely=0.5,relwidth=0.1,relheight=0.1,anchor="s")

	offset = 0
	width = int(cwidth/4)
	radius = cwidth*2/6
	while True:
		canvas.delete('all')
		if offset >= 360:
			offset = 0
		draw_colorcircle(radius,width,offset,100,50)
		colors = get_triadic(offset,100,50)
		f_color1["bg"],f_color2["bg"],f_color3["bg"] = colors[0],colors[1],colors[2]
		root.update()
		offset += 2

	root.mainloop()

if __name__ == "__main__":
	choice = input("1 or 2? ")
	if choice == "1":
		main()
	else:
		main2()
