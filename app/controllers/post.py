# -*- coding: utf-8 -*-
import functools, json, requests
from app.extensions import db

from flask import flash, redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session
from datetime import datetime

from app.models.user import User, Post
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

from app.services.github import GitHub

blueprint = Blueprint('post', __name__, url_prefix='/post')

class PostForm(FlaskForm):
    body = TextAreaField("Enter your volunteering event here!", validators=[DataRequired()])
    submit = SubmitField('Submit')

@blueprint.route('/', methods=['GET', 'POST'])
def makePost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=User(username="testFakeUsername", avatar_url="fake", github_id=123))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home.index'))
    return render_template('tutorial/postForm.html', form = form)
