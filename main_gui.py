# load Libs
from tgnLIB import *
from tkinter import *
import PIL
from PIL import Image, ImageTk
#MCP23017 I2C
mcp = MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
mcp.config(0, 0)
mcp.config(1, 0)
mcp.config(2, 0)
mcp.config(3, 0)
mcp.pullup(4, 1)
mcp.pullup(5, 1)
mcp.pullup(6, 1)
mcp.pullup(7, 1)
#LCD
mylcd = lcd()
# var
counterLCD = 0
backlight = 1
LCDpower = 1
screen = 0
buttons = []
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
bground = "black"
fground = "green"
abground = "gray"
afground = "green"
afbground = "green"
buttona = "blue"
buttonb = "green"
colorSet = 1
s1 = 0
s2 = 0
s3 = 0
s4 = 0
son = 0
soff = 0
ontime = "10:19|10:21"
offtime = "10:20|10:22"
phat = "/home/pi/tgn_smart_home/icons/"
#PiHole
api_url = 'http://localhost/admin/api.php'
#functions
def save_settings():
	write_eeprom(1,0x54,0x00,0x01,str(b1))
	write_eeprom(1,0x54,0x00,0x02,str(b2))
	write_eeprom(1,0x54,0x00,0x03,str(b3))
	write_eeprom(1,0x54,0x00,0x04,str(b4))
	write_eeprom(1,0x54,0x00,0x05,str(b5))
	write_eeprom(1,0x54,0x00,0x06,str(b6))

def ini():
	mylcd.backlight(0)
	time.sleep(1)
	mylcd.lcd_clear()
	time.sleep(2)
	mylcd.backlight(1)
	mylcd.lcd_display_string("TGN Smart Home", 1, 1)
	mylcd.lcd_display_string("V1.6 Loading....", 2, 0)
	global ontime
	global offtime
	global s1
	global s2
	global s3
	global s4
	global ondays
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	global colorSet
	global bground
	global fground
	global abground
	global afground
	global afbground
	global buttona
	global buttonb
	global screen
	start_add_C = 0x2a
	index = 0 
	b1A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_C)
		if cach != "X":
			b1A = b1A + cach
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_D = 0x34
	index = 0 
	b2A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_D)
		if cach != "X":
			b2A = b2A + cach
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_E = 0x3e
	index = 0 
	b3A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_E)
		if cach != "X":
			b3A = b3A + cach
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_F = 0x48
	index = 0 
	b4A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_F)
		if cach != "X":
			b4A = b4A + cach
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_G = 0x52
	index = 0 
	b5A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_G)
		if cach != "X":
			b5A = b5A + cach
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_H = 0x5c
	index = 0 
	b6A = ""
	while index < 10:
		cach = read_eeprom(1,0x54,0x00,start_add_H)
		if cach != "X":
			b6A = b6A + cach
		index = index + 1
		start_add_H = start_add_H + 1
	buttons.append(b1A)
	buttons.append(b2A)
	buttons.append(b3A)
	buttons.append(b4A)
	buttons.append(b5A)
	buttons.append(b6A)
	s1 = read_eeprom(1,0x54,0x00,0x08)
	s2 = read_eeprom(1,0x54,0x00,0x09)
	s3 = read_eeprom(1,0x54,0x00,0x0a)
	s4 = read_eeprom(1,0x54,0x00,0x0b)
	start_add_A = 0x0c
	index = 0 
	ontime = ""
	while index < 11:
		cach = read_eeprom(1,0x54,0x00,start_add_A)
		if cach != "X":
			ontime = ontime + cach
		index = index + 1
		start_add_A = start_add_A + 1	
	start_add_B = 0x18
	index = 0 
	offtime = ""
	while index < 11:
		cach = read_eeprom(1,0x54,0x00,start_add_B)
		if cach != "X":
			offtime = offtime + cach
		index = index + 1
		start_add_B = start_add_B + 1
	print("%d: %x" % (4, mcp.input(4) >> 4))
	print("%d: %x" % (5, mcp.input(5) >> 5))
	print("%d: %x" % (6, mcp.input(6) >> 6))
	print("%d: %x" % (7, mcp.input(7) >> 7))
	mcp.output(0, 1)
	time.sleep(0.5)
	mcp.output(1, 1)
	time.sleep(0.5)
	mcp.output(2, 1)
	time.sleep(0.5)
	mcp.output(3, 1)
	time.sleep(0.5)
	mcp.output(0, 0)
	mcp.output(1, 0)
	mcp.output(2, 0)
	mcp.output(3, 0)
	dataX = read_eeprom(1,0x54,0x00,0x01)
	b1=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x02)
	b2=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x03)
	b3=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x04)
	b4=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x05)
	b5=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x06)
	b6=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x07)
	colorSet=int(dataX)
	dataX = read_eeprom(1,0x54,0x00,0x67)
	screen=int(dataX)
	f = open("/home/pi/tgn_smart_home/config/themes.config","r")
	data = []
	for line in f:
		data.append(line)
	if colorSet == 1:
		startLine = 1
	else:
		startLine = ((colorSet - 1)*8)+1
	c1 = (data[startLine].rstrip())
	c2 = (data[(startLine+1)].rstrip())
	c3 = (data[(startLine+2)].rstrip())
	c4 = (data[(startLine+3)].rstrip())
	c5 = (data[(startLine+4)].rstrip())
	c6 = (data[(startLine+5)].rstrip())
	c7 = (data[(startLine+6)].rstrip())
	d,bground = c1.split("=")
	d,fground = c2.split("=")
	d,abground = c3.split("=")
	d,afground = c4.split("=")
	d,afbground = c5.split("=")
	d,buttona = c6.split("=")
	d,buttonb = c7.split("=")
	mylcd.lcd_clear()

