from uuid import uuid4

from sqlalchemy import and_
from sqlalchemy.sql.expression import insert, select, update
from sqlalchemy.exc import IntegrityError

from sequences.db import Transaction
from sequences.db.models.sequences import Sequence


def _get_sequence(sequence_id, session):
    select_stmt = select(
        [
            Sequence.__table__.c.current_value,
            Sequence.__table__.c.updater
        ]
    ).where(
        Sequence.sequence_id == sequence_id
    )
    result = session.execute(select_stmt).first()
    return result if result else (None, None)


def _create_sequence(
        sequence_id, start_value, range_size, alert_threshold, updater_id,
        session):
    insert_stmt = insert(
        Sequence.__table__,
        values={
            "sequence_id": sequence_id,
            "start_value": start_value,
            "current_value": start_value,
            "range_size": range_size,
            "alert_threshold": alert_threshold,
            "updater": updater_id
        },
        returning=[
            Sequence.__table__.c.current_value,
            Sequence.__table__.c.updater
        ]
    )
    result = session.execute(insert_stmt).first()
    return result


def _increment_sequence(sequence_id, current_updater, new_updater, session):
    update_stmt = update(Sequence.__table__).where(
        and_(
            Sequence.__table__.c.sequence_id == sequence_id,
            Sequence.__table__.c.updater == current_updater
        )
    ).values(
        sequence_id=sequence_id,
        updater=new_updater,
        current_value=Sequence.__table__.c.current_value + 1
    ).returning(
        Sequence.__table__.c.current_value,
        Sequence.__table__.c.updater
    )
    result = session.execute(update_stmt).first()
    return result if result else (None, None)


def get_next_value(
        sequence_id, start_value=1, range_size=None, alert_threshold=None):
    new_updater = str(uuid4())
    with Transaction() as session:
        current_value, current_updater = _get_sequence(sequence_id, session)
        if current_value is None:
            # The sequence doesnt exist, create it
            try:
                current_value, current_updater = _create_sequence(
                    sequence_id, start_value, range_size, alert_threshold,
                    new_updater, session)
                # This should always be the case, else IntegrityError
                if current_updater == new_updater:
                    return current_value
            except IntegrityError:
                # Sequence created, just get next value
                pass
        while current_updater != new_updater:
            # While this process is not the process that has set the new value
            # Attempt to increment the value
            current_value, current_updater = _increment_sequence(
                sequence_id, current_updater, new_updater, session)
            # If this process failed to update the sequence
            if not current_value:
                current_value, current_updater = _get_sequence(
                    sequence_id, session)

        return current_value
