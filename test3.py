import unittest
import file3
import mysql.connector
import pymysql
class TestDataProject(unittest.TestCase):
    
    @classmethod 
    def setUpClass(cls):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="mayank",
            database="data_project_tests",
            autocommit=True,
            local_infile=1
            )
        mycursor = mydb.cursor()

        query_to_create_matches_test_table = "CREATE TABLE matches_test_data(id INT PRIMARY KEY,season VARCHAR(40),city VARCHAR(40),date Date,team1 VARCHAR(40),team2 VARCHAR(40),toss_winner VARCHAR(40),toss_decision VARCHAR(40),result VARCHAR(40),dl_applied INT,winner VARCHAR(40),win_by_runs INT,win_by_wickets INT,player_of_match VARCHAR(40),venue VARCHAR(100),umpire1 VARCHAR(40),umpire2 VARCHAR(40),umpire3 VARCHAR(40))"
        mycursor.execute(query_to_create_matches_test_table)

        query_to_create_deliveries_test_table = "CREATE TABLE deliveries_test_data(match_id INT,inning INT,batting_team VARCHAR(40),bowling_team VARCHAR(40),over INT,ball INT,batsman VARCHAR(40),non_striker VARCHAR(40),bowler VARCHAR(40),is_super_over INT,wide_runs INT,bye_runs INT,legbye_runs INT,noball_runs INT,penalty_runs INT,batsman_runs INT,extra_runs INT,total_runs INT,player_dismissed VARCHAR(40),dismissal_kind VARCHAR(40),fielder VARCHAR(40))"
        mycursor.execute(query_to_create_deliveries_test_table)

        query_to_transfer_matches_table_to_mysql = "LOAD DATA LOCAL INFILE '/var/lib/mysql-files/matches.csv' INTO TABLE data_project_tests.matches_test_data FIELDS TERMINATED BY ','  IGNORE 1 LINES;"
        mycursor.execute(query_to_transfer_matches_table_to_mysql)

        query_to_transfer_deliveries_table_to_mysql = "LOAD DATA LOCAL INFILE '/var/lib/mysql-files/deliveries.csv' INTO TABLE data_project_tests.deliveries_test_data FIELDS TERMINATED BY ','  IGNORE 1 LINES;"
        mycursor.execute(query_to_transfer_deliveries_table_to_mysql)

        mycursor.close()
        mydb.close()


    def test_get_extra_runs_per_team(self):
        returned_value = file3.get_extra_runs_per_team('data_project_tests', 'matches_test_data','deliveries_test_data')
        expected_value = {'Gujarat Lions': 2}
        self.assertEqual(returned_value,expected_value)
        file3.plot_graph('data_project_tests','matches_test_data','deliveries_test_data')
   
    @classmethod
    def tearDownClass(cls):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mayank",
        database="data_project_tests"
        )
        mycursor = mydb.cursor()
        query_to_delete_matches_test_data = "DROP TABLE matches_test_data;"
        query_to_delete_deliveries_test_data = "DROP TABLE deliveries_test_data;"
        mycursor.execute(query_to_delete_matches_test_data)
        mycursor.execute(query_to_delete_deliveries_test_data)
        mycursor.close()
        mydb.close()



if __name__ == '__main__':
    unittest.main()