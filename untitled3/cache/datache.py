from django.core.cache import caches
from untitled3.models import *


class DataCache:
    def __init__(self, model=SearchReport, cacheName='default', timeout=60*60*24):
        self.model = model
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getData(self, keyword, searchWord):
        if keyword != '' and searchWord != '':
            data = SearchReport.objects.filter(title__icontains=keyword, statue=1, source=searchWord).values('id').order_by('-report_time')
        elif keyword == '' and searchWord != '':
            data = SearchReport.objects.filter(statue=1, source=searchWord).values('id').order_by('-report_time')
        else:
            data = SearchReport.objects.filter(title__icontains=keyword, statue=1).values('id').order_by('-report_time')
        return data

    def getDataAll(self):
        data = SearchReport.objects.filter(statue=1).values('id').order_by('-report_time')
        return data

    def getValueFromCache(self, keyword, searchWord):
        if keyword or searchWord:
            result = self.getData(keyword, searchWord)
            self.cache.set(keyword, result, self.timeout)
        else:
            result = self.cache.get('getalldata')
            if not result:
                result = self.getDataAll()
                self.cache.set('getalldata', result, self.timeout)
        return result

def getMsgFromDatabase(idListDic):
    l = []
    for id in idListDic:
        l.append(id['id'])
    if idListDic == []:
        data = []
    else:
        data = list(SearchReport.objects.filter(id__in=l, statue=1).values())
    return data

