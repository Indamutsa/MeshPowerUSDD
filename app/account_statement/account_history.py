import requests, re, json
import time 

# In this file we will return account top up and consumption history

# This function return the top up history given the account number
def top_up_history(account):
    print("Account history: " + account)
    
    # Declaring the url that will retrieve data of a given account
    url = 'http://csu.meshpower.co.rw:6001/accounts/api-top-up/v3/204905'
    header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

    # Retrieving data from the url 
    r = requests.get(url, headers=header)
    
    
    #If response is defined
    if r.status_code != 200:
        return "Account number not found"

    # This variable will hold the list of the five recent topups
    top_up = r.json()

    i = 0
    user_info = ''

    # We will concatenate the last five topups
    for data in top_up:
        i = i + 1
        
        # We would like to display only five 
        if i == 5:
            break

        # Retrieving the time and topup amount
        topup_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(data['time'])))
        topup_amount = "Topup: " + str(data['consumed_amount']) + "frw"

        # Contenated string that we return
        user_info = user_info + topup_time + "\n" +topup_amount + "\n"
        
    return user_info



# This function return the consumption history given the account number
def consumption_history(account):
    print("Consumption history: " + account)
    
    # Declaring the url that will retrieve data of a given account
    url = 'http://csu.meshpower.co.rw:6001/accounts/api-consumption/v3/204905'
    header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

    # Retrieving data from the url 
    r = requests.get(url, headers=header)
    
  
    # Check if the request did not fail 
    if r.status_code != 200:
        return "Account number not found"

    # Retrieving the list of consumption history
    consumption = r.json()

    print(consumption)
    
    i = 0
    user_info = ''

    # We will concatenate the last five topups
    for data in consumption:

        # Retrieving the time and amount consumed
        consumed_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(int(data['time'])))
        consumed_amount = "Consumed: " + str(data['consumed_amount']) + "frw"
        balance = "Balance: " + str(data['cash_balance'])

        # Contenated string that we return
        user_info = user_info + consumed_time + "\n" + consumed_amount + "\n" + balance + "\n" 


        i = i + 1
        
        # We would like to display only five 
        if i == 5:
            break

    return user_info
            
