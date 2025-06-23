import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


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

    return render_template('index.html', 
                         title="MLH Fellow", 
                         url=os.getenv("URL"),
                         work_experiences=work_experiences,
                         education=education,
                         hobbies=hobbies)
