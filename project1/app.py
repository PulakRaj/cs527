from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import psycopg2
import time

# MySQL setup
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'cs527-instacart-rds.cy6bq6rmcwmp.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Admin123'
app.config['MYSQL_DB'] = 'instacart'
mysql = MySQL(app)

# Redshift setup
redshift = psycopg2.connect(dbname = 'instacart', 
                            host = 'cs527-cluster.c9dutp9axjuw.us-east-2.redshift.amazonaws.com', 
                            port = '5439', 
                            user = 'admin', 
                            password = 'Admin123')

@app.route('/', methods=['GET', 'POST'])
def index():
    elapsed_time = 0
    try:
        fetchdata = ''
        if request.method == 'POST':
            start_time = time.time()
            query_details = request.form
            query = query_details['my_query']
            if query_details['db'] == 'my_instacart':
                app.config['MYSQL_DB'] = 'instacart'
                redshift = psycopg2.connect(dbname = 'instacart', 
                            host = 'cs527-cluster.c9dutp9axjuw.us-east-2.redshift.amazonaws.com', 
                            port = '5439', 
                            user = 'admin', 
                            password = 'Admin123')
            elif query_details['db'] == 'my_abc':
                app.config['MYSQL_DB'] = 'ABC'
                redshift = psycopg2.connect(dbname = 'abcd', 
                            host = 'cs527-cluster.c9dutp9axjuw.us-east-2.redshift.amazonaws.com', 
                            port = '5439', 
                            user = 'admin', 
                            password = 'Admin123')
            if query_details['options'] == 'my_mysql':
                cur = mysql.connection.cursor()
                cur.execute(query)
                mysql.connection.commit()
                fetchdata = cur.fetchall()
                cur.close
                elapsed_time = time.time() - start_time
            elif query_details['options'] == 'my_redshift':
                cur = redshift.cursor()
                cur.execute(query)
                fetchdata = cur.fetchall()
                cur.close()
                elapsed_time = time.time() - start_time
    except mysql.connect.DatabaseError:
        fetchdata = "There is an error in your SQL syntax."
    except:
        fetchdata = "There is an error in your program."
    return render_template('project1.html', data = fetchdata, time = elapsed_time)

            
if __name__ == "__main__":
    app.run(debug=True)