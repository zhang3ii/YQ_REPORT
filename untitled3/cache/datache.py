from django.core.cache import caches
from untitled3.models import *


class DataCache:
    def __init__(self, model=SearchReport, cacheName='default', timeout=60*60*24):
        self.model = model
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getData(self, keyword):
        data = list(SearchReport.objects.filter(title__icontains=keyword).order_by('-report_time').values())
        return data

    def getDataAll(self):
        data = SearchReport.objects.all().values('id').order_by('-report_time')
        return data

    def getValueFromCache(self, keyword):
        if keyword:
            result = self.cache.get(keyword)
            if not result:
                result = self.getData(keyword)
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
        data = list(SearchReport.objects.filter(id__in=l).values())
        # 这里报错了
    return data

