import datetime
import pickle
import os
import tkinter as tk
from tkinter import *
# from calendar import monthrange
import calendar


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
		self.labels = []
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
				label = self.make_label(self.frame,x,y,h = cellHeight,w = cellWidth,bg = "grey",borderwidth = 2,relief="solid",anchor = 'ne')
				if(offCounter > start and counter < totalDays):
					nCounter = counter + 1
					self.labels.append(self.writeTasks(label,nCounter))
					counter +=1	


				offCounter += 1
		self.refreshLabel()

	def writeTasks(self,label,day):
		labelIndex = day - 1
		itemDate = "{}-{}-{}".format(self.curYear,self.curMonth,day)
		nDateObj = datetime.datetime.strptime(itemDate,'%Y-%m-%d')
		dayObj = DayObj(labelIndex,nDateObj)
		label.bind("<Button-1>",lambda event, date = nDateObj: self.taskWindow(event,dayObj))
		return label
		

	def make_label(self,master, x, y, h, w, *args, **kwargs):
		f = Frame(master,height = h,width = w)
		f.pack_propagate(0) # don't shrink
		f.grid(row=x, column=y)
		label = Label(f, *args, **kwargs)
		label.pack(fill=BOTH, expand=1)
		return label	
	

	def taskWindow(self,event,dayObj):
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
			self.submit = tk.Button(self.buttonFrame,text = "Add", command = lambda : self.addTask(dayObj))
			self.delete = tk.Button(self.buttonFrame,text = "Delete", command = lambda : self.delTask(dayObj))
			self.listBox.pack()
			self.buttonFrame.pack()
			self.taskLabel.grid(row = 0, column = 0)
			self.taskInput.grid(row = 0, column = 1)
			self.submit.grid(row = 1, column = 0)
			self.delete.grid(row = 1, column = 1)
			for item in range(0,len(dayObj.tasks)):
				self.listBox.insert(END, dayObj.tasks[item])
		print("TASK WINDOW OPENED")

	def taskClosed(self):
		print("TASK WAS CLOSED")
		self.isTaskWinOpen = False
		self.taskWin.destroy()
		
	def addTask(self,dayObj):
		taskText = self.taskInput.get()
		if(taskText != ""):
			note = Note(taskText)
			dayObj.addTask(taskText)
			self.listBox.insert(END,taskText)
			self.nm.modifyList()
			self.refreshLabel()
			print(days)
		else:
			print("No text in input")

	def delTask(self,dayObj):
		selection = self.listBox.curselection()
		self.listBox.delete(selection)
		dayObj.delTask(selection[0])
		self.nm.modifyList()
		self.refreshLabel()

# issue: assign text to all the labels but also assign the tasks to each label if it has a day object with tasks inside
	def refreshLabel(self):

		for x in range(0,len(self.labels)):
			labelStr = "Day: {}".format(x)
			self.labels[x].config(text = labelStr)

		for i in range(0,len(days)):
			labelStr = "Day: {}".format(i)
			if(days[i].isEmpty != True):
				for t in range(0,len(days[i].tasks)):
					nStr = labelStr+str(days[i].tasks[t])
					self.labels[days[i].labelIndex].config(text = nStr)
			else:
				self.labels[days.labelIndex].config(text = labelStr)




			
class NoteManager:

	def modifyList(self):
		try:
			with open(filePath,"wb") as nfp:
				pickle.dump(days,nfp)
		except:
			print("ERROR: There was an error saving your data!")


class Note:
	def __init__(self, noteText):
		self.noteText = noteText

	def description(self):
		return "{}\n".format(self.noteText)

class DayObj:
	def __init__(self,labelIndex,date):
		self.labelIndex = labelIndex
		self.tasks = []
		self.date = date
		self.isSaved = False
		
	def addTask(self,note):
		self.tasks.append(note)
		if(self.isSaved == False):
			self.isSaved = True
			days.append(self)


	def delTask(self,id):
		if(self.isSaved == True):
			del(self.tasks[id])
		elif(self.isEmpty == True):
			self.isSaved = False
			days.remove(self)

	def isEmpty(self):
		if(tasks[0] != None):
			return True
		else:
			return False

	# def refreshLabel(self):
	# 	nText = self.labelText
	# 	for item in self.tasks:
	# 		nText += item.description()
	# 	self.label.config(text = nText)
		




filePath = "data.dat"
try:
	with open(filePath,'rb') as fp:
		days = pickle.load(fp)
		print("Data file was successfuly loaded!")
except:
	days = []
	print("No file was loaded!")

AppFrame()
