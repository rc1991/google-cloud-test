from google.appengine.ext import ndb


class Account(ndb.Model):
    userid = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()


