import json

from Utils.LoggerUtil import LoggerUtil
from Utils.DBUtils import DBUtils
from Utils.ConfigUtil import ConfigUtil


class UpdateProfile:
    def __init__(self):
        print("into update class")
        self.log = LoggerUtil(self.__class__.__name__).get()
        self.config = ConfigUtil.get_config_instance()
        self.db_utils = DBUtils()

    def get_client(self):
        address = self.config['mongo']['address']
        port = self.config['mongo']['port']
        auth_db = self.config['mongo']['auth_db']
        is_auth_enabled = self.config['mongo']['is_auth_enabled']
        username = self.config['mongo']['username']
        password = self.config['mongo']['password']

        client = self.db_utils.get_client(address=address, port=port,
                                          username=username, password=password,
                                          auth_db=auth_db, is_auth_enabled=is_auth_enabled)
        return client

    @staticmethod
    def insert_query(source, destination, time, date, num_seats_req, phone_num, email):
        query = dict()
        query['source'] = source
        query['destination'] = destination
        query['time'] = time
        query['date'] = date
        query['num_seats_req'] = num_seats_req
        query['phone_num'] = phone_num
        query['email'] = email
        # query['preferences'] = preferences
        return query

    def update(self, **kwargs):
        print("into update method",kwargs)
        source=kwargs['source']
        destination=kwargs['destination']
        time=kwargs['time']
        date=kwargs['date']
        num_seats_req=kwargs['num_seats_req']
        phone_num=kwargs['phone_num']
        email=kwargs['email']
        client = self.get_client()

        users_database_name = self.config['mongo']['users_database']
        users_hist_collection_name = self.config['mongo']['users_hist_collection_name']
        database = client[users_database_name]
        users_hist_collection = database[users_hist_collection_name]
        print['users_hist_collection',users_hist_collection]
        query = self.insert_query(source, destination, time, date,
                                  num_seats_req, phone_num, email)
        print("query:",type(query))
        try:
            print("into try",type(users_hist_collection))
            users_hist_collection.insert(query)
            self.log.info("Updated profile for user with email : {}".format(kwargs['email']))
        except Exception as e:
            print("ecxeption:",e)
            self.log.error("Error : {}".format(e)) 
