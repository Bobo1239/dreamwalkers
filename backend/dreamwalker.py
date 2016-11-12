from flask import Flask
app = Flask(__name__)

# add sleep min
@app.route('/add_sleep/<user_id>/<amount_min>', methods=['GET', 'POST'])
def addsleep(user_id, amount_min):
    return 'Dump min %s ' % amount_min

# add mililiter alky
@app.route('/add_drink/<user_id>/<amount_mililiter>', methods=['GET', 'POST'])
def adddrink(user_id, amount_mililiter):
    return 'Dump mililiter %s ' % amount_mililiter

# set grade
@app.route('/set_grade/<user_id>/<grade_result>', methods=['GET', 'POST'])
def setgradep(user_id, grade_result):
    return 'Dump grade %s ' % grade_result
        

if __name__ == "__main__":
    app.run()

