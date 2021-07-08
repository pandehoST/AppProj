from flask import Flask, render_template, request, redirect, url_for, session
from ScheduleForms import CreateScheduleForm
import shelve, Schedule, datetime

app = Flask(__name__)
app.secret_key = 'any_random_string'

"""
@app.route('/')
def login():
    return render_template('login.html')
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/userCrowdControl')
def userCrowdControl():
    return render_template('userCrowdControl.html')


@app.route('/userHealthDeclaration')
def userHealthDeclaration():
    return render_template('userHealthDeclaration.html')


@app.route('/userRoomService', methods=['GET', 'POST'])
def userRoomService():
    create_schedule_form = CreateScheduleForm(request.form)

    if request.method == 'POST' and create_schedule_form.validate():

        schedules_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            schedules_dict = db['Schedules']
        except:
            print("Error in retrieving Schedules from storage.db.")

        schedule = Schedule.Schedule(create_schedule_form.cabin_no.data, create_schedule_form.date.data,
                                     create_schedule_form.time.data, create_schedule_form.remarks.data,
                                     create_schedule_form.status.data)
        schedules_dict[schedule.get_id()] = schedule
        db['Schedules'] = schedules_dict

        db.close()

        session['schedule_created'] = schedule.get_id()

        return redirect(url_for('roomService'))
    return render_template('userRoomService.html', form=create_schedule_form)


@app.route('/userMySchedule')
def userMySchedule():
    schedules_dict = {}
    db = shelve.open('storage.db', 'r')
    schedules_dict = db['Schedules']
    db.close()

    schedules_list = []
    for key in schedules_dict:
        if schedules_dict.get(key).get_status() == "Pending":
            schedule = schedules_dict.get(key)
            schedules_list.append(schedule)

    return render_template('userMySchedule.html', count=len(schedules_list), schedules_list=schedules_list)


@app.route('/userRoomServiceHistory')
def userRoomServiceHistory():
    schedules_dict = {}
    db = shelve.open('storage.db', 'r')
    schedules_dict = db['Schedules']
    db.close()

    schedules_list = []
    for key in schedules_dict:
        if schedules_dict.get(key).get_status() == "Complete":
            schedule = schedules_dict.get(key)
            schedules_list.append(schedule)

    return render_template('userRoomServiceHistory.html', count=len(schedules_list), schedules_list=schedules_list)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/roomServiceCabin')
def roomServiceCabin():
    return render_template('roomServiceCabin')


@app.route('/crowdControl')
def crowdControl():
    return render_template('crowdControl.html')


@app.route('/healthDeclaration')
def healthDeclaration():
    return render_template('healthDeclaration.html')


@app.route('/roomService')
def roomService():
    schedules_dict = {}
    db = shelve.open('storage.db', 'r')
    schedules_dict = db['Schedules']
    db.close()

    schedules_list = []
    for key in schedules_dict:
        if schedules_dict.get(key).get_status() == "Pending":
            schedule = schedules_dict.get(key)
            schedules_list.append(schedule)

    return render_template('roomService.html', count=len(schedules_list), schedules_list=schedules_list)


@app.route('/roomServiceComplete')
def roomServiceComplete():
    schedules_dict = {}
    db = shelve.open('storage.db', 'r')
    schedules_dict = db['Schedules']
    db.close()

    schedules_list = []
    for key in schedules_dict:
        if schedules_dict.get(key).get_status() == "Complete":
            schedule = schedules_dict.get(key)
            schedules_list.append(schedule)

    return render_template('roomServiceComplete.html', count=len(schedules_list), schedules_list=schedules_list)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update_schedule(id):
    schedules_dict = {}
    db = shelve.open('storage.db', 'r')
    schedules_dict = db['Schedules']

    schedule = schedules_dict.get(id)
    schedule.set_status("Complete")

    db['Schedules'] = schedules_dict
    db.close()

    return redirect(url_for('roomServiceComplete'))


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser_schedule(id):
    updateUser_form = CreateScheduleForm(request.form)
    if request.method == 'POST' and updateUser_form.validate():

        schedules_dict = {}
        db = shelve.open('storage.db', 'w')
        schedules_dict = db['Schedules']

        scheduleUser = schedules_dict.get(id)
        scheduleUser.set_cabin_no(updateUser_form.cabin_no.data)
        scheduleUser.set_date(updateUser_form.date.data)
        scheduleUser.set_time(updateUser_form.time.data)
        scheduleUser.set_remarks(updateUser_form.remarks.data)

        db['Schedules'] = schedules_dict
        db.close()

        session['schedule_updated'] = scheduleUser.get_id()

        return redirect(url_for('userMySchedule'))
    else:
        schedules_dict = {}
        db = shelve.open('storage.db', 'r')
        schedules_dict = db['Schedules']
        db.close()

        scheduleUser = schedules_dict.get(id)
        updateUser_form.cabin_no.data = scheduleUser.get_cabin_no()
        updateUser_form.date.data = scheduleUser.get_date()
        updateUser_form.time.data = scheduleUser.get_time()
        updateUser_form.remarks.data = scheduleUser.get_remarks()

        return render_template('updateUser.html', form=updateUser_form)


@app.route('/deleteSchedule/<int:id>', methods=['POST'])
def delete_schedule(id):
    schedules_dict = {}
    db = shelve.open('storage.db', 'w')
    schedules_dict = db['Schedules']

    schedule = schedules_dict.pop(id)

    db['Schedules'] = schedules_dict
    db.close()

    session['schedule_deleted'] = schedule.get_id()
    return redirect(url_for('userMySchedule'))


if __name__ == '__main__':
    app.run()
