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
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # reference images ; allow reverse reference
    images = relationship("Image", backref="user")


class Image(Base):
    """
    database model for images
    describes many-to-one relationship between image:user
    """
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary, nullable=False)
    caption = Column(String(140), default="")
    sha256 = Column(String(64), nullable=False)

    # reference image owner/user
    user_id = Column(Integer, ForeignKey("user.id"))


Base.metadata.create_all(engine)
