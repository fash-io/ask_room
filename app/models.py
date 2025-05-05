from datetime import datetime
import enum
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    Boolean,
    Enum,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from database import Base, get_db

from sqlalchemy.dialects.postgresql import UUID

db = get_db()


class UserRole(enum.Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class Badge(Base):
    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", secondary="user_badges", back_populates="badges")


user_badges = Table(
    "user_badges",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("badge_id", UUID(as_uuid=True), ForeignKey("badges.id")),
)

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("followed_id", UUID(as_uuid=True), ForeignKey("users.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    reputation = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    social_links = Column(Text, nullable=True)

    questions = relationship(
        "Question", back_populates="author", cascade="all, delete-orphan"
    )
    answers = relationship(
        "Answer", back_populates="author", cascade="all, delete-orphan"
    )
    question_votes = relationship(
        "QuestionVote", back_populates="user", cascade="all, delete-orphan"
    )
    answer_votes = relationship(
        "AnswerVote", back_populates="user", cascade="all, delete-orphan"
    )
    badges = relationship("Badge", secondary="user_badges", back_populates="users")


question_tags = Table(
    "question_tags",
    Base.metadata,
    Column("question_id", UUID(as_uuid=True), ForeignKey("questions.id")),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id")),
)


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    images = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # relationships
    author = relationship("User", back_populates="questions")
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
    votes = relationship(
        "QuestionVote", back_populates="question", cascade="all, delete-orphan"
    )
    tags = relationship("Tag", secondary=question_tags, back_populates="questions")
    category = relationship("Category", back_populates="questions")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_helpful = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # relationships
    question = relationship("Question", back_populates="answers")
    author = relationship("User", back_populates="answers")
    votes = relationship(
        "AnswerVote", back_populates="answer", cascade="all, delete-orphan"
    )


class VoteValue(enum.Enum):
    down = -1
    up = 1


class QuestionVote(Base):
    __tablename__ = "question_votes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    vote_value = Column(Enum(VoteValue), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user = relationship("User", back_populates="question_votes")
    question = relationship("Question", back_populates="votes")


class AnswerVote(Base):
    __tablename__ = "answer_votes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    answer_id = Column(UUID(as_uuid=True), ForeignKey("answers.id"), nullable=False)
    vote_value = Column(Enum(VoteValue), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user = relationship("User", back_populates="answer_votes")
    answer = relationship("Answer", back_populates="votes")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # relationships
    questions = relationship("Question", secondary=question_tags, back_populates="tags")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # relationships
    questions = relationship(
        "Question", back_populates="category", cascade="all, delete-orphan"
    )
