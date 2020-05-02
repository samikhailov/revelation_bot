from models import User, Question, Answer, get_session


session = get_session()

users = [
    User(telegram_id=141920453),
    User(telegram_id=141920454),
    User(telegram_id=141920455),
    User(telegram_id=141920456),
]
session.add_all(users)
session.commit()

questions = [
    Question(title="Как дела?"),
    Question(title="Чем занимаешься?"),
    Question(title="Как настроени?"),
    Question(title="Как ты?"),
]
session.add_all(questions)
session.commit()

user_1 = session.query(User).get(1)
question = session.query(Question).get(1)

answers = [
    Answer(
        file_id="AwACAgIAAxkBAAOhXqyuJj5KuqinKpo0_YR38osaAAFDAAJwBgAClftpScrlVXUbG-RwGQQ",
        question_id=question.id,
        user_id=user_1.id,
    ),
]
session.add_all(answers)
session.commit()

user_2 = session.query(User).get(2)
answers = [
    Answer(
        file_id="AwACAgIAAxkBAANuXqykOBYnAAF3ZMVusyb3DctyBkR_AAJoBgAClftpSVz2L4alV9FAGQQ",
        question_id=1,
        user_id=user_2.id,
    ),
    Answer(
        file_id="AwACAgIAAxkBAAN4XqynaKdoFZCCNtdw6yDl0N0WrEoAAmsGAAKV-2lJYaf0SIYSl-EZBA",
        question_id=2,
        user_id=user_2.id,
    ),
    Answer(
        file_id="AwACAgIAAxkBAAN-Xqyoi7mZIh1VmjoLD1d6RMn-AQIAAm0GAAKV-2lJLdTg182EnLMZBA",
        question_id=3,
        user_id=user_2.id,
    ),
    Answer(
        file_id="AwACAgIAAxkBAAObXqyuCZfLZJmAl9bBMSHOpAwDv60AAm8GAAKV-2lJeBFmIOTeKUAZBA",
        question_id=4,
        user_id=user_2.id,
    ),
]
session.add_all(answers)
session.commit()
