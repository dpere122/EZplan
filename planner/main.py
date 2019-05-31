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
        return "{} is due on {}".format(self.noteText,self.dateDue)


class AppFrame:
	def __init__(self):
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
					labels.config(text = "Day: "+str(counter))
					labels.bind("<Button-1>",lambda event, nCounter = counter: self.taskWindow(event, nCounter))
					self.days.append(labels)
				offCounter += 1

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
	def taskWindow(self,event,nCounter):
		if(self.isTaskWinOpen == False):
			self.isTaskWinOpen = True
			self.taskWin = Toplevel(self.window)
			self.taskWin.protocol("WM_DELETE_WINDOW", self.taskClosed)
			self.taskWin.geometry("300x250")
			self.taskWin.resizable(width=False,height=False)
			self.listBox = Listbox(self.taskWin , width = 35)
			self.taskLabel = tk.Label(self.taskWin,text = "Task Name: ")
			self.taskInput = tk.Entry(self.taskWin,width = 25)
			self.submit = tk.Button(self.taskWin,text = "Add")
			self.delete = tk.Button(self.taskWin,text = "Delete")
			self.listBox.grid(column = 0, row = 0,columnspan = 2)
			self.taskLabel.grid(column = 0,row = 1)
			self.taskInput.grid(column = 1,row = 1)
			self.submit.grid(column = 0,row = 2)
			self.delete.grid(column = 1,row = 2)
			
			# self.days[nCounter - 1].config(text="Day:{}\n-NEW TASK".format(nCounter))
		print("IS OPENED: "+str(self.isTaskWinOpen))

	def taskClosed(self):
		print("TASK WAS CLOSED")
		self.isTaskWinOpen = False
		self.taskWin.destroy()

	# def loadTasks(self):

	# def addTask(self):


				


class MainMenu:
	def __init__(self):
		print("Welcome to EZplan")
		command = None
		while(command != "exit"):
			print("=================")
			print("Please enter a command or type help for command list: ")
			command = input()
			if (command != "exit"):
				self.initiateCommand(command)

	def initiateCommand(self,curCommand):
		try: 
			commandTokens = curCommand.split(' ',1)[0]
			commandItem = curCommand.split(' ',1)[1]
			if(commandTokens == "create" and isinstance(commandItem,str)):
				self.newNote(commandItem) #Sending note - need date
			elif(commandTokens == "delete"):
				self.deleteNote(int(commandItem)) #Sending ID
			else:
				print("ERROR: Please enter a valid command with correct parameters!")
		except:
			if(commandTokens == "list"):
				self.showNotes()
			elif(commandTokens == "help"):
				print("Commands: \n'create <note>'\n'delete <id>'\n'list'")

	#Create a new note then add to list
	def newNote(self,nNote):
		print("Please enter a date using this format year-month-date: ")
		while True:
			nDateStr = input()
			try:
				nDateObj = datetime.datetime.strptime(nDateStr,'%Y-%m-%d')
				break
			except:
				print("ERROR: There was an error inputting the date please try again!")
		curNote = Note(nNote,nDateObj)
		notes.append(curNote)
		print("Note was created and Saved!")
		self.modifyList()

	#Show list of notes and dates
	def showNotes(self):
		if(len(notes) != 0):
			for n in range(len(notes)):
				print("{}: {}".format(n,notes[n].description()))
		else:
			print("The list is empty!")

	#Delete note with given ID
	def deleteNote(self,ID):
		try:
			notes.pop(ID)
			self.modifyList()
			print("Item at index {} has been deleted!".format(ID))
		except:
			print("ERROR: Please enter the ID of a valid Note!")
	# checks if the list changed if it did then save the list back to file for changes
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
# MainMenu()
