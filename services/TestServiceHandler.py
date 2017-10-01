import json

class TestServiceHandler:
    def getJson(self):
        abc=1
        jsonData={}
        jsonData['owned_stream_list']=self.getOwnedStreamList()
        jsonData['subed_stream_list'] = []
        jsonData['delete_stream_url'] = []
        jsonData['unsubscribe_stream_url'] = []

        return json.dumps(jsonData)

    def getOwnedStreamList(self):
        list=[]
        stream1={}
        stream1['cover_url']='https://www.google.com/search?tbm=isch&source=hp&biw=1377&bih=890&q=scenery&oq=scenery&gs_l=img.3.0.0l10.914.1784.0.3660.8.8.0.0.0.0.154.590.5j1.6.0.dummy_maps_web_fallback...0...1.1.64.img..2.6.588.0..35i39k1.0.kutdfj62TPo#imgrc=GIyLaGhWOYTDNM:'
        stream1['latest_date'] = "2017-09-08"
        stream1['name']='very beautiful'
        stream1['num_of_pics']=10

        stream2 = {}
        stream2['cover_url']='https://www.google.com/search?tbm=isch&source=hp&biw=1377&bih=890&q=scenery&oq=scenery&gs_l=img.3.0.0l10.914.1784.0.3660.8.8.0.0.0.0.154.590.5j1.6.0.dummy_maps_web_fallback...0...1.1.64.img..2.6.588.0..35i39k1.0.kutdfj62TPo#imgrc=5uTP3ICvuo8SGM:'
        stream2['latest_date'] = "2017-09-09"
        stream2['name'] = 'not beautiful'
        stream2['num_of_pics'] = 10

        list.append(stream1)
        list.append(stream2)
        return list

    def getSubscribedStreamList(self):
        return []

    def getStream(self, stream_key):
        return []