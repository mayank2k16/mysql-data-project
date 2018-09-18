from collections import OrderedDict
import matplotlib.pyplot as plt
import pymysql

# connecting to database
def connect_to_database(database_name):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="mayank",
        database=database_name
      )
    return mydb

def get_economy_of_each_bowler_for_2015(database_name, matches, deliveries):
    mydb = connect_to_database(database_name)
    economy_of_each_bowler = dict()
    connector = mydb.cursor()
    fetch_total_runs_and_deliveries_given_by_bowler = "select bowler, sum(total_runs) ,COUNT(bowler)from " + deliveries + " where match_id IN (select id from " + matches + " where season = 2015) group by(bowler);"
    connector.execute(fetch_total_runs_and_deliveries_given_by_bowler)
    result = connector.fetchall()
    for i in range(0,len(result)):
        economy_of_each_bowler[result[i][0]] = (result[i][1]/result[i][2])*6
    top_economical_bowlers = OrderedDict(sorted(economy_of_each_bowler.items(), key=lambda x: x[1]))
    return(top_economical_bowlers)

# plotting the graph
def plot_graph(database_name,matches,deliveries):
    bar_height = []
    bar_footer = []
    economy_per_bowler = get_economy_of_each_bowler_for_2015(database_name,matches,deliveries)   
    counter = 0
    for bowler in economy_per_bowler:
        if(counter > 9):
            break
        else:
            bar_height.append(economy_per_bowler[bowler])
            bar_footer.append(bowler)
            counter = counter+1

    plt.bar(bar_footer, bar_height, label="extras")
    plt.legend()
    plt.ylabel('extra runs per teams')
    plt.xlabel('Teams')
    plt.xticks(rotation=90)
    plt.title('extra runs in 2016')
    plt.show()

if __name__ == '__main__':
  plot_graph('data_project','matches','deliveries')