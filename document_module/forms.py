from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional

class BaseDocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('')

    def __init__(self, submit_label, *args, **kwargs):
        super(BaseDocumentForm, self).__init__(*args, **kwargs)
        self.submit.label.text = submit_label

class CreateDocumentForm(BaseDocumentForm):
    file = FileField('File', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(CreateDocumentForm, self).__init__('Create', *args, **kwargs)

class UpdateDocumentForm(BaseDocumentForm):
    def __init__(self, *args, **kwargs):
        super(UpdateDocumentForm, self).__init__('Update', *args, **kwargs)