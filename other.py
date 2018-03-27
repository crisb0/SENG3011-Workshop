#usr/bin/env python3
import csv

# returns dict 
def get_asx_list():
	with open('ASXListedCompanies.csv', mode='rb') as f:
		reader = csv.reader(f)
		asx_dict = {rows[0]:rows[1] for rows in reader}
	return asx_dict
