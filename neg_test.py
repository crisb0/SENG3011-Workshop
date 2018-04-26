import sys, requests

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
    print("Testing query with missing fields...")
    # test without id
    request = req_deets["format"] % ('?', req_deets["start_date"], req_deets["end_date"], req_deets["stats"])
    res = mk_req(request)
    print(request)

    # test without start_date
    request = req_deets["format"] % (req_deets["page"], '', req_deets["end_date"], req_deets["stats"])
    res = mk_req(request)
    print(request) 

    # test without end_date
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], '', req_deets["stats"])
    res = mk_req(request)
    print(request) 

    # test without stats
    request = req_deets["format"] % (req_deets["page"], req_deets["start_date"], req_deets["end_date"], '')
    res = mk_req(request)
    print(request) 


def mk_req(request):
    res = requests.get(request)
    test_for_err(res) 

def test_for_err(res):
    pass

def read_request():
    negerr_req(api_list[sys.argv[1]])

if __name__ == '__main__':
    read_request()

