import mysql.connector
from log_handler.Setup import logger
import json


class database:


    def __init__(self):
        self.db_error = False
        config_json = open('./config/config.json')
        config = json.load(config_json)
        config_json.close()
        try:
            self.mydb = mysql.connector.connect(
                host=config["mysql"]["host"],
                user=config["mysql"]["username"],
                password=config["mysql"]["password"],
                database=config["mysql"]["database"],
                port = config["mysql"]["db_port"]
            )
        except Exception as e:
            logger.error(e)
            self.db_error = True

        else:
            logger.info("mysql is connect")
            self.mycursor = self.mydb.cursor(dictionary=True)


    def login(self,user_name,password):
        sql = f"select user_name, password from user where user_name = %s;"
        val = user_name
        self.mycursor.execute(sql,(val,))
        # row_headers = [x[0] for x in self.mycursor.description]
        select = self.mycursor.fetchall()
        if len(select) == 0:
            return 'user not found' , False
        else:
            if password == select[0]['password']:
                return 'login successfully' , True
            else:
                return 'password is wrong', False


    def signUp(self,user_name, password,first_name,last_name,email,mobile):
        try:
            sql = "insert into user(user_name, password, first_name, last_name, email, mobile) values" \
                "(%s, %s, %s, %s, %s, %s);"
            val = (user_name, password,first_name,last_name,email,mobile)
            self.mycursor.execute(sql,val)
            self.mydb.commit()
        except mysql.connector.IntegrityError as e:
            logger.error(e)
            return False
        else:
            return True




    def connectionClose(self):
        self.mycursor.close()
        self.mydb.close()