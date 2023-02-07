from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, Bot
from .buttons import *
from .models import Log, User
from .services import get_videos
from .tgadmin import TGAdmin, rek_video, rek_rasm, admin_inline_handler


def my_decorator_func(func):
    def wrapper_func(update, context):
        try:
            user_id = update.callback_query.from_user.id
        except AttributeError:
            user_id = update.message.from_user.id
        else:
            print("Vapshe dabdala xatolik")
        dostup = [727652365]
        if user_id in dostup:
            func(update, context)
            return 0
        my_channel_id = ['@fintechhubuz', '@fintech_jobs']
        statuss = ['creator', 'administrator', 'member']
        # if user_id == ""
        for j in my_channel_id:
            for i in statuss:
                if i == context.bot.get_chat_member(chat_id=j, user_id=user_id).status:
                    break
            else:
                context.bot.send_message(user_id,
                                         "Assalomu Alaykum FintechHub tekin video kurslar botiga xush kelibsiz 👨🏻‍💻\n\nQuydagi kanalarga obuna bo'ling va 👉/start bosing",
                                         reply_markup=inline_btns("reklama"))
                return False
        func(update, context)

    return wrapper_func


@my_decorator_func
def start(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    tg_user = User.objects.filter(user_id=user.id).first()

    if not tglog:
        tglog = Log()
        tglog.user_id = user.id
        tglog.messages = {"state": 0}
        tglog.save()

    log = tglog.messages
    if not tg_user:
        tg_user = User()
        tg_user.user_id = user.id
        tg_user.user_name = user.username
        tg_user.first_name = user.first_name
        tg_user.save()
    else:
        if tg_user.menu == 1:
            log.clear()
            log['admin_state'] = 1
            tglog.messages = log
            tglog.save()
            TGAdmin(update, context)
            return 0
    tg_user.menu_log = 0
    tg_user.save()
    log.clear()
    log['state'] = 0
    tglog.messages = log
    tglog.save()

    if not tg_user:
        update.message.reply_html("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
    else:
        update.message.reply_html("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))

    tglog.messages = log
    tglog.save()


# def ctg_id(msg):
#     r = requests.get('https://eduon-backend.uz/api/v1/courses/categories/')
#     data = r.json()
#     print(">>>", msg)
#     for i in data:
#         if i['name'] == msg:
#             return i['id']


# def get_sub_id(sub):
#     url = "https://eduon-backend.uz/api/v1/courses/subcategories/"
#     response = requests.get(url).json()
#     for i in response:
#         if i['name'] == sub:
#             return i

def photo_handler(update, context):
    user = update.message.from_user
    tg_user = User.objects.filter(user_id=user.id).first()
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    state = log.get('state', 0)
    astate = log.get('admin_state', 0)
    if astate == 100:
        rek_rasm(update, context)
        return 0


def video_handler(update, context):
    user = update.message.from_user
    video = update.message.video
    tg_user = User.objects.filter(user_id=user.id).first()
    print(update.message.message_id, user.id)

    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    state = log.get('state', 0)
    astate = log.get('admin_state', 0)
    print("state:", state, "astatte", astate)
    if astate == 100:
        rek_video(update, context)
        return 0
    elif astate == 702:
        rek_video(update, context)
        return 0
    elif astate == 708:
        rek_video(update, context)
        return 0


def message_handler(update: Update, context: CallbackContext):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    msg = update.message.text
    state = log.get('state', 0)
    print(log, state)

    if tg_user.menu == 1:
        TGAdmin(update, context)
        return 0

    if msg == "/adm1NF1nTech22":
        update.message.reply_text('Parolni kiriting')
        log['admin_state'] = 0
        tglog.messages = log
        tglog.save()
        return 0

    if msg == "🔝 Bosh Menu":
        log['state'] = 1
        update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
        return 0

    if msg == "Statistika 📊":
        users = User.objects.all()
        update.message.reply_text(f"🧑🏻‍💻 Botdagi obunachilar: {len(users)} ta\n"
                                  f"Bot 07.01.2023 dan faoliyatda\n\n"
                                  f"📊 @ITresursbot statistikasi")
        return 0

    if msg == "🔙 Orqaga":
        if log['state'] == 2:
            log['state'] = 1
            update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
            tglog.messages = log
            tglog.save()
            return 0

        elif state == 6:
            log['state'] = 1
            update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
            tglog.messages = log
            tglog.save()
            return 0

        elif log['state'] == 1:
            update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
            tglog.messages = log
            tglog.save()
            return 0

        # elif log['state'] == 10:
        #     log['state'] = 9
        #     update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns('manu1'))
        #     tglog.messages = log
        #     tglog.save()
        #     return 0

        elif log['state'] == 9:
            log['state'] = 1
            update.message.reply_text("Kurslar bo'limiga xush kelibsiz", reply_markup=btns("manu1"))
            tglog.messages = log
            tglog.save()
            return 0

        elif log['state'] == 14:
            markup = btns('course', ctg=log.get('course'))
            subbtn = btns('subfree', sub=log.get('sub'))
            if subbtn.keyboard:
                log['state'] = 13
                update.message.reply_text("Darslikni yuklab olish uchun o'zingizga tegishli modulni tanlang 👇",
                                          reply_markup=subbtn)
                tglog.messages = log
                tglog.save()
                return 0
            log['state'] = 12
            update.message.reply_text("Quydagi modullardan birini tanlang 👇", reply_markup=markup, )
            tglog.messages = log
            tglog.save()
            return 0

        elif log['state'] == 12:
            log['state'] = 10
            update.message.reply_text("Kurs yo'nalishini tanlang 👇", reply_markup=btns('manu1'))
            tglog.messages = log
            tglog.save()
            return 0

        elif log['state'] == 10:
            update.message.reply_text("Kurs yo'nalishini tanlang 👇", reply_markup=btns('ctgs'))
            log['state'] = 6
            tglog.messages = log
            tglog.save()
            return 0

        elif log['state'] == 13:
            markup = btns('course', ctg=log.get('course'))
            log['state'] = 12
            update.message.reply_text("Quydagi modullardan birini tanlang 👇", reply_markup=markup)
            tglog.messages = log
            tglog.save()
            return 0

    elif msg == "Biz bilan bog'lanish 📞":
        update.message.reply_html("🙎🏻‍♂️ Savol va takliflar bo'yicha :\n "
                                  "@NizomiddinHusniddinov")
        return 0

    if log.get('admin_state') == 0:
        if msg == "F1nTech2022":
            tg_user.menu = 1
            tg_user.save()
            log.clear()
            log['admin_state'] = 1
            tglog.messages = log
            tglog.save()
            # update.message.reply_text("Admin bo'limiga xush kelibsiz")
            TGAdmin(update, context)
            return 0
        else:
            update.message.reply_text("Parolni notog'ri kiridingiz")
            return 0
    else:
        if msg == "Kurslar 👨🏻‍💻":
            log['state'] = 5
            log['state'] = 6
            update.message.reply_text("Kurs yo'nalishini tanlang 👇", reply_markup=btns('ctgs'))
            print(log, state)

        elif state == 6:
            markup = btns('coursee', ctg=msg)

            log['coursee'] = msg
            if not markup:
                log['state'] = 6
                update.message.reply_text("Uzur hozircha bu Kategoriyaga oid hech qanday kurs topilmadi🤷‍️")
            else:
                log['state'] = 10
                update.message.reply_text("Quydagi modullardan birini tanlang 👇", reply_markup=markup)

        elif state == 10:
            markup = btns('course', ctg=msg)

            log['course'] = msg
            if not markup:
                log['state'] = 10
                update.message.reply_text("Uzur hozircha bu Kategoriyaga oid hech qanday kurs topilmadi🤷‍️")
            else:
                log['state'] = 12
                update.message.reply_text("Quydagi modullardan birini tanlang 👇", reply_markup=markup)

        elif state == 12:
            log['sub'] = msg
            markup = btns('subfree', sub=msg)
            if not markup:
                log['state'] = 12
                update.message.reply_text("Uzur hozircha bu Kursga oid videolar topilmadi 🤷‍")
            else:
                log['state'] = 13
                update.message.reply_text("Darslikni yuklab olish uchun o'zingizga tegishli modulni tanlang 👇",
                                          reply_markup=markup)
        elif state == 13:
            log['videos'] = msg

            print("Bu yerda qanaqa video keladi", msg)
            teacher = Course.objects.filter(name=log.get('sub', None)).first()
            print(teacher, log)
            if not teacher:
                update.message.reply_text("Qandaydir xatolik")
                return 0

            markup = btns('video_name', video=msg, teacher_id=teacher.id)
            print(markup)
            if not markup.keyboard:
                log['state'] = 13
                update.message.reply_text("Uzur hozircha bu Kursga oid videolar topilmadi 🤷‍")
            else:
                log['state'] = 14
                update.message.reply_text("Darsliklardan birini tanlang 👇", reply_markup=markup)

        elif state == 14:
            teacher = Course.objects.filter(name=log.get('sub', None)).first()
            print(teacher, log)
            if not teacher:
                update.message.reply_text("Qandaydir xatolik")
                return 0

            videos = get_videos(log['videos'], name=msg, teacher=teacher.id)
            print(videos)
            if not videos:
                update.message.reply_text("Hozircha video darsliklar topilmadi 🤷‍")
            else:
                # update.message.reply_text(f"Sz qidirgan {msg} bo'yicha {len(videos)} ta element topildi.")
                # update.message.reply_text(f"Videolarni yuklash jarayoni ketmoqda bu ozgina vaqt olishi "
                #                           f"mumkin.oqulaylik uchun oldindan uzur so'raymiz")
                for i in videos:
                    print(i["chat_id"], i['video'])
                    context.bot.forward_message(chat_id=5392556467, from_chat_id=i['chat_id'],
                                                message_id=i['video']).copy(user.id)

        tglog.messages = log
        tglog.save()


def inline_handler(update, context):
    query = update.callback_query
    user = query.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    state = log.get('admin_state', 0)
    print(log, state)

    if tg_user.menu == 1:
        admin_inline_handler(update, context)
        return 0

    tglog.messages = log
    tglog.save()
