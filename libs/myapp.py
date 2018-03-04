import cherrypy
from tgnLIB import read_eeprom, write_eeprom, ifI2C, send

buttons = ["1","2","3","4","5","6"]
b1 = 0
b2 = 0
b3 = 0
b4 = 0
b5 = 0
b6 = 0
port_s = 1
ip_s = "127.0.0.1"
ROM_ADDRESS = 0x53
if ifI2C(ROM_ADDRESS) == "found device":
	start_add_X = 0x2b
	index = 0
	port_a = ""
	while index < 4:
		cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_X)
		if cach != "X":
			port_a = port_a + cach
		index = index + 1
		start_add_X = start_add_X + 1
	start_add_Z = 0x30
	index = 0
	ip_a = ""
	while index < 15:
		cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_Z)
		if cach != "X":
			ip_a = ip_a + cach
		index = index + 1
		start_add_Z = start_add_Z + 1
	port_s = int(port_a)
	ip_s = ip_a

	start_add_C = 0x2a
	index = 0
	b1A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_C)
		if cach != "X":
			b1A = b1A + cach
		index = index + 1
		start_add_C = start_add_C + 1
	start_add_D = 0x34
	index = 0 
	b2A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_D)
		if cach != "X":
			b2A = b2A + cach
		index = index + 1
		start_add_D = start_add_D + 1
	start_add_E = 0x3e
	index = 0 
	b3A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_E)
		if cach != "X":
			b3A = b3A + cach
		index = index + 1
		start_add_E = start_add_E + 1
	start_add_F = 0x48
	index = 0 
	b4A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_F)
		if cach != "X":
			b4A = b4A + cach
		index = index + 1
		start_add_F = start_add_F + 1
	start_add_G = 0x52
	index = 0 
	b5A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_G)
		if cach != "X":
			b5A = b5A + cach
		index = index + 1
		start_add_G = start_add_G + 1
	start_add_H = 0x5c
	index = 0 
	b6A = ""
	while index < 10:
		cach = read_eeprom(1,ROM_ADDRESS,0x00,start_add_H)
		if cach != "X":
			b6A = b6A + cach
		index = index + 1
		start_add_H = start_add_H + 1
	buttons = []
	buttons.append(b1A)
	buttons.append(b2A)
	buttons.append(b3A)
	buttons.append(b4A)
	buttons.append(b5A)
	buttons.append(b6A)

class tgn_smart_home(object):

	@cherrypy.expose
	def index(self):
		return """<html>
			<div align="center"><font size="5">
			<head>TGN Smart Home</head>
			<body>
			<form method="get" action="check">
			<input type="password" name="pw" />
			<button type="submit">Login</button>
			</form>
			</body>
			</html>"""

	@cherrypy.expose
	def check(self,pw=8):
		if pw == "rhjk0096":
			return """<html>
			<div align="center"><font size="5">
			<head>TGN Smart Home</head>
			<body>
			<br>Login OK
			<META HTTP-EQUIV=REFRESH CONTENT='0; URL=webapp'><br>
			</body>
			</html>"""
		else:
			return """<html>
			<div align="center"><font size="5">
			<head>TGN Smart Home</head>
			<body>
			<br>wrong Password
			</body>
			</html>"""
	@cherrypy.expose
	def webapp(self,com="0"):

		global b1
		global b2
		global b3
		global b4
		global b5
		global b6

		if ifI2C(ROM_ADDRESS) == "found device":
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x01)
			b1=int(dataX)
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x02)
			b2=int(dataX)
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x03)
			b3=int(dataX)
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x04)
			b4=int(dataX)
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x05)
			b5=int(dataX)
			dataX = read_eeprom(1,ROM_ADDRESS,0x00,0x06)
			b6=int(dataX)

		if com == "button1":
			if b1 == 0:
				send(1,1)
				b1 = 1
			else:
				send(1,0)
				b1 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x01,str(b1))

		if com == "button2":
			if b2 == 0:
				send(2,1)
				b2 = 1
			else:
				send(2,0)
				b2 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x02,str(b2))

		if com == "button3":
			if b3 == 0:
				send(3,1)
				b3 = 1
			else:
				send(3,0)
				b3 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x03,str(b3))

		if com == "button4":
			if b4 == 0:
				send(4,1)
				b4 = 1
			else:
				send(4,0)
				b4 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x04,str(b4))

		if com == "button5":
			if b5 == 0:
				send(5,1)
				b5 = 1
			else:
				send(5,0)
				b5 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x05,str(b5))

		if com == "button6":
			if b6 == 0:
				send(6,1)
				b6 = 1
			else:
				send(6,0)
				b6 = 0
			write_eeprom(1,ROM_ADDRESS,0x00,0x06,str(b6))



		stats = ""
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

		return """<html>
			<div align="center"><font size="5">
			<head>TGN Smart Home</head>
			<body>
			<br><br>Home Control<br><br>

			<TABLE>
			
			<TR>
			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button1'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button2'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button3'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TR>
			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button4'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button5'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button6'>
			<input type='submit' value=%s style='width:200px;height:50px;'>
			</form>

			<TR>
			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button7'>
			<input type='submit' value='ALL ON' style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button8'>
			<input type='submit' value='ALL OFF' style='width:200px;height:50px;'>
			</form>

			<TH>
			<form method="get" action="webapp">
			<INPUT TYPE='HIDDEN' NAME='com' VALUE='button9'>
			<input type='submit' value='Restart System' style='width:200px;height:50px;'>
			</form>

			<TR>
			<TH><TH>
			Swistch:%s

			</TABLE>

			</body>
			</html>"""% (buttons[0],buttons[1],buttons[2],buttons[3],buttons[4],buttons[5],stats)

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host': ip_s,
				'server.socket_port': port_s})
	cherrypy.quickstart(tgn_smart_home())