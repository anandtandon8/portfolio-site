import os
import datetime
from playhouse.shortcuts import model_to_dict
from peewee import *
from flask import Flask, render_template, request
from dotenv import load_dotenv
from dateutil import parser
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), 
                         user=os.getenv("MYSQL_USER"), 
                         password=os.getenv("MYSQL_PASSWORD"), 
                         host=os.getenv("MYSQL_HOST"), 
                         port=3306)

# print(mydb)

# a model (columns) for sql table for timeline posts
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/')
def index():
    work_experiences = [
        {
            'title': 'Software Engineering Intern',
            'company': 'Toyota',
            'period': 'May 2025 – Aug 2025',
            'responsibilities': [
                'Built secure AWS infra for a WordPress site, boosting reliability with an EC2 autopatching solution w/ SSM',
                'Proposed scaling the autopatching solution org-wide to 500+ instances to reduce manual patching by 70%'
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'Ontario Aerospace Competition',
            'period': 'Apr 2023 – Aug 2024',
            'responsibilities': [
                'Built an HTML website for ONTAC with clean CSS styling to promote STEM interest to youth across Ontario',
                'Automated updates to accelerate patch releases by creating a CI/CD pipeline with Jekyll & GitHub Actions',
                'Configured DNS records to host the site on GitHub Pages, supporting 200+ weekly visitors with high uptime'
            ]
        },
        
        {
            'title': 'Production Engineering Fellow',
            'company': 'MLH',
            'period': 'June 2025 – Sept 2025',
            'responsibilities': [
                'Learning industry standard production engineering practices and tools with MLH and Meta'
            ]
        }
    ]

    education = [
        {
            'institution': 'University of Waterloo',
            'degree': 'Software Engineering',
            'period': '2024-2029',
            'gpa': '3.9/4.0',
            'courses': 'Data Structures, Algorithms, Methods of Software Engineering, Machine Learning, Linear Algebra, Calculus'
        },
        {
            'institution': 'The Woodlands Secondary School',
            'degree': 'High School',
            'period': '2020-2024',
            'gpa': '97.5%',
            'courses': None
        }
    ]

    about_me = {
        'description': 'I\'m currently studying at the University of Waterloo, with a major in Software Engineering. I just wrapped up my first year and am an aspiring software engineer. I also do photography on the side for fun.'
    }

    travel_map = {
        'title': 'All of the countries I\'ve been to',
        'description': 'I\'m from Mississauga, Ontario, Canada. Other countries I\'ve been to include the United States, Denmark, Spain, Portugal, Dominican Republic, India, France, and the United Kingdom.',
        'image': './static/img/my-map.png'
    }

    return render_template('index.html', 
                         title="Anand Tandon's Portfolio", 
                         url=os.getenv("URL"),
                         work_experiences=work_experiences,
                         education=education,
                         hobbies=hobbies,
                         about_me=about_me,
                         travel_map=travel_map)


@app.route('/hobbies')
def hobbies():
    hobbies = [
        {
            'title': 'Photography',
            'description': 'I love taking photos of nature and the streets. I lost my camera a year ago, and I just got back into it with a new one, it\'s been great!',
            'image': './static/img/photography_example.jpg'
        },
        {
            'title': 'Programming',
            'description': 'I love programming and learning new technologies. My favourite part is probably high level systems design like in the image below.',
            'image': './static/img/programming_example.png'
        }
    ]
    
    return render_template('hobbies.html', title="My Hobbies", hobbies=hobbies)

# add ordinal suffixes to numbers
def ordinal(n):
    if 10 <= n <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

# generate a more visually appealing datetime for the timeline posts
def format_datetime(dt):
    day = ordinal(dt.day)

    try:
        time_str = dt.strftime(f"%-I:%M %p")
    except ValueError:
        time_str = dt.strftime(f"%#I:%M %p")
    return dt.strftime(f"%B {day}, %Y, ") + time_str + " GMT"

@app.route('/timeline')
def timeline():
    timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]     # fetch posts from database using peewee
    for post in timeline_posts:
        if isinstance(post['created_at'], str):
            post['created_at'] = parser.parse(post['created_at'])
        post['formatted_date'] = format_datetime(post['created_at'])
    return render_template('timeline.html', title="Timeline Posts", timeline_posts=timeline_posts)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    if 'name' not in request.form or request.form['name'].strip() == "":
        return "Invalid name", 400
    if 'email' not in request.form or request.form['email'].strip() == "":
        return "Invalid email", 400
    if not re.search(r'(.+?)@(.+?)\.(.+?)', request.form['email']):
        return "Invalid email", 400
    if 'content' not in request.form or request.form['content'].strip() == "":
        return "Invalid content", 400
    
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)    # add to database using peewee
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {'timeline_posts': [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]}  

# this should have try/catch for better error handling, more likely to have an error than other methods
@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.args.get('id')
    post = TimelinePost.get_by_id(id)
    post.delete_instance()      # super easy with peewee!
    return {'message': f'Timeline post {id} deleted successfully'}

