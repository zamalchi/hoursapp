if (__name__ == "__main__"):
	print("Import class: from Labeler import *")
	print("Exiting...")
	exit()



# class that creates an object for labeling and id'ing HTML objects

class Labeler:
	RECORD = "record"
	NAME = "name"
	START = "start"
	END = "end"
	DURATION = "duration"
	BILLABLE = "billable"
	EMERGENCY = "emergency"
	LABEL = "label"
	DESCRIPTION = "description"
	SUBMIT = "submit"
	INSERT = "insert"

	def __init__(self, i=None):
		if i != None:
			self.i = int(i)
		else:
			self.i = None


	def inc(self):
		if self.i != None:
			self.i += 1

	def dec(self):
		if self.i != None:
			self.i -= 1


	#############################################
	def record(self):
		if self.i != None:
			return Labeler.RECORD + str(self.i)
		else:
			return Labeler.RECORD

	def name(self):
		if self.i != None:
			return Labeler.NAME + str(self.i)
		else:
			return Labeler.NAME

	def start(self):
		if self.i != None:
			return Labeler.START + str(self.i)
		else:
			return Labeler.START

	def end(self):
		if self.i != None:
			return Labeler.END + str(self.i)
		else:
			return Labeler.END

	def duration(self):
		if self.i != None:
			return Labeler.DURATION + str(self.i)
		else:
			return Labeler.DURATION

	def billable(self):
		if self.i != None:
			return Labeler.BILLABLE + str(self.i)
		else:
			return Labeler.BILLABLE

	def emergency(self):
		if self.i != None:
			return Labeler.EMERGENCY + str(self.i)
		else:
			return Labeler.EMERGENCY

	def label(self):
		if self.i != None:
			return Labeler.LABEL + str(self.i)
		else:
			return Labeler.LABEL

	def description(self):
		if self.i != None:
			return Labeler.DESCRIPTION + str(self.i)
		else:
			return Labeler.DESCRIPTION

	def submit(self):
		if self.i != None:
			return Labeler.SUBMIT + str(self.i)
		else:
			return Labeler.SUBMIT

	def insert(self):
		if self.i != None:
			return Labeler.INSERT + str(self.i)
		else:
			return Labeler.INSERT
	#############################################
