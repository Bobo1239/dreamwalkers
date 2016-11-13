import psycopg2
import datetime
import random
import numpy as np
import tflearn

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, DateTime, Float
from sqlalchemy.orm import Session, relationship, backref, joinedload_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm import load_only


Base = declarative_base()

# Preprocessing function
# Takes a [[creation: DateTime, sleep_min: minutes, grade: float]] and
# outputs a [[sleep_percentage: float]] (array of arrays for future extensibility (e.g. alcohol))
def preprocess(data):
    for i in range(len(data)):
        data[i][1] = (float(data[i][1]) / (float((now - data[i][0]).total_seconds()) / 60.0))
    data=data[:,1:-1] # slice creation and grade away
    return np.array(data, dtype=np.float32)

class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    current_datum_id = ForeignKey(("Datum.id"), nullable=True)

    def __init__(self, name):
        self.name = name

    def current_datum(self, session):
        return session.query(Datum).filter(Datum.user_id == self.id, Datum.grade == None).first()

    def create_datum(self, session, debug_creation=datetime.datetime.now()):
        new_datum = Datum(self.id, debug_creation)
        session.add(new_datum)
        session.commit()
        self.current_datum_id = new_datum.id

    def add_sleep(self, minutes, session, debug_creation=datetime.datetime.now()):
        if self.current_datum(session) == None:
            self.create_datum(session, debug_creation)
        self.current_datum(session).add_sleep(minutes)
        session.commit()

    def set_grade(self, grade, session, debug_creation=datetime.datetime.now()):
        if self.current_datum(session) == None:
            # TODO: warning
            return
        now = datetime.datetime.now()
        datum = self.current_datum(session)
        sleep_percent = datum.sleep_minutes / (float((now - datum.creation).total_seconds()) / 60.)
        self.current_datum(session).set_grade(grade)

    def predict_grade(self):
        return self.current_datum(session).predict_grade()

class Datum(Base):
    __tablename__='data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", uselist=False)
    creation = Column(DateTime, nullable=False)
    sleep_minutes = Column(Integer, nullable=False)
    grade = Column(Float, nullable=True)

    def __init__(self, user_id, creation = datetime.datetime.now()):
        self.user_id = user_id
        self.creation = creation
        self.sleep_minutes = 0
        self.grade = None

    def add_sleep(self, minutes):
        # TODO: add sleep_minutes to value in db
        if self.grade == None:
            self.sleep_minutes += minutes
        # else:
            # TODO; log warning

    def set_grade(self, grade):
        self.grade = grade

    def to_numpy_array(self):
        return np.array([self.creation, self.sleep_minutes, self.grade])

    def predict_grade(self):
        time_delta = float((datetime.datetime.now() - self.creation).total_seconds()) / 60.0
        return model.predict([[float(self.sleep_minutes) / time_delta]])[0]


session = None
model = None

from flask import Flask
app = Flask(__name__)

def get_user(id):
    return session.query(User).filter(User.id == id).first()

@app.route('/add_sleep/<user_id>/<amount_min>', methods=['GET', 'POST'])
def add_sleep(user_id, amount_min):
    if amount_min == "demo":
        return str(model.predict([[5.0 / 24.0]])[0])
    else:
        user = get_user(int(user_id))
        user.add_sleep(int(amount_min), session)
        session.commit()
        return str(user.predict_grade())

@app.route('/add_drink/<user_id>/<amount_milliliter>', methods=['GET', 'POST'])
def add_drink(user_id, amount_milliliter):
    get_user(int(user_id)).add_drink(int(amount_milliliter), session)
    return str(user.predict_grade())

@app.route('/set_grade/<user_id>/<grade>', methods=['GET', 'POST'])
def set_grade(user_id, grade):
    user = get_user(int(user_id))
    user.set_grade(float(grade), session)
    session.commit()
    # TODO ...
    return 'Success: Grade %s' % grade


if __name__ == '__main__':
    print("Start!")
    engine = create_engine('postgres:///dreamwalkers', echo=False)

    Datum.__table__.drop(engine)
    User.__table__.drop(engine)

    Base.metadata.create_all(engine)

    session = Session(engine)

    user = User(name="User1")
    session.add(user)

    print("Creating Dataset!")
    for i in range(1, 1000):
        sleep_h_per_day = 2.0 + random.random() * 6.0
        days = random.random() * 300.0 + 10.0
        creation = datetime.datetime.now() - datetime.timedelta(days)
        sleep_sum = sleep_h_per_day * days * 60.0;
        # Sleep more -> get better grade
        grade = 8.0/sleep_h_per_day;
        user.add_sleep(sleep_sum, session, debug_creation=creation)
        user.set_grade(grade, session, debug_creation=creation)
    session.commit()


    # Craete stuff...

    data = session.query(Datum) \
                  .filter(Datum.grade != None) \
                  .options(load_only("creation", "sleep_minutes", "grade")) \
                  .all()

    data = np.array([r.to_numpy_array() for r in data])

    now = datetime.datetime.now()

    processed_data = preprocess(data)

    grades = [a for a in data[:, -1]]

    input_ = tflearn.input_data(shape=[None, 1])
    linear = tflearn.single_unit(input_)
    regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                    metric='R2', learning_rate=0.02)
    model = tflearn.DNN(regression)
    model.fit(processed_data, grades, n_epoch=1000, show_metric=True, snapshot_epoch=False)


    print(model.predict([[8.0 / 24.0], [2.0 / 24.0]]))

    app.run(host='0.0.0.0', port=80)
