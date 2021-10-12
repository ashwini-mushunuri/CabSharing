from Utils.LoggerUtil import LoggerUtil
from Utils.DBUtils import DBUtils
from Utils.ConfigUtil import ConfigUtil


class PostCabReq:
   def __init__(self):
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

   def post_request(self):
       client = self.get_client()
       users_database_name = self.config['mongo']['users_database']
       users_hist_collection_name = self.config['mongo']['add_users_collection']
       database = client[users_database_name]
       users_hist_collection = database[users_hist_collection_name]

       try:
           getData = users_hist_collection.find_one({'email' : 'saio3139@gmail.com'})
           # for x in getData :
           #     print('ig ogt dataaaaaaaaaaaaaaaaa', getData[x])
           self.log.info("Updated profile for user with email : {}".format(getData))
       except Exception as e:
           self.log.error("Error : {}".format(e))
       """
       Check if there is a cab available b/w source and destination
       If there is one, check if there are required number of seats available.
       If yes, then return the cab list.
       :return:
       """
       pass
