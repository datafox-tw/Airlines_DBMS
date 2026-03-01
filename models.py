from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class DictModel:
    def __getitem__(self, key):
        return getattr(self, key, None)
    
    def keys(self):
        # Return all public attributes (columns)
        return [c.name for c in self.__table__.columns]

class Airport(db.Model, DictModel):
    __tablename__ = 'airport'
    airport_id = db.Column(db.BigInteger, primary_key=True)
    airport_name = db.Column(db.String(50), nullable=False)
    
class Airplane(db.Model, DictModel):
    __tablename__ = 'airplane'
    plane_id = db.Column(db.BigInteger, primary_key=True)
    manufacturer = db.Column(db.String(50), nullable=False)
    plane_name = db.Column(db.String(50), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    max_mileage = db.Column(db.Integer, nullable=False)
    startdate = db.Column(db.Date, nullable=False)

class Route(db.Model, DictModel):
    __tablename__ = 'route'
    route_id = db.Column(db.BigInteger, primary_key=True)
    depart_airport = db.Column(db.BigInteger, db.ForeignKey('airport.airport_id'))
    arrive_airport = db.Column(db.BigInteger, db.ForeignKey('airport.airport_id'))
    max_route_height = db.Column(db.Integer)
    
    # Relationships
    departure = db.relationship('Airport', foreign_keys=[depart_airport])
    arrival = db.relationship('Airport', foreign_keys=[arrive_airport])

class Flight(db.Model, DictModel):
    __tablename__ = 'flight'
    flight_id = db.Column(db.BigInteger, primary_key=True)
    plane_id = db.Column(db.BigInteger, db.ForeignKey('airplane.plane_id'))
    route_id = db.Column(db.BigInteger, db.ForeignKey('route.route_id'))
    depart_time = db.Column(db.DateTime, nullable=False)
    arrive_time = db.Column(db.DateTime, nullable=False)
    max_luggage_capacity = db.Column(db.Integer)
    max_sell_amount = db.Column(db.Integer)
    
    # Relationships
    airplane = db.relationship('Airplane', backref='flights')
    route = db.relationship('Route', backref='flights')
    
    @property
    def ticket_sold(self):
        return Ticket.query.filter_by(flight_id=self.flight_id).count()

class Ticket(db.Model, DictModel):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.BigInteger, primary_key=True)
    customer_nationality = db.Column(db.String)
    customer_id = db.Column(db.String)
    flight_id = db.Column(db.BigInteger, db.ForeignKey('flight.flight_id'))
    purchasing_time = db.Column(db.DateTime)
    ticket_level = db.Column(db.String(1))
    ticket_seat = db.Column(db.String(10))
    price = db.Column(db.BigInteger)
    status = db.Column(db.String(1))

class Employee(db.Model, DictModel):
    __tablename__ = 'employee'
    employee_id = db.Column(db.BigInteger, primary_key=True)
    employee_position = db.Column(db.String(30), nullable=False)
    employee_salary = db.Column(db.Integer, nullable=False)
    hired_time = db.Column(db.Date, nullable=False)

class Execute(db.Model, DictModel):
    __tablename__ = 'execute'
    flight_id = db.Column(db.BigInteger, db.ForeignKey('flight.flight_id'), primary_key=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employee.employee_id'), primary_key=True)
    employee_title = db.Column(db.String(30), nullable=False)
    
    employee = db.relationship('Employee', backref='assignments')
    flight = db.relationship('Flight', backref='crew')

class Parts(db.Model, DictModel):
    __tablename__ = 'parts'
    parts_id = db.Column(db.BigInteger, primary_key=True)
    parts_name = db.Column(db.String(50), nullable=False)
    plane_id = db.Column(db.BigInteger, db.ForeignKey('airplane.plane_id'))
    maintain_frequency = db.Column(db.Integer, nullable=False)
    max_maintain_times = db.Column(db.Integer, nullable=False)

class Maintain(db.Model, DictModel):
    __tablename__ = 'maintain'
    parts_id = db.Column(db.BigInteger, db.ForeignKey('parts.parts_id'), primary_key=True)
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employee.employee_id'), primary_key=True)
    maintain_date = db.Column(db.Date, primary_key=True)
    maintain_cost = db.Column(db.Integer)
    
    part = db.relationship('Parts', backref='maintenance_history')
    worker = db.relationship('Employee', backref='maintenance_tasks')
