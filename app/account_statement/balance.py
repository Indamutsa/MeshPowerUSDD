#Find the balance
import requests
import re


#url = 'http://data.meshpower.co.rw/accounts/api/v3/171579'

def findBalance(userinput):
	#Converting the user input into a string from unicode
	userinput = str(userinput)

	if userinput == '1*2*1*':
		return 'CON Enter your phone number:'
	elif '1*2*2*' in userinput and len(userinput) > 6:
		# Define the regular expression that will exact the account number as input
		regex = re.compile(r"[0-9]{5-8}")

		# Here we extract an array which should have size of 1
		matches = re.findall(regex, userinput)

		if matches is None or len(matches[0]) < 10:
			return "Unknown phone number, try again"

		print("Phone number: ",matches[0])

		# Getting the url that will be passed in to get the associated account
		url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
		header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

		# Retrieving data from the url 
		r = requests.get(url, headers=header)
		data = r.json()

		# Checking if the incoming account is equal to the data from the database
		if matches[0] == data['account']:
			
			balance = str(data['balance'])
			currency = data['currency']
			account = str(data['account'])
			user_phone = str(data['phone-number'])

			return 'Account number: ' + str(balance)
		else:
			return 'Incorrect phone number, Please try again'

	print("Account ", userinput ,"  balance: 250frw")
#	return  "Balance: " + balance + currency + " \nAccount: 41585"  #account

