from sanic_wtf import SanicForm
from wtforms import TextField, SelectField


class ShareAddEditForm(SanicForm):
    """
    for editing the shares
    """
    # description = TextAreaField('Description', validators=[DataRequired()])
    storage_mount_type = SelectField('Share type',
                                     choices=[('unc', 'UNC'), ('smb', 'SMB/CIFS'), ('nfs', 'NFS')])
    storage_mount_user = TextField('Share User')
    storage_mount_password = TextField('Share Password')
    storage_mount_server = TextField('Share hostname or IP address')
    storage_mount_path = TextField('Path')

    def __init__(self, *args, **kwargs):
        super(ShareAddEditForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(ShareAddEditForm, self).validate()
        if not initial_validation:
            return False
        return True
