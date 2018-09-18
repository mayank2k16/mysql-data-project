import mysql.connector
import pymysql
import matplotlib.pyplot as plt
from collections import OrderedDict
width = 0.80

# connecting to database
def connect_to_database(database_name):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="mayank",
        database=database_name
      )
    return mydb


# getting the unique number of seasons

def get_unique_years(database_name,table_name):
    mydb = connect_to_database(database_name)
    connector = mydb.cursor()
    query_to_get_distinct_years = "SELECT `season` FROM" + "`"+ table_name +"`" + "GROUP BY `season`;"
    connector.execute(query_to_get_distinct_years)
    distinct_tuples = connector.fetchall()
    distinct_years = []
    for years in distinct_tuples:
         distinct_years.append(years[0])
    return distinct_years

def get_winnings_dictionary_for_each_year(database_name,table_name):
    mydb = connect_to_database(database_name)
    connector = mydb.cursor()
    team_names = OrderedDict([('Sunrisers Hyderabad', []), ('Rising Pune Supergiants', []), ('Kolkata Knight Riders', []),('Kings XI Punjab', []),
                  ('Royal Challengers Bangalore', []), ('Mumbai Indians', []), ('Delhi Daredevils', []), ('Gujarat Lions', []),
                  ('Chennai Super Kings', []), ('Rajasthan Royals', []), ('Deccan Chargers', []), ('Kochi Tuskers Kerala', []), ('Pune Warriors', [])])
    unique_years = get_unique_years(database_name,table_name)
    for team in team_names:
        number_of_winnings_per_year = []
        for years in unique_years:
            str_year = str(years)
            query_to_get_winnings_per_year = "SELECT COUNT(winner) FROM" + "`"+ table_name +"`" + "WHERE season = " + str_year +" AND winner ='"+team+ "';"
            connector.execute(query_to_get_winnings_per_year)
            values = connector.fetchone()
            number_of_winnings_per_year.append(values[0])       
        team_names[team] = number_of_winnings_per_year
    return team_names

get_winnings_dictionary_for_each_year('data_project','matches')
# cummulative sum of bottoms for the stacked bar graphs
def calculate_bottom(team_name,database_name,table_name):
    years = get_unique_years(database_name,table_name)
    team_names = get_winnings_dictionary_for_each_year(database_name,table_name)
    if(database_name == 'data_project'):
        cummulative_sum_for_bottom = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    else:
        cummulative_sum_for_bottom = [0, 0, 0, 0, 0]
    for team in team_names:
        for year in range(0, len(years)):
            if team == team_name:
                return cummulative_sum_for_bottom
            cummulative_sum_for_bottom[year] += team_names[team][year]
    return cummulative_sum_for_bottom

# plotting the stacked bar graph

def plot_graph(database_name,table_name):
    bar_footer = get_unique_years(database_name,table_name)
    team_names = get_winnings_dictionary_for_each_year(database_name,table_name)
    for team in team_names:
        if team == 'Sunrisers Hyderabad':
            plt.bar(bar_footer, team_names[team], width, label=team)
        else:
            plt.bar(bar_footer, team_names[team], width, label=team, bottom=calculate_bottom(
                team,database_name,table_name))

    plt.ylabel('stacked teams')
    plt.xlabel('years')
    plt.title('Stacked graph for IPL')
    plt.legend()
    plt.show()

if __name__ == '__main__':
  plot_graph('data_project','matches')      