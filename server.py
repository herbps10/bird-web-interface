from flask import Flask, render_template, request, redirect
import subprocess
import datetime
import calendar

def run_command(command):
    process = subprocess.Popen(command, stdout = subprocess.PIPE)
    out, err = process.communicate()

    return out

app = Flask(__name__)


@app.route('/')
def homepage():
    location_file = open('location.txt', 'r').read()
    location = location_file.split(',')

    df = run_command(['df'])
    uptime = run_command(['uptime'])
    internal_battery_voltage = 8.9
    external_battery_voltage = 12.4
    months = calendar.month_name

    return render_template('homepage.html',
        location = location,
        df = df,
        uptime = uptime,
        internal_battery_voltage = internal_battery_voltage,
        external_battery_voltage = external_battery_voltage,
        now = datetime.datetime.now(),
        months = months
    )

@app.route('/save/location', methods=['POST'])
def save():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    
    location_file = open('location.txt', 'w')
    location_file.write(latitude + ',' + longitude)
    location_file.close()

    return redirect('/')

@app.route('/save/date', methods=['POST'])
def save_date():
    day = request.form['day']
    month = request.form['month']
    year = request.form['year']
    time = request.form['time']

    format_string = "%m/%d/%Y %T"
    date_set = month + "/" + day + "/" + year + " " + time

    command = ["sudo", "date", '+"' + format_string + '"', "-s", date_set]

    run_command(command)
    run_command(["sudo", "hwclock", "-w"])
    #return format_string + " " + date_set

    return redirect('/')

if __name__ == "__main__":
    app.run('0.0.0.0', debug = True)
