import datetime
import pickle
import os
class Note:
    
    def __init__(self, noteText, dateDue):
        self.noteText = noteText
        self.dateDue = dateDue
		

    def description(self):
        return "{} is due on {}".format(self.noteText,self.dateDue)


#Create a new note then add to list
def newNote(nNote):
	print("Note {} created succesfully!".format(nNote))
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
	modifyList()

#Show list of notes and dates
def showNotes():
	for n in range(len(notes)):
		print("{}: {}".format(n,notes[n].description()))

#Delete note with given ID
def deleteNote(ID):
	try:
		notes.pop(ID)
		modifyList()
		print("Item at index {} has been deleted!".format(ID))
	except:
		print("ERROR: Please enter the ID of a valid Note!")
	


# checks if the list changed if it did then save the list back to file for changes
def modifyList():
	try:
		with open(filePath,"wb") as nfp:
			pickle.dump(notes,nfp)
	except:
		print("ERROR: There was an error saving your data!")



def mainMenu():
	print("Welcome to EZplan")
	print("=================")
	command = None
	while(command != "exit"):
		print("Please enter a command or type help for command list: ")
		command = input()
		if (command != "exit"):
			initiateCommand(command)

def initiateCommand(curCommand):
	try: 
		commandTokens = curCommand.split(' ',1)[0]
		commandItem = curCommand.split(' ',1)[1]
		if(commandTokens == "create" and isinstance(commandItem,str)):
			newNote(commandItem) #Sending note - need date
		elif(commandTokens == "delete"):
			deleteNote(int(commandItem)) #Sending ID
		else:
			print("ERROR: Please enter a valid command with correct parameters!")
	except:
		if(commandTokens == "list"):
			showNotes()


filePath = "data.dat"
try:
	with open(filePath,'rb') as fp:
		notes = pickle.load(fp)
		print("Data file was successfuly loaded!")
except:
	notes = []
	print("No file was loaded!")

mainMenu()
