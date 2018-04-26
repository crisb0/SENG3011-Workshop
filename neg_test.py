import sys, requests, re, json

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

def negerr_req(req_deets):
    # test without id
    request = req_deets["format"] % ('?', req_deets["start_date"], req_deets["end_date"], req_deets["stats"])
    t1 = mk_req(request)

    # test without start_date
    request = req_deets["format"] % (req_deets["page"], '', req_deets["end_date"], req_deets["stats"])
    t2 = mk_req(request)

    # test without end_date
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], '', req_deets["stats"])
    t3 = mk_req(request)

    # test without stats
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], req_deets["end_date"], '')
    t4 = mk_req(request)

    request = req_deets["format"] % ('', '', '', '')
    t5 = mk_req(request)

    if not t1 and not t2 and not t3 and not t4:
        print("!error not correctly returned for missing parameter(s)")

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

def read_request():
    negerr_req(api_list[sys.argv[1]])

if __name__ == '__main__':
    read_request()

