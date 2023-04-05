import logging
import re

validcontracts = ["artist", "dealer"]

validmonths = ['January', 'Feburary', 'March', 'April', 'May','June',\
    'July', 'August', 'September', 'October', 'November', 'December']

validKeys = ['contractType', 'month', 'helperBadgeQt', 'additionalChairsQt', 'artistNumber', \
    'shortenedYear', 'day', 'signerName', 'signerEmail', 'approverName', 'approverEmail']


def is_valid_date(year, month, day):
    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year%4==0 and (year%100 != 0 or year%400==0):
        day_count_for_month[2] = 29
    return (1 <= month <= 12 and 1 <= day <= day_count_for_month[month])
 
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

def create_contract(request):
    
    content = request.get_json()
    # Check if request.getjson() returns a dict
    if type(content) != dict:
        return {'error': "request does not return a json"}, 400
    
    # check if content contains all keys
    for key in validKeys:
        if key not in content.keys():
            return {'error': f"missing or invalid {key} field"}, 400
    
    # check if contractType is valid
    if content['contractType'] not in validcontracts:
        return {'error': "missing or invalid 'contractType' field"}, 400
    
    #TODO TEMPORARY DELETE LATER
    if content['contractType'] == "dealer":
        return {'error': "'contractType' dealer not implemented yet"}, 501

    # check if month is valid
    if content['month'] not in validmonths:
        return {'error': "missing or invalid 'month' field"}, 400
    
    # check if helperBadgeQt is valid
    if type(content['helperBadgeQt']) != int or content['helperBadgeQt'] < 0:
        return {'error': "missing or invalid 'helperBadgeQt' field"}, 400
    
    # check if additionalChairsQt is valid
    if type(content['additionalChairsQt']) != int or content['additionalChairsQt'] < 0:
        return {'error': "missing or invalid 'additionalChairsQt' field"}, 400
    
    # check if day is valid
    if type(content['day']) != int:
        return {'error': "missing or invalid 'day' field"}, 400
    
    # check if day is valid
    if type(content['shortenedYear']) != int:
        return {'error': "missing or invalid 'year' field"}, 400

    # date validation
    year = 2000 + content['shortenedYear'] # TODO: change in 2100 :)
    day = content['day']
    month = validmonths.index[content['month']] + 1
    if (not is_valid_date(year, month, day)):
        return {'error': "invalid date"}, 400

    if type(content['signerName']) != str:
        return {'error': "missing or invalid 'signerName' field"}, 400    
    
    if type(content['email']) != str or check_email(content['email']):
        return {'error': "missing or invalid 'email' field"}, 400

    if type(content['approverName']) != str:
        return {'error': "missing or invalid 'approverName' field"}, 400   
    
    if type(content['approverEmail']) != str or check_email(content['approverEmail']):
        return {'error': "missing or invalid 'approverEmail' field"}, 400 

    content['additionalChairsQt']
    content['helperBadgeQt']
    

    logging.warn(request.get_json(force=True)['contentType'])
    

    
    return {'error': "NOT IMPLEMENTED YET"}, 500 #TODO
