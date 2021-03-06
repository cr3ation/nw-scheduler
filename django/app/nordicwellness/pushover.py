from pushover import Client
from nordicwellness.config import settings as conf

def send(activity):
    if not activity:
        return

    message = "\nā± {0} \n\nšš»āāļø {1}".format(activity.start_time_str, activity.instructor) 
    title = "ā %s" % activity.name
    __send(message, title)


def __send(message, title):
    if not message or not title:
        return
    
    client = Client(conf.pushover_user, api_token=conf.pushover_token)
    client.send_message(message, title=title)