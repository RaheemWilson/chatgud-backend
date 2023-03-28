# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'Category'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    image = Column(Text)
    categoryOrder = Column(Integer)


class Proficiency(Base):
    __tablename__ = 'Proficiency'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    preferenceOrder = Column(Integer, nullable=False)


class Resource(Base):
    __tablename__ = 'Resource'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(Enum('audio', 'image', 'video', 'text', name='ResourceType'), nullable=False)
    transcription = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    media = Column(Text, nullable=False)

    TaskChoice = relationship('TaskChoice', secondary='_ResourceToTaskChoice')


class TaskChoice(Base):
    __tablename__ = 'TaskChoice'

    id = Column(Text, primary_key=True)


class PrismaMigration(Base):
    __tablename__ = '_prisma_migrations'

    id = Column(String(36), primary_key=True)
    checksum = Column(String(64), nullable=False)
    finished_at = Column(DateTime(True))
    migration_name = Column(String(255), nullable=False)
    logs = Column(Text)
    rolled_back_at = Column(DateTime(True))
    started_at = Column(DateTime(True), nullable=False, server_default=text("now()"))
    applied_steps_count = Column(Integer, nullable=False, server_default=text("0"))


class Quiz(Base):
    __tablename__ = 'Quiz'

    id = Column(Text, primary_key=True)
    categoryId = Column(ForeignKey('Category.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    proficiencyId = Column(ForeignKey('Proficiency.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

    Category = relationship('Category')
    Proficiency = relationship('Proficiency')


class Task(Base):
    __tablename__ = 'Task'

    id = Column(Text, primary_key=True)
    problem = Column(Text, nullable=False)
    categoryId = Column(ForeignKey('Category.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    proficiencyId = Column(ForeignKey('Proficiency.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    answer = Column(ForeignKey('Resource.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    options = Column(ForeignKey('TaskChoice.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    type = Column(Text, nullable=False)

    Resource = relationship('Resource')
    Category = relationship('Category')
    TaskChoice = relationship('TaskChoice')
    Proficiency = relationship('Proficiency')


class User(Base):
    __tablename__ = 'User'

    id = Column(Text, primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    username = Column(Text)
    age = Column(Integer, nullable=False)
    nationality = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    dateCreated = Column(TIMESTAMP(precision=3), server_default=text("CURRENT_TIMESTAMP"))
    proficiencyId = Column(ForeignKey('Proficiency.id', ondelete='SET NULL', onupdate='CASCADE'))

    Proficiency = relationship('Proficiency')


t__ResourceToTaskChoice = Table(
    '_ResourceToTaskChoice', metadata,
    Column('A', ForeignKey('Resource.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    Column('B', ForeignKey('TaskChoice.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    Index('_ResourceToTaskChoice_AB_unique', 'A', 'B', unique=True)
)


class CategoryActivity(Base):
    __tablename__ = 'CategoryActivity'

    id = Column(Text, primary_key=True)
    taskId = Column(ForeignKey('Task.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    categoryId = Column(ForeignKey('Category.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

    Category = relationship('Category')
    Task = relationship('Task')


class CompletedCategory(Base):
    __tablename__ = 'CompletedCategory'

    id = Column(Text, primary_key=True)
    userId = Column(ForeignKey('User.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    categoryId = Column(ForeignKey('Category.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    score = Column(Integer, nullable=False)
    dateStarted = Column(TIMESTAMP(precision=3), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dateCompleted = Column(TIMESTAMP(precision=3), nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    Category = relationship('Category')
    User = relationship('User')


class CompletedQuiz(Base):
    __tablename__ = 'CompletedQuiz'

    id = Column(Text, primary_key=True)
    score = Column(Integer, nullable=False)
    dateStarted = Column(TIMESTAMP(precision=3), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    dateCompleted = Column(TIMESTAMP(precision=3), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    userId = Column(ForeignKey('User.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    quizId = Column(ForeignKey('Quiz.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

    Quiz = relationship('Quiz')
    User = relationship('User')


class DailyChallenge(Base):
    __tablename__ = 'DailyChallenge'

    id = Column(Text, primary_key=True)
    taskId = Column(ForeignKey('Task.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, unique=True)
    dayOrder = Column(Integer, nullable=False)

    Task = relationship('Task')


class QuizQuestion(Base):
    __tablename__ = 'QuizQuestion'

    id = Column(Text, primary_key=True)
    taskId = Column(ForeignKey('Task.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    quizId = Column(ForeignKey('Quiz.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    questionOrder = Column(Integer, nullable=False)

    Quiz = relationship('Quiz')
    Task = relationship('Task')


class CompletedChallenge(Base):
    __tablename__ = 'CompletedChallenge'

    id = Column(Text, primary_key=True)
    dateCompleted = Column(TIMESTAMP(precision=3), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    score = Column(Integer, nullable=False)
    userId = Column(ForeignKey('User.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    dailyChallengeId = Column(ForeignKey('DailyChallenge.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)

    DailyChallenge = relationship('DailyChallenge')
    User = relationship('User')
