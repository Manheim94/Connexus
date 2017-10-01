from google.appengine.ext import ndb


class Image(ndb.Model):
    comments = ndb.StringProperty()
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    upload_date = ndb.DateProperty()


class Stream(ndb.Model):
    cover_url = ndb.StringProperty()
    create_date = ndb.DateProperty()
    name = ndb.StringProperty()
    num_of_views = ndb.IntegerProperty()
    tags = ndb.StringProperty(repeated=True)


class Pigeon(ndb.Model):
    pigeon_id = ndb.StringProperty() # user's id


class Subscription(ndb.Model):
    Pigeon_key = ndb.KeyProperty(kind="Pigeon")
    Stream_key = ndb.KeyProperty(kind="Stream")
