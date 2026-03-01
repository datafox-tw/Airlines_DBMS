from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from models import db, Airport, Airplane, Route, Flight, Ticket, Employee, Execute, Maintain, Parts

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass the exception message to the template
    return render_template('error.html', error_message=str(e)), 500

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    # v1.0 Feature: Dashboard
    now = datetime.now()
    # Closest flights (for demo, showing latest 5 records in history)
    upcoming_flights = Flight.query.order_by(Flight.depart_time.desc()).limit(5).all()
    # Statistics
    total_flights = Flight.query.count()
    total_airports = Airport.query.count()
    total_employees = Employee.query.count()
    
    return render_template('dashboard.html', 
                         upcoming_flights=upcoming_flights,
                         total_flights=total_flights,
                         total_airports=total_airports,
                         total_employees=total_employees,
                         now=now)

@app.route("/flight/search")
def flightSearch():
    airports = Airport.query.all()
    return render_template('flight.html', data=airports)

@app.route('/flight/search/submit', methods=['POST'])
def flightSubmit():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    departure = request.form.get('departure')
    destination = request.form.get('destination')

    # Querying using ORM
    query = Flight.query.join(Route)
    
    if start_date and end_date:
        query = query.filter(Flight.depart_time.between(start_date, end_date))
    
    if departure != 'default_departure':
        query = query.filter(Route.depart_airport == departure)
    
    if destination != 'default_destination':
        query = query.filter(Route.arrive_airport == destination)
    
    flights = query.order_by(Flight.depart_time).all()
    
    # Bridge for legacy templates
    keys = Flight.__table__.columns.keys()
    
    return render_template('flightsubmit.html', 
                         data=flights, 
                         keys=keys,
                         start_date=start_date, 
                         end_date=end_date, 
                         departure=departure, 
                         destination=destination)

@app.route("/flight/insert")
def flightIns():
    airports = Airport.query.all()
    planes = Airplane.query.all()
    return render_template('flightinsert.html', airports=airports, planes=planes)

@app.route('/flight/insert/submit', methods=['POST'])
def flightInsSubmit():
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    
    route = Route.query.filter_by(depart_airport=departure, arrive_airport=destination).first()
    if not route:
        raise Exception("找不到對應的航線，請確認出發地與目的地。")

    max_id = db.session.query(db.func.max(Flight.flight_id)).scalar() or 0
    
    new_flight = Flight(
        flight_id=max_id + 1,
        plane_id=request.form.get('airplane'),
        route_id=route.route_id,
        depart_time=request.form.get('depart_time'),
        arrive_time=request.form.get('arrive_time'),
        max_luggage_capacity=request.form.get('max_luggage_capacity'),
        max_sell_amount=request.form.get('max_sell_amount')
    )
    
    db.session.add(new_flight)
    db.session.commit()
    return render_template('success.html')

@app.route("/flight/delete")
def flightDel():
    return render_template('flightdelete.html')

@app.route("/flight/delete/submit", methods=['POST'])
def flightDelSubmit():
    fid = request.form.get('flight_id')
    flight = Flight.query.get(fid)
    if flight:
        # Cascade logic from legacy: Update tickets to status 'P'
        Ticket.query.filter_by(flight_id=fid).update({"status": 'P'})
        db.session.delete(flight)
        db.session.commit()
    return render_template('success.html')

@app.route("/flight/crew")
def flightCrew():
    return render_template('flightcrew.html')

@app.route("/flight/crew/submit", methods=['POST'])
def flightCrewSubmit():
    fid = request.form.get('flight_id')
    crews = Execute.query.filter_by(flight_id=fid).order_by(Execute.employee_title).all()
    keys = Execute.__table__.columns.keys()
    return render_template('flightcrewsubmit.html', execute=crews, keys=keys, flight_id=fid)

@app.route("/flight/crew/insert")
def flightCrewInsert():
    return render_template('crewinsert.html')

