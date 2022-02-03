from pushover import Client
from nordicwellness.config import settings as conf

def send(activity):
    if not activity:
        return

    message = "\n⏱ {0} \n\n🏋🏻‍♀️ {1}".format(activity.start_time_str, activity.instructor) 
    title = "✅ %s" % activity.name
    __send(message, title)


def __send(message, title):
    if not message or not title:
        return
    
    client = Client(conf.pushover_user, api_token=conf.pushover_token)
    client.send_message(message, title=title)