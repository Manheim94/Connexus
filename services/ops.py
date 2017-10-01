
# Database related operation
from datetime import date

from google.appengine.ext import ndb

from models import Image, Stream, Pigeon, Subscription


def create_stream(pigeon_id, name, cover_url,
                  sub_list, tag_list):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream = Stream()
    stream.key = ndb.Key(Stream, name, parent=pigeon_key)
    stream.name = name
    stream.cover_url = cover_url
    stream.tags = tag_list
    stream.create_date = date.today()
    # TODO: create subscription with sub_list
    stream.put()
    return


def stream_exists(name):
    if Stream.query(Stream.name == name).fetch():
        return True
    return False


def get_self_stream(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    stream_key_list = Stream.query(ancestor=pigeon_key).fetch()
    # TODO: return a list of dict of stream
    return []


def get_sub_stream(pigeon_id):
    pigeon_key = ndb.Key(Pigeon, pigeon_id)
    sub_key_list = Subscription.query(
        Subscription.Pigeon_key == pigeon_key).fetch()
    # TODO: return a list of dict of stream
    return []


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
    return


def _get_stream_dict(stream_key):
    stream_dict = {}
    stream_dict['Key'] = stream_key
    stream_dict['Name'] = stream_key.get().name
    image_list = Image.query(ancestor=stream_key).order(Image.upload_date).fetch()
    if image_list:
        stream_dict['LastPictDate'] = image_list[0].upload_date
        stream_dict['NumOfPict'] = len(image_list)
    else:
        stream_dict['LastPictDate'] = stream_key.get().create_date
        stream_dict['NumOfPict'] = 0
    stream_dict['Views'] = stream_key.get().num_of_views
    return stream_dict