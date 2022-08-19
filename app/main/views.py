from crypt import methods
import hashlib
from flask import render_template,abort,flash, redirect,url_for,current_app, request
from flask_login import login_required,current_user
from . import main
from .forms import EditProfileForm,EditProfileAdminForm, PostForm
from ..models import Permission, Post, Role, User
from .. import db
from ..decorators import admin_required


@main.route('/',methods=['GET','POST'])
def index():
    """Note the way the author attribute of the new post object is set to the expression
        current_user._get_current_object(). The current_user variable from Flask-
        Login, like all context variables, is implemented as a thread-local proxy object. This
        object behaves like a user object but is really a thin wrapper that contains the actual user
        object inside. The database needs a real user object, which is obtained by calling
        _get_current_object()."""

    form  = PostForm()

    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body = form.body.data, author = current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))

    page = request.args.get('page',1,type = int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page = current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out = False)
    posts = pagination.items
    return render_template('index.html',form = form, posts = posts, pagination = pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    if user.avatar_hash is None:
        user.avatar_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()
        db.session.add(user)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)


@main.route('/edit-profile', methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("Your profile has been updated.")
        return redirect(url_for('.user',username = current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form = form)

@main.route('/edit-profile/<int:id>',methods = ['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user = user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user',username = user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html',form = form, user = user)

@main.route('/post/<int:id>')
def post(id):
    """Note that the post.html template receives a list with just the post to render. Sending a
    list is necessary so that the _posts.html template referenced by index.html and user.html
    can be used in this page as well."""
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts = [post])

@main.route('/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user !=post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(404)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post',id = post.id))
    form.body.data = post.body
    return render_template('edit_post.html',form = form)
