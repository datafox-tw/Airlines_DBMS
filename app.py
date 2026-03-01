from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/flight/search")
def flightSearch():
    sql_cmd = "select * from airport;"
 
    query_data = db.session.execute(text(sql_cmd)).fetchall()
    return render_template('flight.html', data = query_data)

@app.route('/flight/search/submit', methods=['POST'])
def flightSubmit():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    departure = request.form.get('departure')
    destination = request.form.get('destination')

    if departure == 'default_departure' and destination == 'default_destination':
        sql_cmd = f"""
                    Select f.*, r.depart_airport, r.arrive_airport, s.ticket_sold
                    From (Select *
                            From flight
                            Where DATE(depart_time) Between '{start_date}' And
                            '{end_date}') As f
                    Join route As r on f.route_id = r.route_id
                    Left Join (Select flight_id , Count(*) As ticket_sold
                                From ticket
                                Group by flight_id) As s on f.flight_id = s.flight_id
                    Order By f.depart_time;
                    """
    elif departure == 'default_departure':
        sql_cmd = f"""
                    Select f.*, r.depart_airport, r.arrive_airport, s.ticket_sold
                    From (Select *
                            From flight
                            Where DATE(depart_time) Between '{start_date}' And
                            '{end_date}') As f
                    Join route As r on f.route_id = r.route_id
                    Left Join (Select flight_id , Count(*) As ticket_sold
                                From ticket
                                Group by flight_id) As s on f.flight_id = s.flight_id
                    Where r.arrive_airport = {destination}
                    Order By f.depart_time;
                    """
    elif destination == 'default_destination':
        sql_cmd = f"""
                    Select f.*, r.depart_airport, r.arrive_airport, s.ticket_sold
                    From (Select *
                            From flight
                            Where DATE(depart_time) Between '{start_date}' And
                            '{end_date}') As f
                    Join route As r on f.route_id = r.route_id
                    Left Join (Select flight_id , Count(*) As ticket_sold
                                From ticket
                                Group by flight_id) As s on f.flight_id = s.flight_id
                    Where r.depart_airport = {departure}
                    Order By f.depart_time;
                    """
    else:
        sql_cmd = f"""
                    Select f.*, r.depart_airport, r.arrive_airport, s.ticket_sold
                    From (Select *
                            From flight
                            Where DATE(depart_time) Between '{start_date}' And
                            '{end_date}') As f
                    Join route As r on f.route_id = r.route_id
                    Left Join (Select flight_id , Count(*) As ticket_sold
                                From ticket
                                Group by flight_id) As s on f.flight_id = s.flight_id
                    Where r.depart_airport = {departure} And r.arrive_airport = {destination}
                    Order By f.depart_time;
                    """
 
    query_data = db.session.execute(text(sql_cmd))
    keys = query_data.keys()
    query_data = query_data.fetchall()
    return render_template('flightsubmit.html', data = query_data, keys = keys \
            , start_date = start_date, end_date = end_date, departure = departure, destination = destination)

@app.route("/flight/insert")
def flightIns():
    sql1 = "select * from airport;"
    sql2 = "select * from airplane;"
 
    airports = db.session.execute(text(sql1)).fetchall()
    planes = db.session.execute(text(sql2)).fetchall()
    return render_template('flightinsert.html', airports = airports, planes = planes)

@app.route('/flight/insert/submit', methods=['POST'])
def flightInsSubmit():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    sql_cmd = f"""
                Select route_id
                From route
                Where depart_airport = {departure}
                And arrive_airport = {destination};
                """
    route = db.session.execute(text(sql_cmd)).fetchall()

    sql_cmd = "Select Max(flight_id) From flight;"
    max_id = db.session.execute(text(sql_cmd)).fetchall()

    id = max_id[0][0] + 1
    depart_time = request.form.get('depart_time')
    arrive_time = request.form.get('arrive_time')
    airplane = request.form.get('airplane')
    route_id = route[0][0]
    max_luggage_capacity = request.form.get('max_luggage_capacity')
    max_sell_amount = request.form.get('max_sell_amount')

    sql_cmd = f"""
                INSERT INTO flight (
                    flight_id,
                    plane_id,
                    route_id,
                    depart_time,
                    arrive_time,
                    max_luggage_capacity,
                    max_sell_amount
                ) VALUES (
                    {id},
                    {airplane},
                    {route_id},
                    '{depart_time}',
                    '{arrive_time}',
                    {max_luggage_capacity},
                    {max_sell_amount}
                );
                """
 
    db.session.execute(text(sql_cmd))
    db.session.commit()
    return render_template('success.html')

@app.route("/flight/delete")
def flightDel():
    return render_template('flightdelete.html')

@app.route("/flight/delete/submit", methods=['POST'])
def flightDelSubmit():
    id = request.form.get('flight_id')

    sql1 = f"""
                Delete From flight
                Where flight_id = {id};
                """
    sql2 = f"""
                Update ticket
                Set status = 'P'
                Where flight_id = {id};
                """
 
    db.session.execute(text(sql1))
    db.session.execute(text(sql2))
    db.session.commit()
    return render_template('success.html')

