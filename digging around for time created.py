# Bible is here: https://developer.atlassian.com/cloud/jira/software/rest/#api-rest-agile-1-0-board-boardId-backlog-get
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime


class ConvertedTime:
    """Will take a passed jira date and slice it to be used with the datetime module"""
    def __init__(self, absolute_date):
        self.year = absolute_date[0:4]
        self.month = absolute_date[5:7]
        self.day = absolute_date[8:10]
        self.hours = absolute_date[11:13]
        self.minutes = absolute_date[14:16]
        self.seconds = absolute_date[17:19]

    def ymd(self):
        """Returns the jira date in Year Month Day format"""
        return "{0}:{1}:{2}".format(self.year, self.month, self.day)

    def hms(self):
        """Returns the jira date in Hour Minute Second format"""
        return "{0}:{1}:{2}".format(self.hours, self.minutes, self.seconds)

    def calc_downtime(self):
        return datetime.timedelta(hours=int(self.hours), minutes=int(self.minutes), seconds=int(self.seconds))

    def date_time(self):
        return datetime.datetime(year=int(self.year), month=int(self.month), day=int(self.day), hour=int(self.hours),
                                 minute=int(self.minutes), second=int(self.seconds))

    def present_downtime(self):
        pass


def downtime_calc(start, end):
    return start - end


user = "cliff.weir@kindred.ai"
password = "ylFvAn3StGU9nVomcoMcE3E9"
URL = "https://daedalus.atlassian.net/rest/agile/1.0/board/1/issue?fields=summary&fields=description&fields=started&" \
      "fields=created&fields=resolution&fields=resolutiondate"

auth = HTTPBasicAuth(user, password)

headers = {
    "Accept": "application/json"
}

response = requests.request(
    "GET",
    URL,
    headers=headers,
    auth=auth
)

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
data = json.loads(response.text)
y = 0
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
    print(x["fields"]["summary"])

    print(x["fields"]["description"])  # In the Final Version this line will most likely be removed. It will be replaced
    # with orb, site and other Kindred specific fields

    print("Issue was created on {0}, {1}".format(start_date.ymd(), start_date.hms()))
    if x["fields"]["resolutiondate"] is None:
        print("The issue was not resolved/marked as resolved.")
    else:
        print("Issue was resolved on {0}, {1}.".format(end_date.ymd(), end_date.hms()))
        if end_date.date_time() - start_date.date_time() is not None:
            downtime_test = end_date.date_time() - start_date.date_time()
            print("Downtime: {0}.".format(downtime_test))
        else:
            print("No downtime recorded")

