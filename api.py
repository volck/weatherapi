from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import secrets

app = Flask(__name__)
CORS(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = secrets.user
app.config['MYSQL_DATABASE_PASSWORD'] = secrets.password
app.config['MYSQL_DATABASE_DB'] = "weather"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/getALL')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_all():
    cur = mysql.connect().cursor()
    cur.execute('''select * from weather.weather_station''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})



@app.route('/getNEWEST')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_newest_weatherreport():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT ID, time_captured, temperature FROM weather_station ORDER BY id DESC LIMIT 1;''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})



@app.route('/getDailyMax')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_daily_max():
    cur = mysql.connect().cursor()
    cur.execute('''select * from weather_station WHERE time_captured >= CURDATE() ORDER BY temperature DESC LIMIT 1;''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})

@app.route('/getDailyMin')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_daily_min():
    cur = mysql.connect().cursor()
    cur.execute('''select * from weather_station WHERE time_captured >= CURDATE() ORDER BY temperature LIMIT 1;''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})



@app.route('/getYesterdayMax')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_yesterday_max():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM weather_station WHERE DATE(time_captured) = DATE(NOW() - INTERVAL 1 DAY) ORDER BY temperature DESC LIMIT 1;''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})


@app.route('/getYesterdayMin')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def get_yesterday_min():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM weather_station WHERE DATE(time_captured) = DATE(NOW() - INTERVAL 1 DAY) ORDER BY temperature LIMIT 1;''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})

# get history for graphs

@app.route('/getYesterdaysTemperatures')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def getYesterdaysTemperatures():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM weather_station WHERE DATE(time_captured) = DATE(NOW() - INTERVAL 1 DAY)''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})


@app.route('/getTodaysTemperatures')
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def getTodaysTemperatures():
    cur = mysql.connect().cursor()
    cur.execute('''SELECT * FROM weather_station WHERE DATE(time_captured) = DATE(NOW())''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'weather' : r})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', threaded=True)
