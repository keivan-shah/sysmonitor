# SYSMONITOR
A mini project in python than acts as a system monitor. This `python3` application makes use of the `Tkinter` package for the GUI and `psutil` Library to make the necessary function calls to get the underlying system details as required.  
_____________________________________________________________________________________________________________________________________

# INSTALLATION:
1. **Install Python 3.5.2**
2. **Install Pip**
3. **Install Tkinter**
4. Open terminal in `sysmonitor/ ` and type
```shell
$ pip install -r requirements.txt
```
(It will install all the requirements for the project.)

_____________________________________________________________________________________________________________________________________

# RUNNING:

In the `sysmonitor` open terminal and type:
```shell
$ python3 sysmonitor.py
```
**OR**

Double click on the `sysmonitor.py` file and select `Run`

(The sysmonitor.py should be a executable file for this method to work.)
_____________________________________________________________________________________________________________________________________

# OUTPUT:

The Widget should popup right away. The widget has Tabs for 5 things that are:
* CPU Usage
* Memory Usage
* Sensors
* CPU Usage Graph
* Processes

You can switch between Tabs to look at the different system information provided by this widget.

1. **CPU Usage:**

  ![CPU Usage](/screenshots/1.png)

  This tab shows the current CPU Usage in percentage along with certain other information such as the current CPU frequency, Number of CPU's and the Total Number of Running Processes.

2. **Memory Usage:**

  ![Memory Usage](/screenshots/2.png)

  This tab shows the current RAM, Swap and Disk Memory Usage of the Computer.

3. **Sensors:**

  ![Sensors](/screenshots/3.png)

  This tab shows the current CPU tempertaure and its percentage with respect to the critical tempertaure. Also it shows the estimated on time of the laptop based on the current battery status and also displays the power source.

4. **CPU Usage Graph:**

  ![CPU Usage Graph](/screenshots/4.png)

  This tab shows a graph of the CPU Usage wrt to time.

5. **Processes:**

  ![Processes](/screenshots/5.png)

  This tab show the current active Processes sorted wrt to the percentage CPU Usage. Also right click on the process gives a menu to kill the process or the process Tree. This can be useful to kill non responding programs.
