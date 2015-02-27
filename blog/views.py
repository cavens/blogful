import math
from flask import render_template

from blog import app
from .database import session
from .models import Post


@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
  count = session.query(Post).count()
  pages_total = math.ceil(count/paginate_by)
  
  start = page * paginate_by +1
  end = start + paginate_by
  
  has_next = page < pages_total
  has_prev = page > 1
  
  posts = session.query(Post)
  posts = posts.order_by(Post.datetime.desc())
  posts = posts[start:end]
  
  return render_template("posts.html",
                         posts = posts,
                         has_next = has_next,
                         has_prev = has_prev,
                         page = page,
                         total_pages = total_pages
                         )
