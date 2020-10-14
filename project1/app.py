from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'cs527-instacart-rds.cy6bq6rmcwmp.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Admin123'
app.config['MYSQL_DB'] = 'instacart'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    while True:
        try:
            fetchdata = ''
            if request.method == 'POST':
                queryDetails = request.form
                query = queryDetails['my_query']
                cur = mysql.connection.cursor()
                cur.execute(query)
                mysql.connection.commit()
                fetchdata = cur.fetchall()
                cur.close
        except mysql.connect.DatabaseError:
            fetchdata = "There is an error in your SQL syntax."
        except:
            fetchdata = "There is an error in your program."
        return render_template('project1.html', data = fetchdata)
            


if __name__ == "__main__":
    app.run(debug=True)