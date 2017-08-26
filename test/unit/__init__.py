import os
from unittest import TestCase

from sequences.db import Transaction

DATABASE_TEST_URI = os.environ["DATABASE_TEST_URI"]
assert DATABASE_TEST_URI != os.environ["DATABASE_URI"]


class BaseTestCase(TestCase):

    fixtures = []

    def setUp(self):
        # I Hate This
        from sequences import db
        db.DATABASE_URI = DATABASE_TEST_URI

        with Transaction() as session:
            for fixture in self.fixtures:
                session.query(fixture.model_class).delete()

        with Transaction() as session:
            for fixture in self.fixtures:
                models = []
                for model_data in fixture.models:
                    models.append(fixture.model_class(**model_data))
                session.add_all(models)
