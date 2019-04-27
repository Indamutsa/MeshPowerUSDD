#Find the balance
import requests, re
from app.utils.ussd_util import goBackToRoot, goBackOnce



def findAccountNumber(userinput, lang_id, language):
    #Converting the user input into a string from unicode
    userinput = str(userinput)

    print(lang_id, language)

    # As the user to enter the phone number
    if userinput == "1*" + lang_id['num'] +"*1*":
        return 'CON ' + language[lang_id['lang']]['account-phone']


    elif '1*2*1*' in userinput and len(userinput) > 9:
        # Define the regular expression that will exact the phone number as input
        regex = re.compile(r"[0-9]{10}")

        # Here we extract an array which should have size of 1
        matches = re.findall(regex, userinput)

        # Let the user know that his phone is not found
        if len(matches) == 0:
            return "CON " + language[lang_id['lang']]['phone-not-found']
        

        # Getting the url that will be passed in to get the associated account
        url = 'http://csu.meshpower.co.rw:6001/accounts/api-phone/v3/' + matches[0]
        header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

        # Retrieving data from the url 
        r = requests.get(url, headers=header)

        #If response is not defined
        if r.status_code != 200:
            return language[lang_id['lang']]['phone-request-failed']

        data = r.json()

        # If the dictionary returned of given number has no account
        for key, value in data.items():
            if value == "No such account" or value == "ERROR":
                return "CON " + language[lang_id['lang']]['phone-not-found']

        # Checking if the incoming phone is equal to the data from the database
        if matches[0] == data['phone-number']:
            account = str(data['account'])
                
            return 'Account number: ' + str(account)
        else:
            return 'CON Incorrect phone number, Please try again\n\n0. Back\n00. Back Home'
    else:
        return "CON " + language[lang_id['lang']]['phone-not-found']

