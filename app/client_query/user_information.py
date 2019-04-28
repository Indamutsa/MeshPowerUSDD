from app.utils.ussd_util import  initiliaze_user_space
import re, requests

def applyForService(inputdata):
    num = countStar(inputdata)

    district = ["Bugesera"]

    if num == 3:
        return "CON Enter your name"
    elif num == 4:
        return "CON Enter your sector"
    elif num == 5:
        return "CON Enter your District"
    elif num == 6:
        userInfo = ""
        hello = inputdata[6:].split("*")
        hellow = ["Name: ", "Sector: ", "District: "]
        
        for h, p in zip(hello, hellow):
            print(p, h)
            userInfo += p + "" + h + "\n"

        return "CON " + "You entered: \n\n" + userInfo + "\nPress\n1. confirm\n00. Go Home"
    elif '1' in inputdata[:2] and num == 7:
        return "Thank you for submitting, we shall get back to you asap"

def reportIssues(inputdata):
    
    num = countStar(inputdata)
    
    if inputdata == '1*2*6*':
        return 'CON Enter your account\n\n0. Back\n00. Back Home'

    elif re.match("[126*]+\*[0-9]{6}\*$", inputdata):
        # Define the regular expression that will extract the account number as input
        regex = re.compile(r"[0-9]{6}")
      
        # Here we extract an array which should have size of 1
        matches = re.findall(regex, inputdata)
     
        if len(matches) == 0:
            return "CON Account number not found\n\n0. Back\n00. Back Home"
        
        # Getting the url that will be passed in to get the associated account
        url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
        header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}
 
        # Retrieving data from the url 
        r = requests.get(url, headers=header)
        
        #If response is defined
        if r.status_code == 200:
            return "CON Briefly, tell us your issue"
        
    elif re.match("[126*]+\*[0-9]{6}\*[\w]+\*$", inputdata) and num == 5:

        print (num , "======================================================================")
        #elif num == 4:
        print("sdfssssssssssssssssssssssss")
        userInfo = ""
        
        hello = inputdata[6:].split("*")
        hellow = ["account: ", "Issue: "]
        
        
        for h, p in zip(hello, hellow):
            print(p, h)
            userInfo += p + "" + h + "\n"
        
        return "CON " + "You entered: \n\n" + userInfo + "\nPress\n1. confirm\n00. Go Home"
    elif '1' in inputdata[:2] and num == 6:
        return "Thank you for submitting, we shall get back to asap"


def countStar(word):
    character = '*'
    num = word.count(character)

    return num
