import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        res = self.client.get('/')
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "<title>Anand Tandon&#39;s Portfolio</title>" in html
        assert '<div class="education">' in html
        assert '''
            <h3>University of Waterloo</h3>
            <p>Software Engineering</p>
            <p>2024-2029</p>
            <p>GPA: 3.9/4.0</p>
            ''' in html
        assert '<img src="./static/img/my-map.png">' in html

    # GET testing
    def test_timeline(self):
        res = self.client.get('/api/timeline_post')
        assert res.status_code == 200
        assert res.is_json
        json = res.get_json()
        assert "timeline_posts" in json
        assert len(json['timeline_posts']) == 0

    # POST testing
    def test_timeline_post(self):
        testPost = {
            'name': 'A. Test',
            'email': 'test@example.com',
            'content': 'This is a test case.'
        }
        
        # Send the post to the timeline
        res = self.client.post('/api/timeline_post', data=testPost)
        assert res.status_code == 200
        assert res.is_json
        resData = res.get_json()
        assert resData['name'] == testPost['name']
        assert resData['email'] == testPost['email']
        assert resData['content'] == testPost['content']
        assert resData['id'] # Doesn't matter what the id of the post is, it just needs an id

        # Check the post is in the database
        resTimeline = self.client.get('/api/timeline_post')
        assert resTimeline.status_code == 200
        assert resTimeline.is_json
        json = resTimeline.get_json()
        assert "timeline_posts" in json
        assert len(json['timeline_posts']) > 0

        timelineAPITestPost = json['timeline_posts'][0]
        assert timelineAPITestPost['name'] == testPost['name']
        assert timelineAPITestPost['email'] == testPost['email']
        assert timelineAPITestPost['content'] == testPost['content']
        assert timelineAPITestPost['id'] == resData['id']

        # Check that the post is on the timeline page
        timelinePage = self.client.get('/timeline')
        assert timelinePage.status_code == 200
        html = timelinePage.get_data(as_text=True)
        assert f"<h3>{testPost['name']}</h3>" in html
        assert f'<div class="timeline-email">{testPost["email"]}</div>' in html
        assert f"<p>{testPost['content']}</p>" in html

        
    # DELETE testing
    def test_timeline_delete(self):
        # Add a post to the database
        testPost = {
            'name': 'A. Test',
            'email': 'test@example.com',
            'content': 'This is a test post that will be deleted.'
        }
        
        # Send the post to the timeline
        res = self.client.post('/api/timeline_post', data=testPost)
        assert res.status_code == 200
        assert res.is_json
        resData = res.get_json()
        postID = resData["id"]

        # Delete the post
        deleteRes = self.client.delete(f'/api/timeline_post?id={postID}')
        assert deleteRes.status_code == 200

    
    def test_bad_routes(self):
        url = '/api/timeline_post'
        
        # No Name
        res = self.client.post(url, data={"email": "noname@gmail.com", "content": "I have no name parameter!"})
        assert res.status_code == 400
        html = res.get_data(as_text=True)
        assert "Invalid name" in html

        # No Content
        res = self.client.post(url, data={"email": "nocontent@gmail.com", "name": "Joe McNoconent", 'content': ""})
        assert res.status_code == 400
        html = res.get_data(as_text=True)
        assert "Invalid content" in html

        # No email
        res = self.client.post(url, data={"email": "isNotAnEmail", "name": "Emm Ail", "content": "My email is bad!"})
        assert res.status_code == 400
        html = res.get_data(as_text=True)
        assert "Invalid email" in html