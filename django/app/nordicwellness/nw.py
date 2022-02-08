import http.client
import nordicwellness.config.settings as conf
import datetime
import json
import logging
import sys
import xmltodict

def _get(url):
    """GET data from Nordic-Wellness API. 

    Returns: 
    json: json object. None if serialnumber not found or failed to contact API."""
    try:
        conn = http.client.HTTPSConnection(conf.server)

        # Generate credentials with
        # printf "username:password" | iconv -p ISO-8859-1 | base64 -i -

        headers = {
            # 'authorization': "Basic %s" % (conf.jss_credential),
            'Accept': 'application/json'
        }

        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)
        return data
    except Exception as err:
        logging.error("[GET] {0} - HTTP status: {1}. {2}".format(url, res.status, err))
        return None

def _post(url, payload):
    """POST data to Nordic-Wellness API. 

    Parameters: 
    url: /Booking
    payload: json formatted data"""
    try:
        conn = http.client.HTTPSConnection(conf.server)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        conn.request("POST", url, json.dumps(payload), headers=headers)

        res = conn.getresponse()
        data = res.read().decode("utf-8")
        return data
    except Exception as err:
        logging.error("HTTP request: {0}. {1}".format(res.status, err))
        return None

def _del(url):
    """DELETE data to Jamf Pro. 

    Parameters: 
    url: /JSSResource/computers/serialnumber/%s
    """
    try:
        conn = http.client.HTTPSConnection(conf.jss_server)

        # Generate credentials with
        # printf "username:password" | iconv -t ISO-8859-1 | base64 -i -
        headers = {
            'authorization': "Basic %s" % (conf.jss_credential),
            'Accept': 'application/xml'
        }

        conn.request("DELETE", url, headers=headers)
        res = conn.getresponse()
        # Exit if error was found
        if res.status != 200:
            raise Exception("")
        data = res.read().decode("utf-8")
        return data
    except Exception as err:
        logging.error("[DELETE] {0} - HTTP status: {1}. {2}".format(url, res.status, err))
        return None



# GET METHODS
def get_activities():
    dates = ""

    url = "/GroupActivity/timeslot?clubIds={0}&activities=&dates={1}&time=&employees={2}&datespan=true&userId={3}".format(conf.clubid, dates, conf.employeeid, conf.userid)
    data = _get(url)
    return data

# PUT METHODS
def book_groupactivitiy(activity):
    """
    Book an event. Payload example:

    payload = {
        "ActivityId": "82317251",
        "UserId": "333305",
        "QueueType": "ordinary"
    }
    """
    payload = {
    'ActivityId': '%s' % activity.id,
    'UserId': '%s' % conf.userid,
    'QueueType': 'ordinary'
    }

    url = "/Booking"
    data = _post(url, payload)
    return data

# Helper functions
def get_datestring():
    returnValue = ""
    for x in range(0, 12):
        date = datetime.datetime.today() + datetime.timedelta(days=x)
        returnValue +=  date.strftime('%Y-%m-%d')
        if x < 11:
            returnValue += ","

    return returnValue 