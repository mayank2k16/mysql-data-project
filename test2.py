import unittest
import file2
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


    def test_get_unique_years(self):
        returned_value = file2.get_unique_years('data_project_tests','matches_test_data')
        expected_value = ['2008', '2010', '2013', '2015', '2016']
        self.assertEqual(returned_value,expected_value)

    def test_get_winnings_dictionary_for_each_year(self):
        returned_value = file2.get_winnings_dictionary_for_each_year('data_project_tests','matches_test_data')
        expected_value ={'Sunrisers Hyderabad': [1, 0, 0, 0, 0],
                         'Rising Pune Supergiants': [0, 0, 0, 0, 1],
                         'Kolkata Knight Riders': [0, 0, 0, 1, 0],
                         'Kings XI Punjab': [0, 1, 0, 0, 0],
                         'Royal Challengers Bangalore': [0, 0, 0, 0, 0], 
                         'Mumbai Indians': [0, 0, 0, 0, 0], 
                         'Delhi Daredevils': [0, 0, 1, 0, 0], 
                         'Gujarat Lions': [0, 0, 0, 0, 0], 
                         'Chennai Super Kings': [0, 0, 0, 1, 0], 
                         'Rajasthan Royals': [0, 0, 0, 0, 0], 
                         'Deccan Chargers': [0, 0, 0, 0, 0], 
                         'Kochi Tuskers Kerala': [0, 0, 0, 0, 0], 
                         'Pune Warriors': [0, 0, 0, 0, 0]}
        self.assertEqual(returned_value,expected_value)
        file2.plot_graph('data_project_tests','matches_test_data')
   
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