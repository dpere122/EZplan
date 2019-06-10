
class Note:
	def __init__(self, taskText):
		self.tasks = []
		self.tasks.append(taskText)

	def getTaskList(self):
		return self.tasks
