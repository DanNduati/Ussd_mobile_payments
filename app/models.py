from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phonenumber = Column(String, nullable=False)
    units = relationship("Unit", back_populates="owner")


class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="units")

