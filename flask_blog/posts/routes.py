from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm
from flask_blog.posts.utils import save_post_picture

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.picture.data:
            # post_track = save_post_track(form.track.data)
            post_picture = save_post_picture(form.picture.data)
            post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=post_picture, track=form.track)
        # post = Post(title=form.title.data, content=form.content.data, image_file=save_post_picture(form.picture.data), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Updated Post',
                           form=form, legend='Update Post')
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

