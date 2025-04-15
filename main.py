import json
import re
import os
from flask import Flask, render_template, request, send_file, make_response
from feedgen.feed import FeedGenerator
from dotenv import load_dotenv
from routes.editor import editor_routes
from routes.scrapbook import sp_routes
from classes import *
load_dotenv()

app = Flask(__name__)
app.register_blueprint(editor_routes)
app.register_blueprint(sp_routes)

with open("articles.json", "r", encoding="utf-8") as f:
    articles_data = json.load(f)
categories = {} # Category name:str -> [Article]
articles = {} # ID:str = Article

# RSS Feed
fg = FeedGenerator()
fg.title("Mathias")
fg.id("Mathias")
fg.author({'name': "Mathias DPX", "email": "mathias@dupeux.net"})
fg.language("en")
fg.link(href=os.getenv("URL"))
fg.description("Blog RSS feed")

# Register articles
for article_data in articles_data:
    category_name = article_data.get("category", "Uncategorized")
    category_list = categories.get(category_name, [])

    article = Article(
        template=article_data.get("template"),
        title=article_data.get("title"),
        category=category_name
    )

    if article.template in articles.keys():
        raise KeyError(f"Two articles linking to the same template ({article.template})")

    articles[article.template] = article
    category_list.append(article)
    categories[category_name] = category_list

    fe = fg.add_entry()
    fe.id(article.template)
    fe.link(href=os.getenv("URL")+"/p/"+article.template)
    fe.title(article.title)

@app.route("/")
@app.route("/p")
def index():
    """Homepage"""
    return render_template("home.html", categories=categories.items())

@app.route("/rss")
def rss_feed():
    """RSS feed"""
    pretty = request.args.get("pretty", False, type=bool)
    response = make_response(fg.rss_str(pretty=pretty), 200)
    response.mimetype = "application/xml"
    return response

@app.route("/atom")
def atom_feed():
    """Atom feed"""
    pretty = request.args.get("pretty", False, type=bool)
    response = make_response(fg.atom_str(pretty=pretty), 200)
    response.mimetype = "application/xml"
    return response

@app.route("/favicon.ico")
def favicon():
    return send_file("static/favicon.ico")

@app.route("/contact")
def contact():
    """Contact page"""
    return render_template("contact.html")

@app.route("/p/<article_id>/")
def article(article_id:str):
    """Render an article"""
    if not re.match(r'[a-zA-Z0-9-]+', article_id):
        return ">:("
    article = articles[article_id]
    return render_template(f"articles/{article.template}.html")

if __name__ == "__main__":
    app.run(debug=True)
