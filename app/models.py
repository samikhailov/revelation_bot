from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, create_engine, UniqueConstraint
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import settings


Base = declarative_base()


def get_session():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


user_answer_table = Table(
    "user_answer",
    Base.metadata,
    Column("user", Integer, ForeignKey("user.id")),
    Column("answer", Integer, ForeignKey("answer.id")),
)


class User(Base):
    """Модель данных пользователя"""

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_answers = relationship("Answer", backref="user")
    watched_answers = relationship("Answer", secondary=user_answer_table, back_populates="users_watched")
    last_question_id = Column(Integer, ForeignKey("question.id"))

    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("telegram_id"),)

    def __repr__(self):
        return "<User model - id: {}, telegram_id: {}>".format(self.id, self.telegram_id)


class Question(Base):
    """Модель данных вопроса"""

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    answers = relationship("Answer", backref="question")
    waiting_answer_for_user = relationship("User", backref="last_question")

    __tablename__ = "question"
    __table_args__ = (UniqueConstraint("title"),)

    def __repr__(self):
        return "<Question model - id: {}, title: {}>".format(self.id, self.title)


class Answer(Base):
    """Модель данных ответов на вопросы"""

    id = Column(Integer, primary_key=True)
    file_id = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    users_watched = relationship("User", secondary=user_answer_table, back_populates="watched_answers")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __tablename__ = "answer"
    __table_args__ = (
        UniqueConstraint("file_id"),
        UniqueConstraint("question_id", "user_id"),
    )

    def __repr__(self):
        return "<Answer model {}>".format(self.id)


if __name__ == "__main__":
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(engine)
