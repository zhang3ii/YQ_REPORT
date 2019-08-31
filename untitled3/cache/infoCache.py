from django.core.cache import caches
from django.db import connection


class InfoDataCache():
    '''
    缓存模块
    '''
    def __init__(self, dict, cacheName='default', timeout=60 * 60 * 3):
        self.dict = dict
        self.cache = caches[cacheName]
        self.timeout = timeout
        self.cursor = connection.cursor()

    def get_info(self):
        sql = """select unified_store.unified_store_id,unified_store.store_name,unified_store.store_phone,
        unified_store.store_industry_name,store_relation.create_at,unified_store.latitude,unified_store.longitude,
        store_relation.hlj_store_id,store_relation.dzdp_store_id,store_relation.bhhl_store_id
        from store_relation,unified_store where 
        unified_store.unified_store_id = store_relation.unified_store_id and unified_store.unified_store_id = '{}'""".format(
            self.dict)

        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        data = {}
        if res:
            latitude = res[5]
            longitude = res[6]
            store_industry_name = res[3]
            lat_down = float(latitude) - 0.02
            lat_up = float(latitude) + 0.02
            long_left = float(longitude) - 0.02
            long_right = float(longitude) + 0.02
            nums = """select unified_store_id,store_name,latitude,longitude from unified_store where  latitude >{} and latitude <{} and longitude >{} and longitude <{} and store_industry_name = '{}'""".format(
                lat_down, lat_up, long_left, long_right, store_industry_name)
            self.cursor.execute(nums)
            shop_num = self.cursor.fetchall()
            budy = ''
            if res[7] != 0:
                budy += '婚礼纪 '
            if res[8] != 0:
                budy += '大众点评 '
            if res[9] != 0:
                budy += '百合婚礼'
            response = {
                'store_id': str(res[0]),
                'store_name': res[1],
                'store_phone': res[2],
                'store_industry_name': res[3],
                'create_at': res[4],
                'relation': budy,
                'center': [longitude, latitude],
            }
            shop_mark = []
            for s_n in shop_num:
                if s_n[3] == longitude and s_n[2] == latitude:
                    shops = {
                        'label': {
                            'content': "<a href='http://192.168.88.119:8080/#/info/{}' target='_blank' style = 'color:red'>{}</a>".format(
                                s_n[0], s_n[1])},
                        'position': [s_n[3], s_n[2]],
                    }
                else:
                    shops = {
                        'label': {
                            'content': "<a href='http://192.168.88.119:8080/#/info/{}' target='_blank'>{}</a>".format(
                                s_n[0], s_n[1])},
                        'position': [s_n[3], s_n[2]],
                    }
                shop_mark.append(shops)
            self.cache.set('info',(shop_mark, response),self.timeout)
            return (shop_mark, response)

    def getinfoFromCache(self):
        data = self.cache.get('info')
        if data is None:
            data = self.get_info()
        return data

