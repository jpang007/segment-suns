import requests
import json
from datetime import datetime
from dateutil import parser

userFirstName = ""
userLastName = ""
userEmail = ""
userPhone = ""
userTimeStamp = "" #grab submitted timestamp 
# formIDs 
formID = ["0"] #change this to the formID for every new form
page = 1 #always set this to 1 
numberOfPages = 5 #this field must be manually set, hard to scrape automatically 
count = 1

for rangeI in range(page,numberOfPages + 1): 
    url = "https://www.formstack.com/api/v2/form/" + formID[0] + "/submission.json?page=" + str(rangeI) +"&per_page=100&data=false&expand_data=false"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer <insert bearer token here> "
    }
    #formstack 
    response = requests.get(url, headers=headers)
    y = json.loads(response.text)
    for i in y["submissions"]:
        userTimeStamp = i["timestamp"]
        for j in i.values():
            # print (j)
            if type(j) == dict:
                for z in j.values():
                    if z["type"] == "name": # and z["field"] == "131500967": sometimes these fields are needed if there are multiple names for example
                        userFirstName = (z["value"]["first"])
                        userLastName = (z["value"]["last"])
                    elif z["type"] == "email":
                        userEmail = (z["value"])
                    elif z["type"] == "phone": # and z["field"] == "131500969":
                        userPhone = (z["value"])

        # checks, if field is missing Segment will still ingest! Make sure valuable data e.g email is there
        if userFirstName == "":
            print ("first name missing")
        if userLastName == "":
            print ("last name missing")
        if userPhone == "":
            print ("phone missing")
        if userEmail == "":
            print ("email missing")
        if userTimeStamp == "":
            print ("timestamp missing")
        #datetime(year, month, day, hour, minute, second)
        if parser.parse(userTimeStamp) > datetime(2022,10,31, 14, 00, 00): #This shouldn't be needed if doing the historical pull first and then the ongoing connection after. 
            print (count, userFirstName, userLastName, userPhone, userTimeStamp, userEmail, formID[0])
                #JSON Construction 
                # test URL (grab link from Segment Workspace Source Function)
                # Formstack Stream URL (grab link from Segment Workspace Connections)
            requests.post('formstack stream url', \
                json={  'FormID': formID[0],\
                        'originalTimestamp': userTimeStamp,\
                        'name': {\
                                'first': userFirstName,\
                                'last': userLastName\
                                },\
                        'email': userEmail,\
                        'cell_phone_number': userPhone})
        count += 1

