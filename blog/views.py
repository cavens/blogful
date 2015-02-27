import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)

import math
import mistune
from flask import render_template, request, redirect, url_for

from blog import app
from .database import session
from .models import Post


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
def add_post_get():
  return render_template("add_post.html")
  
@app.route("/post/add", methods=["POST"])
def add_post_post():
  post = Post(
  title = request.form["title"],
  content = mistune.markdown(request.form["content"])
  )
  logging.debug("Before post")
  session.add(post)
  logging.debug("Before commit")
  session.commit()
  logging.debug("Before return")
  return redirect(url_for("posts"))
  
  
  
  
  
  
  