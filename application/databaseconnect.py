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


    def defineMatch(self,match_id,home_team_id,away_team_id,stadium_id,date):
        try:
            sql = "insert into matches(match_id,home_team_id,away_team_id,stadium_id,date) values" \
                    "(%s, %s, %s, %s, %s);"
            val = (match_id,home_team_id,away_team_id,stadium_id,date)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.IntegrityError as e:
            logger.error(e)
            return False
        else:
            return True

    def addStadium(self,id,name,seats_num,home_team_id):
        try:
            sql = "insert into stadiums(id,name,seats_num,home_team_id) values" \
                    "(%s, %s, %s, %s);"
            val = (id,name,seats_num,home_team_id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.IntegrityError as e:
            logger.error(e)
            return False
        else:
            return True


    def defineSeat(self,stadium_id,number_of_seat,match_id):
        all_seats = []
        for i in range(number_of_seat):
            all_seats.append(tuple([stadium_id,i,True,None,match_id]))
        try:
            sql = "insert into seats(stadium_id,seat_num,is_available,user_id_,match_id) values" \
                    "(%s, %s, %s, %s,%s);"
            self.mycursor.executemany(sql, all_seats)
            self.mydb.commit()
        except Exception as e:
            logger.error(e)
            return False,e
        else:
            return True,'done'


    def buyTicket(self,user_name,seat_num,match_id):
        sql = f"select is_available from seats where seat_num = %s and match_id=%s;"
        val = (seat_num,match_id)
        self.mycursor.execute(sql,val)
        select = self.mycursor.fetchall()
        if len(select) == 0:
            return  False,'This Seats Dosent Exists ! :|' ,
        else:
            if select[0]['is_available']:
                sql = f"update seats set is_available = 0 , user_id_ = %s where seat_num = %s and match_id = %s;"
                val = (user_name,seat_num, match_id)
                self.mycursor.execute(sql,val)
                self.mydb.commit()
                return True, 'done'
            else:
                return False , 'not_done'

    def connectionClose(self):
        self.mycursor.close()
        self.mydb.close()