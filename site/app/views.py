from flask import render_template, request, url_for, flash, redirect
from app import app
from article_collector import cyberleninka_parser
from database import mysql
from datetime import datetime
from flask import send_from_directory

db = mysql.mysql()

@app.route('/')
@app.route('/export/<path:path>')
def send_report(path=""):
    return send_from_directory('export', path)

@app.route('/litparser')
def litparser():
    return render_template("literature_parser.html")

@app.route('/results')
def litparser_results():
    search_text = request.values['request']
    limit = int(request.values['limit'])
    collector = cyberleninka_parser.Cyberleninka_parser("chrome")
    articles = collector.Get_articles(search_text, limit)
    dbres = db.AddRequestResult(articles, {"text":search_text, "limit":limit, "date":datetime.now()})
    filename = collector.Export(articles, search_text)
    return render_template("parser_results.html", articles=articles, search_text=search_text, limit=limit, dbres=dbres, fname=filename)