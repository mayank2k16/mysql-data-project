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

def get_extra_runs_per_team(database_name,matches,deliveries):
    extra_runs = dict()
    mydb = connect_to_database(database_name)
    connector = mydb.cursor()
    query_to_get_distinct_years = "select bowling_team, sum(extra_runs) from " + deliveries + " where match_id IN (select id from " + matches + " where season = 2016) group by(bowling_team);"
    connector.execute(query_to_get_distinct_years)
    distinct_years = connector.fetchall()
    for year in range(0,len(distinct_years)):
        extra_runs[distinct_years[year][0]] = distinct_years[year][1]
    return(extra_runs)

# plotting the graph
def plot_graph(database_name,matches,deliveries):
    bar_height = []
    bar_footer = []
    extra_runs = get_extra_runs_per_team(database_name,matches,deliveries)
    for each_extra_run in extra_runs:
        bar_footer.append(each_extra_run)
        bar_height.append(extra_runs[each_extra_run])

    plt.bar(bar_footer, bar_height, label="extras")
    plt.legend()
    plt.ylabel('extra runs per teams')
    plt.xlabel('Teams')
    plt.xticks(rotation=90)
    plt.title('extra runs in 2016')
    plt.show()

if __name__ == '__main__':
  plot_graph('data_project','matches','deliveries')