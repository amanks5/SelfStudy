from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import UUID, String, DateTime, Text, Integer, Float
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
import uuid

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = "users"
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = mapped_column(String(254), unique=True)
    hash = mapped_column(String(60))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class UserNote(db.Model):
    __tablename__ = "user_notes"
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = mapped_column(UUID(as_uuid=True))
    title = mapped_column(Text())
    content = mapped_column(Text())
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class UserFlashCard(db.Model):
    __tablename__ = "user_flashcards"
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = mapped_column(UUID(as_uuid=True))
    front = mapped_column(Text())
    back = mapped_column(Text())
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    #spaced rep based on a quality scale of 0-5 w/ 5 being understand the card the most
    ease_factor = mapped_column(Float(), default=2.5) #each card start w mid value of 2.5 cause its on a scale of 0-5
    interval = mapped_column(Integer(), default=1) #how many days until this card will be shown again, default = 1 day
    repetitions = mapped_column(Integer(), default=0) #how many time user successfully recalls flashcard in a row
    due_date = mapped_column(DateTime(timezone=True), default=func.now()) #when flashcard is scheduled for review next

def init(app):
    db.init_app(app)
    with app.app_context():
        try: # idk why, but sometimes this fails but its ok????
            db.create_all()
        except:
            pass

def signup(app, bcrypt, email, password):
    with app.app_context():
        user = User(
            email=email,
            hash=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            traceback.print_exc()
            return None
        return user.uuid

def login(app, bcrypt, email, password):
    with app.app_context():
        try:
            user = db.session.execute(db.select(User).where(User.email == email)).scalar_one()
            if bcrypt.check_password_hash(user.hash, password):
                return user.uuid
        except:
            traceback.print_exc()
        return None

def get_user_email(app, uuid):
    with app.app_context():
        user = db.session.execute(db.select(User).where(User.uuid == uuid)).scalar_one()
        return user.email
