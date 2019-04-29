from app.utils.ussd_util import  initiliaze_user_space
import re, requests

def applyForService(inputdata, lang_id, language):
    
    num = countStar(inputdata)
    print(inputdata)
    if num == 3:
        return 'CON ' + language[lang_id['lang']]['service-application']['enter-name']
    
    elif num == 4:
        return  'CON ' + language[lang_id['lang']]['service-application']['enter-sector']
    
    elif num == 5:
        return  'CON ' + language[lang_id['lang']]['service-application']['enter-district']
    
    elif num == 6:
    
        userInfo = ""
        hello = inputdata[6:].split("*")

        hellow = [language[lang_id['lang']]['service-application']['name'], language[lang_id['lang']]['service-application']['sector'], language[lang_id['lang']]['service-application']['district']]
        
        for h, p in zip(hello, hellow):
            print(p, h)
            userInfo += p + "" + h + "\n"

        return "CON " + language[lang_id['lang']]['service-application']['entered'] + "\n\n" + userInfo + language[lang_id['lang']]['service-application']['confirm']
    
    elif '1' in inputdata[:2] and num == 7:
        return language[lang_id['lang']]['service-application']['thank']

def reportIssues(inputdata, lang_id, language):
    
    num = countStar(inputdata)

    if inputdata == '1*' + lang_id['num'] + '*6*':
   
        return 'CON ' + language[lang_id['lang']]['balance']['account-balance']  

    elif re.match("[126*]+\*[0-9]{6}\*$", inputdata):
        # Define the regular expression that will extract the account number as input
        regex = re.compile(r"[0-9]{6}")
      
        # Here we extract an array which should have size of 1
        matches = re.findall(regex, inputdata)
     
        if len(matches) == 0:
            return "CON " + language[lang_id['lang']]['balance']['account-not-found'] 
        
        # Getting the url that will be passed in to get the associated account
        url = 'http://csu.meshpower.co.rw:6001/accounts/api-account/v3/' + matches[0]
        header = {'X-Authorization': 'Szr7Zdd03aaEkz13XNOdn02vR7j35vvL'}

        try:
            # Retrieving data from the url 
            r = requests.get(url, headers=header)
             
            #If response is defined
            if r.status_code == 200:

                print("************************#######`************************************************", r.status_code)    
                return "CON " + language[lang_id['lang']]['report-issue']['brief-query'] 
        except Exception as e:
            print(e)
            return language[lang_id['lang']]['balance']['system-failure'] 

    elif re.match("[126*]+\*[0-9]{6}\*[\w]+\*$", inputdata) and num == 5:

        print (num , "======================================================================")
        
        userInfo = ""
        
        hello = inputdata[6:].split("*")
        hellow = [language[lang_id['lang']]['report-issue']['account'] , language[lang_id['lang']]['report-issue']['issue'] ]
        
        for h, p in zip(hello, hellow):
            userInfo += p + "" + h + "\n"
        
        return "CON " + language[lang_id['lang']]['service-application']['entered'] + "\n\n" + userInfo + language[lang_id['lang']]['service-application']['confirm'] 

    elif '1' in inputdata[:2] and num == 6:
        return language[lang_id['lang']]['service-application']['thank'] 

def countStar(word):
    character = '*'
    num = word.count(character)

    return num
