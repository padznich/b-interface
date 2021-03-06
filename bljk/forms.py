# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import Optional


class FormSummary(FlaskForm):

    identifier = StringField('Identifier', validators=[Optional()])
    date_from = DateField('Date From', validators=[Optional()])
    date_to = DateField('Date To', validators=[Optional()])


class FormDetail(FlaskForm):

    identifier = SelectField("Identifier", choices=[])
