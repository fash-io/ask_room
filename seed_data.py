from faker import Faker
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Question, Answer, Tag, Category, Badge, BadgeCategory, BadgeLevel, Notification, NotificationType
from passlib.context import CryptContext
import uuid
from datetime import datetime, timedelta
import random

fake = Faker()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Static categories and tags
CATEGORY_NAMES = ["Frontend", "Backend", "DevOps", "UI/UX", "Mobile"]
TAG_NAMES = [
    "React", "Next.js", "Tailwind", "Figma", "Node.js",
    "Django", "Flutter", "SQL", "GraphQL"
]

def seed_categories(db: Session):
    # Define categories
    categories = [
        {"name": "Frontend", "description": "Questions about frontend development including HTML, CSS, JavaScript, and frontend frameworks"},
        {"name": "Backend", "description": "Questions about server-side programming, APIs, and backend frameworks"},
        {"name": "DevOps", "description": "Questions about deployment, CI/CD, containerization, and infrastructure"},
        {"name": "UI/UX", "description": "Questions about user interface design, user experience, and design principles"},
        {"name": "Mobile", "description": "Questions about mobile app development for iOS, Android, and cross-platform frameworks"},
        {"name": "Database", "description": "Questions about database design, queries, optimization, and management"},
        {"name": "Security", "description": "Questions about application security, authentication, authorization, and best practices"},
        {"name": "Testing", "description": "Questions about unit testing, integration testing, QA, and test automation"},
        {"name": "AI/ML", "description": "Questions about artificial intelligence, machine learning, and data science"},
        {"name": "Blockchain", "description": "Questions about blockchain technology, smart contracts, and cryptocurrencies"},
    ]
    
    # Add categories to database
    for category_data in categories:
        # Check if category already exists
        existing = db.query(Category).filter(Category.name == category_data["name"]).first()
        if not existing:
            category = Category(
                id=uuid.uuid4(),
                name=category_data["name"],
                description=category_data["description"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(category)
    
    db.commit()
    return db.query(Category).all()

def seed_tags(db: Session):
    # Define tags
    tags = [
        # Frontend
        "React", "Next.js", "Vue.js", "Angular", "Svelte", 
        "JavaScript", "TypeScript", "HTML", "CSS", "Tailwind CSS",
        "SASS", "Bootstrap", "Material UI", "Webpack", "Vite",
        
        # Backend
        "Node.js", "Express", "Django", "Flask", "FastAPI",
        "Spring Boot", "Laravel", "Ruby on Rails", "ASP.NET", "GraphQL",
        "REST API", "WebSockets", "Microservices", "Serverless",
        
        # DevOps
        "Docker", "Kubernetes", "AWS", "Azure", "GCP",
        "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible",
        "Monitoring", "Logging", "Prometheus", "Grafana",
        
        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "SQLite", "Firebase", "Supabase",
        "ORM", "SQL", "NoSQL", "Database Design",
        
        # Mobile
        "iOS", "Android", "React Native", "Flutter", "Kotlin",
        "Swift", "Xamarin", "Mobile UI", "Push Notifications",
        
        # Other
        "Python", "Java", "C#", "Go", "Rust",
        "PHP", "Ruby", "Performance", "Accessibility", "SEO",
        "Testing", "Security", "Authentication", "Authorization",
        "Machine Learning", "AI", "Data Science", "Blockchain", "Web3"
    ]
    
    # Add tags to database
    for tag_name in tags:
        # Check if tag already exists
        existing = db.query(Tag).filter(Tag.name == tag_name).first()
        if not existing:
            tag = Tag(
                id=uuid.uuid4(),
                name=tag_name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(tag)
    
    db.commit()
    return db.query(Tag).all()

def seed_users(db: Session, n=20):
    users = []
    
    # Create users with more realistic data
    for i in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}"
        
        # Create a more realistic bio
        bio_templates = [
            f"Software developer specializing in {random.choice(['frontend', 'backend', 'full-stack', 'mobile', 'DevOps'])} development.",
            f"{random.choice(['Senior', 'Junior', 'Mid-level'])} engineer at {fake.company()}.",
            f"Passionate about {random.choice(['web development', 'mobile apps', 'AI', 'blockchain', 'cloud computing'])}.",
            f"{random.choice(['Student', 'Professional', 'Hobbyist'])} programmer learning {random.choice(['React', 'Python', 'JavaScript', 'Go', 'Rust'])}.",
            f"Building {random.choice(['web apps', 'mobile apps', 'tools', 'libraries'])} since {random.randint(2010, 2022)}."
        ]
        
        # Create social links as JSON
        social_links_templates = [
            f'{{"github": "https://github.com/{username}", "twitter": "https://twitter.com/{username}"}}',
            f'{{"linkedin": "https://linkedin.com/in/{username}", "website": "https://{username}.dev"}}',
            f'{{"github": "https://github.com/{username}", "stackoverflow": "https://stackoverflow.com/users/123456/{username}"}}',
        ]
        
        # Hash a password
        hashed_password = pwd_context.hash(f"password{i}")
        
        # Create user with varying reputation
        reputation = random.choice([
            random.randint(1, 50),      # New users (50%)
            random.randint(51, 500),    # Established users (30%)
            random.randint(501, 5000),  # Experienced users (15%)
            random.randint(5001, 20000) # Power users (5%)
        ])
        
        # Create user with varying join dates
        days_ago = random.randint(1, 365 * 3)  # Up to 3 years ago
        join_date = datetime.utcnow() - timedelta(days=days_ago)
        
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=f"{username}@example.com",
            password_hash=hashed_password,
            display_name=f"{first_name} {last_name}",
            avatar_url=f"https://ui-avatars.com/api/?name={first_name}+{last_name}&background=random",
            bio=random.choice(bio_templates),
            social_links=random.choice(social_links_templates),
            reputation=reputation,
            created_at=join_date,
            updated_at=join_date,
            last_login=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            is_active=True,
            role="user" if random.random() < 0.9 else ("moderator" if random.random() < 0.8 else "admin"),
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    return users

def seed_questions(db: Session, users, categories, tags, n=50):
    questions = []
    
    # Create questions with more realistic data
    for _ in range(n):
        user = random.choice(users)
        category = random.choice(categories)
        
        # Select tags that make sense for the category
        relevant_tags = []
        if category.name == "Frontend":
            relevant_tags = [t for t in tags if t.name in ["React", "Next.js", "Vue.js", "JavaScript", "HTML", "CSS", "Tailwind CSS"]]
        elif category.name == "Backend":
            relevant_tags = [t for t in tags if t.name in ["Node.js", "Express", "Django", "FastAPI", "GraphQL", "REST API"]]
        elif category.name == "DevOps":
            relevant_tags = [t for t in tags if t.name in ["Docker", "Kubernetes", "AWS", "CI/CD", "Terraform"]]
        elif category.name == "Database":
            relevant_tags = [t for t in tags if t.name in ["PostgreSQL", "MongoDB", "SQL", "ORM", "Supabase"]]
        else:
            # For other categories, just pick random tags
            relevant_tags = tags
            
        # If no relevant tags found, use all tags
        if not relevant_tags:
            relevant_tags = tags
            
        question_tags = random.sample(relevant_tags, k=min(random.randint(1, 4), len(relevant_tags)))
        
        # Create more realistic titles
        title_templates = [
            f"How to {fake.bs().lower()} with {random.choice([t.name for t in question_tags])}?",
            f"Best practices for {fake.bs().lower()} in {random.choice([t.name for t in question_tags])}",
            f"Understanding {fake.bs().lower()} in {random.choice([t.name for t in question_tags])}",
            f"{random.choice([t.name for t in question_tags])}: {fake.bs().lower()}?",
            f"Problem with {fake.bs().lower()} when using {random.choice([t.name for t in question_tags])}",
            f"How to fix {fake.bs().lower()} error in {random.choice([t.name for t in question_tags])}?",
        ]
        
        # Create more realistic question bodies
        body_templates = [
            f"I'm trying to {fake.bs().lower()} using {random.choice([t.name for t in question_tags])}, but I'm running into issues. {fake.paragraph(nb_sentences=3)}\n\nHere's my code:\n\n\`\`\`\n{fake.paragraph(nb_sentences=2)}\n\`\`\`\n\nAny help would be appreciated!",
            f"What's the best way to {fake.bs().lower()} with {random.choice([t.name for t in question_tags])}? I've tried {fake.paragraph(nb_sentences=2)}, but it's not working as expected.\n\nHas anyone found a good solution for this?",
            f"I'm new to {random.choice([t.name for t in question_tags])} and I'm trying to understand how to {fake.bs().lower()}. {fake.paragraph(nb_sentences=3)}\n\nCan someone explain this concept to me?",
            f"I'm getting the following error when trying to {fake.bs().lower()} with {random.choice([t.name for t in question_tags])}:\n\n\`\`\`\n{fake.sentence()}\n\`\`\`\n\n{fake.paragraph(nb_sentences=2)}\n\nHow can I fix this?",
        ]
        
        # Create question with varying creation dates
        days_ago = random.randint(1, min(365, (datetime.utcnow() - user.created_at).days))
        creation_date = datetime.utcnow() - timedelta(days=days_ago)
        
        question = Question(
            id=uuid.uuid4(),
            title=random.choice(title_templates),
            body=random.choice(body_templates),
            author_id=user.id,
            category_id=category.id,
            created_at=creation_date,
            updated_at=creation_date,
            view_count=random.randint(10, 1000),
        )
        db.add(question)
        db.commit() 
        
        for tag in question_tags:
            question.tags.append(tag)
        
        db.commit()
        questions.append(question)
    
    return questions

def seed_answers(db: Session, users, questions, n=100):
    for _ in range(n):
        # Pick a random question
        question = random.choice(questions)
        
        # Don't let the author answer their own question (usually)
        available_users = [u for u in users if u.id != question.author_id or random.random() < 0.1]
        if not available_users:
            available_users = users
            
        user = random.choice(available_users)
        
        # Create more realistic answer bodies
        body_templates = [
            f"Based on my experience, you should {fake.bs().lower()}. {fake.paragraph(nb_sentences=2)}\n\nHere's an example:\n\n\`\`\`\n{fake.paragraph(nb_sentences=1)}\n\`\`\`\n\nHope this helps!",
            f"I've faced this issue before. The problem is that {fake.bs().lower()}. {fake.paragraph(nb_sentences=2)}\n\nTry this approach instead.",
            f"The best practice for this is to {fake.bs().lower()}. {fake.paragraph(nb_sentences=3)}",
            f"According to the documentation, you need to {fake.bs().lower()}. {fake.paragraph(nb_sentences=2)}\n\nCheck out this resource for more information: {fake.uri()}",
        ]
        
        # Create answer with varying creation dates (after question date)
        days_after_question = random.randint(0, (datetime.utcnow() - question.created_at).days)
        if days_after_question == 0:
            hours_after_question = random.randint(1, 23)
            creation_date = question.created_at + timedelta(hours=hours_after_question)
        else:
            creation_date = question.created_at + timedelta(days=days_after_question)
            
        # Determine if this answer should be marked as helpful
        is_helpful = random.random() < 0.3  # 30% chance of being marked helpful
        
        answer = Answer(
            id=uuid.uuid4(),
            body=random.choice(body_templates),
            author_id=user.id,
            question_id=question.id,
            created_at=creation_date,
            updated_at=creation_date,
            is_helpful=is_helpful
        )
        db.add(answer)
        
        # Create a notification for the question author
        if random.random() < 0.8:  # 80% chance of creating a notification
            notification = Notification(
                id=uuid.uuid4(),
                user_id=question.author_id,
                type=NotificationType.answer_posted,
                message=f"New answer to your question: '{question.title[:50]}...' by {user.username}",
                link=f"/questions/{question.id}#answer-{answer.id}",
                is_read=random.random() < 0.5,  # 50% chance of being read
                created_at=creation_date,
            )
            db.add(notification)
            
        # If answer is helpful, create a notification for the answer author
        if is_helpful:
            notification = Notification(
                id=uuid.uuid4(),
                user_id=user.id,
                type=NotificationType.answer_accepted,
                message=f"Your answer was accepted for the question: '{question.title[:50]}...'",
                link=f"/questions/{question.id}#answer-{answer.id}",
                is_read=random.random() < 0.3,  # 30% chance of being read
                created_at=creation_date + timedelta(days=random.randint(1, 7)),
            )
            db.add(notification)
    
    db.commit()

def seed_badges(db: Session):
    # Define badges
    badges = [
        {
            "name": "First Answer",
            "description": "Posted your first answer",
            "criteria": {"type": "answers_posted", "threshold": 1},
            "category": BadgeCategory.participation,
            "level": BadgeLevel.bronze,
        },
        {
            "name": "First Approval",
            "description": "Received your first approved answer",
            "criteria": {"type": "approved_answers", "threshold": 1},
            "category": BadgeCategory.quality,
            "level": BadgeLevel.bronze,
        },
        {
            "name": "10 Approved Answers",
            "description": "Received 10 approved answers",
            "criteria": {"type": "approved_answers", "threshold": 10},
            "category": BadgeCategory.quality,
            "level": BadgeLevel.silver,
        },
        {
            "name": "100 Reputation",
            "description": "Reached 100 reputation points",
            "criteria": {"type": "reputation", "threshold": 100},
            "category": BadgeCategory.community,
            "level": BadgeLevel.silver,
        },
        {
            "name": "Question Master",
            "description": "Posted 20 or more questions",
            "criteria": {"type": "questions_posted", "threshold": 20},
            "category": BadgeCategory.participation,
            "level": BadgeLevel.silver,
        },
        {
            "name": "Helpful Contributor",
            "description": "Got 20+ upvotes on your answers",
            "criteria": {"type": "upvotes_received", "threshold": 20},
            "category": BadgeCategory.quality,
            "level": BadgeLevel.silver,
        },
        {
            "name": "All-Star Contributor",
            "description": "Earned 1,000+ reputation points",
            "criteria": {"type": "reputation", "threshold": 1000},
            "category": BadgeCategory.community,
            "level": BadgeLevel.gold,
        },
    ]
    
    # Add badges to database
    for badge_data in badges:
        # Check if badge already exists
        existing = db.query(Badge).filter(Badge.name == badge_data["name"]).first()
        if not existing:
            badge = Badge(
                id=uuid.uuid4(),
                name=badge_data["name"],
                description=badge_data["description"],
                criteria=badge_data["criteria"],
                category=badge_data["category"],
                level=badge_data["level"],
                created_at=datetime.utcnow(),
            )
            db.add(badge)
    
    db.commit()
    return db.query(Badge).all()

def seed_admin_user(db: Session):
    # Check if admin user already exists
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        return existing
        
    # Create admin user
    hashed_password = pwd_context.hash("admin123")  # Change this in production!
    admin = User(
        id=uuid.uuid4(),
        username="admin",
        email="admin@example.com",
        password_hash=hashed_password,
        display_name="Admin User",
        bio="System administrator",
        reputation=1000,
        is_active=True,
        role="admin",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
    
def run_all():
    db = SessionLocal()
    try:
        print("🌱 Seeding database...")
        categories = seed_categories(db)
        print(f"✅ Seeded {len(categories)} categories")
        
        tags = seed_tags(db)
        print(f"✅ Seeded {len(tags)} tags")
        
        admin = seed_admin_user(db)
        print(f"✅ Created admin user: {admin.username}")
        
        users = seed_users(db)
        print(f"✅ Seeded {len(users)} users")
        
        questions = seed_questions(db, users, categories, tags)
        print(f"✅ Seeded {len(questions)} questions")
        
        seed_answers(db, users, questions)
        print(f"✅ Seeded answers and notifications")
        
        print("✅ Database seeding complete!")
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_all()
