from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, UniqueConstraint, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def now(): return datetime.now(timezone.utc)

class Role(Base):
    __tablename__ = 'roles'
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    label: Mapped[str] = mapped_column(String(80))

class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    password_hash: Mapped[str] = mapped_column(String(300))
    role: Mapped[str] = mapped_column(ForeignKey('roles.code'), default='student')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    native_language_id: Mapped[str | None] = mapped_column(ForeignKey('languages.id'), nullable=True)
    target_language_id: Mapped[str | None] = mapped_column(ForeignKey('languages.id'), nullable=True)
    daily_goal: Mapped[int] = mapped_column(Integer, default=15)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)

class Language(Base):
    __tablename__ = 'languages'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    code: Mapped[str] = mapped_column(String(12), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    native_name: Mapped[str] = mapped_column(String(120), default='')
    tts_locale: Mapped[str | None] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, default='')
    flag: Mapped[str] = mapped_column(String(12), default='🌐')
    icon: Mapped[str] = mapped_column(String(40), default='BookOpen')
    color: Mapped[str] = mapped_column(String(16), default='#2563EB')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Level(Base):
    __tablename__ = 'course_levels'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    code: Mapped[str] = mapped_column(String(12), unique=True)
    name: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text, default='')
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    language_id: Mapped[str] = mapped_column(ForeignKey('languages.id', ondelete='RESTRICT'), index=True)
    level_id: Mapped[str] = mapped_column(ForeignKey('course_levels.id', ondelete='RESTRICT'))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default='')
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

class Module(Base):
    __tablename__ = 'modules'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    course_id: Mapped[str] = mapped_column(ForeignKey('courses.id', ondelete='CASCADE'), index=True)
    title: Mapped[str] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (UniqueConstraint('course_id', 'sort_order'),)

class Lesson(Base):
    __tablename__ = 'lessons'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    module_id: Mapped[str] = mapped_column(ForeignKey('modules.id', ondelete='CASCADE'))
    language_id: Mapped[str] = mapped_column(ForeignKey('languages.id', ondelete='RESTRICT'), index=True)
    level_id: Mapped[str] = mapped_column(ForeignKey('course_levels.id', ondelete='RESTRICT'), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default='')
    duration_minutes: Mapped[int] = mapped_column(Integer, default=15)
    lesson_order: Mapped[int] = mapped_column(Integer, default=1)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    video_url: Mapped[str] = mapped_column(Text, default='')
    audio_url: Mapped[str] = mapped_column(Text, default='')
    objectives: Mapped[list] = mapped_column(JSON, default=list)
    content: Mapped[str] = mapped_column(Text, default='')
    grammar_notes: Mapped[str] = mapped_column(Text, default='')
    __table_args__ = (UniqueConstraint('module_id','lesson_order'),)

class Vocabulary(Base):
    __tablename__ = 'vocabulary_items'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'), index=True)
    word: Mapped[str] = mapped_column(String(255))
    translation: Mapped[str] = mapped_column(Text, default='')
    pronunciation: Mapped[str] = mapped_column(String(255), default='')
    example_sentence: Mapped[str] = mapped_column(Text, default='')
    example_translation: Mapped[str] = mapped_column(Text, default='')
    audio_url: Mapped[str] = mapped_column(Text, default='')

class Question(Base):
    __tablename__ = 'quiz_questions'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'), index=True)
    question_text: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str] = mapped_column(Text, default='')
    question_type: Mapped[str] = mapped_column(String(24), default='mcq')
    time_limit_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answer_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)

class Option(Base):
    __tablename__ = 'quiz_options'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    question_id: Mapped[str] = mapped_column(ForeignKey('quiz_questions.id', ondelete='CASCADE'), index=True)
    option_text: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

class Enrollment(Base):
    __tablename__ = 'student_languages'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    language_id: Mapped[str] = mapped_column(ForeignKey('languages.id', ondelete='CASCADE'))
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (UniqueConstraint('user_id','language_id'),)

class Progress(Base):
    __tablename__ = 'lesson_progress'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'))
    status: Mapped[str] = mapped_column(String(30), default='in_progress')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint('user_id','lesson_id'),)

class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'))
    score: Mapped[int] = mapped_column(Integer)
    total_questions: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[int] = mapped_column(Integer)
    passed: Mapped[bool] = mapped_column(Boolean)
    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    answers: Mapped[list] = mapped_column(JSON, default=list)

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'))
    __table_args__ = (UniqueConstraint('user_id', 'lesson_id'),)

class DailyActivity(Base):
    __tablename__ = 'daily_activity'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    day: Mapped[str] = mapped_column(String(10))
    minutes: Mapped[int] = mapped_column(Integer, default=0)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    __table_args__ = (UniqueConstraint('user_id','day'),)

class Achievement(Base):
    __tablename__ = 'achievements'
    code: Mapped[str] = mapped_column(String(40), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))
    threshold: Mapped[int] = mapped_column(Integer, default=1)

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    achievement_code: Mapped[str] = mapped_column(ForeignKey('achievements.code'), primary_key=True)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class CourseEnrollment(Base):
    """Independent student-to-course enrollment; legacy language selections are retained."""
    __tablename__ = 'course_enrollments'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    course_id: Mapped[str] = mapped_column(ForeignKey('courses.id', ondelete='RESTRICT'), index=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    __table_args__ = (UniqueConstraint('user_id', 'course_id'),)

class FlashcardState(Base):
    __tablename__ = 'flashcard_states'
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    vocabulary_id: Mapped[str] = mapped_column(ForeignKey('vocabulary_items.id', ondelete='CASCADE'), primary_key=True)
    state: Mapped[str] = mapped_column(String(12), default='revise')
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    # Nulls on legacy cards deliberately mean "not yet scheduled", not fabricated history.
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    interval_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    repetitions: Mapped[int | None] = mapped_column(Integer, nullable=True)

class QuizSession(Base):
    """One-time quiz ticket; prevents scored attempts being replayed."""
    __tablename__ = 'quiz_sessions'
    id: Mapped[str] = mapped_column(String(70), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    lesson_id: Mapped[str] = mapped_column(ForeignKey('lessons.id', ondelete='CASCADE'))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
