import psycopg2
import datetime
import random
import numpy as np
import tflearn

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, DateTime, Float
from sqlalchemy.orm import Session, relationship, backref,\
                                joinedload_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm import load_only
from tflearn.data_utils import load_csv



Base = declarative_base()


# Connect to an existing database
# conn = psycopg2.connect("dbname=dreamwalkers user=bobo1239")

# Open a cursor to perform database operations
# cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
# cur.execute("SELECT * FROM test;")
# cur.fetchone()
# (1, 100, "abc'def")

# Make the changes to the database persistent
# conn.commit()

# Close communication with the database
# cur.close()
# conn.close()

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
        # print(new_datum.id)
        self.current_datum_id = new_datum.id

    def add_sleep(self, minutes, session, debug_creation=datetime.datetime.now()):
        if self.current_datum(session) == None:
            # print("WTF")
            self.create_datum(session, debug_creation)
        # print(self.current_datum_id)
        self.current_datum(session).add_sleep(minutes)
        session.commit()

    def set_grade(self, grade, session, debug_creation=datetime.datetime.now()):
        if self.current_datum(session) == None:
            print("KJSADKJSAHDAKJD")
            # TODO: warning
            return
        now = datetime.datetime.now()
        datum = self.current_datum(session)
        sleep_percent = datum.sleep_minutes / (float((now - datum.creation).total_seconds()) / 60.)
        # print("------------------------")
        # print(sleep_percent * 24.0)
        # print(grade)
        # print(self.current_datum(session).id)
        self.current_datum(session).set_grade(grade)
        # self.create_datum(session, debug_creation=debug_creation)

class Datum(Base):
    __tablename__='data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", uselist=False)
    creation = Column(DateTime, nullable=False)
    sleep_minutes = Column(Integer, nullable=False)
    grade = Column(Float, nullable=True)
    # sleeping_minutes = Column(Integer, nullable=False)

    def __init__(self, user_id, creation = datetime.datetime.now()):
        self.user_id = user_id
        self.creation = creation
        self.sleep_minutes = 0
        self.grade = None

    def add_sleep(self, minutes):
        # TODO: add sleep_minutes to value in db
        # cur.execute("UPDATE dreamworks SET learning_time = learning_time + %s", minutes)
        if self.grade == None:
            self.sleep_minutes += minutes
        # else:
            # TODO; log warning

    # def add_learning(self, minutes):
    #     # TODO: shouln't be able 
    #     # TODO: prepared staetment? security?
    #     cur.execute("UPDATE dreamworks SET learning_time = learning_time + %s", minutes)

    def set_grade(self, grade):
        self.grade = grade

    def to_numpy_array(self):
        return np.array([self.creation, self.sleep_minutes, self.grade])


if __name__ == '__main__':

    print("ASD")
    engine = create_engine('postgres://localhost/dreamwalkers', echo=False)

    Datum.__table__.drop(engine)
    User.__table__.drop(engine)

    Base.metadata.create_all(engine)

    session = Session(engine)

    user = User(name="asd")
    session.add(user)
    # session.commit()

    # # user.add_sleep(15, session)

    for i in range(1, 1000):
        sleep_h_per_day = 2.0 + random.random() * 6.0
        days = random.random() * 300.0 + 10.0
        creation = datetime.datetime.now() - datetime.timedelta(days)
        sleep_sum = sleep_h_per_day * days * 60.0;
        grade = 8.0/sleep_h_per_day;

        # print("===========")
        # print(24.0 * sleep_sum / (datetime.timedelta(days).total_seconds() / 60))
        # print("===========")
        # print("grade: " + str(grade))
        user.add_sleep(sleep_sum, session, debug_creation=creation)
        # print(user.current_datum(session).id)
        user.set_grade(grade, session, debug_creation=creation)
        # print(user.current_datum(session).id)
        session.commit()



    # Craete stuff...

    data = session.query(Datum) \
                  .filter(Datum.grade != None) \
                  .options(load_only("creation", "sleep_minutes", "grade")) \
                  .all()

    data = np.array([r.to_numpy_array() for r in data])

    # TODO: just specify datatype?
    # np_array = np.array(data[0][0].to_numpy_array())
    # do this efficiently...; currently allocates new array each iteration (?)
    # for datum in data:
        # np_array = np.append(np_array, datum[0].to_numpy_array())

    # print(np_array)


    # data_asd, labels = load_csv('titanic_dataset.csv', target_column=0,
                        # categorical_labels=True, n_classes=2)

    # labels = np.array([([1., 0.] if (i < len(data) * 0.8) else [0., 1.]) for i in range(len(data))])
    # asd

    # print(data)
    # print(labels)
    # for datum in data:


    # print(np_array[0])

    # asd


    now = datetime.datetime.now()
    # Preprocessing function
    def preprocess(data):
        # Sort by descending id and delete columns
        for i in range(len(data)):
            # print("aaaaaaaaaaaaaaaaaaaaaaa")
            # print(data[i][0])
            # print(data[i][1])
            # print(data[i][2])
            # print((now - data[i][0]).total_seconds() / 60)
            # print(data[i][1] / (float((now - data[i][0]).total_seconds()) / 60.))
            # print(data[i][2])
            data[i][1] = (float(data[i][1]) / (float((now - data[i][0]).total_seconds()) / 60.0))
        # [r.pop(0) for r in data] # remove creation as it's not needed anymore
        data=data[:,1:-1]


        # for i in data:
            # print(i)
        return np.array(data, dtype=np.float32)


    # Ignore 'name' and 'ticket' columns (id 1 & 6 of data array)

    # Preprocess data
    processed_data = preprocess(data)

    out = [a for a in data[:, -1]]
    # print(type(out[0]))
    # asd

    # # Build neural network
    # net = tflearn.input_data(shape=[None, 1])
    # net = tflearn.fully_connected(net, 32)
    # net = tflearn.fully_connected(net, 32)
    # # net = tflearn.fully_connected(net, 1, activation='softmax')
    # net = tflearn.regression(net, 1)

    # net = tflearn.input_data(shape=[None, 1])
    # # linear = tflearn.single_unit(input_)
    # net = tflearn.fully_connected(net, 1, activation='softmax')
    # net = tflearn.regression(net, optimizer='sgd', loss='mean_square',
    #         metric='R2', learning_rate=0.01)

    # # Define model
    # model = tflearn.DNN(net)
    # # Start training (apply gradient descent algorithm)

    input_ = tflearn.input_data(shape=[None, 1])
    linear = tflearn.single_unit(input_)
    regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                    metric='R2', learning_rate=0.02)
    m = tflearn.DNN(regression)
    m.fit(processed_data, out, n_epoch=1000, show_metric=True, snapshot_epoch=False)

    # labels = [[a] for a in data[:, -1]]
    # print(type(labels[0][0]))

    # model.fit(processed_data, labels, n_epoch=10, batch_size=16, show_metric=True, validation_set=0.1)

    print(m.predict([[8.0 / 24.0], [2.0 / 24.0]]))

    # session.add(node)
    # session.commit()