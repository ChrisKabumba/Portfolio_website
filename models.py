from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import urlencode
import hashlib
from typing import List

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(String(250))

    projects: Mapped[List['Projects']] = relationship(back_populates="user")

    def avatar(self, size):
        email_encoded = self.email.lower().encode('utf-8')
        email_hash = hashlib.md5(email_encoded).hexdigest()
        params = urlencode({"d": "identicon", "s": str(size)})
        return f"https://www.gravatar.com/avatar/{email_hash}?{params}"

class Projects(db.Model):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(10))

    user: Mapped[List['User']] = relationship(back_populates="projects")
