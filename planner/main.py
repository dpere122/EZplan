import datetime
import os
import tkinter as tk
from tkinter import *
import calendar
import NoteManager
import Note


class AppFrame:
	
	def __init__(self):
		self.now = datetime.datetime.now()
		self.nm = NoteManager.NoteManager()
		self.curYear = self.now.year
		self.curMonth = self.now.month
		self.isTaskWinOpen = False
		self.window = tk.Tk()
		self.window.title("EZPlanner")
		self.window.geometry("840x700")
		self.window.iconbitmap(r"planner\images\cal_icon.ico")
		self.window.attributes('-topmost',0)
		# ALL COMPONENTS RESIZE BUT ARE NOT UPDATED UNTIL THEY ARE REGENERATED(POSSIBLE FEATURE) 
		self.window.resizable(width=False,height=False)
		self.banner = tk.Frame(self.window)
		self.banner.pack(fill = X)
		self.btnLeft = tk.Button(self.banner,text = "<-",font = ("Courier",20),relief = "groove", command = lambda: self.validateDate(-1))
		self.btnLeft.pack(side = LEFT,fill = Y)
		self.btnRight = tk.Button(self.banner,text = "->",font = ("Courier",20),relief = "groove",command = lambda: self.validateDate(1))
		self.btnRight.pack(side = RIGHT, fill = Y)
		self.weekDays = tk.Frame(self.window,borderwidth = 1, relief = "solid")
		self.weekDays.pack(fill = X)
		self.genCalendar(self.curYear,self.curMonth)
		# gen labels for days of the week
		self.window.update()
		fWidth = self.window.winfo_width()
		cellWidth = int((fWidth / 7))
		weekDaysList = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		for x in range(len(weekDaysList)):
			weekDayLabel = self.make_label(self.weekDays,0,x,h = 20,w = cellWidth,relief = "groove",borderwidth = 1,text = "{}".format(weekDaysList[x]))

		self.window.mainloop()

	# Button action to delete past cells and generate new month cells
	def validateDate(self, interval):
		self.frame.destroy()
		self.calLabel.destroy()
		self.curMonth += interval
		if(self.curMonth < 1):
			self.curYear -=1
			self.curMonth = 12
		elif(self.curMonth > 12):
			self.curYear += 1
			self.curMonth = 1
		self.genCalendar(self.curYear,self.curMonth)


	# Should be responsible for keeping track of the month and how many days in each month
	def genCalendar(self,year,month):
		self.labels = []
		self.frame = tk.Frame(self.window)
		self.calLabel = tk.Label(self.banner,anchor = CENTER,text = "{} : {}".format(calendar.month_name[month],str(self.curYear)),height = 2,font = ("Ariel",20))
		self.calLabel.pack(side = TOP)
		self.frame.pack(fill = BOTH)		
		self.frame.update()
		self.banner.update()
		self.weekDays.update()
		fWidth = self.window.winfo_width()
		fHeight = self.window.winfo_height() - self.banner.winfo_height() - self.weekDays.winfo_height()
		cellWidth = (fWidth / 7)
		cellHeight = (fHeight / 6)

		counter = 0
		start,totalDays = calendar.monthrange(year,month)
		offCounter = 0
		curDate = datetime.datetime(self.now.year,self.now.month,self.now.day)

		# creates cells for each day of the month
		for x in range(0,6):
			for y in range(0,7):
				# Labels packed inside frames due to a resizing issue
				label = self.make_label(self.frame,x,y,h = cellHeight,w = cellWidth,bg = "white",borderwidth = 2,relief="groove",anchor = 'ne',justify = RIGHT,wraplength=110)
				
				if(offCounter > start and counter < totalDays):
					self.labels.append(label)
					counter +=1	
					offDate = datetime.datetime(self.curYear,self.curMonth,counter)
					if(curDate > offDate):
						label.config(bg = "grey")


				offCounter += 1
		self.refreshLabels()
		
	# Responisble for changing the text of each cell according to the notemanager and tasks for each item in the dictionary
	def refreshLabels(self):
		counter = 0
		for label in self.labels:
			counter += 1
			labelStr = "Day {}:\n".format(counter)
			label.config(text = labelStr)
			date = datetime.datetime(self.curYear,self.curMonth,counter)
			label.bind("<Button-1>",lambda event, date = date: self.taskWindow(event,date))
			if(date in self.nm.noteDatabase.keys()):
				labelStr += self.nm.getDateTasks(date)
				label.config(text = labelStr)



	# creates labels packed inside frame
	def make_label(self,master, x, y, h, w, *args, **kwargs):
		f = Frame(master,height = h,width = w)
		f.pack_propagate(0) # don't shrink
		f.grid(row=x, column=y)
		label = Label(f, *args, **kwargs)
		label.pack(fill=BOTH, expand=1)
		return label	
	
	# task window to add or delete tasks
	def taskWindow(self,event,date):
		if(self.isTaskWinOpen == False):
			self.isTaskWinOpen = True
			self.taskWin = Toplevel(self.window)
			self.taskWin.protocol("WM_DELETE_WINDOW", self.taskClosed)
			self.taskWin.geometry("300x230")
			self.taskWin.iconbitmap(r"planner\images\cal_icon.ico")
			self.taskWin.resizable(width=False,height=False)
			self.taskWin.update()
			self.buttonFrame = tk.Frame(self.taskWin)
			self.listBox = Listbox(self.taskWin,width = self.taskWin.winfo_width())
			self.taskLabel = tk.Label(self.buttonFrame,text = "Task Name: ")
			self.taskInput = tk.Entry(self.buttonFrame,width = 25)
			self.submit = tk.Button(self.buttonFrame,text = "Add", command = lambda : self.addTask(date))
			self.delete = tk.Button(self.buttonFrame,text = "Delete", command = lambda : self.delTask(date))
			self.listBox.pack()
			self.buttonFrame.pack()
			self.taskLabel.grid(row = 0, column = 0)
			self.taskInput.grid(row = 0, column = 1)
			self.submit.grid(row = 1, column = 0)
			self.delete.grid(row = 1, column = 1)
			self.taskWin.attributes('-topmost',1)
			if(date in self.nm.noteDatabase.keys()):
				for item in self.nm.noteDatabase.get(date).tasks:
					self.listBox.insert(END, item)
		print("TASK WINDOW OPENED")
	# Ensures theres only one task window open at a time
	def taskClosed(self):
		print("TASK WAS CLOSED")
		self.isTaskWinOpen = False
		self.taskWin.destroy()
	# Add tasks while changing our database file
	def addTask(self,date):
		if(self.taskInput.get() != ""):
			taskText = self.taskInput.get()
			self.nm.addNote(taskText,date)
			self.listBox.insert(END,taskText)
			self.refreshLabels()
			self.taskInput.delete(0,'end')

	# Deletes a task while updating our database file
	def delTask(self,date):
		selection = self.listBox.curselection()
		taskText = self.listBox.get(selection)
		if(selection != None):
			self.nm.delNote(date,taskText)
			self.listBox.delete(selection)
			self.refreshLabels()

AppFrame()
