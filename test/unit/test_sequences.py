from sequences import get_next_value

from test.unit import BaseTestCase
from test.unit.fixtures.sequence_data import SequenceData


class TestSequences(BaseTestCase):

    fixtures = [SequenceData]

    def test_get_next_value(self):
        for index in xrange(1, 20):
            assert get_next_value("SEQUENCE_ID") == index

    def test_get_next_value_start_value(self):
        for index in xrange(5, 20):
            assert get_next_value("START_SEQUENCE_ID", 5) == index
