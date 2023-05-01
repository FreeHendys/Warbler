import os
from unittest import TestCase
from sqlalchemy import exc
from app import app
from models import db, User, Message, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

db.create_all()


class ModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create client, add fake data."""
        db.drop_all()
        db.create_all()

        self.uid = 234
        u = User.signup(
            "JimmyBob", "jimmybob@idkifthisisgoingtowork.com", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text="Bruckner 4 is better in every aspect than Beethoven 5",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(
            self.u.messages[0].text, "Bruckner 4 is better in every aspect than Beethoven 5")

    def test_message_likes(self):
        m1 = Message(
            text="Beethoven 5 is better in every aspect than Bruckner 4",
            user_id=self.uid
        )

        m2 = Message(
            text="you are an idiot",
            user_id=self.uid
        )

        u = User.signup("Yared", "yared@email.com", "password", None)
        uid = 1231
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m2)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m2.id)
