from google.appengine.api import mail
import re
import ops
import webapp2
import json
from google.appengine.api import users
import storage_ops
from google.appengine.api import search
import logging
import random


class CreateStreamServiceHandler(webapp2.RequestHandler):
    def post(self):

        user_id = self.request.get('user_id')  # from Zhangyi 'current_user' exactly
        name = self.request.get('name')  # from page
        cover_url = self.request.get('cover_url')  # from page    can be empty!

        if cover_url == "":
            num = int(random.random() * 5)
            cover_url = "https://storage.googleapis.com/pigeonhole-apt.appspot.com/" \
                        "defaultcoverimagefolderyaohuazhao/" + str(num) + ".jpg"

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
            mail.send_mail(sender='yaohua@pigeonhole-apt.appspotmail.com',
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
        index = search.Index(name='newSearchTwo')

        name_str = self.getSubStrings(name)

        '''add docu into index'''
        fields = [
            search.TextField(name='name', value = name),
            search.TextField(name='tag', value = tags),
            search.TextField(name='helper_name', value=name_str)]

        d = search.Document(fields=fields)
        try:
            add_result = index.put(d)  # return array
        except search.Error:
            logging.exception('An error occurred on adding.')

    def getSubStrings(self,str):
        string_list = []
        length = len(str)
        string_list.extend([str[i:j + 1] for i in xrange(length) for j in xrange(i, length)])
        return " ".join(string_list)


class SearchServiceHandler(webapp2.RequestHandler):
    def get(self):

        searchContent = self.request.get('searchContent')
        query = searchContent
        try:
            index = search.Index(name='newSearchTwo')
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

class SecondSearchServiceHandler(webapp2.RequestHandler):
    def get(self):

        searchContent = self.request.get('searchContent')
        query = searchContent
        try:
            index = search.Index(name='newSearchTwo')
            search_results = index.search(query)  # result list
            #returned_count = len(search_results.results)
            number_found = search_results.number_found

            streamList = []
            for doc in search_results:
                streamList.append( doc.fields[0].value )

        except search.Error:
            logging.exception('An error occurred on search.')

        streamInfo = ops.get_search_stream_two(streamList)
        return_info = {
            'num' : number_found,
            'streams': streamInfo
        }
        self.response.write(json.dumps(return_info))


class TrendingServiceHandler(webapp2.RequestHandler):
    def get(self):
        userid = self.request.get('user_id')
        destination = ops.get_cron_destination(userid)
        trending = ops.get_trending_stream()
        return_info = {
            'rate' : destination,
            'trending': trending
        }
        self.response.write(json.dumps(return_info))




class CronServiceHandler(webapp2.RequestHandler):
    def get(self):
        count1 = ops.get_c1()
        count2 = ops.get_c2()
        count3 = ops.get_c3()

        count1 = count1+1
        count2 = count2+1
        count3 = count3+1
        if(count1==1):
            count1=0
            userList = ops.get_cron_pigeon_id_list(1)
            if userList:
                for i in range(len(userList)):
                    self.send_simple_message(userList[i])

        if(count2==12):
            count2=0
            userList = ops.get_cron_pigeon_id_list(12)
            if userList:
                for i in range(len(userList)):
                    self.send_simple_message(userList[i])

        if(count3==288):
            count3=0
            userList = ops.get_cron_pigeon_id_list(288)
            if userList:
                for i in range(len(userList)):
                    self.send_simple_message(userList[i])

        ops.set_c1(count1)
        ops.set_c2(count2)
        ops.set_c3(count3)



    def send_simple_message(self,email):
        msg=""
        for stream in ops.get_trending_stream():
            msg += " Trending Stream Name: " + stream['Name']
            url = 'https://pigeonhole-apt.appspot.com/view_single?stream_id='+stream['Name']
            msg +=' Click Here for More: '
            msg += url
            
        mail.send_mail(sender='pigeon_apt@pigeonhole-apt.appspotmail.com',
                        to = str(email),
                        subject = 'From Pigeon Group',
                        body = msg
        )


class SetDestinationService(webapp2.RequestHandler):
    def get(self):
        userid = self.request.get('user_id')
        desti = self.request.get('rate')
        if desti =='no':
            ops.set_cron_destination(-1, userid)
        if desti == '5min':
            ops.set_cron_destination(1, userid)
        if desti == '1hour':
            ops.set_cron_destination(12, userid)
        if desti == '1day':
            ops.set_cron_destination(288, userid)

class GetSearchSuggestionService(webapp2.RequestHandler):
    def get(self):

        searchContent = self.request.get('searchContent')
        query = searchContent
        try:
            index = search.Index(name='newSearchTwo')
            search_results = index.search(query)  # result list
            #returned_count = len(search_results.results)
            number_found = search_results.number_found

            streamList = []
            for doc in search_results:
                streamList.append( doc.fields[0].value )

        except search.Error:
            logging.exception('An error occurred on search.')

        import locale
        locale.setlocale(locale.LC_ALL, '')
        streamList = sorted(streamList, cmp=locale.strcoll)

        return_info = {
            'result': streamList
        }
        self.response.write(json.dumps(return_info))