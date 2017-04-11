import psutil as pc
from tkinter import *
from tkinter.ttk import *
import power

battery_directory = "/sys/class/power_supply/BAT1/"

class SystemMonitor():
	def __init__(self):
		self.root = Tk()
		self.root.title('System Monitor')
		# self.root.geometry("600x300+150+150")
		
		#NoteBook
		self.n = Notebook(self.root)
		self.f1 = Frame(self.n)   # CPU Usage
		self.f2 = Frame(self.n)   # Sensors
		self.n.add(self.f1, text='CPU Usage')
		self.n.add(self.f2, text='CPU Temperature')
		self.n.pack()

					######################### CPU USAGE ############################
		#Current CPU usage
		self.cur_cpu = pc.cpu_percent()

		#Progress Bar to show current CPU usage
		self.cpu_bar = Progressbar(self.f1, length=300, value = self.cur_cpu, mode="determinate")
		self.cpu_bar.pack(padx=5, pady=5)

		#Variable string to store current CPU usage 
		self.cpu_percent = StringVar()
		self.cpu_percent.set(str(self.cur_cpu)+" %")
		self.label_perc = Label(self.f1, text = "CPU Usage: " )
		self.label_perc.pack()
		self.per = Label(self.f1, textvariable = self.cpu_percent )
		self.per.pack()

					######################### SENSORS ############################
		#Current Sensor Values
		self.temperature = pc.sensors_temperatures()
		self.battery = pc.sensors_battery()

		self.battery_estimate = ""
		self.power_source = ""
		source = power.PowerManagement().get_providing_power_source_type()
		if(source == power.POWER_TYPE_AC):
			self.power_source = "AC"
		elif(source == power.POWER_TYPE_BATTERY):
			self.power_source = "BATTERY"
		elif(source == power.POWER_TYPE_UPS):
			self.power_source = "UPS"
		else:
			self.power_source = "UNKNOWN"

		self.temp_cur = self.temperature['coretemp'][0][1]
		self.temp_critical = self.temperature['coretemp'][0][3]

		self.sensor_window = Panedwindow(self.f2, orient=VERTICAL)
		self.sensor_frame1 = Labelframe(self.sensor_window, text='Temperature', width=100, height=100)
		self.sensor_frame2 = Labelframe(self.sensor_window, text='Battery', width=100, height=100)
		self.sensor_window.add(self.sensor_frame1)
		self.sensor_window.add(self.sensor_frame2)

		#Progress Bar to show current temperature
		self.temp_bar = Progressbar(self.sensor_frame1, length=300, value = self.temp_cur, mode="determinate", maximum = self.temp_critical)
		self.temp_bar.pack(padx=5, pady=5)

		self.cur_temp = StringVar()
		self.cur_temp.set("cur_temp: "+str(self.temp_cur))
		self.cur_temp_label = Label(self.sensor_frame1, textvariable = self.cur_temp )
		self.cur_temp_label.pack(side = LEFT)
		self.label_temp = Label(self.sensor_frame1, text = "critical_temp: "+str(self.temp_critical) )
		self.label_temp.pack(side = RIGHT)

		#Battery Status
		self.batt_estimate = StringVar()
		self.batt_estimate.set("Battery Estimate: "+str(self.battery_estimate))
		self.batt_estimate_label = Label(self.sensor_frame2, textvariable = self.batt_estimate )
		self.batt_estimate_label.pack()
		self.label_batt_type = Label(self.sensor_frame2, text = "Power Source:"+self.power_source )
		self.label_batt_type.pack(side = LEFT)


		self.sensor_frame1.pack()
		self.sensor_frame2.pack(side = LEFT)
		self.sensor_window.pack()

		#Call Update() after 500ms
		self.f1.after(500, self.update_cpu)
		self.f2.after(0,self.update_sensors)
		#The Main Loop
		self.root.mainloop()

	#The Update function to update the CPU Usage Values
	def update_cpu(self):
		self.cur_cpu = pc.cpu_percent()
		self.cpu_percent.set(str(self.cur_cpu)+" %")#UPDATE CPU PERCENTAGE VARIABLE
		self.cpu_bar["value"] = self.cur_cpu
		# print(self.cur_cpu)
		self.f1.after(500, self.update_cpu)

	def update_sensors(self):
		self.temperature = pc.sensors_temperatures()
		self.battery = pc.sensors_battery()

		self.temp_cur = self.temperature['coretemp'][0][1]
		self.temp_bar["value"] = self.temp_cur
		self.cur_temp.set("cur_temp: "+str(self.temp_cur))

		try:
			f = open(battery_directory+"charge_now","r")
			charge = int(f.read().strip('\n'))
			f.close()
			f = open(battery_directory+"current_now","r")
			current = int(f.read().strip('\n'))
			f.close()
			if current==0:
				self.battery_estimate = "Charging"
			else:
				hours = int((charge/current/3600))
				mins = int(((charge/current)%3600)/60)
				self.battery_estimate = str(hours)+" hrs "+str(mins)+" mins"
			self.batt_estimate.set("Battery Estimate: "+str(self.battery_estimate))
		except Exception as e:
			print (e)
		self.f2.after(5000,self.update_sensors)


test = SystemMonitor()