from os import getcwd
import os
import csv
terminal = os.system
pwd = getcwd

def open_dir(directory = ".", pwd = pwd()):
	if(directory == "."):
		return
	try:
		os.chdir(os.path.join(pwd, str(directory)))
	except:
		os.mkdir(os.path.join(pwd, str(directory)))
		os.chdir(directory)

	return getcwd()

def delete(directory = None, file = None, pwd = pwd()):
	if file is None:
		for root, dirs, files in os.walk(directory, topdown=False):
			if(directory == '/'):
				print("Dangerous. Stopping right away!")
				return None
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		return directory
	else:
		if(file in os.listdir()):
			os.remove(os.path.join(pwd(), file))
		return file

class csvhandler():
	def __init__(self, filename = None, headers = []):
		self.input_file = filename
		self.output_file = None
		self.headers = headers
		self.input_data = []
		self.output_data = []

	def read_from_file(self, ignore = False):
		if ignore:
			with open(self.input_file, 'r') as input_file:
				reader = csv.reader(input_file)
				for row in reader:
					self.input_data.append(row)
	    
		else:
			with open(self.input_file, 'r') as input_file:
				reader = csv.DictReader(input_file)
				self.headers = reader.fieldnames
				for row in reader:
					row = list(row.values())
					self.input_data.append(list(row))

	def append_row(self, list_of_elems):
		filename = self.output_file
		headers = self.headers
		if(os.path.exists(filename)):
			with open(filename, 'a') as output_file:
				writer = csv.writer(output_file, delimiter = ",")
				writer.writerow(list_of_elems)
		else:
			with open(filename, 'w') as output_file:
				writer = csv.writer(output_file, delimiter = ",")
				writer.writerow(headers)
				writer.writerow(list_of_elems)

	def make_csv(self, filename=None):
		if filename == None:
			filename = self.input_file
		self.output_file = filename
		if(os.path.exists(filename)):
			os.remove(filename)
		for row in self.output_data:
			self.append_row(row)