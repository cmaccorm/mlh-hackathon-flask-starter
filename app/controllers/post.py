# -*- coding: utf-8 -*-
import functools, json, requests
from app.extensions import db

from flask import flash, redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session
from datetime import datetime

from app.models.user import User, Post
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, InputRequired

from app.services.github import GitHub

blueprint = Blueprint('post', __name__, url_prefix='/post')

class PostForm(FlaskForm):
    Event = StringField('Event',validators=[InputRequired()])
    Location = StringField('Location',validators=[InputRequired()])
    Date = DateTimeField('Date', validators=[InputRequired('Please enter YY-mm-dd H:M:S')], format='%Y-%m-%d %H:%M:%S')
    Cap = IntegerField ('last name', validators=[InputRequired()])
    submit = SubmitField('Submit')


@blueprint.route('/', methods=['GET', 'POST'])
def makePost():
    form = PostForm()
    if form.validate_on_submit():
        data = GitHub.get_user_from_token(session['access_token'])
        post = Post(Event=form.Event.data, Location=form.Location.data
            ,Date=form.Date.data,Cap=form.Cap.data,
            author=db.session.query(User).get(data['id']))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.makePost'))
        # return render_template('tutorial/showPosts.html', post=post)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('tutorial/postForm.html', form = form, posts=posts)
