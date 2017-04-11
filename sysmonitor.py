import psutil as pc
from tkinter import *
from tkinter.ttk import *
import power
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from collections import deque

battery_directory = "/sys/class/power_supply/BAT1/"

class SystemMonitor():
	def __init__(self):
		self.root = Tk()
		self.root.title('System Monitor')
		# self.root.geometry("600x300+150+150")
		
		#NoteBook
		self.n = Notebook(self.root)
		self.f1 = Frame(self.n)   # CPU Usage
		self.f2 = Frame(self.n)   # Memory
		self.f3 = Frame(self.n)   # Sensors
		self.f4 = Frame(self.n)   # Graph
		self.n.add(self.f1, text='CPU Usage')
		self.n.add(self.f2, text='Memory')
		self.n.add(self.f3, text='CPU Temperature')
		self.n.add(self.f4, text='Graph')
		self.n.pack()

					######################### CPU USAGE ############################
		#Current CPU usage
		self.cur_cpu = pc.cpu_percent()
		self.cpu_arr = deque()
		self.cpu_arr.append(self.cur_cpu)

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

					#########################  MEMORY  ###########################
		self.ram = pc.virtual_memory()
		self.swap = pc.swap_memory()
		self.disk = pc.disk_usage('/home')
		self.ram_percent = self.ram[2]
		self.swap_percent = self.swap[3]
		self.disk_percent = self.disk[3]

		self.memory_window = Panedwindow(self.f2, orient=VERTICAL)
		self.memory_frame1 = Labelframe(self.memory_window, text='RAM', width=100, height=100)
		self.memory_frame2 = Labelframe(self.memory_window, text='Swap', width=100, height=100)
		self.memory_frame3 = Labelframe(self.memory_window, text='Disk', width=100, height=100)
		self.memory_window.add(self.memory_frame1)
		self.memory_window.add(self.memory_frame2)
		self.memory_window.add(self.memory_frame3)	

		self.ram_bar = Progressbar(self.memory_frame1, length=300, value = self.ram_percent, mode="determinate")
		self.ram_bar.pack(padx=5, pady=5)
		self.ram_val = StringVar()
		self.ram_val.set("Ram Used: "+str(self.ram_percent)+"%")
		self.ram_label = Label(self.memory_frame1, textvariable = self.ram_val)
		self.ram_label.pack(side = LEFT)

		self.swap_bar = Progressbar(self.memory_frame2, length=300, value = self.swap_percent, mode="determinate")
		self.swap_bar.pack(padx=5, pady=5)
		self.swap_val = StringVar()
		self.swap_val.set("Swap Used: "+str(self.swap_percent)+"%")
		self.swap_label = Label(self.memory_frame2, textvariable = self.swap_val)
		self.swap_label.pack(side = LEFT)

		self.disk_bar = Progressbar(self.memory_frame3, length=300, value = self.disk_percent, mode="determinate")
		self.disk_bar.pack(padx=5, pady=5)
		self.disk_val = StringVar()
		self.disk_val.set("Disk Used: "+str(self.disk_percent)+"%")
		self.disk_label = Label(self.memory_frame3, textvariable = self.disk_val)
		self.disk_label.pack(side = LEFT)

		self.memory_frame1.pack()
		self.memory_frame2.pack()
		self.memory_frame3.pack()
		self.memory_window.pack()	


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

		self.sensor_window = Panedwindow(self.f3, orient=VERTICAL)
		self.sensor_frame1 = Labelframe(self.sensor_window, text='Temperature', width=100, height=100)
		self.sensor_frame2 = Labelframe(self.sensor_window, text='Battery', width=100, height=100)
		self.sensor_window.add(self.sensor_frame1)
		self.sensor_window.add(self.sensor_frame2)

		#Progress Bar to show current temperature
		self.temp_bar = Progressbar(self.sensor_frame1, length=300, value = self.temp_cur, mode="determinate", maximum = self.temp_critical)
		self.temp_bar.pack(padx=5, pady=5)

		self.cur_temp = StringVar()
		self.cur_temp.set("cur_temp: "+str(self.temp_cur)+"`C")
		self.cur_temp_label = Label(self.sensor_frame1, textvariable = self.cur_temp )
		self.cur_temp_label.pack(side = LEFT)
		self.label_temp = Label(self.sensor_frame1, text = "critical_temp: "+str(self.temp_critical)+"\u2103" )
		self.label_temp.pack(side = RIGHT)

		#Battery Status
		self.batt_estimate = StringVar()
		self.batt_estimate.set("Battery Estimate: "+str(self.battery_estimate))
		self.batt_estimate_label = Label(self.sensor_frame2, textvariable = self.batt_estimate )
		self.batt_estimate_label.pack()
		self.label_batt_type = Label(self.sensor_frame2, text = "Power Source: "+self.power_source )
		self.label_batt_type.pack(side = LEFT)

		self.sensor_frame1.pack()
		self.sensor_frame2.pack(side = LEFT)
		self.sensor_window.pack()

					######################### GRAPH ############################
		self.fig = plt.figure()
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.f4)
		self.canvas.get_tk_widget().pack()


					######################### UPDATE ############################		

		#Call Update() after 500ms
		self.job1 = self.f1.after(500, self.update_cpu)
		self.job2 = self.f2.after(1000,self.update_memory)
		self.job3 = self.f3.after(100,self.update_sensors)
		self.job4 = self.f4.after(100,self.update_graph)
		#The Main Loop
		self.root.mainloop()
		print ("Killing everything")
		self.f1.after_cancel(self.job1)
		self.f2.after_cancel(self.job2)
		self.f3.after_cancel(self.job3)
		self.f4.after_cancel(self.job4)
		sys.exit()

	#The Update function to update the CPU Usage Values
	def update_cpu(self):
		self.cur_cpu = pc.cpu_percent()
		self.cpu_arr.append(self.cur_cpu)
		if(len(self.cpu_arr)>100):
			self.cpu_arr.popleft()
		self.cpu_percent.set(str(self.cur_cpu)+" %")#UPDATE CPU PERCENTAGE VARIABLE
		self.cpu_bar["value"] = self.cur_cpu
		# print(self.cur_cpu)
		# print(self.cpu_arr)
		self.job1 = self.f1.after(500, self.update_cpu)

	#The Update function to update the Memory Values
	def update_memory(self):
		self.ram = pc.virtual_memory()
		self.swap = pc.swap_memory()
		self.disk = pc.disk_usage('/home')
		self.ram_percent = self.ram[2]
		self.swap_percent = self.swap[3]
		self.disk_percent = self.disk[3]
		self.ram_val.set("Ram Used: "+str(self.ram_percent)+"%")
		self.swap_val.set("Swap Used: "+str(self.swap_percent)+"%")
		self.disk_val.set("Disk Used: "+str(self.disk_percent)+"%")
		self.job2 = self.f2.after(1000,self.update_memory)

	#The Update function to update the Sensor Values
	def update_sensors(self):
		self.temperature = pc.sensors_temperatures()
		self.battery = pc.sensors_battery()

		self.temp_cur = self.temperature['coretemp'][0][1]
		self.temp_bar["value"] = self.temp_cur
		self.cur_temp.set("cur_temp: "+str(self.temp_cur)+"\u2103")

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
				hours = int((charge/current))
				mins = int(((charge/current)-hours)*60)
				self.battery_estimate = str(hours)+" hrs "+str(mins)+" mins"
			self.batt_estimate.set("Battery Estimate: "+str(self.battery_estimate))
		except Exception as e:
			print (e)
		self.job3 = self.f3.after(3000,self.update_sensors)

	def update_graph(self):
		v = np.array(self.cpu_arr)
		x = np.arange(0,len(v),1)
		# print (len(x),len(v))
		plot(x,v)
		self.job4 = self.f4.after(500, self.update_graph)

def plot(x, y):
	plt.clf()
	plt.plot(x,y)
	plt.axis([0,100,0,100])
	plt.gcf().canvas.draw()


test = SystemMonitor()