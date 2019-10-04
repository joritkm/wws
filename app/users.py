import os
import yaml
import crypt
from hmac import compare_digest
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     IntegerField,
                     SelectField,
                     TextField)
from wtforms.validators import DataRequired, Length

from . import app, login
from . import logger


@login.user_loader
def load_user(id: str):
    return User(id)

class LoginForm(FlaskForm):
    id = StringField("User ID",validators=[DataRequired(),Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(),Length(max=64)])


class RSVPForm(FlaskForm):
    
    duration_choices = [
        ("Fri, 12.06 - Sat, 14.06","Fri, 12.06 - Sat, 14.06"),
        ("Fri, 12.06 - Sun, 15.06","Fri, 12.06 - Sun, 15.06")
    ]
    accommodations_choices = [
        ("Selbstorganisiert","Selbstorganisiert"),
        ("Im Bus!","Im Bus!")
    ]
    
    name = StringField("Name",validators=[DataRequired(),Length(max=64)])
    adults = IntegerField("Erwachsene", validators=[DataRequired()],default=1)
    kids = IntegerField("Kinder",default=0)
    duration = SelectField("Aufenthalt",choices=duration_choices, validators=[DataRequired()])
    accommodations = SelectField("Unterkunft",choices=accommodations_choices)
    comment = TextField("Kommentare/Fragen/Einwände",validators=[Length(max=256)])

    def with_data(self,data):
        if data:
            self.name.data = data.get("name",None)
            self.adults.data = data.get("adults",1)
            self.kids.data = data.get("kids",0)
            self.duration.data = data.get("duration",
                                          self.duration_choices[0])
            self.accommodations.data = data.get("accommodations",
                                                self.accommodations_choices[0])
            self.comment.data = data.get("comment","")


class User(UserMixin):
    id = None
    _password_hash = None

    _rsvp_data_fields = [
        "name",
        "adults",
        "kids",
        "duration",
        "accommodations",
        "comment"
    ]
    
    @property
    def _rsvp_data_path(self):
        if self.id:
            return os.path.join(app.config["RSVP_PATH"],self.id)

    @staticmethod
    def load(_id):
        with open(app.config["PASSWD"]) as _f:
            try:
                return yaml.safe_load(_f)[_id]
            except KeyError:
                logger.warning(format("No such key {}", _id))
                return None

    def authenticate(self, password):
        if not self._password_hash:
            return False
        return compare_digest(self._password_hash, 
                              crypt.crypt(password, 
                                          self._password_hash))

    def fetch_rsvp(self):
        assert(self.id)
        if os.path.isfile(self._rsvp_data_path):
            with open(self._rsvp_data_path) as _f:
                data = yaml.safe_load(_f)
            return data

    def save_rsvp(self, form_data):
        assert(self.id)
        data = {x:y for x,y in form_data.items() if x in self._rsvp_data_fields}
        with open(self._rsvp_data_path, "w") as _f:
            yaml.safe_dump(data, _f)

    def __init__(self, _id=None):
        if _id:
            user_data = self.load(_id)
            if user_data:
                self.id = _id
                self._password_hash = user_data["password_hash"]