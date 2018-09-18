import mysql.connector
import matplotlib.pyplot as plt
from collections import OrderedDict
def get_most_mvp_players(database_name, matches):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mayank",
    database=database_name
    )

    mycursor = mydb.cursor()
    query = "SELECT `player_of_match`,COUNT(player_of_match) FROM" + "`"+ matches +"`" + "GROUP BY `player_of_match`;"
    mycursor.execute(query)

    most_valuable_players = mycursor.fetchall()
    top_valuable_players = OrderedDict(sorted(most_valuable_players,key = lambda x: x[1],reverse=True))
    return top_valuable_players
def plot_graph(database_name, matches):
    bar_footer = []
    bar_height = []
    most_valuable_players = get_most_mvp_players(database_name, matches)

    counter = 0
    for player in most_valuable_players:
        if counter == 10:
            break
        else:
            bar_height.append(most_valuable_players[player])
            bar_footer.append(player)
            counter = counter+1

    plt.bar(bar_footer,bar_height,label="seasons")
    plt.legend()
    plt.ylabel('Number of matches')
    plt.xlabel('Season')
    plt.title('Number of matches in IPL')
    plt.show()

if __name__ == '__main__':
  plot_graph('data_project','matches')