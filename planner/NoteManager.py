import pickle
import Note
# Key component to this class is the dictionary and how it stores our data
# Simply a dictionary with dates as keys and values are string arrays 
class NoteManager:
	def __init__(self):
		try:
			with open("planner\database\data.dat",'rb') as fp:
				self.noteDatabase = pickle.load(fp)
				print("Data file was successfuly loaded!")
		except:
			self.noteDatabase = {}
			print("No file was loaded!")		

	def addNote(self,taskText,date):
		if(date in self.noteDatabase.keys()):
			self.noteDatabase.get(date).tasks.append(taskText)
		else:
			note = Note.Note(taskText)
			self.noteDatabase.update({date:note})
		self.modifyList()

	# if there are no more tasks within a note class for a given date then delete that key/Value pair
	def delNote(self,date,taskText):
		if(date in self.noteDatabase.keys()):
			if(taskText in self.noteDatabase.get(date).tasks):
				self.noteDatabase.get(date).tasks.remove(taskText)
			else: 
				print("There was a problem finding and removing a task")
			if(self.getDateTasks(date) == ""):
				del(self.noteDatabase[date])
		else:
			print("There is no date within the noteDatabase")
		self.modifyList()
			
	def getDateTasks(self,date):
		taskStr = ""
		if(date in self.noteDatabase.keys()):
			for item in self.noteDatabase.get(date).tasks:
				taskStr += "{}\n".format(item)
		else:
			print("That date isnt within the list of dates")
		return taskStr


	def modifyList(self):
		try:
			with open("planner\database\data.dat","wb") as nfp:
				pickle.dump(self.noteDatabase,nfp)
		except:
			print("ERROR: There was an error saving your data!")
