import unittest
from peewee import *
from app import TimelinePost
from playhouse.shortcuts import model_to_dict

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
       test_db.drop_tables(MODELS)
       test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="Test McTestface",
            email='test@example.com',
            content='This is a test post')
        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Tester Ditesterino",
            email='example@test.com',
            content='This is another test post')
        assert second_post.id == 2

        posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
        assert len(posts) == 2
        assert posts[0]["name"] == second_post.name

