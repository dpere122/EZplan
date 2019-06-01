import datetime
import pickle
import os
import tkinter as tk
from tkinter import *
# from calendar import monthrange
import calendar


class Note:
    def __init__(self, noteText, dateDue):
        self.noteText = noteText
        self.dateDue = dateDue

    def description(self):
        return "{}".format(self.noteText)


class AppFrame:
	
	def __init__(self):
		self.nm = NoteManager()
		now = datetime.datetime.now()
		self.curYear = now.year
		self.curMonth = now.month
		self.isTaskWinOpen = False
		self.window = tk.Tk()
		self.window.title("EZPlanner")
		self.window.geometry("840x600")
		self.window.resizable(width=False,height=False)
		self.banner = tk.Frame(self.window,borderwidth = 2, relief = "solid")
		self.banner.pack(fill = X)
		self.btnLeft = tk.Button(self.banner,text = "<-", command = lambda: self.validateDate(-1))
		self.btnLeft.pack(side = LEFT)
		self.btnRight = tk.Button(self.banner,text = "->",command = lambda: self.validateDate(1))
		self.btnRight.pack(side = RIGHT)
		self.genCalendar(self.curYear,self.curMonth)
		self.window.mainloop()

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
		self.days = []
		self.frame = tk.Frame(self.window)
		self.calLabel = tk.Label(self.banner,anchor = CENTER,text = "{} : {}".format(calendar.month_name[month],str(self.curYear)),height = 2,font = ("Ariel",25))
		self.calLabel.pack(side = TOP)
		self.frame.pack(fill = BOTH)		
		self.frame.update()
		self.banner.update()
		fWidth = self.frame.winfo_width()
		fHeight = self.window.winfo_height() - self.banner.winfo_height()
		cellWidth = (fWidth / 7)
		cellHeight = (fHeight / 6)
		counter = 0
		# make this dynamic
		start,totalDays = calendar.monthrange(year,month)
		# print("start: "+ str(start)+" totalDays: "+ str(totalDays))
		offCounter = 0
		# print(self.window.winfo_height())
		for x in range(0,6):
			for y in range(0,7):
				labels = self.make_label(self.frame,x,y,h = cellHeight,w = cellWidth,bg = "grey",borderwidth = 2,relief="solid",anchor = 'ne')
				if(offCounter > start and counter < totalDays):
					counter +=1	
					# labels.config(text = "Day: "+str(counter))
					self.writeTasks(labels,counter)
					
				offCounter += 1

	def writeTasks(self,label,day):
		label.config(text = "Day: "+str(day))
		itemDate = "{}-{}-{}".format(self.curYear,self.curMonth,day)
		nDateObj = datetime.datetime.strptime(itemDate,'%Y-%m-%d')
		label.bind("<Button-1>",lambda event, date = nDateObj: self.taskWindow(event, nDateObj))
		self.days.append(label)
		for i in range(0,len(notes)):
			if(notes[i].dateDue == nDateObj):
				label.config(text = "Day: {}\n{}".format(day,notes[i].description())) 

	def make_label(self,master, x, y, h, w, *args, **kwargs):
		f = Frame(master,height = h,width = w)
		f.pack_propagate(0) # don't shrink
		f.grid(row=x, column=y)
		label = Label(f, *args, **kwargs)
		label.pack(fill=BOTH, expand=1)
		return label	
	

				

	# restrictions include: only one window open at a time
	# both task and tasks of current date are shown 
	# text input to add tasks
	# then list view to show tasks 
	def taskWindow(self,event,date):
		print(date)
		curTasks = []
		if(self.isTaskWinOpen == False):
			self.isTaskWinOpen = True
			self.taskWin = Toplevel(self.window)
			self.taskWin.protocol("WM_DELETE_WINDOW", self.taskClosed)
			self.taskWin.geometry("300x220")
			self.taskWin.resizable(width=False,height=False)
			self.taskWin.update()
			self.buttonFrame = tk.Frame(self.taskWin)
			self.listBox = Listbox(self.taskWin,width = self.taskWin.winfo_width())
			self.taskLabel = tk.Label(self.buttonFrame,text = "Task Name: ")
			self.taskInput = tk.Entry(self.buttonFrame,width = 25)
			self.submit = tk.Button(self.buttonFrame,text = "Add", command = lambda : self.addTask(date))
			self.delete = tk.Button(self.buttonFrame,text = "Delete", command = lambda : self.delTask(curTasks))
			self.listBox.pack()
			self.buttonFrame.pack()
			self.taskLabel.grid(row = 0, column = 0)
			self.taskInput.grid(row = 0, column = 1)
			self.submit.grid(row = 1, column = 0)
			self.delete.grid(row = 1, column = 1)
			# I should make a method for this
			for i in range(0,len(notes)):
				if(notes[i].dateDue == date):
					curTasks.append(i)
					self.listBox.insert(END,notes[i].description())
			
			# self.days[nCounter - 1].config(text="Day:{}\n-NEW TASK".format(nCounter))
		print("IS OPENED: "+str(self.isTaskWinOpen))

	def taskClosed(self):
		print("TASK WAS CLOSED")
		self.isTaskWinOpen = False
		self.taskWin.destroy()
		
	def addTask(self,date):
		taskText = self.taskInput.get()
		if(taskText != ""):
			note = Note(taskText,date)
			notes.append(note)
			self.listBox.insert(END, note.description())
			self.listBox.update()
			self.nm.modifyList()
		else:
			print("No Text in input")

	def delTask(self,taskList):
		selection = self.listBox.curselection()
		self.listBox.delete(selection)
		del(notes[taskList[selection[0]]])
		self.nm.modifyList()



			
class NoteManager:

	def modifyList(self):
		try:
			with open(filePath,"wb") as nfp:
				pickle.dump(notes,nfp)
		except:
			print("ERROR: There was an error saving your data!")



filePath = "data.dat"
try:
	with open(filePath,'rb') as fp:
		notes = pickle.load(fp)
		print("Data file was successfuly loaded!")
except:
	notes = []
	print("No file was loaded!")

AppFrame()
