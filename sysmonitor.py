import psutil as pc
from tkinter import *
from tkinter.ttk import *

class SystemMonitor():
	def __init__(self):
		self.root = Tk()
		self.root.title('System Monitor')
		# self.root.geometry("600x300+150+150")
		
		#NoteBook
		self.n = Notebook(self.root)
		self.f1 = Frame(self.n)   # CPU Usage
		self.f2 = Frame(self.n)   # CPU Temperatue
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

					######################### CPU TEMPERATURE ############################


		#Call Update() after 500ms
		self.root.after(500, self.update_cpu)
		#The Main Loop
		self.root.mainloop()

	#The Update function to update the CPU Usage Values
	def update_cpu(self):
		self.cur_cpu = pc.cpu_percent()
		self.cpu_percent.set(str(self.cur_cpu)+" %")	#UPDATE CPU PERCENTAGE
		self.cpu_bar["value"] = self.cur_cpu
		# print(self.cur_cpu)
		self.root.after(500, self.update_cpu) 


test = SystemMonitor()