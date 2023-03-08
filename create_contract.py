import logging

validcontracts = ["artist", "dealer"]

validmonths = ['January', 'Feburary', 'March', 'April', 'May','June',\
    'July', 'August', 'September', 'October', 'November', 'December']

validKeys = ['contractType', 'month', 'helperBadgeQt', 'additionalChairsQt', 'artistNumber', \
    'helper1Number', 'shortenedYear', 'day', 'signerName', 'signerEmail', 'approverName', 'approverEmail']

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
        #TODO: if the check is dealer, return a "NOT IMPLEMENTED YET" error (501) | temporary
        return {'error': "missing or invalid 'contractType' field"}, 400

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
    if type(content['day']) != int or content['day'] < 1 or content['day'] > 31:
        return {'error': "missing or invalid 'additionalChairsQt' field"}, 400

    logging.warn(request.get_json(force=True)['contentType'])
    

    
    return {'error': "NOT IMPLEMENTED YET"}, 500 #TODO
