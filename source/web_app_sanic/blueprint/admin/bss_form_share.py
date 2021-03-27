from sanic_wtf import SanicForm
from wtforms import StringField, SelectField


class BSSShareAddEditForm(SanicForm):
    """
    for editing the shares
    """
    # description = TextAreaField('Description', validators=[DataRequired()])
    storage_mount_type = SelectField('Share type',
                                     choices=[('unc', 'UNC'), ('smb', 'SMB/CIFS'), ('nfs', 'NFS')])
    storage_mount_user = StringField('Share User')
    storage_mount_password = StringField('Share Password')
    storage_mount_server = StringField('Share hostname or IP address')
    storage_mount_path = StringField('Path')

    def __init__(self, *args, **kwargs):
        super(BSSShareAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(BSSShareAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True