@app.route("/flight/crew")
def flightCrew():
    return render_template('flightcrew.html')

@app.route("/flight/crew/submit", methods=['POST'])
def flightCrewSubmit():
    id = request.form.get('flight_id')

    sql_cmd = f"""
                Select *
                From execute
                Where flight_id = {id}
                Order by employee_title;
                """
 
    query_data = db.session.execute(text(sql_cmd))
    keys = query_data.keys()
    query_data = query_data.fetchall()
    return render_template('flightcrewsubmit.html', execute = query_data, keys = keys)

@app.route("/flight/crew/insert")
def flightCrewInsert():
    return render_template('crewinsert.html')

@app.route("/flight/crew/insert/submit", methods=['POST'])
def flightCrewInsertSubmit():
    flight_id = request.form.get('flight_id')
    employee_id = request.form.get('employee_id')
    employee_title = request.form.get('employee_title')

    sql_cmd = f"""
                Insert into execute (
                    flight_id, employee_id, employee_title
                )
                Values (
                    {flight_id}, {employee_id}, '{employee_title}'
                );
                """
 
    db.session.execute(text(sql_cmd))
    db.session.commit()
    return render_template('success.html')

@app.route("/flight/crew/delete")
def flightCrewDelete():
    return render_template('crewdelete.html')

@app.route("/flight/crew/delete/submit", methods=['POST'])
def flightCrewDeleteSubmit():
    flight_id = request.form.get('flight_id')
    employee_id = request.form.get('employee_id')

    sql_cmd = f"""
                Delete From execute
                Where flight_id = {flight_id}
                And employee_id = {employee_id};
                """
 
    db.session.execute(text(sql_cmd))
    db.session.commit()
    return render_template('success.html')

@app.route("/employee/position")
def empPosition():
    sql_cmd = f"""
                select employee_position, count(*) as employee_count
                from employee
                group by employee_position;
                """
 
    query_data = db.session.execute(text(sql_cmd)).fetchall()
    return render_template('empposition.html', employees = query_data)

@app.route('/employee/position/submit', methods=['POST'])
def empPositionSubmit():
    position = request.form.get('selectedemployee')

    sql_cmd = f"""
                select *
                from employee
                where employee_position = '{position}';
                """
 
    query_data = db.session.execute(text(sql_cmd))
    keys = query_data.keys()
    query_data = query_data.fetchall()
    return render_template('empsubmit.html', employees = query_data, keys = keys)

@app.route("/employee/id")
def empId():
    return render_template('empid.html')

@app.route('/employee/id/submit', methods=['POST'])
def empIdSubmit():
    id = request.form.get('emp_id')

    sql_cmd = f"""
                select *
                from employee
                where employee_id = {id};
                """
 
    query_data = db.session.execute(text(sql_cmd))
    keys = query_data.keys()
    query_data = query_data.fetchall()
    return render_template('empsubmit.html', employees = query_data, keys = keys)

@app.route("/partschedule")
def partSchedule():
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=6)

    sql_cmd = f"""
        SELECT pt.parts_id, pt.plane_id, mt.last_mt + pt.maintain_frequency AS mt_needed
        FROM (
            SELECT parts_id, MAX(maintain_date) AS last_mt
            FROM maintain
            GROUP BY parts_id
        ) AS mt
        JOIN parts AS pt ON mt.parts_id = pt.parts_id
        WHERE mt.last_mt + pt.maintain_frequency BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY mt_needed, pt.plane_id;
    """
    query_data = db.session.execute(text(sql_cmd))
    days = [start_date + timedelta(days=i) for i in range(7)]
    schedule = [{} for i in range(7)]
    for row in query_data:
        for i in range(7):
            if row[2] == days[i]:
                if row[1] not in schedule[i].keys():
                    schedule[i][row[1]] = [row]
                else:
                    schedule[i][row[1]].append(row)
    keys = [schedule[i].keys() for i in range(7)]
    return render_template('partschedule.html', schedule = schedule, keys = keys, days = days)

@app.route("/maintainrecord")
def maintainRecord():
    return render_template('maintainrecord.html')

@app.route("/maintainrecord/submit", methods=['POST'])
def maintainRecordSubmit():
    mt_date = request.form.get('mt_date')
    worker_id = request.form.get('worker_id')
    parts_id = request.form.get('parts_id')
    mt_cost = request.form.get('mt_cost')

    sql_cmd = f"""
                Insert Into maintain (parts_id , employee_id, maintain_date , maintain_cost)
                Values ({parts_id}, {worker_id}, '{mt_date}', {mt_cost});
                """
 
    db.session.execute(text(sql_cmd))
    db.session.commit()
    return render_template('success.html')

@app.route("/ticket/update")
def ticUpdate():
    return render_template('ticketupdate.html')

@app.route('/ticket/update/submit', methods=['POST'])
def ticUpdateSubmit():
    id = request.form.get('ticket_id')
    status = request.form.get('status')

    sql_cmd = f"""
                Update ticket
                Set status = '{status}'
                Where ticket_id = {id};
                """
 
    db.session.execute(text(sql_cmd))
    db.session.commit()
    return render_template('success.html')

if __name__ == '__main__':
    app.run()