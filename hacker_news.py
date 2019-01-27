from flask import Flask, render_template, request
from google.cloud import bigquery
from flask import jsonify

app = Flask(__name__)
client = bigquery.Client()

@app.route("/search")
def search():
    return render_template('search.html')


@app.route('/results',methods = ['POST'])
def results():
    if request.method == 'POST':
      title = request.form.get("searchTitle")
      text = request.form.get("searchText")
      date = request.form.get("searchDate")
      print(date)
      if date:
        query_string = "select title, text, url, CAST(DATE(time_ts) AS DATE) as formatted_date  FROM `bigquery-public-data.hacker_news.stories` where title like '%{}%' and text like '%{}%' and DATE(time_ts)='{}' LIMIT 1000".format(title, text, date)
      else:
        query_string = "select title, text, url, CAST(DATE(time_ts) AS DATE) as formatted_date FROM `bigquery-public-data.hacker_news.stories` where title like '%{}%' and text like '%{}%' LIMIT 1000".format(title, text)
      
      query_job = client.query(query_string)
      results = query_job.result()
      data = []
      for row in results:
        print(row)
        record = {}
        record["title"] = row.title
        record["text"] = row.text
        record["URL"] = row.url
        record["date"] = row.formatted_date.strftime("%Y-%m-%d")
        data.append(record)
      return jsonify({"articles":data})