@app.route("/flight/crew/insert/submit", methods=['POST'])
def flightCrewInsertSubmit():
    new_crew = Execute(
        flight_id=request.form.get('flight_id'),
        employee_id=request.form.get('employee_id'),
        employee_title=request.form.get('employee_title')
    )
    db.session.add(new_crew)
    db.session.commit()
    return render_template('success.html')

@app.route("/flight/crew/delete")
def flightCrewDelete():
    return render_template('crewdelete.html')

@app.route("/flight/crew/delete/submit", methods=['POST'])
def flightCrewDeleteSubmit():
    fid = request.form.get('flight_id')
    eid = request.form.get('employee_id')
    crew = Execute.query.filter_by(flight_id=fid, employee_id=eid).first()
    if crew:
        db.session.delete(crew)
        db.session.commit()
    return render_template('success.html')

@app.route("/employee/position")
def empPosition():
    # Get distinct positions and counts
    stats = db.session.query(Employee.employee_position, db.func.count(Employee.employee_id))\
                      .group_by(Employee.employee_position).all()
    return render_template('empposition.html', employees=stats)

@app.route('/employee/position/submit', methods=['POST'])
def empPositionSubmit():
    pos = request.form.get('selectedemployee')
    emps = Employee.query.filter_by(employee_position=pos).all()
    keys = Employee.__table__.columns.keys()
    return render_template('empsubmit.html', employees=emps, keys=keys)

@app.route("/employee/id")
def empId():
    return render_template('empid.html')

@app.route('/employee/id/submit', methods=['POST'])
def empIdSubmit():
    eid = request.form.get('emp_id')
    emp = Employee.query.filter_by(employee_id=eid).all() # Template expects a list
    keys = Employee.__table__.columns.keys()
    return render_template('empsubmit.html', employees=emp, keys=keys)

@app.route("/partschedule")
def partSchedule():
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=6)

    # Legacy SQL was complex: mt.last_mt + pt.maintain_frequency
    # Refactoring this to a slightly cleaner ORM approach or keeping hybrid if needed.
    # For 1.0, let's use ORM for readability.
    
    # Subquery for last maintenance
    subq = db.session.query(
        Maintain.parts_id,
        db.func.max(Maintain.maintain_date).label('last_mt')
    ).group_by(Maintain.parts_id).subquery()
    
    query = db.session.query(Parts, subq.c.last_mt)\
                      .join(subq, Parts.parts_id == subq.c.parts_id).all()
    
    days = [start_date + timedelta(days=i) for i in range(7)]
    schedule = [{} for _ in range(7)]
    
    for part, last_mt in query:
        next_mt = last_mt + timedelta(days=part.maintain_frequency)
        for i in range(7):
            if next_mt == days[i]:
                if part.plane_id not in schedule[i]:
                    schedule[i][part.plane_id] = []
                # Match legacy structure: [parts_id, plane_id, mt_needed]
                schedule[i][part.plane_id].append([part.parts_id, part.plane_id, next_mt])
                
    keys = [s.keys() for s in schedule]
    return render_template('partschedule.html', schedule=schedule, keys=keys, days=days)

@app.route("/maintainrecord")
def maintainRecord():
    return render_template('maintainrecord.html')

@app.route("/maintainrecord/submit", methods=['POST'])
def maintainRecordSubmit():
    new_mt = Maintain(
        parts_id=request.form.get('parts_id'),
        employee_id=request.form.get('worker_id'),
        maintain_date=request.form.get('mt_date'),
        maintain_cost=request.form.get('mt_cost')
    )
    db.session.add(new_mt)
    db.session.commit()
    return render_template('success.html')

@app.route("/ticket/update")
def ticUpdate():
    return render_template('ticketupdate.html')

@app.route('/ticket/update/submit', methods=['POST'])
def ticUpdateSubmit():
    tid = request.form.get('ticket_id')
    status = request.form.get('status')
    ticket = Ticket.query.get(tid)
    if ticket:
        ticket.status = status
        db.session.commit()
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5005, debug=True)