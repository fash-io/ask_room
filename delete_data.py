from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Question, Answer, Tag, Category, Badge, BadgeCategory, BadgeLevel, Notification, NotificationType, question_tags

db = SessionLocal()

db.query(User).delete()
db.query(Question).delete()
db.query(Answer).delete()
db.query(Tag).delete()
db.query(Category).delete()
db.query(Badge).delete()
db.query(BadgeCategory).delete()
db.query(BadgeLevel).delete()
db.query(Notification).delete()
db.query(NotificationType).delete()

db.commit()