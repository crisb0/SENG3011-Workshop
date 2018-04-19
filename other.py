import csv, re

# returns dict 
def get_asx_list():
    with open('ASXListedCompanies.csv', mode='rt') as f:
        reader = csv.reader(f)
        asx_dict = {rows[0]:rows[1] for rows in reader}
    return asx_dict

def getFacebookID(name, asx_dict):
        # name can be provided as ASX ticker code (WOW.ASX) OR company name (Woolworths)    
        # if ticker code (regex ***.ASX): look through dict
        company_name = name
        try:
            #if name provided is an instrument id
            match = re.match(r'([A-Za-z]{3})\.ASX', name).group(1)
            if match is not None and match in asx_dict:
                company_name = asx_dict[match]
                company_name = re.sub('\sLIMITED','',company_name)
                instrument_id = name
            else:
                print("Company not found")
                ### eRROR HANDLING REQUIRED
        except:
            pass

        #TODO: if company name string provided, find instrument id
        return company_name
