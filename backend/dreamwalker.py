from flask import Flask
app = Flask(__name__)

@app.route("/add_sleep/<user_id>/<amount_min>", methods=['GET', 'POST'])
def addsleep(user_id, amount_min):
    return 'Dump min %s ' % amount_min


@app.route("/add_drink/<user_id>/<amount_mililiter>", methods=['GET', 'POST'])
def addsleep(user_id, amount_mililiter):
    return 'Dump mililiter %s ' % amount_mililiter

@app.route("/set_grade/<user_id>/<grade_result>", methods=['GET', 'POST'])
def addsleep(user_id, grade_result):
    return 'Dump grade %s ' % grade_result

@app.route("/")
def hello1():
    return '{"hello": "world"}'

@app.route('/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username
        


if __name__ == "__main__":
    app.run()
