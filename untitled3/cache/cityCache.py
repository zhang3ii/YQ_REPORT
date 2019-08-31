from django.core.cache import caches
from django.db import connection


class CityDataCache():
    '''
    缓存模块
    '''
    def __init__(self, city, cacheName='default', timeout=60 * 60 * 3):
        self.city = city
        self.cache = caches[cacheName]
        self.timeout = timeout
        self.cursor = connection.cursor()

    def get_city(self):

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

        data = {}
        mess = []
        sql = """SELECT unified_store.unified_store_id,unified_store.store_name,unified_store.store_area,
        unified_store.store_city,unified_store.store_industry_name,store_relation.update_at,
        store_relation.hlj_store_id,store_relation.dzdp_store_id,store_relation.bhhl_store_id,store_relation.hbh_store_id
        from unified_store,store_relation where unified_store.unified_store_id = store_relation.unified_store_id and store_city = '{}' LIMIT 20;""".format(
            self.city)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for c in res:
            ids = [c[6], c[7], c[8]]
            store_id = ids[0]
            if store_id == 0:
                store_id = ids[1]
                if store_id == 0:
                    store_id = ids[2]
            index = """SELECT store_index,store_id from biz_store_sort WHERE store_id = '{}';""".format(store_id)
            self.cursor.execute(index)
            rank = self.cursor.fetchone()
            store_index = rank[0]
            search_id = rank[1]
            company = """SELECT screen_name from weibo_company where plat_store_id = '{}';""".format(search_id)
            self.cursor.execute(company)
            screen_name = self.cursor.fetchone()
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
            }
            mess.append(response)
        cities = """SELECT store_city from unified_store GROUP BY store_city"""
        self.cursor.execute(cities)
        city_list = self.cursor.fetchall()
        c_list = []
        for city in city_list:
            city_label = {
                'value': city[0],
                'label': city[0]
            }
            c_list.append(city_label)
        self.cache.set('city_cache',(mess,c_list),self.timeout)

    def getCityFromCache(self):
        data = self.cache.get('city_cache')
        if data is None:
            data = self.get_city()
        return data