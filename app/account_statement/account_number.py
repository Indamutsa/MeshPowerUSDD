#Find the balance
import requests, re

def findAccountNumber(userinput):
	#Converting the user input into a string from unicode
	userinput = str(userinput)

	if userinput == '1*2*1*':
		return 'CON Enter your phone number'
	elif '1*2*1*' in userinput and len(userinput) > 6:
		# Define the regular expression that will exact the phone number as input
		regex = re.compile(r"[0-9]{10}")

		# Here we extract an array which should have size of 1
		matches = re.findall(regex, userinput)


		if len(matches) == 0:
			return "Phone number not found"
		

		# Getting the url that will be passed in to get the associated account
		url = 'http://csu.meshpower.co.rw:6001/accounts/api-phone/v3/' + matches[0]
		header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

		# Retrieving data from the url 
		r = requests.get(url, headers=header)

		#If response is not defined
		if r.status_code != 200:
			return "Phone number not found"

		data = r.json()

		for key, value in data.items():
			if value == "No such account" or value == "ERROR":
				return "Phone number not found"

		# Checking if the incoming phone is equal to the data from the database
		if matches[0] == data['phone-number']:
			account = str(data['account'])
			
			return 'Account number: ' + str(account)
		else:
			return 'Incorrect phone number, Please try again'
	else:
		return "Phone number not found"
