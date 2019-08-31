from django.core.cache import caches
from django.db import connection
import time
import pymysql

class Test():
    def __init__(self, cacheName='default',timeout=60 * 60 * 3):
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getValue(self):
        data = self.cache.get('1')
        if not data:
            data = 1
            time.sleep(10)
            self.cache.set('1',data,self.timeout)
        return data

class DataCache():
    '''
    缓存模块
    '''
    def __init__(self, dict, city, industry, rank, cacheName='default', timeout=60 * 60 * 3):
        self.dict = dict
        self.city = city
        self.industry = industry
        self.rank = rank
        self.cache = caches[cacheName]
        self.timeout = timeout
        self.cursor = connection.cursor()

    def getData(self):

        def tran(num):
            if num == 0:
                return '否'
            else:
                return '是'

        def index_tran(store_id):
            if store_id == 0:
                index = ''
            else:
                ss = """select store_index from biz_store_sort where store_id = '{}'""".format(store_id)
                self.cursor.execute(ss)
                index = self.cursor.fetchone()[0]
            return index

        dict = self.dict
        city = self.city
        industry = self.industry
        # rank = request.args['rank']
        sal = """SELECT unified_store.unified_store_id,unified_store.store_name,unified_store.store_area,
        unified_store.store_city,unified_store.store_industry_name,store_relation.update_at,
        store_relation.hlj_store_id,store_relation.dzdp_store_id,store_relation.bhhl_store_id,store_relation.hbh_store_id
        from unified_store,store_relation where unified_store.unified_store_id = store_relation.unified_store_id """
        if dict:
            sal = sal + """and unified_store.store_name like '%{}%' """.format(dict)
        if city:
            sal = sal + """and unified_store.store_city = '{}' """.format(city)
        if industry:
            sal = sal + """and unified_store.store_industry_name = '{}' """.format(industry)
        print(sal)

        self.cursor.execute(sal)
        res = self.cursor.fetchall()
        search_total = len(res)
        page_num = search_total // 15 * 10
        # 添加模型
        model = {}

        for c in res:
            hlj_store_rank = index_tran(c[6])
            dzdp_store_rank = index_tran(c[7])
            bhhl_store_rank = index_tran(c[8])
            partnership_hlj = tran(c[6])
            partnership_dp = tran(c[7])
            partnership_bhhl = tran(c[8])
            partnership_hbh = tran(c[9])
            response = {
                'store_id': c[0],
                'store_name': c[1],
                'area': c[2],
                'city': c[3],
                'industry': c[4],
                'update_time': c[5],
                'partnership_hlj': partnership_hlj,
                'partnership_dp': partnership_dp,
                'partnership_bhhl': partnership_bhhl,
                'partnership_hbh': partnership_hbh,
                'hlj_store_rank': hlj_store_rank,
                'dzdp_store_rank': dzdp_store_rank,
                'bhhl_store_rank': bhhl_store_rank,
            }
            if self.rank == '1':
                key = hlj_store_rank
                try:
                    key = int(key)
                except:
                    key = 0
                model[key] = response
            elif self.rank == '2':
                key = dzdp_store_rank
                try:
                    key = int(key)
                except:
                    key = 0
                model[key] = response
            elif self.rank == '3':
                key = bhhl_store_rank
                try:
                    key = int(key)
                except:
                    key = 0
                model[key] = response
        self.cache.set('getAllData'+str(self.rank), model, timeout=5 * 60)

        return model

    def getDataFromCache(self):
        data = self.cache.get('getAllData'+str(self.rank))
        if data is None:
            data = self.getData()
        return data

