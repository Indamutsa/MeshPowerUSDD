#Find the balance
import requests, re, json

#url = 'http://data.meshpower.co.rw/accounts/api/v3/171579'

# Find balance 
def findBalance(userinput, lang_id, language):
    
    #Converting the user input into a string from unicode
    userinput = str(userinput)

    print(lang_id['num'], "######################", userinput)

    if userinput == '1*' + lang_id['num'] + '*2*':
        return 'CON ' + language[lang_id['lang']]['balance']['account-balance']

    #elif '1*2*2*' in userinput and len(userinput) == 6:
    elif re.match("[12*]+\*[0-9]{6}\*$", userinput):

        # Define the regular expression that will extract the account number as input
        regex = re.compile(r"[0-9]{6}")

        # Here we extract an array which should have size of 1
        matches = re.findall(regex, userinput)


        if len(matches) == 0:
            return "CON " + language[lang_id['lang']]['balance']['account-not-phone']

        # Getting the url that will be passed in to get the associated account
        url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
        header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

        try:
            # Retrieving data from the url 
            r = requests.get(url, headers=header)
            print(r)        
            #If response is defined
            if r.status_code != 200:
                return  language[lang_id['lang']]['balance']['system-failure']

            data = r.json()
        except:
            return 'CON ' + language[lang_id['lang']]['balance']['account-not-found']


        for key, value in data.items():
            if value == "No such account" or value == "ERROR":
                return language[lang_id['lang']]['balance']['account-not-found']


        # Checking if the incoming account is equal to the data from the database
        if len(data) > 2 and matches[0] == data['account']:
                
            balance = str(data['balance'])
            currency = data['currency']
            
            return language[lang_id['lang']]['balance']['balance'] + balance +""+ currency
        else:
            return 'CON ' + language[lang_id['lang']]['balance']['incorrect-account']
    else:
        return 'CON ' + language[lang_id['lang']]['balance']['incorrect-account']


# Find account summary
def find_account_summary(userinput, lang_id, language):

    #Converting the user input into a string from unicode
    userinput = str(userinput)

    if userinput == '1*' + lang_id['num'] + '*7*': 
         return 'CON ' + language[lang_id['lang']]['balance']['account-balance']

    #elif '1*2*2*' in userinput and len(userinput) == 6:
    elif re.match("[127*]+\*[0-9]{6}\*$", userinput):

        # Define the regular expression that will extract the account number as input
        regex = re.compile(r"[0-9]{6}")

        # Here we extract an array which should have size of 1
        matches = re.findall(regex, userinput)


        if len(matches) == 0:
            return "CON " + + language[lang_id['lang']]['balance']['account-not-phone']

        # Getting the url that will be passed in to get the associated account
        url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
        header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}
        
        try:
            # Retrieving data from the url 
            r = requests.get(url, headers=header)
             
            #If response is defined
            if r.status_code != 200:
                return "Account number not found"

            data = r.json()
        except:
            return language[lang_id['lang']]['balance']['system-failure']  

        for key, value in data.items():
            if value == "No such account" or value == "ERROR":
                return language[lang_id['lang']]['balance']['account-not-found']

        # Checking if the incoming account is equal to the data from the database
        if len(data) > 2 and matches[0] == data['account']:
                
            balance = str(data['balance'])
            currency = data['currency']
            tariff_name = str(data['plan_tariff_name']).split()[-1]
            remaining = str(data['days_remaining'])
            name = data['name']
            account = str( data['account']) 

            return language[lang_id['lang']]['summary']['title'] + name + language[lang_id['lang']]['summary']['account-number'] + account +language[lang_id['lang']]['summary']['balance'] + balance +''+ currency + language[lang_id['lang']]['summary']['tariff_name'] + tariff_name + language[lang_id['lang']]['summary']['remaining'] + remaining

        else:
            return language[lang_id['lang']]['balance']['incorrect-account'] 
    else:
        return language[lang_id['lang']]['balance']['bad-input']

