import os

# Rename settings_sample.py to settings.py
server = "api1.nordicwellness.se"

clubid = os.environ.get('NW_CLUB_ID')           # Hammarby Sjöstad = "129%2C19439"
userid = os.environ.get('NW_USER_ID')           #
employeeid = os.environ.get('NW_EMPLOYE_ID')    # Elina = 5429

pushover_user = os.environ.get('PUSHOVER_USER')
pushover_token = os.environ.get('PUSHOVER_TOKEN')