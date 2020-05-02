import random
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import settings
import templates
from models import User, Question, Answer, get_session


def start(update, context):
    session = get_session()
    user = session.query(User).filter(User.telegram_id == update.message.chat.id).first()
    if user is None:
        session.add(User(telegram_id=update.message.chat.id))
        session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id, text=templates.start)


def question(update, context):
    session = get_session()
    user = session.query(User).filter(User.telegram_id == update.message.chat.id).first()
    all_questions = session.query(Question).all()
    relevant_questions = set(all_questions) - set([answer.question for answer in user.created_answers])
    if relevant_questions != set():
        question = random.choice(tuple(relevant_questions))
        user.last_question_id = question.id
        session.commit()
        context.bot.send_message(chat_id=user.telegram_id, text=templates.question_exists.format(question.title))
    else:
        context.bot.send_message(chat_id=user.telegram_id, text=templates.question_does_not_exists)


def answer(update, context):
    session = get_session()
    user = session.query(User).filter(User.telegram_id == update.message.chat.id).first()
    all_answers = session.query(Answer).all()
    relevant_answers = set(all_answers) - set(user.watched_answers)
    if relevant_answers != set():
        answer = random.choice(tuple(relevant_answers))
        user.watched_answers.append(answer)
        session.commit()
        context.bot.send_message(chat_id=user.telegram_id, text=answer.question.title)
        context.bot.send_voice(chat_id=user.telegram_id, voice=answer.file_id)
        context.bot.send_message(chat_id=user.telegram_id, text=templates.answer_positive)
    else:
        context.bot.send_message(chat_id=user.telegram_id, text=templates.answer_negative)


def voice(update, context):
    session = get_session()
    user = session.query(User).filter(User.telegram_id == update.message.chat.id).first()
    if user.last_question_id is not None:
        answer = Answer(file_id=update.message.voice.file_id, question_id=user.last_question_id, user_id=user.id)
        session.add(answer)
        user.last_question_id = None
        user.watched_answers.append(answer)
        session.commit()
        context.bot.send_message(chat_id=user.telegram_id, text=templates.voice_last_question_is_not_none)
    else:
        context.bot.send_message(chat_id=user.telegram_id, text=templates.voice_last_question_is_none)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    updater = Updater(token=settings.TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("question", question))
    dp.add_handler(CommandHandler("story", answer))
    dp.add_handler(MessageHandler(Filters.voice, voice))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
