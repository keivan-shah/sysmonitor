#!/usr/bin/python3

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
from operator import itemgetter

battery_directory = "/sys/class/power_supply/BAT1/"

class SystemMonitor():
	def __init__(self):
		print("Starting System Monitor")
		self.root = Tk()
		self.root.title('System Monitor')
		self.root.iconbitmap('@sysmonitor.xbm')
		# self.root.geometry("600x300+150+150")
		
		#NoteBook
		self.n = Notebook(self.root)
		self.f1 = Frame(self.n)   # CPU Usage
		self.f2 = Frame(self.n)   # Memory
		self.f3 = Frame(self.n)   # Sensors
		self.f4 = Frame(self.n)   # Graph
		self.f5 = Frame(self.n)	  # Processes
		self.n.add(self.f1, text='CPU Usage')
		self.n.add(self.f2, text='Memory')
		self.n.add(self.f3, text='CPU Temperature')
		self.n.add(self.f4, text='Graph')
		self.n.add(self.f5, text='Processes')
		self.n.pack(fill=BOTH)

################################################### CPU USAGE ######################################################
		#Current CPU usage
		self.cur_cpu = pc.cpu_percent()
		self.cpu_arr = deque()
		self.cpu_arr.append(self.cur_cpu)

		#Progress Bar to show current CPU usage
		self.cpu_bar = Progressbar(self.f1, length=300, value = self.cur_cpu, mode="determinate")
		self.cpu_bar.pack(padx=5, pady=5,fill=BOTH)

		#Variable string to store current CPU usage 
		self.cpu_percent = StringVar()
		self.cpu_percent.set("CPU Usage: "+str(self.cur_cpu)+" %")
		self.cpu_percent_label = Label(self.f1, textvariable = self.cpu_percent )
		self.cpu_percent_label.place(relx=0.5, rely=0.2, anchor=CENTER)

		self.cpu_freq = pc.cpu_freq()
		self.cpu_freq_val = StringVar()
		self.cpu_freq_val.set(str("Current CPU Freq: "+str(int(self.cpu_freq[0]))+"/"+str(int(self.cpu_freq[2]))+" MHz"))
		self.cpu_freq_label = Label(self.f1, textvariable = self.cpu_freq_val )
		self.cpu_freq_label.place(relx=0.5, rely=0.3, anchor=CENTER)

		self.cpu_count_label = Label(self.f1, text = "Number of CPUs: "+str(pc.cpu_count()) )
		self.cpu_count_label.place(relx=0.5, rely=0.4, anchor=CENTER)

		self.pid = pc.pids()
		self.pid_val = StringVar()
		self.pid_val.set(str("Total Running Processes: "+str(len(self.pid))))
		self.pid_label = Label(self.f1, textvariable = self.pid_val )
		self.pid_label.place(relx=0.5, rely=0.5, anchor=CENTER)

######################################################  MEMORY  ####################################################
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

		# RAM Used
		self.ram_bar = Progressbar(self.memory_frame1, length=300, value = self.ram_percent, mode="determinate")
		self.ram_bar.pack(padx=5, pady=5,fill=BOTH)
		self.ram_val = StringVar()
		self.ram_val.set("Ram Used: "+str(self.ram_percent)+"%")
		self.ram_label = Label(self.memory_frame1, textvariable = self.ram_val)
		self.ram_label.pack(side = LEFT,fill=BOTH)

		#Swap Used
		self.swap_bar = Progressbar(self.memory_frame2, length=300, value = self.swap_percent, mode="determinate")
		self.swap_bar.pack(padx=5, pady=5,fill=BOTH)
		self.swap_val = StringVar()
		self.swap_val.set("Swap Used: "+str(self.swap_percent)+"%")
		self.swap_label = Label(self.memory_frame2, textvariable = self.swap_val)
		self.swap_label.pack(side = LEFT,fill=BOTH)

		#Disk Space Used
		self.disk_bar = Progressbar(self.memory_frame3, length=300, value = self.disk_percent, mode="determinate")
		self.disk_bar.pack(padx=5, pady=5,fill=BOTH)
		self.disk_val = StringVar()
		self.disk_val.set("Disk Used: "+str(self.disk_percent)+"%")
		self.disk_label = Label(self.memory_frame3, textvariable = self.disk_val)
		self.disk_label.pack(side = LEFT,fill=BOTH)

		self.memory_frame1.pack(fill=BOTH)
		self.memory_frame2.pack(fill=BOTH)
		self.memory_frame3.pack(fill=BOTH)
		self.memory_window.pack(fill=BOTH)	

