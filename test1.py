import unittest
import file1
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

        query_to_create_test_table = "CREATE TABLE matches_test_data(id INT PRIMARY KEY,season VARCHAR(40),city VARCHAR(40),date Date,team1 VARCHAR(40),team2 VARCHAR(40),toss_winner VARCHAR(40),toss_decision VARCHAR(40),result VARCHAR(40),dl_applied INT,winner VARCHAR(40),win_by_runs INT,win_by_wickets INT,player_of_match VARCHAR(40),venue VARCHAR(100),umpire1 VARCHAR(40),umpire2 VARCHAR(40),umpire3 VARCHAR(40))"
        mycursor.execute(query_to_create_test_table)

        query_to_transfer_data_from_csv_to_mysql = "LOAD DATA LOCAL INFILE '/var/lib/mysql-files/matches.csv' INTO TABLE data_project_tests.matches_test_data FIELDS TERMINATED BY ','  IGNORE 1 LINES;"
        mycursor.execute(query_to_transfer_data_from_csv_to_mysql)
        mycursor.close()
        mydb.close()


    def test_matches_played_per_year(self):
        returned_value = file1.get_number_of_matches_per_year('data_project_tests', 'matches_test_data')
        expected_value = [('2008', 1), ('2010', 1), ('2013', 1), ('2015', 2), ('2016', 1)]
        self.assertEqual(returned_value,expected_value)
        file1.plot_graph('data_project_tests','matches_test_data')
   
    @classmethod
    def tearDownClass(cls):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mayank",
        database="data_project_tests"
        )
        mycursor = mydb.cursor()
        query_to_delete_test_data = "DROP TABLE matches_test_data;"
        mycursor.execute(query_to_delete_test_data)
        mycursor.close()
        mydb.close()



if __name__ == '__main__':
    unittest.main()