def on():
	global son
	global soff
	if son == 0:
		soff = 0
		son = 1
		msg = "Automatic_on"
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		if s1 == 1:
			send(1,1)
			time.sleep(1)
			b1 = 1
		if s2 == 1:
			send(2,1)
			time.sleep(1)
			b2 = 1
		if s3 == 1:
			send(3,1)
			time.sleep(1)
			b3 = 1
		if s4 == 1:
			send(4,1)
			b4 = 1
	save_settings()

def off():
	global son
	global soff
	if soff == 0:
		soff = 1
		son = 0
		msg = "Automatic_off"
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		if s1 == 1:
			send(1,0)
			time.sleep(1)
			b1 = 0
		if s2 == 1:
			send(2,0)
			time.sleep(1)
			b2 = 0
		if s3 == 1:
			send(3,0)
			time.sleep(1)
			b3 = 0
		if s4 == 1:
			send(4,0)
			b4 = 0
	save_settings()

def pcf8563ReadTimeB():
	t = bus.read_i2c_block_data(address,register,7);
	t[0] = t[0]&0x7F  #sec
	t[1] = t[1]&0x7F  #min
	t[2] = t[2]&0x3F  #hour
	t[3] = t[3]&0x3F  #day
	t[4] = t[4]&0x07  #month   -> dayname
	t[5] = t[5]&0x1F  #dayname -> month
	cach = ("%x:%x" %(t[2],t[1]))
	on1,on2 = ontime.split("|")
	off1,off2 = offtime.split("|")
	ond = "yes"
	if ond == "yes" and cach == on1 or cach == on2:
		on()
	if ond == "yes" and cach == off1 or cach == off2:
		off()
	return("%s  20%x/%x/%x %x:%x:%x" %(w[t[4]],t[6],t[5],t[3],t[2],t[1],t[0]))

def About():
    print("Main Controll V.1.4")
def callback1():
	setn = "python /home/pi/tgn_smart_home/libs/auto_cam.py video "+E1.get()
	os.system(setn)
def callback2():
	setn = "python /home/pi/tgn_smart_home/libs/auto_cam.py capture 0"
	os.system(setn)
def callback3():
	setn = "lxterminal -e python /home/pi/tgn_smart_home/libs/auto_cam.py timer 0"
	os.system(setn)
def callback4():
	setn = "lxterminal -e python /home/pi/tgn_smart_home/libs/camGpio.py"
	os.system(setn)
def callback5():
	setn = "python /home/pi/tgn_smart_home/libs/auto_cam.py preview 0"
	os.system(setn)
def callback6():
	stream()