###################################################### SENSORS #####################################################
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
		self.temp_bar.pack(padx=5, pady=5,fill=BOTH)

		#Temperature
		self.cur_temp = StringVar()
		self.cur_temp.set("cur_temp: "+str(self.temp_cur)+"`C")
		self.cur_temp_label = Label(self.sensor_frame1, textvariable = self.cur_temp )
		self.cur_temp_label.pack(side = LEFT,fill=BOTH)
		self.label_temp = Label(self.sensor_frame1, text = "critical_temp: "+str(self.temp_critical)+"\u2103" )
		self.label_temp.pack(side = RIGHT,fill=BOTH)

		#Battery Status
		self.batt_estimate = StringVar()
		self.batt_estimate.set("Battery Estimate: "+str(self.battery_estimate))
		self.batt_estimate_label = Label(self.sensor_frame2, textvariable = self.batt_estimate )
		self.batt_estimate_label.pack(fill=BOTH)
		self.label_batt_type = Label(self.sensor_frame2, text = "Power Source: "+self.power_source )
		self.label_batt_type.pack(side = LEFT,fill=BOTH)

		self.sensor_frame1.pack(fill=BOTH)
		self.sensor_frame2.pack(side = LEFT,fill=BOTH)
		self.sensor_window.pack(fill=BOTH)

################################################### GRAPH ##########################################################
		#Graph Variables
		self.fig = Figure(figsize=(0.1,0.1))
		ax = self.fig.add_subplot(111)
		self.line, = ax.plot(range(50))
		ax.axis([0,50,0,100])
		ax.set_title ("CPU Usage", fontsize=12)
		ax.set_ylabel("Percentage", fontsize=10)
		ax.set_xlabel("Time", fontsize=10)
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.f4)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side='top', fill=BOTH, expand=1,ipadx=180)

############################################### PROCESSES ##########################################################
		self.kill_process_id = 0

		self.scrollbar = Scrollbar(self.f5)
		self.scrollbar.pack(side=RIGHT, fill=Y)

		self.update_button = Button(self.f5, text="Update", command=self.update_processes)
		self.update_button.pack(side=TOP)

		tv = Treeview(self.f5)
		tv['columns'] = ('cpu', 'id','status')
		tv.heading("#0", text='Process Name', anchor='w')
		tv.column("#0", anchor="w", width=75)
		tv.heading('cpu', text='% CPU')
		tv.column('cpu', anchor='center', width=40)
		tv.heading('id', text='PID')
		tv.column('id', anchor='center', width=35)
		tv.heading('status', text='Status')
		tv.column('status', anchor='center', width=40)
		tv.pack(fill=BOTH)
		self.treeview = tv

		tv.tag_configure('active', background='green')
		# attach listbox to scrollbar
		self.treeview.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.treeview.yview)

		self.pMenu = Menu(self.f5, tearoff=0)
		self.pMenu.add_command(label="Kill Process", command=self.kill_process)
		self.pMenu.add_command(label="Kill Process Tree", command=self.kill_process_tree)
		self.pMenu.add_command(label="Cancel")

		self.treeview.bind("<Button-3>", self.process_popup)
		self.treeview.bind("<Button-2>", self.process_popup)


