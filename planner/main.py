import datetime
import pickle
import os
import tkinter as tk
from tkinter import *


class Note:
    def __init__(self, noteText, dateDue):
        self.noteText = noteText
        self.dateDue = dateDue
		

    def description(self):
        return "{} is due on {}".format(self.noteText,self.dateDue)


class AppFrame:
	def __init__(self):
		self.days = []
		self.isTaskWinOpen = False
		self.window = tk.Tk()
		self.window.title("EZPlanner")
		self.window.geometry("800x600")
		self.window.resizable(width=False,height=False)
		self.frame = tk.Frame(self.window)
		self.frame.pack()
		self.createButtons()
		print(self.days)
		self.window.mainloop()


	# Should be responsible for keeping track of the month and how many days in each month
	def createButtons(self):
		counter = 0
		for x in range(0,5):
			for y in range(0,7):
				counter +=1
				labels = tk.Label(self.frame,font=("Courier",15),bg = "grey",borderwidth = 2,relief="solid",anchor = 'ne',width = 12,height=6,text=str(counter))
				labels.grid(column = y,row= x)
				labels.bind("<Button-1>",lambda event, nCounter = counter: self.taskWindow(event, nCounter))
				self.days.append(labels)

	# restrictions include: only one window open at a time
	# both task and tasks of current date are shown 
	# text input to add tasks
	# then list view to show tasks 
	def taskWindow(self,event,nCounter):
		if(self.isTaskWinOpen == False):
			self.isTaskWinOpen = True
			self.taskWin = Toplevel(self.window)
			self.taskWin.protocol("WM_DELETE_WINDOW", self.taskClosed)
			self.taskWin.geometry("300x300")
			self.taskLabel = tk.Label(self.taskWin,text = "Task Name: ")
			self.taskLabel.grid(column = 0,row = 0)
			self.taskInput = tk.Entry(self.taskWin,width = 30)
			self.taskInput.grid(column = 1,row = 0)
			# self.days[nCounter - 1].config(text="Day:{}\n-NEW TASK".format(nCounter))
		print("IS OPENED: "+str(self.isTaskWinOpen))

	def taskClosed(self):
		print("TASK WAS CLOSED")
		self.isTaskWinOpen = False
		self.taskWin.destroy()

				


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
