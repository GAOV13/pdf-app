from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional

class BaseDocumentForm(FlaskForm):
    """
    Formulario base para documentos.

    Campos:
    - title (StringField): Título del documento.
    - description (TextAreaField): Descripción del documento.
    - submit (SubmitField): Botón para enviar el formulario.
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('')

    def __init__(self, submit_label, *args, **kwargs):
        """
        Inicializa el formulario base de documentos.

        Entradas:
        - submit_label (str): Texto del botón de envío.
        """
        super(BaseDocumentForm, self).__init__(*args, **kwargs)
        self.submit.label.text = submit_label

class CreateDocumentForm(BaseDocumentForm):
    """
    Formulario para la creación de documentos.

    Campos:
    - file (FileField): Archivo del documento.
    """
    file = FileField('File', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario de creación de documentos.
        """
        super(CreateDocumentForm, self).__init__('Create', *args, **kwargs)

class UpdateDocumentForm(BaseDocumentForm):
    """
    Formulario para la actualización de documentos.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario de actualización de documentos.
        """
        super(UpdateDocumentForm, self).__init__('Update', *args, **kwargs)