################################################### UPDATE #########################################################		

		#Call Update() after 100 ms
		self.job1 = self.f1.after(1000, self.update_cpu)
		self.job2 = self.f2.after(1000,self.update_memory)
		self.job3 = self.f3.after(1000,self.update_sensors)
		self.job4 = self.f4.after(1000,self.update_graph)
		self.job5 = self.f5.after(1000,self.update_processes)
		#The Main Loop
		self.root.mainloop()
		#Kill everything once the window is closed.
		print ("Killing everything.")
		self.f1.after_cancel(self.job1)
		self.f2.after_cancel(self.job2)
		self.f3.after_cancel(self.job3)
		self.f4.after_cancel(self.job4)
		self.f5.after_cancel(self.job5)
		print ("Good Bye!")
		sys.exit()

################################################### UPDATE FUNCTIONS #########################################################

	#The Update function to update the CPU Usage Values
	def update_cpu(self):
		self.cur_cpu = pc.cpu_percent()
		self.cpu_arr.append(self.cur_cpu)
		if(len(self.cpu_arr)>50):
			self.cpu_arr.popleft()
		self.cpu_percent.set("CPU Usage: "+str(self.cur_cpu)+" %")#UPDATE CPU PERCENTAGE VARIABLE
		self.cpu_bar["value"] = self.cur_cpu

		self.cpu_freq = pc.cpu_freq()
		self.cpu_freq_val.set(str("Current CPU Freq: "+str(int(self.cpu_freq[0]))+"/"+str(int(self.cpu_freq[2]))+" MHz"))

		self.pid = pc.pids()
		self.pid_val.set(str("Total Running Processes: "+str(len(self.pid))))

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
		self.job3 = self.f3.after(2000,self.update_sensors)

	#The Update function to update the Graph
	def update_graph(self):
		x, y = self.line.get_data()
		self.line.set_ydata(np.array(self.cpu_arr))
		self.line.set_xdata(np.arange(0,len(self.cpu_arr),1))
		self.canvas.draw()
		self.job4 = self.f4.after(500, self.update_graph)

	def update_processes(self):
		# print("Updating Processes")
		all_items = self.treeview.get_children()
		for item in all_items:
			self.treeview.delete(item)
		list = []
		for p in pc.process_iter():
			try:
				list.append(p.as_dict(attrs=['pid','name','cpu_percent','status','ppid']))
			except pc.NoSuchProcess:
				pass
		list = sorted(list,key=itemgetter('cpu_percent'), reverse=True)
		for pinfo in list:
			name = pinfo['name']
			pid = pinfo['pid']
			ppid = pinfo['ppid']
			status = pinfo['status']
			cpu = pinfo['cpu_percent']
			if ppid>1:
				if status == "running": 
					self.treeview.insert('', 'end', text=name, values=(cpu,pid,status), tags=('active'))
				else:
					self.treeview.insert('', 'end', text=name, values=(cpu,pid,status))




################################################# POPUPS #########################################################

	#Processes Menu PopUp
	def process_popup(self, event):
		iid = self.treeview.identify_row(event.y)
		if iid:
			# mouse pointer over item
			self.treeview.selection_set(iid)
			# print(self.treeview.item(iid)['values'][1])
			self.kill_process_id = self.treeview.item(iid)['values'][1]
			self.pMenu.post(event.x_root, event.y_root)
		else:
			self.pMenu.unpost()

	def kill_process(self):
		if self.kill_process_id:
			code = pc.Process(self.kill_process_id).kill()
			print("process {} terminated with exit code {}".format(self.kill_process_id, code))
			self.kill_process_id = 0
			self.job5 = self.f5.after(100, self.update_processes)
		else:
			print ("Please Try Again.")

	def kill_process_tree(self):
		if self.kill_process_id:
			procs = pc.Process(self.kill_process_id).children(recursive=True)
			for p in procs:
				p.terminate()
			gone, still_alive = pc.wait_procs(procs, timeout=3, callback=on_terminate)
			for p in still_alive:
				p.kill()
			code = pc.Process(self.kill_process_id).kill()
			print("process {} terminated with exit code {}".format(self.kill_process_id, code))
			self.kill_process_id = 0
			self.job5 = self.f5.after(100, self.update_processes)
		else:
			print ("Please Try Again.")

def on_terminate(proc):
	print("process {} terminated with exit code {}".format(proc, proc.returncode))


test = SystemMonitor()
