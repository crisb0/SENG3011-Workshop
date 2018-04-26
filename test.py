import urllib.request
import json
import sys
import difflib

# Make an HTTP request for the given company name, start and end date, and stats,
# according to the request format specified in the group_data.
def make_request(group_data, comp_name, start_date, end_date, stats):
    if group_data["time_format"] == "with_millis":
        start_date = start_date.replace("Z",".000Z")
        end_date = end_date.replace("Z",".000Z")
    if group_data["time_format"] == "no_z":
        start_date = start_date.replace("Z","")
        end_date = end_date.replace("Z","")
    request = group_data["format"] %(comp_name, start_date, end_date, ",".join(stats))
    print("================== currently testing %s for %s from %s to %s =================" % (group_data["name"], comp_name, start_date, end_date))
    try:
        webURL = urllib.request.urlopen(request)
        encoding = webURL.info().get_content_charset('utf-8')
        result = webURL.read()
    except urllib.error.HTTPError as e:
        encoding = e.info().get_content_charset('utf-8')
        result = e.read()
    return json.loads(result.decode(encoding))

# Given two group datas, and request parameters, run the request for both groups
# and generate an HTML file that contains the side-by-side diff of their output.
def compare(group_data1, group_data2, comp_name, start_date, end_date, stats):
    res1 = json.dumps(make_request(group_data1, comp_name, start_date, end_date, stats),sort_keys=True, indent=4)
    res2 = json.dumps(make_request(group_data2, comp_name, start_date, end_date, stats),sort_keys=True, indent=4)
    diff = difflib.HtmlDiff().make_file(res1.splitlines(), res2.splitlines(), fromdesc=group_data1["name"], todesc=group_data2["name"])
    with open ("comparing_%s_%s_%s.html" % (group_data1["name"], group_data2["name"], comp_name), "w") as output_file:
        output_file.write(diff)

# Given a list of group data for different teams and some request parameters, compare 
# the responses to the request for all groups in the list pairwise.
def compare_all(urls, comp_name, start_date, end_date, stats):
    for i in range(len(urls)):
        for url in urls[i+1:]:
            compare(urls[i], url, comp_name, start_date, end_date, stats)
    return None

api_list = [ { "name": "qt3.14", "format": "http://qt314.herokuapp.com/v2/company/%s?start_date=%s&end_date=%s&stats=%s", "time_format": "correct" },
             { "name": "moose",  "format": "http://seng3011-moose.herokuapp.com/v2/company?id=%s&start_date=%s&end_date=%s&stats=%s", "time_format": "with_millis" },
             ]
# TODO: add crushing beasts once we figure out how to make a successful request to them.
# { "name": "crushing beasts", "format": "http://188.166.238.3/api/v1/fbstats?instid=%s&startdate=%s&enddate=%s&stats=%s", "time_format": "no_z" }  ]

compare_all(api_list, "woolworths", "2015-10-01T08:45:10Z", "2015-11-01T08:45:10Z", ["id","name","website","description","category","fan_count","post_like_count","post_comment_count","post_type"])
compare_all(api_list, "anzaustralia", "2016-11-01T08:45:10Z", "2017-12-01T08:45:10Z", ["id","name","website","description","category","fan_count"])
compare_all(api_list, "accenture", "2017-11-01T00:00:00Z", "2017-11-09T00:00:00Z", ["id","name","website","description","category","fan_count", "post_type", "post_like_count", "post_comment_count"])
compare_all(api_list, "HyundaiAustralia", "2017-03-01T00:00:00Z", "2017-11-09T12:59:00Z", ["id","name","website","description","category", "post_type", "post_like_count", "post_message"])
compare_all(api_list, "medibank", "2018-01-12T00:00:00Z", "2018-02-12T00:00:00Z", ["id","name", "post_like_count", "post_message"])