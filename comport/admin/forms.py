from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired
from comport.department.models import Department

class NewDepartmentForm(Form):
    department_name = TextField('Department Name', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(NewDepartmentForm, self).__init__(*args, **kwargs)
        self.department = None

    def validate(self):
        initial_validation = super(NewDepartmentForm, self).validate()
        if not initial_validation:
            return False

        self.department = Department.query.filter_by(name=self.department_name.data).first()
        if self.department:
            self.department_name.errors.append('Department name already registered.')
            return False

        return True

class NewInviteForm(Form):
    department_id = SelectField("Department", coerce=int)

    def __init__(self, *args, **kwargs):
        super(NewInviteForm, self).__init__(*args, **kwargs)
