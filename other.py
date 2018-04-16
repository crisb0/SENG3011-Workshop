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

def createFields(stats):
    page_stats = ['id']
    post_stats = ['id']
    for x in stats: 
        match = re.match('^post_(.*)', x)
        if match is not None:
            match = match.group(1)
            field = match;
            if match == 'like_count':
                field = 'likes.limit(0).summary(total_count)'
            if match == 'comment_count':
                field = 'comments.limit(0).summary(total_count)'
            if x != 'post_id':
                post_stats.append(field)
        else:
            if x == 'description':
                x = 'about'
            if x != 'id':
                page_stats.append(x)

    print(','.join(page_stats), ','.join(post_stats))
    return ','.join(page_stats), ','.join(post_stats)
