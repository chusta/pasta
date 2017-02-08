import datetime
from sqlalchemy import Column, Integer, String, LargeBinary
from .database import Base, engine

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
    """
    database model for users
    describes one-to-many relationship between user:image
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    # reference images ; allow reverse reference
    images = relationship("Image", back_populates="parent")


class Image(Base):
    """
    database model for images
    describes many-to-one relationship between image:user
    """
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)
    caption = Column(String(140))   # 140 char limit (twitter-esque)

    # reference image owner/user
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates("images"))


Base.metadata.create_all(engine)
