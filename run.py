from driver import Driver
from decouple import config
import datetime
import csv
import utils

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

def __startBetting(driver, counter=1):
	filepath = __getFilePath()
	try:
		file = open(filepath)
		next(file)
		csvreader = csv.reader(file)
		isFirst = True

		for row in csvreader:
			phone, password, code, stake = row
			driver.bet(phone, password, code, stake, isFirst)
			isFirst = False

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
		driver = Driver()
		__startBetting(driver)
		driver.printReport()

	else:
		utils.printError('*'*10)
		utils.printError('\n')
		utils.printError('Contact BRI\n')
		utils.printError('*'*10)