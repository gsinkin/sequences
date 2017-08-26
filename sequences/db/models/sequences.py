from sqlalchemy import Column, BigInteger, String, DateTime, Float, func

from . import Base


class Sequence(Base):

    __tablename__ = 'sequences'

    id = Column(BigInteger, primary_key=True)
    sequence_id = Column(String(255), nullable=False, unique=True)
    updater = Column(String(36), nullable=False, unique=True)
    current_value = Column(BigInteger, nullable=False, default=0)
    start_value = Column(BigInteger, nullable=False, default=1)
    range_size = Column(BigInteger, nullable=True)
    alert_threshold = Column(Float, nullable=True)

    updated_at = Column(
        DateTime, nullable=False, default=func.now(),
        onupdate=func.now())
    created_at = Column(
        DateTime, nullable=False, default=func.now())
