from google.appengine.api import mail
import re
import ops
import webapp2
import json
from google.appengine.api import users
import storage_ops
from google.appengine.api import search
import logging


class CreateStreamServiceHandler(webapp2.RequestHandler):
    def post(self):

        user_id = self.request.get('user_id')  # from Zhangyi 'current_user' exactly
        name = self.request.get('name')  # from page
        cover_url = self.request.get('cover_url')  # from page    can be empty!
        subscribers = self.request.get('subscribers')  # from page
        message = self.request.get('message')  # from page
        tags = self.request.get('tags')  # from page

        '''stream already exits, return false'''
        if ops.stream_exists(name):
            return_info = {
                'status': False,
            }
            self.response.write(json.dumps(return_info))
            return

        tag_list = re.findall(r'#\w+', tags)
        sub_list = re.findall(r'[\w\.-]+@[\w\.-]+', subscribers)  # a list of emails

        '''send email'''
        if len(sub_list)!=0:
            mail.send_mail(sender='yaohua@hallowed-forge-181415.appspotmail.com',
                           to=sub_list,
                           subject='You have subscribed the stream: ' + name,
                           body=message
                           )

        '''create stream'''
        ops.create_stream(user_id, name, cover_url, sub_list, tag_list)
        storage_ops.create_stream_in_storage(name)
        return_info = {
            'status': True,
        }
        self.response.write(json.dumps(return_info))

        '''create and add to index'''
        self.AddToIndex(name,tags)

    def AddToIndex(self,name,tags):
        '''index created, exist all way'''
        index = search.Index(name='streamSearch')

        '''add docu into index'''
        fields = [
            search.AtomField(name='name', value = name),
            search.TextField(name='tag', value = tags) ]
        d = search.Document(fields=fields)
        try:
            add_result = index.put(d)  # return array
        except search.Error:
            logging.exception('An error occurred on adding.')



class SearchServiceHandler(webapp2.RequestHandler):
    def get(self):

        searchContent = self.request.get('searchContent')
        query = searchContent
        try:
            index = search.Index(name='streamSearch')
            search_results = index.search(query)  # result list
            #returned_count = len(search_results.results)
            number_found = search_results.number_found

            streamList = []
            for doc in search_results:

                streamList.append( doc.fields[0].value )

        except search.Error:
            logging.exception('An error occurred on search.')

        streamInfo = ops.get_search_stream(streamList)
        return_info = {
            'num' : number_found,
            'streams': streamInfo
        }
        self.response.write(json.dumps(return_info))


class TrendingServiceHandler(webapp2.RequestHandler):
    def get(self):
        trending = ops.get_trending_stream()
        return_info = {
            'trending': trending,
        }
        self.response.write(json.dumps(return_info))




class CronServiceHandler(webapp2.RequestHandler):
    def get(self):
        count = ops.get_cron_count()
        des = ops.get_cron_destination()
        count = count+1

        '''count==des time due'''
        if count == des:
            count = 0
            ops.set_cron_count(count)
            self.send_simple_message()

    def send_simple_message():
        mail.send_mail(sender='yaohua@hallowed-forge-181415.appspotmail.com',
                        to = ['ymh2ee@outlook.com','628zhao@gmail.com'],
                        subject = 'From Pigeon Group',
                        body = 'The trending streams are: '
        )




