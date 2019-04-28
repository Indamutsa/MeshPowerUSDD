#Find the balance
import requests, re, json



#url = 'http://data.meshpower.co.rw/accounts/api/v3/171579'

def findBalance(userinput):
    try:
        #Converting the user input into a string from unicode
        userinput = str(userinput)

        if userinput == '1*2*2*':
            return 'CON Enter your account\n\n0. Back\n00. Back Home'
        #elif '1*2*2*' in userinput and len(userinput) == 6:
        elif re.match("[12*]+\*[0-9]{6}\*$", userinput):

            # Define the regular expression that will extract the account number as input
            regex = re.compile(r"[0-9]{6}")

            # Here we extract an array which should have size of 1
            matches = re.findall(regex, userinput)


            if len(matches) == 0:
                return "CON Account number not found\n\n0. Back\n00. Back Home"

            # Getting the url that will be passed in to get the associated account
            url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
            header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

            # Retrieving data from the url 
            r = requests.get(url, headers=header)
            print(r)        
            #If response is defined
            if r.status_code != 200:
                return "Account number not found"

            data = r.json()
             
            for key, value in data.items():
                if value == "No such account" or value == "ERROR":
                    return "Account number not found"


            # Checking if the incoming account is equal to the data from the database
            if len(data) > 2 and matches[0] == data['account']:
                    
                balance = str(data['balance'])
                currency = data['currency']
                
                return 'Balance: ' + balance +""+ currency
            else:
                return 'Incorrect account number, try again'
        else:
            print("NO such account number")
    except:
        return "Bad input, try again"
