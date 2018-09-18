import mysql.connector
import matplotlib.pyplot as plt
def get_number_of_matches_per_year(database_name, table_name):
      mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mayank",
        database=database_name
      )

      mycursor = mydb.cursor()
      query = "SELECT `season`,COUNT(`season`) FROM" + "`"+ table_name +"`" + "GROUP BY `season`;"
      mycursor.execute(query)

      no_of_matches_per_year = mycursor.fetchall()
      return no_of_matches_per_year
def plot_graph(database_name, table_name):
      bar_footer = []
      bar_height = []
      no_of_matches_per_year = get_number_of_matches_per_year(database_name, table_name)
      for match in no_of_matches_per_year:
        bar_footer.append(match[0])
        bar_height.append(match[1])
      plt.bar(bar_footer,bar_height,label="seasons")
      plt.legend()
      plt.ylabel('Number of matches')
      plt.xlabel('Season')
      plt.title('Number of matches in IPL')
      plt.show()

if __name__ == '__main__':
  plot_graph('data_project','matches')
