#forms.py - help forms handing and data validation

from wtforms import Form, TextField, DateField, IntegerField, \
                        SelectField, validators
                            
class AddTask(Form):
    task_id = IntegerField('Priority')
    name = TextField('Task Name', [validators.Required()])
    due_date = DateField('Date Due (mm/dd/yyyy)', [validators.Required()],
                            format = '%m/%d/%Y')
    priority = SelectField('Priority', [validators.Required()],choices=[('1','1'),
                            ('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
                            ('7','7'),('8','8'),('9','9'),('10','10')])
    status = IntegerField('Status')
    
    