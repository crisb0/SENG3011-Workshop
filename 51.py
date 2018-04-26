import sys, requests, json

api_list = {    "qt3.14": { "format":"http://qt314.herokuapp.com/v2/company/%s%s%s%s",
                             "page":"accenture?",
                             "start_date":"start_date=2015-10-01T08:45:00Z",
                             "end_date": "&end_date=2016-10-01T08:45:00Z",
                             "stats": "&stats=id"
                         },
                 "moose": {  "format": "http://seng3011-moose.herokuapp.com/v2/company%s%s%s%s",
                             "page": "?id=accenture",
                             "start_date": "&start_date=2015-10-01T08:45:00.000Z",
                             "end_date": "&end_date=2015-10-01T08:45:00.000Z",
                             "stats": "&stats=id"
                         }
             }


def bad_format():
    api = sys.argv[1]
    req_deets = api_list[api]

    # testing with badly formatted start and end dates
    request = req_deets["format"] % (req_deets["page"], "&start_date=2015.10.01T", "&end_date=2016.10.01T", req_deets["stats"])
    t1 = mk_req(request)

    # testing with stats as list given with spaces instead of commas
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], req_deets["end_date"], "&stats=id name website")
    t2 = mk_req(request)    

    # testing with non-existent statistic
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], req_deets["end_date"], "&stats=id,name,blah,post_id,post_blah")
    t3 = mk_req(request)

    # testing same exact start and end date
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], req_deets["start_date"], req_deets["stats"])
    t4 = mk_req(request)

    if not t1 and not t2 and not t3 and not t4:
        print("!error not returned upon incorrect formatting of query parameters")


def mk_req(request):
     res = requests.get(request)
     if str(res) != "<Response [400]>":
         return True
     try:
         res_json = res.json()
         if re.search('request_status.*:.*fail', str(res_json)):
             return True
     except:
         pass
     return False



if __name__ == '__main__':
    bad_format()
