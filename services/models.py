from google.appengine.ext import ndb


class Image(ndb.Model):
    comments = ndb.StringProperty()
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    gps_lon = ndb.FloatProperty()
    gps_lat = ndb.FloatProperty()
    upload_date = ndb.DateProperty(auto_now_add=True)


class Stream(ndb.Model):
    cover_url = ndb.StringProperty()
    create_date = ndb.DateProperty(auto_now_add=True)
    name = ndb.StringProperty()
    num_of_views = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)
    view_dates = ndb.DateTimeProperty(repeated=True)


class Pigeon(ndb.Model):
    pigeon_id = ndb.StringProperty()  # user's id



class Subscription(ndb.Model):
    Pigeon_key = ndb.KeyProperty(kind="Pigeon")
    Stream_key = ndb.KeyProperty(kind="Stream")


class CronJob(ndb.Model):
    pid = ndb.StringProperty()
    destination = ndb.IntegerProperty()


class Count(ndb.Model):
    c1 = ndb.IntegerProperty()
    c2 = ndb.IntegerProperty()
    c3 = ndb.IntegerProperty()
