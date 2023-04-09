from driver import Driver
from selenium import webdriver
from decouple import config
import datetime
import csv
import utils
import threading
from webdriver_manager.opera import OperaDriverManager
import os
import shutil

__banner = """
88                          
88                      @@  
88                        
88,dPPYba,  88   ,,a"'  88  
88P'    "8a  88	"R      88  
88       d8   88        88
88b,   ,a8"   88        88
8Y"Ybbd8"'    88        88  
"""

def __valid() -> bool:
	canExpire = config('canExpire')
	if canExpire == '1':
		endTimestamp = (float) (config('daysToExpire'))
		currTimeStamp = datetime.datetime.now().timestamp()
		return currTimeStamp < endTimestamp

	return True

def __getFilePath() -> str:
	filePath = input('Drag the CSV file here to begin\n')
	return filePath.strip().rstrip('\'').rstrip('\"').lstrip('\'').lstrip('\"')

def __bet(options, executablePath, phone, password, code, stake, lock):
	driver = Driver(options=options, executablePath=executablePath, lock=lock)
	driver.bet(phone, password, code, stake)
	driver.saveReport()

def __betThreads(filepath, options, executablePath, lock,retry=False):
	file = open(filepath)
	next(file) #removes the headers

	threads = list()
	csvreader = csv.reader(file)
	for row in csvreader:
		if not retry:
			phone, password, code, stake = row
		else:
			phone, password, code, stake, _, __ = row
			if _ == 'LOGIN':
				continue
		x = threading.Thread(target=__bet, args=(options, executablePath, phone, password, code, stake,lock,))
		threads.append(x)
		x.start()

	for index, thread in enumerate(threads):
		thread.join()
	
	failed = printReport()
	if failed > 0:
		response = input('There above accounts failed. Would you like to retry? (yes/no) ')
		if response.lower() == 'yes':
			__betThreads('failed.csv',options=options, executablePath=executablePath, lock=lock, retry=True)
		else:
			if not retry:
				destination = __getDestination(filepath)
				print('destination: ', destination)
				failedPath = os.path.join(destination, 'failed.csv')
				shutil.move('failed.csv', failedPath)
	
	file.close()

def __getDestination(filepath):
	if len(filepath.split('\\')) > 0:
		return os.path.dirname(os.path.abspath(filepath))
	else:
		return os.path.abspath()

def __startBetting(counter=1):
	filepath = __getFilePath()
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('allow-elevated-browser')
		options.add_experimental_option('w3c', True)
		options.add_argument("--headless")
		executablePath = OperaDriverManager().install()	
		lock = threading.Lock()
		
		__betThreads(filepath, options, executablePath, lock)
	except:
		utils.printError('\n!!!!! There was an error reading the file !!!!!\nRETRY '+ counter)
		if counter < 3:
			counter += 1
			__startBetting(counter=counter)
		else:
			utils.printError('\n\n!!!!! Confirm the validity of the CSV file and try again !!!!!\n\n')

def failedCount() -> int:
	file = open('failed.csv')
	next(file) #removes header
	rowCount = sum(1 for row in file)
	file.close()
	return rowCount

def printReport() -> int:
	rowCount = failedCount()
	if rowCount > 0:
		file = open('failed.csv')
		next(file) #removes header
		csvreader = csv.reader(file)
		print('\n\n\n')
		utils.printError('-'*100)

		for row in csvreader:
			utils.printError(row)

		utils.printError('-'*100)
		print('\n')

		file.close()

	return rowCount
		

if __name__ == '__main__':
	print(__banner)
	if __valid():
		with open('failed.csv', 'w') as file:
			writer = csv.writer(file)
			headers = ['username','password','booking_code','stake', 'error', 'error_details']
			writer.writerow(headers)
		__startBetting()

	else:
		utils.printError('*'*10)
		utils.printError('\n')
		utils.printError('Contact BRI\n')
		utils.printError('*'*10)