def callback7():
	setn = "lxterminal -e python2 /home/pi/tgn_smart_home/libs/digi-cam.py"
	os.system(setn)
def callback8():
	mcp.output(3, 0)
	mcp.output(2, 1)
	setRTC()
	time.sleep(5)
	mcp.output(2, 0)
	mcp.output(3, 1)
def callback9():
	global b1
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b1 == 0:
		msg = "Turn_on_" + buttons[0]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(1,1)
		b1 = 1
	else:
		msg = "Turn_off_" + buttons[0]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(1,0)
		b1 = 0
	write_eeprom(1,0x54,0x00,0x01,str(b1))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback10():
	global b2
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b2 == 0:
		msg = "Turn_on_" + buttons[1]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(2,1)
		b2 = 1
	else:
		msg = "Turn_off_" + buttons[1]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(2,0)
		b2 = 0
	write_eeprom(1,0x54,0x00,0x02,str(b2))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback11():
	global b3
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b3 == 0:
		msg = "Turn_on_" + buttons[2]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(3,1)
		b3 = 1
	else:
		msg = "Turn_off_" + buttons[2]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(3,0)
		b3 = 0
	write_eeprom(1,0x54,0x00,0x03,str(b3))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback12():
	global b4
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b4 == 0:
		msg = "Turn_on_" + buttons[3]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(4,1)
		b4 = 1
	else:
		msg = "Turn_off_" + buttons[3]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(4,0)
		b4 = 0
	write_eeprom(1,0x54,0x00,0x04,str(b4))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback13():
	global b5
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b5 == 0:
		msg = "Turn_on_" + buttons[4]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(5,1)
		b5 = 1
	else:
		msg = "Turn_off_" + buttons[4]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(5,0)
		b5 = 0
	write_eeprom(1,0x54,0x00,0x05,str(b5))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback14():
	global b6
	mcp.output(3, 0)
	mcp.output(2, 1)
	if b6 == 0:
		msg = "Turn_on_" + buttons[5]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(6,1)
		b6 = 1
	else:
		msg = "Turn_off_" + buttons[5]
		print(msg)
		os.system('sudo bash /home/pi/tgn_smart_home/libs/pushbullet.sh ' + msg)
		send(6,0)
		b6 = 0
	write_eeprom(1,0x54,0x00,0x06,str(b6))
	mcp.output(3, 1)
	mcp.output(2, 0)
