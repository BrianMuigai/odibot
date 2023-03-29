from driver import Driver
from decouple import config
import datetime
import csv

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
	if canExpire == 1:
		endTimestamp = config('daysToExpire')
		currTimeStamp = datetime.datetime.now().timestamp()
		return currTimeStamp < endTimestamp

	return False

def __getFilePath() -> str:
	filePath = input('Drag the CSV file here to begin\n')
	return filePath

def __startBetting(driver, counter=1):
	filepath = __getFilePath()
	try:
		file = open(filepath)
		next(file)
		csvreader = csv.reader(file)

		for row in csvreader:
			phone, password, code, stake = row
			driver.bet(phone, password, code, stake)

		file.close()
	except:
		file.close()
		print('\n!!!!! There was an error reading the file !!!!!\nRETRY ', counter)
		if counter < 3:
			counter += 1
			__startBetting(counter=counter)
		else:
			print('\n\n!!!!! Confirm the validity of the CSV file and try again !!!!!\n\n')
		

if __name__ == '__main__':
	print(__banner)
	if __valid():
		driver = Driver()
		__startBetting(driver)
		driver.report()

	else:
		print('*'*10)
		print('\n')
		print('Contact BRI\n')
		print('*'*10)