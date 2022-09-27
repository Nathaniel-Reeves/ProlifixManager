from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from ..db import DatabaseConnection

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = DatabaseConnection()
    session = db.get_session()
    posts = session.sql(
        """SELECT p.`id`, `title`, `body`, `created`, `author_id`, `username`
        FROM `test`.`post` p JOIN `test`.`user` u ON p.`author_id` = u.`id`        ORDER BY created DESC;"""
    ).execute()
    posts = posts.fetch_all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = DatabaseConnection()
            session = db.get_session()
            session.sql(
                '''INSERT INTO `test`.`post` (`title`, `body`, `author_id`)
                VALUES (?, ?, ?)'''
            ).bind((title, body, g.user['id'])).execute()
            session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db = DatabaseConnection()
    session = db.get_session()
    post = session.sql(
        """SELECT p.`id`, `title`, `body`, `created`, `author_id`, `username`
        FROM `test`.`post` p JOIN `test`.`user` u ON p.`author_id` = u.`id`
        WHERE p.id = ?"""
    ).bind((id,)).execute().fetch_one()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = DatabaseConnection()
            session = db.get_session()
            post = session.sql(
                """UPDATE `test`.`post` SET `title` = ?, `body` = ?
                WHERE `id` = ?"""
            ).bind((title, body, id)).execute()
            session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)

    db = DatabaseConnection()
    session = db.get_session()
    session.sql('DELETE FROM `test`.`post` WHERE `id` = ?').bind((id,)).execute()
    session.commit()
    return redirect(url_for('blog.index'))
