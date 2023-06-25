from pushover import Pushover
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
    
    pushover = Pushover(conf.pushover_token)
    pushover.user(conf.pushover_user)

    msg = pushover.msg(message)
    msg.set("title", title)

    pushover.send(msg)