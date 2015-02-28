import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)

import math
import mistune
from flask import render_template, request, redirect, url_for

from blog import app
from .database import session
from .models import Post

from flask import flash
from flask.ext.login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from .models import User


@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
  page_index = page-1
  count = session.query(Post).count()
  pages_total = math.ceil(count/paginate_by)
  
  start = page_index * paginate_by
  end = start + paginate_by
  
  has_next = page_index < pages_total -1
  has_prev = page_index > 0
  
  posts = session.query(Post)
  posts = posts.order_by(Post.datetime.desc())
  posts = posts[start:end]
  
  return render_template("posts.html",
                         posts = posts,
                         has_next = has_next,
                         has_prev = has_prev,
                         page = page,
                         pages_total = pages_total
                         )


@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
  return render_template("add_post.html")
  
@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
  post = Post(
  title = request.form["title"],
  content = mistune.markdown(request.form["content"]),
  author = current_user
  )
  session.add(post)
  session.commit()
  return redirect(url_for("posts"))
  
@app.route("/post/<id>")
@login_required
def add_post_details(id):
  post = session.query(Post).filter(Post.id == id).first()
  return render_template("details.html", post = post)
  
@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_get(id):
  post = session.query(Post).filter(Post.id == id).first()
  return render_template("edit.html", post = post)
  
@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post(id):
  new_title = request.form["title"]
  new_content = mistune.markdown(request.form["content"])

  session.query(Post).filter(Post.id == id).update({"title": (new_title)})
  session.query(Post).filter(Post.id == id).update({"content": (new_content)})

  session.commit()
  return redirect(url_for("posts"))
  
  
@app.route("/post/<id>/delete")
@login_required
def del_post_step1(id):
  post = session.query(Post).filter(Post.id == id).first()
  logging.debug("This is postid {}".format(post))
  return render_template("delete_confirm.html", post = post)
  
@app.route("/post/<id>/delete/confirm")  
@login_required
def del_post_step2(id):
  post = session.query(Post).filter(Post.id == id).first()
  session.delete(post)
  session.commit
  return redirect(url_for("posts"))
  
  
@app.route("/login", methods=["GET"])
def login_get():
  return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
  email = request.form["email"]
  password = request.form["password"]
  user = session.query(User).filter_by(email=email).first()
  if not user or not check_password_hash(user.password, password):
    logging.debug("in if")
    flash("Incorrect username or password","danger")
    return redirect (url_for("login_get"))
  
  login_user(user)
  return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout")
def logout():
  logout_user()
  return redirect (url_for("posts"))

  
  
  
  
  
  