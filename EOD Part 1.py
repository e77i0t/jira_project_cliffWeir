# so the point here is to grab the date, orb site and downtime from jira and format it correctly
# Later on may assign variables to custom fields for readabilities sake but as of right now it doesn't seem urgent
# customfield_10033 is the orb number
# customfield_10034 is the orbsite
# customfield_10037 is "slack Working Channel"
# Ticket ID is stored in the 'key' key, which is on the same level as the "issues" key. This script adds the "key"
# key to the "issues" dictionary per ticket so it can be called later.
# Pages are ordered by incident level by default. Since this board doesn't use them it defaults to date created. This
# may cause issues later as only 50 tickets are returned by default, so if this board ever adopts the standard JIRA
# incident levels some changes will have to be made

# The line below refers to a python script in this project folder that I store my token in
from storage import temp_token
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

token = temp_token
user = 'cliff.weir@kindred.ai'
# Below are the additional arguments that the module requests appends onto the url
parameters = {'fields': ['summary, description, started, created, resolution, resolution date, customfield_10034, '
                         'customfield_10037, customfield_10033']}

URL = "https://kindredai.atlassian.net/rest/agile/latest/board/117/issue"

auth = HTTPBasicAuth(user, token)

headers = {
    "Accept": "application/json"
}

# The actual HTTP request, with the information request saved to "response"
response = requests.get(
    URL,
    params=parameters,
    headers=headers,
    auth=auth)

# This stores the info pulled with the http request
data = (json.loads(response.text))

# This list of customers is used with the "sites" dictionary to properly loop through all the dictionary values holding
# the tickets. Since dictionaries are inherently unsorted tethering them to a list ensures everything stays in order
# It SHOULD be possible to write this script in such a way that it can pull the orbsite from jira so it could update
# itself when we get new customers, but let's focus on what's in front of us
customers = ['gapfrs', 'gapglt', 'memdhl', 'aehzt', 'cribst', 'acecat']
# Each "sites" key is the shortform version of a site Kindred operates on. Each value is a list, with the first index
# being the full name of the orb site. Tickets will be added to each value, corresponding with their orb site.
# When I get metabase access, I could probably work total downtime into the value list, at index 1. If it's added as a
# string I'll be able to reference it easily without having to adapt the ticket printing code.
sites = {'gapfrs': ['Gap Fresno'], 'gapglt': ['Gap Gallatin'], 'memdhl': ['Memphis DHL'], 'aehzt':
    ['American Eagile Hazelton'], 'cribst': ['Carters Braselton'], 'acecat': ['Ascena ']}

current_date = datetime.date.today()
# This loop appends the issues into the relevant "sites" value.
for x in data['issues']:
    # This line checks if the customer site in the ticket is present in the keys of the "sites" dictionary
    # PAIN POINT: This script will not be able to track issues that occur in multiple sites, if that issue is recorded
    # in a single ticket. As of right now adapting the script to accommodate that possibility is outside of its scope
    if x['fields']['customfield_10034'] in sites.keys():
        # The below line checks if any tickets were made today, will only add tickets if they were made today
        # EDIT THE LINE BELOW TO 'NOT IN' TO CONTINUE TESTING
        if str(current_date) not in x['fields']['created']:
            temp_orbsite = x['fields']['customfield_10034']
            # This line adds the ticket id to the tickets "fields" dictionary for use later
            x['fields']['ticket_id'] = x['key']
            # Appends the ticket to the "sites" value, by using the tickets orbsite as the dictionary key
            sites[temp_orbsite].append(x['fields'])

issues = False
print("End of Day Report {}".format(current_date))
# If the len of any 'sites' value is greater than one, then issues were added to it
for x in customers:
    if len(sites[x]) > 1:
        issues = True
if issues:
    print("Incidents and Downtime")
    for x in customers:
        # This checks the values of the site dictionary, if there's anything in there besides the site name it means
        # a ticket was added to it. If there is nothing but the site name, the script doesn't make a section for it
        if len(sites[x]) > 1:
            print("{0} - {1}\n {2}" .format(sites[x][0], "Placeholder Downtime", "*" * 40))
            # "ticket" is equivalent to an index from a 'site' values list.
            for ticket in sites[x]:
                if type(ticket) is str:
                    continue
                else:
                    print("{0} | {1} | {2} | {3}\n".format(ticket['summary'], ticket['customfield_10033'],
                    'downtime placeholder', 'https://kindredai.atlassian.net/projects/PI/issues/'+ticket['ticket_id']))

# Will add downtime formatting when I get metabase access
