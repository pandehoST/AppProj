from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class CreateScheduleForm(Form):
    cabin_no = StringField('Cabin No.', [validators.Length(min=1, max=150), validators.DataRequired()], default='R.309')
    date = StringField('Date', [validators.Length(min=1, max=150), validators.DataRequired()])
    time = StringField('Time', [validators.Length(min=1, max=150), validators.DataRequired()])
    remarks = TextAreaField('Remarks', [validators.Optional()])
    status = SelectField('Status', [validators.Optional()], choices=[('Pending', 'Pending'), ('Complete', 'Complete')], default='Pending')
