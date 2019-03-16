import requests
from requests.auth import HTTPBasicAuth
import json
import datetime


class ConvertedTime:
    """Will take a passed jira date and slice it to be used with the datetime module"""
    def __init__(self, absolute_date):
        self.year = int(absolute_date[0:4])
        self.month = int(absolute_date[5:7])
        self.day = int(absolute_date[8:10])
        self.hours = int(absolute_date[11:13])
        self.minutes = int(absolute_date[14:16])
        self.seconds = int(absolute_date[17:19])

    def calc_downtime(self):
        """Returns a timedelta variable for use in calculating downtime"""
        return datetime.timedelta(hours=self.hours, minutes=self.minutes, seconds=self.seconds)

    def date_time(self):
        """Creates a combined date and time variable. Is used with .strftime('%c') for formatting"""
        return datetime.datetime(year=self.year, month=self.month, day=self.day, hour=self.hours, minute=self.minutes,
                                 second=self.seconds)

# Variables to be passed during the HTTP request
user = "cliff.weir@kindred.ai"
token = "ylFvAn3StGU9nVomcoMcE3E9"
URL = "https://daedalus.atlassian.net/rest/agile/1.0/board/1/issue?fields=summary&fields=description&fields=started&" \
      "fields=created&fields=resolution&fields=resolutiondate"

auth = HTTPBasicAuth(user, token)

headers = {
    "Accept": "application/json"
}

# The actual HTTP request, with the information request saved to "response"
response = requests.get(URL, headers=headers, auth=auth)

# JSON-ing the requested data and assigning it to "data"
data = json.loads(response.text)
# This for loop takes the http request and formats the information for the EOD
# Each run through the loop handles the formatting of a single issue
for x in data["issues"]:
    # Creates a ConvertedTime object for use with the datetime module
    start_date = ConvertedTime(x["fields"]["created"])
    # Converts the sliced date into a timedelta object allowing it to be added, subtracted, ect. from other dates
    start_time = start_date.calc_downtime()
    # Checks if the issue has a "resolutiondate". If so, the same processes applied to the "created" field are applied
    # to the "resolutiondate" field, as well as creating a "downtime" variable
    if x["fields"]["resolutiondate"] is not None:
        end_date = ConvertedTime(x["fields"]["resolutiondate"])
        end_time = end_date.calc_downtime()
    # print(x.keys()) Just here for digging through the json
    # print(x.values()) Just here for digging through the json
    print("Summary: {}".format(x["fields"]["summary"]))

    print("Description: {}".format(x["fields"]["description"]))  # In the Final Version this line will most likely be
    # removed. It will be replaced with orb, site and other Kindred specific fields

    print("Issue created: {}".format(start_date.date_time().strftime("%c")))
    if x["fields"]["resolutiondate"] is None:
        print("The issue was not resolved/marked as resolved.")
    else:
        print("Issue resolved: {}.".format(end_date.date_time().strftime("%c")))
        if end_date.date_time() - start_date.date_time() is not None:
            downtime = end_date.date_time() - start_date.date_time()
            print("Total downtime: {}".format(downtime))
        else:
            print("No downtime recorded")

