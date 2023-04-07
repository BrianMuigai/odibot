from driver import Driver
from selenium import webdriver
from decouple import config
import datetime
import csv
import utils
import threading
from webdriver_manager.opera import OperaDriverManager

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
	return filePath.strip()

def __bet(options, executablePath, phone, password, code, stake):
	driver = Driver(options=options, executablePath=executablePath)
	driver.bet(phone, password, code, stake)
	driver.printReport()

def __startBetting(counter=1):
	filepath = __getFilePath()
	try:
		file = open(filepath)
		next(file) #remove the headers
		csvreader = csv.reader(file)
		threads = list()

		options = webdriver.ChromeOptions()
		options.add_argument('allow-elevated-browser')
		options.add_experimental_option('w3c', True)
		options.add_argument("--headless")
		executablePath = OperaDriverManager().install()
	
		for row in csvreader:
			phone, password, code, stake = row
			x = threading.Thread(target=__bet, args=(options, executablePath, phone, password, code, stake,))
			threads.append(x)
			x.start()

		for index, thread in enumerate(threads):
			thread.join()

		file.close()
	except:
		utils.printError('\n!!!!! There was an error reading the file !!!!!\nRETRY '+ counter)
		if counter < 3:
			counter += 1
			__startBetting(counter=counter)
		else:
			utils.printError('\n\n!!!!! Confirm the validity of the CSV file and try again !!!!!\n\n')
		

if __name__ == '__main__':
	print(__banner)
	if __valid():
		__startBetting()

	else:
		utils.printError('*'*10)
		utils.printError('\n')
		utils.printError('Contact BRI\n')
		utils.printError('*'*10)