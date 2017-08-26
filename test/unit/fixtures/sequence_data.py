from sequences.db.models.sequences import Sequence
from test.unit.fixtures import Fixture


class SequenceData(Fixture):

    model_class = Sequence
    models = [
        {
            "sequence_id": "TEST_SEQUENCE",
            "updater": "UPDATER",
            "current_value": 200,
            "start_value": 100,
            "range_size": 150,
        }
    ]