def callback15():
	mcp.output(3, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	from subprocess import call
	call(['shutdown', '-h', 'now'], shell=False)
def callback16():
	mcp.output(3, 0)
	mylcd.lcd_clear()
	mylcd.backlight(0)
	from subprocess import call
	call(['reboot', '-h', 'now'], shell=False)
def callback17():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py rtc"
	os.system(setn)
def callback18():
	setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py funk"
	os.system(setn)
def callback19():
	global screen
	if screen == 1:
		screen = 0
	else:
		screen = 1
	write_eeprom(1,0x54,0x00,0x67,str(screen))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def callback20():
	global LCDpower
	if LCDpower == 1:
		LCDpower = 0
		mylcd.lcd_clear()
		mylcd.backlight(0)
	else:
		LCDpower = 1
		mylcd.lcd_display_string("TGN Smart Home", 1, 1)
		mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
		mylcd.backlight(1)
def callback21():
	global backlight
	if backlight == 1:
		backlight = 0
		mylcd.backlight(0)
	else:
		backlight = 1
		mylcd.backlight(1)
# updating window (Clock and Temps)
the_time=''
TIME = newtime = time.time()
class Window(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			global the_time
			global counterLCD
			newtime = time.time()
			if newtime != the_time:
				if mcp.input(7) >> 7 == 1:
					print("exit")
					mcp.output(3, 0)
					mylcd.lcd_clear()
					mylcd.backlight(0)
					root.quit()
				if mcp.input(4) >> 4 == 1:
					callback7()
				if mcp.input(5) >> 5 == 1:
					callback12()
				stats = 'Switch:'
				if b1 == 0:
					stats=stats+'OFF|'
				if b1 == 1:
					stats=stats+'On|'
				if b2 == 0:
					stats=stats+'OFF|'
				if b2 == 1:
					stats=stats+'On|'
				if b3 == 0:
					stats=stats+'OFF|'
				if b3 == 1:
					stats=stats+'On|'
				if b4 == 0:
					stats=stats+'OFF|'
				if b4 == 1:
					stats=stats+'On|'
				if b5 == 0:
					stats=stats+'OFF|'
				if b5 == 1:
					stats=stats+'On|'
				if b6 == 0:
					stats=stats+'OFF|'
				if b6 == 1:
					stats=stats+'On|'
				counterLCD = counterLCD + 1
				if counterLCD == 30 and LCDpower == 1:
					mylcd.lcd_clear()
					mylcd.lcd_display_string("TGN Smart Home", 1, 1)
					mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
				if counterLCD == 60 and LCDpower == 1:
					mylcd.lcd_clear()
					r = requests.get(api_url)
					dataPIhole = json.loads(r.text)
					DNSQUERIES = dataPIhole['dns_queries_today']
					ADSBLOCKED = dataPIhole['ads_blocked_today']
					CLIENTS = dataPIhole['unique_clients']
					mylcd.lcd_display_string("Ad Blocked:"+str(ADSBLOCKED), 1, 0)
					mylcd.lcd_display_string("Queries:"+str(DNSQUERIES), 2, 0)
					counterLCD = 0
				if backlight == 0 and LCDpower == 1:
					mylcd.backlight(0)
				the_time= pcf8563ReadTimeB()+"\nCPU:"+str(getCpuTemperature())+"°C\n"+stats
				self.display_time.config(text=the_time, font=('times', 20, 'bold'), bg=afbground)
			self.display_time.after(1000, change_value_the_time)
		change_value_the_time()
# updating window (Weather and PiHole)
class WindowB(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			global the_time
			newtime = time.time()
			if newtime != the_time:
				r = requests.get(api_url)
				dataPIhole = json.loads(r.text)
				DNSQUERIES = dataPIhole['dns_queries_today']
				ADSBLOCKED = dataPIhole['ads_blocked_today']
				CLIENTS = dataPIhole['unique_clients']
				temp_data = get_dht11()
				data = weather_info(6947479)
				m_symbol = '\xb0' + 'C'
				output = '---------------------------------------\n'
				output = output+'Current weather in: '+data['city']+','+data['country']+'\n'
				output = output+str(data['temp'])+'°C  '+data['sky']+'\n'
				output = output+'Max:'+str(data['temp_max'])+'°C, Min:'+str(data['temp_min'])+'°C\n'
				output = output+'\n'
				output = output+'Wind Speed:'+str(data['wind'])+'km/h \n'
				output = output+'Humidity:'+str(data['humidity'])+'% \n'
				output = output+'Cloud:'+str(data['cloudiness'])+'% \n'
				output = output+'Pressure:'+str(data['pressure'])+'hpa \n'
				output = output+'Sunrise at:'+str(data['sunrise'])+'\n'
				output = output+'Sunset at:'+str(data['sunset'])+'\n'
				output = output+'Icon ID:'+str(data['icon'])+'\n'
				output = output+'Last update from the server:'+str(data['dt'])+'\n'
				output = output+'---------------------------------------\n'
				output = output+temp_data+'\n'
				output = output+'---------------------------------------\n'
				output = output+'Ad Blocked:'+str(ADSBLOCKED)+' Client:'+str(CLIENTS)+' DNS Queries:'+str(DNSQUERIES)
				self.display_time.config(text=output, font=('times', 17, 'bold'), bg=afbground)
				phatI = phat+get_icon_name(str(data['icon']))
				load = Image.open(phatI)
				render = ImageTk.PhotoImage(load)
				img = Label(self, image=render)
				img.image = render
				img.config(bg=afbground)
				img.place(x=0, y=150)
			self.display_time.after(3600000, change_value_the_time)
		change_value_the_time()
def st1():
	global colorSet
	colorSet = 1
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st2():
	global colorSet
	colorSet = 2
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st3():
	global colorSet
	colorSet = 3
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st4():
	global colorSet
	colorSet = 4
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st5():
	global colorSet
	colorSet = 5
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
def st6():
	global colorSet
	colorSet = 6
	write_eeprom(1,0x54,0x00,0x07,str(colorSet))
	time.sleep(1)
	os.execv(sys.executable, ['python3'] + sys.argv)
#Main Prog
ini()
mylcd.lcd_display_string("TGN Smart Home", 1, 1)
mylcd.lcd_display_string("IP:"+get_ip(), 2, 0)
mcp.output(3, 1)
root = Tk()
#fullscreen mode
WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
root.overrideredirect(screen) 
root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))

root.wm_title("Main Control IP:"+get_ip())
menu = Menu(root)
root.config(background = bground, menu=menu)

filemenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
filemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Refresh Clock", command=callback8)
filemenu.add_command(label="Digi Cam", command=callback7)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

stylemenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
stylemenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="Color", menu=stylemenu)
stylemenu.add_command(label="Dark/Green", command=st1)
stylemenu.add_command(label="Gray", command=st2)
stylemenu.add_command(label="White/Gray", command=st3)
stylemenu.add_command(label="Gray/White", command=st4)
stylemenu.add_command(label="Blue/White", command=st5)
stylemenu.add_command(label="Blue/Green", command=st6)

setmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
setmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="Settings", menu=setmenu)
setmenu.add_command(label="Fullscreen", command=callback19)
setmenu.add_command(label="RTC Automatic", command=callback17)
setmenu.add_command(label="Remote Controll", command=callback18)

helpmenu = Menu(menu)
menubar = Menu(root, background=bground, foreground=fground,activebackground=abground, activeforeground=afground)
helpmenu = Menu(menubar, tearoff=0, background=bground,foreground=fground,activebackground=abground, activeforeground='white')
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

leftFrame = Frame(root, width=400, height = 400)
leftFrame.configure(background=bground)
leftFrame.grid(row=0, column=0, padx=10, pady=3)

infFrame1 = Frame(leftFrame)
infFrame1.configure(background=bground)
infFrame1.grid(row=0, column=0, padx=10, pady=3)
infLabel1 = Label(infFrame1, text="Weather Infos:")
infLabel1.configure(background=bground, foreground=fground)
infLabel1.grid(row=0, column=1, padx=10, pady=3)

rightFrame = Frame(root, width=400, height = 400)
rightFrame.configure(background=bground)
rightFrame.grid(row=0, column=1, padx=10, pady=3)

buttonFrame = Frame(rightFrame)
buttonFrame.configure(background=bground)
buttonFrame.grid(row=1, column=0, padx=10, pady=3)
buttonLabel1 = Label(buttonFrame, text="Camera Options")
buttonLabel1.configure(background=bground, foreground=fground)
buttonLabel1.grid(row=0, column=1, padx=10, pady=3)
buttonLabel2 = Label(buttonFrame, text="Record length:")
buttonLabel2.configure(background=bground, foreground=fground)
buttonLabel2.grid(row=1, column=0, padx=10, pady=3)
E1 = Entry(buttonFrame, width=18)
E1.grid(row=1, column=1, padx=10, pady=3)
B1 = Button(buttonFrame, text="Record", bg=buttona, width=15, command=callback1)
B1.grid(row=1, column=2, padx=10, pady=3)
B5 = Button(buttonFrame, text="Preview", bg=buttonb, width=15, command=callback5)
B5.grid(row=2, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame, text="Capture", bg=buttonb, width=15, command=callback2)
B2.grid(row=2, column=1, padx=10, pady=3)
B3 = Button(buttonFrame, text="Timer Capture", bg=buttonb, width=15, command=callback3)
B3.grid(row=2, column=2, padx=10, pady=3)
B4 = Button(buttonFrame, text="Motion Detector", bg=buttonb, width=15, command=callback4)
B4.grid(row=3, column=0, padx=10, pady=3)
B7 = Button(buttonFrame, text="Digi Cam", bg=buttonb, width=15, command=callback7)
B7.grid(row=3, column=1, padx=10, pady=3)
B6 = Button(buttonFrame, text="Stream", bg=buttonb, width=15, command=callback6)
B6.grid(row=3, column=2, padx=10, pady=3)

