# Database related operation
from datetime import datetime, timedelta

from google.appengine.ext import ndb

from models import Image, Stream, Pigeon, Subscription, CronJob, Count


def create_stream(pigeon_id, name, cover_url,
                  sub_list, tag_list):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream = Stream()
    stream.key = ndb.Key(Stream, name, parent=pigeon_key)
    stream.name = name
    stream.cover_url = cover_url
    stream.tags = tag_list
    stream.put()
    for pid in sub_list:
        if pid != pigeon_id:
            if not pigeon_exists(pid):
                create_pigeon(pid)
            suber_key = ndb.Key(Pigeon, pid)
            sub = Subscription()
            sub.Pigeon_key = suber_key
            sub.Stream_key = stream.key
            sub.put()
    return


def stream_exists(name):
    if Stream.query(Stream.name == name).fetch():
        return True
    return False


def get_self_stream(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream_list = Stream.query(ancestor=pigeon_key).fetch()
    return map(_get_stream_dict, stream_list)


def get_sub_stream(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    sub_list = Subscription.query(
        Subscription.Pigeon_key == pigeon_key).fetch()
    stream_list = []
    for sub in sub_list:
        if sub.Stream_key.get():
            stream_list.append(sub.Stream_key.get())
    return map(_get_stream_dict, stream_list)


def pigeon_exists(pigeon_id):
    if Pigeon.query(Pigeon.pigeon_id == pigeon_id).fetch():
        return True
    return False


def create_pigeon(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    pigeon = Pigeon()
    pigeon.key = pigeon_key
    pigeon.pigeon_id = pigeon_id
    pigeon.put()
    create_cron(pigeon_id)
    return


def _get_stream_dict(stream):
    stream_dict = dict()
    stream_dict['Name'] = stream.name
    image_list = Image.query(ancestor=stream.key).order(Image.upload_date).fetch()
    if image_list:
        stream_dict['LastPictDate'] = str(image_list[-1].upload_date)  # Yaohua Mod
        stream_dict['NumberOfPict'] = len(image_list)
    else:
        stream_dict['LastPictDate'] = str(stream.create_date)   # Yaohua Mod
        stream_dict['NumberOfPict'] = 0
    stream_dict['Views'] = stream.num_of_views
    return stream_dict


def get_all_stream():
    stream_list = Stream.query().order(Stream.create_date).fetch()
    return map(lambda s: {"Name": s.name, "CoverPage": s.cover_url},
               stream_list)


def get_single_stream(name):
    stream_list = Stream.query(Stream.name == name).fetch()
    if not stream_list:
        return []
    stream = stream_list[0]
    # count the number of views and discard the overtime logs
    delta = timedelta(hours=1)
    for i, dt in enumerate(stream.view_dates):
        if datetime.now() - dt < delta:
            stream.view_dates = stream.view_dates[i:]
            break
    stream.view_dates.append(datetime.now())
    stream.num_of_views = len(stream.view_dates)
    stream.put()
    # return images
    img_list = Image.query(ancestor=stream.key).order(Image.upload_date).fetch()
    return map(lambda img: img.url, img_list[::-1])


def delete_stream(name):
    stream_list = Stream.query(Stream.name == name).fetch()
    if stream_list:
        stream_list[0].key.delete()
    return


def create_subscription(pigeon_id, name):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream_list = Stream.query(Stream.name == name).fetch()
    stream_key = stream_list[0].key
    sub = Subscription()
    sub.Pigeon_key = pigeon_key
    sub.Stream_key = stream_key
    sub.put()
    return


def delete_subscription(pigeon_id, name):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream_list = Stream.query(Stream.name == name).fetch()
    stream_key = stream_list[0].key
    sub_list = Subscription.query(Subscription.Pigeon_key == pigeon_key,
                                  Subscription.Stream_key == stream_key).fetch()
    if sub_list:
        sub_list[0].key.delete()
    return


def get_trending_stream():
    stream_list = Stream.query().fetch()
    for stream in stream_list:
        # count the number of views and discard the overtime logs
        delta = timedelta(hours=1)
        for i, dt in enumerate(stream.view_dates):
            if datetime.now() - dt < delta:
                stream.view_dates = stream.view_dates[i:]
                break
        stream.view_dates.append(datetime.now())
        stream.num_of_views = len(stream.view_dates)
        stream.put()
    stream_list = Stream.query().order(Stream.num_of_views).fetch()
    return map(lambda s: {"Name": s.name,
                          "CoverPage": s.cover_url,
                          "NumberOfViews": s.num_of_views},
               stream_list[::-1][:3])

def create_image(comment, name, url, stream_name):
    stream_list = Stream.query(Stream.name == stream_name).fetch()
    if stream_list:
        stream = stream_list[0]
        image_key = ndb.Key(Image, url, parent=stream.key)
        img = Image()
        img.key = image_key
        img.name = name
        img.url = url
        img.comments = comment
        img.put()
    return


def get_search_stream(stream_name_list):
    result = []
    count = 0
    for i, name in enumerate(stream_name_list):
        if count >= 5:
            break
        stream_list = Stream.query(Stream.name == name).fetch()
        if stream_list:
            count += 1
            stream = stream_list[0]
            result.append({"Name": stream.name,
                           "CoverPage": stream.cover_url})
    return result


def get_stream_owner(stream_name):
    stream_list = Stream.query(Stream.name == stream_name).fetch()
    d = {}
    if stream_list:
        stream = stream_list[0]
        d = {"Id": stream.key.parent().get().pigeon_id}
    return d


def is_subscribed(name, pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream_list = Stream.query(Stream.name == name).fetch()
    stream_key = stream_list[0].key
    sub_list = Subscription.query(Subscription.Pigeon_key == pigeon_key,
                                  Subscription.Stream_key == stream_key).fetch()
    return True if sub_list else False


def get_c1():
    count_list = Count.query().fetch()
    return count_list[0].c1


def get_c2():
    count_list = Count.query().fetch()
    return count_list[0].c2


def get_c3():
    count_list = Count.query().fetch()
    return count_list[0].c3


def set_c1(i):
    count_list = Count.query().fetch()
    count_list[0].c1 = i
    count_list[0].put()
    return


def set_c2(i):
    count_list = Count.query().fetch()
    count_list[0].c2 = i
    count_list[0].put()
    return


def set_c3(i):
    count_list = Count.query().fetch()
    count_list[0].c3 = i
    count_list[0].put()
    return


def create_cron(pigeon_id):
    cron = CronJob()
    cron.pid = pigeon_id
    cron.destination = -1
    cron.put()


def get_cron_pigeon_id_list(des):
    cron_list = CronJob.query(CronJob.destination == des).fetch()
    pigeon_id_list = []
    for c in cron_list:
        pigeon_id_list.append(c.pid)
    return pigeon_id_list


def get_cron_destination(pigeon_id):
    cron_list = CronJob.query(CronJob.pid == pigeon_id).fetch()
    if cron_list:
        return cron_list.destination
    return -1


def set_cron_destination(des, pigeon_id):
    cron_list = CronJob.query(CronJob.pid == pigeon_id).fetch()
    if cron_list:
        cron_list[0].destination = des
        cron_list[0].put()
    return