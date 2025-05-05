# seed_data.py
from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Question, Answer, Tag, Category

import random
from datetime import datetime

fake = Faker()

# Static categories and tags
CATEGORY_NAMES = ["Frontend", "Backend", "DevOps", "UI/UX", "Mobile"]
TAG_NAMES = [
    "React", "Next.js", "Tailwind", "Figma", "Node.js",
    "Django", "Flutter", "SQL", "GraphQL"
]

def seed_categories(db: Session):
    db.query(Category).delete()
    db.commit()

    categories = [
        Category(name="Frontend"),
        Category(name="Backend"),
        Category(name="DevOps"),
        Category(name="UI/UX"),
        Category(name="Mobile"),
    ]

    db.add_all(categories)
    db.commit()
    return categories

def seed_tags(db: Session):
    db.query(Tag).delete()
    db.commit()
    tags = [
        Tag(name="React"),
        Tag(name="Next.js"),
        Tag(name="Tailwind"),
        Tag(name="Figma"),
        Tag(name="Node.js"),
        Tag(name="Django"),
        Tag(name="Flutter"),
        Tag(name="SQL"),
        Tag(name="GraphQL"),
        Tag(name="Python"),
        Tag(name="Java"),
    ]
    db.add_all(tags)
    db.commit()
    return tags

def seed_users(db: Session, n=10):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password_hash="fakehashedpassword",  # Replace with hash if needed
            bio=fake.sentence(),
            created_at=datetime.utcnow(),
        )
        db.add(user)
        users.append(user)
    db.commit()
    return users

def seed_questions(db: Session, users, categories, tags, n=20):
    questions = []
    for _ in range(n):
        user = random.choice(users)
        category = random.choice(categories)
        question_tags = random.sample(tags, k=random.randint(1, 3))
        question = Question(
            title=fake.sentence(nb_words=6),
            body=fake.paragraph(nb_sentences=3),
            author_id=user.id,
            category_id=category.id,
            created_at=datetime.utcnow(),
        )
        db.add(question)
        db.commit() 
        for tag in question_tags:
            question.tags.append(tag)
        db.commit()
        questions.append(question)
    return questions

def seed_answers(db: Session, users, questions, n=50):
    for _ in range(n):
        answer = Answer(
            body=fake.paragraph(),
            author_id=random.choice(users).id,
            question_id=random.choice(questions).id,
            created_at=datetime.utcnow(),
            is_helpful = random.choice([True, False])
        )
        db.add(answer)
    db.commit()
    
def run_all():
    db: Session = SessionLocal()

    # Re-create all tables (optional)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

    print("🌱 Seeding database...")
    categories = seed_categories(db)
    print("🌱 Seeding categories done...")
    tags = seed_tags(db)
    print("🌱 Seeding tags done...")
    users = seed_users(db)
    print("🌱 Seeding users done...")
    questions = seed_questions(db, users, categories, tags)
    print("🌱 Seeding questions done...")
    seed_answers(db, users, questions)
    print("🌱 Seeding answers done...")
    db.close()
    print("✅ Seeding complete!")

if __name__ == "__main__":
    run_all()