seperatorFrame = Frame(rightFrame)
seperatorFrame.configure(background=bground)
seperatorFrame.grid(row=2, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame1 = Frame(rightFrame)
buttonFrame1.configure(background=bground)
buttonFrame1.grid(row=3, column=0, padx=10, pady=3)
buttonLabel1 = Label(buttonFrame1, text="Home Control")
buttonLabel1.configure(background=bground, foreground=fground)
buttonLabel1.grid(row=0, column=1, padx=10, pady=3)

B1 = Button(buttonFrame1, text=buttons[0], bg=buttonb, width=15, command=callback9)
B1.grid(row=1, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame1, text=buttons[1], bg=buttonb, width=15, command=callback10)
B2.grid(row=1, column=1, padx=10, pady=3)
B3 = Button(buttonFrame1, text=buttons[2], bg=buttonb, width=15, command=callback11)
B3.grid(row=1, column=2, padx=10, pady=3)
B4 = Button(buttonFrame1, text=buttons[3], bg=buttonb, width=15, command=callback12)
B4.grid(row=2, column=0, padx=10, pady=3)
B5 = Button(buttonFrame1, text=buttons[4], bg=buttonb, width=15, command=callback13)
B5.grid(row=2, column=1, padx=10, pady=3)
B6 = Button(buttonFrame1, text=buttons[5], bg=buttonb, width=15, command=callback14)
B6.grid(row=2, column=2, padx=10, pady=3)

seperatorFrame1 = Frame(rightFrame)
seperatorFrame1.configure(background=bground)
seperatorFrame1.grid(row=4, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame1, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

infFrame1 = Frame(rightFrame)
infFrame1.configure(background=bground)
infFrame1.grid(row=5, column=0, padx=10, pady=3)
infLabel1 = Label(infFrame1, text="Timer Settings:")
infLabel1.configure(background=bground, foreground=fground)
infLabel1.grid(row=0, column=1, padx=10, pady=3)
oText1 = "Start:"+ontime
infLabel2 = Label(infFrame1, text=oText1)
infLabel2.configure(background=bground, foreground=fground)
infLabel2.grid(row=1, column=0, padx=10, pady=3)
oText2 = "End:"+offtime
infLabel3 = Label(infFrame1, text=oText2)
infLabel3.configure(background=bground, foreground=fground)
infLabel3.grid(row=1, column=2, padx=10, pady=3)
oText3 = "Automatic:"+s1+s2+s3+s4
infLabel4 = Label(infFrame1, text=oText3)
infLabel4.configure(background=bground, foreground=fground)
infLabel4.grid(row=1, column=1, padx=10, pady=3)

app=Window(rightFrame)

seperatorFrame2 = Frame(rightFrame)
seperatorFrame2.configure(background=bground)
seperatorFrame2.grid(row=7, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame2, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame2 = Frame(rightFrame)
buttonFrame2.configure(background=bground)
buttonFrame2.grid(row=8, column=0, padx=10, pady=3)
buttonLabel2 = Label(buttonFrame2, text="System Control")
buttonLabel2.configure(background=bground, foreground=fground)
buttonLabel2.grid(row=0, column=1, padx=10, pady=3)

B1 = Button(buttonFrame2, text="Shutdown", bg=buttonb, width=15, command=callback15)
B1.grid(row=1, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame2, text="Reboot", bg=buttonb, width=15, command=callback16)
B2.grid(row=1, column=1, padx=10, pady=3)
B3 = Button(buttonFrame2, text="Exit", bg=buttonb, width=15, command=root.quit)
B3.grid(row=1, column=2, padx=10, pady=3)

app=WindowB(leftFrame)

seperatorFrame3 = Frame(leftFrame)
seperatorFrame3.configure(background=bground)
seperatorFrame3.grid(row=2, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame3, text="")
seperatorLabel1.configure(background=bground)
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame3 = Frame(leftFrame)
buttonFrame3.configure(background=bground)
buttonFrame3.grid(row=3, column=0, padx=10, pady=3)

B1 = Button(buttonFrame3, text="LCD On/Off", bg=buttonb, width=15, command=callback20)
B1.grid(row=0, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame3, text="LCD Backlight", bg=buttonb, width=15, command=callback21)
B2.grid(row=0, column=1, padx=10, pady=3)

root.mainloop()