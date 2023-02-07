from telegram_bot.buttons import admin_btn, admin_inline_btn, btns_add_ctg
from telegram_bot.models import Log, User, Category, Sub, Course, Videos, Categoryy
from telegram_bot.video_btn_admin import video_btn, video_pag, video_inline_btn
from telegram_bot.views import btns


def tg_paginate(update, context, page=1, key=True, tur='ctg'):
    if tur == 'sub':
        ctg = Course.objects.all().order_by("-pk")
    elif tur == 'ctgss':
        ctg = Categoryy.objects.all().order_by("-pk")
    else:
        ctg = Category.objects.all().order_by("-pk")

    if len(ctg) == 0:
        update.message.reply_text("Bu bo'limda hech narsa topilmadi")
        return 0

    if page > len(ctg):
        context.bot.answer_callback_query(update.id, "Bundan keyin kurs yo'q ekan 🥲")
        return 0
    if page < 1:
        context.bot.answer_callback_query(update.id, "Bundan keyin kurs yo'q ekan 🥲")
        return 0

    if key:
        print(ctg)
        for i in range(page - 1, page):

            strr = f"Name: {ctg[i].name}"
            if tur == 'sub':
                strr += f'\nCategory: {ctg[i].ctg.name}'

            update.message.edit_text(strr,
                                     reply_markup=admin_inline_btn("pagination_ctg",
                                                                   len=len(ctg),
                                                                   ctg=ctg[i],
                                                                   tur=tur,
                                                                   page=page))
    else:
        for i in range(page - 1, page):
            update.message.delete()
            strr = f"Name: {ctg[i].name}"
            if tur == 'sub':
                strr += f'\nCategory: {ctg[i].ctg.name}'
            update.message.reply_text(strr,
                                      reply_markup=admin_inline_btn("pagination_ctg",
                                                                    len=len(ctg),
                                                                    ctg=ctg[i],
                                                                    tur=tur,
                                                                    page=page))


def TGAdmin(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    msg = update.message.text
    state = log.get('admin_state', 0)

    if msg == "Bo'lim":
        log['admin_state'] = 2
        update.message.reply_text("Quyidagilardan birini tanlang 👇", reply_markup=btns_add_ctg("ctg"))
        tg_paginate(update, context, key=False)
        tglog.messages = log
        tglog.save()
        # print(state)
        return 0

    elif msg == "Mentor":
        update.message.reply_text("Quyidagilardan birini tanlang 👇", reply_markup=btns_add_ctg("sub"))
        tg_paginate(update, context, key=False, tur="sub")
        log['admin_state'] = 2
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Kategoriya":
        update.message.reply_text("Quyidagilardan birini tanlang 👇", reply_markup=btns_add_ctg("ctgss"))
        tg_paginate(update, context, key=False, tur="ctgss")
        log['admin_state'] = 2
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Video":
        update.message.reply_text("Videoni Faqatgina nomi chiqadi \nVideoni ko'rish uchun oddiy botdan foydalaning 👇",
                                  reply_markup=btns_add_ctg("vid"))
        log['admin_state'] = 2
        video_pag(update, context, key=False, tur="vid")
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Yunalish":
        update.message.reply_text("Quyidagilardan birini tanlang 👇", reply_markup=btns_add_ctg("cur"))
        log['admin_state'] = 2
        video_pag(update, context, key=False, tur="cur")
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Botga qaytish 🏘":
        log.clear()
        log['admin_state'] = 10
        log['state'] = 1
        tg_user.menu = 0
        tg_user.save()
        update.message.reply_text("Menuga xush kelibsiz 👇", reply_markup=btns("manu1"))
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Users 👤":
        users = User.objects.all()
        update.message.reply_text(f"Sizda {len(users)} ta foydalanuvchilar bor")
        log['admin_state'] = 150
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "◀ Orqaga" or msg == "🔙 Orqaga":
        log['admin_state'] = 1
        update.message.reply_text("Admin bo'limiga xush kelibsiz", reply_markup=admin_btn('admin_menu'))
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Reklama yuborish":
        dostup = [5081682094, 886612894, 80413645]
        if user.id in dostup:
            log['admin_state'] = 100
            update.message.reply_text("Reklama uchun post yuboring")
            tglog.messages = log
            tglog.save()
            return 0
        else:
            update.message.reply_text("Kechirasiz sizga ruxsat berilmagan 🫠")
            return 0
    elif state == 1:
        update.message.reply_text("Admin bo'limiga xush kelibsiz", reply_markup=admin_btn('admin_menu'))

    if state == 3:
        try:
            root = Category.objects.get(pk=log.get("edit_ctg_content_id", 0))
            root.name = msg
            root.save()
            tg_paginate(update, context, key=False)
        except:
            update.message.reply_text("Bunday bulim topilmadi")
            return 0

    if msg == "Yangi Bulim qo'shish":
        log['admin_state'] = 12
        update.message.reply_text("Bo'limni qo'shish uchun Categoriya nomini kiriting", reply_markup=btns("ctgs"))
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Yangi Kategoriya qo'shish":
            log['admin_state'] = 170
            update.message.reply_text("Yangi Bo'lim qo'shish uchun nom kiriting")
            tglog.messages = log
            tglog.save()
            return 0

    elif msg == "Yangi Mentor qo'shish":
        log['admin_state'] = 500
        update.message.reply_text("Mentor qo'shish uchun Bo'lim tanlang tanlang", reply_markup=btns("mentor_uchun_ctg"))
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Yangi Video qo'shish":
        log['admin_state'] = "700"
        update.message.reply_text("Video qo'shish uchun Yunalishni tanlang", reply_markup=video_btn("video_tech"))
        tglog.messages = log
        tglog.save()
        return 0

    elif msg == "Yangi Yunalish qo'shish":
        log['admin_state'] = 600
        update.message.reply_text("Video qo'shish uchun Mentor tanlang", reply_markup=video_btn("course"))
        tglog.messages = log
        tglog.save()
        return 0

    elif state == 100:
        log['admin_state'] = 101
        log['message_id'] = update.message.message_id
        update.message.reply_text(msg, reply_markup=admin_btn("conf"))
        update.message.reply_text("Shu reklamani jo'natamizmi 🧐")
    elif state == 101:

        if msg == "Ha":
            print(log)
            for i in User.objects.all():
                try:
                    context.bot.forward_message(
                        chat_id=5392556467,
                        message_id=log['message_id'],
                        from_chat_id=user.id
                    ).copy(i.user_id)
                except Exception as e:
                    print(e)
                    update.message.reply_text(
                        f" ID: {i.user_id} Username: ({i.user_name}) 👈 mana shu userlaga reklamani yuborib bo'lmadi")
            log['admin_state'] = 1
            update.message.reply_text("Reklama barcha foydalanuvchilarga jo'natildi",
                                      reply_markup=admin_btn('admin_menu'))
        else:
            log['admin_state'] = 100
            update.message.reply_text("Reklama uchun post yuboring")
            tglog.messages = log
            tglog.save()
            return 0
    elif state == 500:
        ctg = Category.objects.filter(name=msg).first()
        if not ctg:
            update.message.reply_text("Bizda bunday ctg yo'q")
            return 0
        log['curs_ctg'] = ctg.id
        update.message.reply_text("Mentor qo'shish uchun nomini kiriting!", )
        log['admin_state'] = 501
    elif state == 501:
        if msg == "Ha":
            log['admin_state'] = 1
            root = Course()
            root.name = log["acourse"]
            root.ctg_id = log["curs_ctg"]
            root.save()
            update.message.reply_text("Course qo'shilidi ✅", reply_markup=admin_btn('admin_menu'))
        elif msg == "Yo'q":
            log['admin_state'] = 1
            update.message.reply_text("Course qo'shilmadi ❌\nEndi nma qilamiz 🧐", reply_markup=admin_btn("admin_menu"))
        else:
            log["acourse"] = msg
            update.message.reply_html(f"Siz rostan ham <b>{msg}</b> Courseni qo'shmoqchimisizmi?",
                                      reply_markup=admin_btn('conf'))
    elif state == 505:
        root = Sub.objects.filter(pk=log['edit_sub_id']).first()
        if not root:
            update.message.reply_text("Sub topilmadi \n/start")
        root.name = msg
        root.save()
        video_pag(update, context, key=False, tur="cur")

    elif state == 600:
        ctg = Course.objects.filter(name=msg).first()
        if not ctg:
            update.message.reply_text("Bizda bunaqa Course yo'q")
            return 0
        log['curs_video'] = ctg.id
        update.message.reply_text("Yunalish qo'shish uchun Nom kiriting!", )
        log['admin_state'] = 601
    elif state == 601:
        if msg == "Ha":
            log['admin_state'] = 1
            root = Sub()
            root.name = log["acourse"]
            root.course_id = log["curs_video"]
            root.save()
            update.message.reply_text("Yunalish qo'shilidi ✅", reply_markup=admin_btn('admin_menu'))
        elif msg == "Yo'q":
            log['admin_state'] = 1
            update.message.reply_text("Yunalish qo'shilmadi ❌\nEndi nma qilamiz 🧐",
                                      reply_markup=admin_btn("admin_menu"))
        else:
            log["acourse"] = msg
            update.message.reply_html(f"Siz rostan ham <b>{msg}</b> Yunalishni qo'shmoqchimisizmi?",
                                      reply_markup=admin_btn("conf"))
    elif state == 170:
        if msg == "Ha":
            if "categoryy_change_id" in log:
                root = Categoryy.objects.get(pk=log["categoryy_change_id"])
                root.name = log['ctgsss']
                root.save()
                log.clear()
                log['admin_state'] = 1
                update.message.reply_text("Kategoriya o'zgartirildi ✅", reply_markup=admin_btn('admin_menu'))

                tglog.messages = log
                tglog.save()
                return 0

            log['admin_state'] = 1
            root = Categoryy()
            root.name = log["ctgsss"]
            root.save()
            update.message.reply_text("Kategoriya qo'shilidi ✅", reply_markup=admin_btn('admin_menu'))
        elif msg == "Yo'q":
            log['admin_state'] = 1
            update.message.reply_text("Kategoriya qo'shilmadi ❌\nEndi nma qilamiz 🧐",
                                      reply_markup=admin_btn("admin_menu"))
        else:
            log["ctgsss"] = msg
            update.message.reply_html(f"Siz rostan ham <b>{msg}</b> Kategoriyasini qo'shmoqchimisizmi?",
                                      reply_markup=admin_btn("conf"))
    elif state == 605:
        root = Course.objects.filter(pk=log['edit_course_id']).first()
        if not root:
            update.message.reply_text("Course topilmadi \n/start")
        root.name = msg
        root.save()
        tg_paginate(update, context, key=False, tur="sub")
        print('a')

    elif state == "700":
        ctg = Course.objects.filter(name=msg).first()
        if not ctg:
            update.message.reply_text("Bizda bunaqa O'qituvchi yo'q")
            return 0
        log['curs_id'] = ctg.id
        log['curs_name'] = ctg.name
        update.message.reply_text("Video qo'shish uchun Yunalishni tanlang!",
                                  reply_markup=video_btn('videos',
                                                         teacher_id=ctg.id
                                                         ))
        log['admin_state'] = 700

    elif state == 700:
        ctg = Sub.objects.filter(name=msg, course_id=log['curs_id']).first()
        if not ctg:
            update.message.reply_text("Bizda bunaqa Yunalish yo'q")
            return 0
        log['sub_video_id'] = ctg.id
        log['sub_video_name'] = ctg.name
        update.message.reply_text("Video qo'shish uchun Nom kiriting!", )
        log['admin_state'] = 701

    elif state == 701:
        log['VideoName'] = msg
        update.message.reply_text("❗❗❗Diqqat yubormoqchi bo'gan videoingizni"
                                  " uchbu chatdan hech qachon o'chirib tashamang aks holda botda xatoliklar bo'lib "
                                  "qo'lishi mumkin")
        update.message.reply_text("Qo'shmoqchi bo'gan videoingizni yuboring!")
        log['admin_state'] = 702

    elif state == 702:
        if msg == "Ha":
            log['admin_state'] = 1
            print(log)
            root = Videos()
            root.name = log['VideoName']
            root.sub_id = log['sub_video_id']
            root.video = log['video_msg_id']
            root.chat_id = user.id
            root.save()
            print(root)
            update.message.reply_text("Video qo'shilidi ✅\nKo'rish uchun Oddiy botdan foydalaning",
                                      reply_markup=admin_btn('admin_menu'))
        elif msg == "Yo'q":
            log['admin_state'] = 1
            update.message.reply_text("Yunalish qo'shilmadi ❌\nEndi nma qilamiz 🧐",
                                      reply_markup=admin_btn("admin_menu"))
        else:
            update.message.reply_text("Faqat Ha yoki Yo'q tugmalaridan birini bosing")
    elif state == 705:
        root = Videos.objects.filter(pk=log['edit_video_id']).first()
        if not root:
            update.message.reply_text("video topilmadi \n/start")
        root.name = msg
        root.save()
        video_pag(update, context, key=False, tur='vid')

    elif state == 12:
        parent = Categoryy.objects.filter(name=msg).first()
        if not parent:
            update.message.reply_text("Bratishka aldama")
            return 0

        log['ParentCtg'] = msg
        log['admin_state'] = "12"
        update.message.reply_text("Yangi Bo'lim uchun Nom kiriting!")

    elif state == "12":
        if msg == "Ha":
            log['admin_state'] = 1
            root = Category()
            root.name = log['actg']
            root.ctg = Categoryy.objects.filter(name=log['ParentCtg']).first()
            root.save()
            update.message.reply_text("Bo'lim qo'shilidi ✅", reply_markup=admin_btn('admin_menu'))
        elif msg == "Yo'q":
            log['admin_state'] = 1
            update.message.reply_text("Bo'lim qo'shilmadi ❌\nEndi nma qilamiz 🧐",
                                      reply_markup=admin_btn("admin_menu"))
        else:
            log['actg'] = msg
            update.message.reply_html(f"Siz rostan ham <b>{msg}</b> bo'limini qo'shmoqchimisizmi?",
                                      reply_markup=admin_btn('conf'))

    tglog.messages = log
    tglog.save()
    return 0


def admin_inline_handler(update, context):
    query = update.callback_query
    user = query.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    state = log.get('admin_state', 0)

    data_sp = query.data.split('_')
    print("qwer", data_sp)
    if data_sp[0] == 'next':
        page = int(data_sp[-1]) + 1
        if data_sp[1] == 'sub' or data_sp[1] == 'ctg' or data_sp[1] == 'ctgss':
            tg_paginate(query, context, page=page, tur=data_sp[1])
        else:
            video_pag(query, context, page=page, tur=data_sp[1])
    elif data_sp[0] == 'prev':
        page = int(data_sp[-1]) - 1
        if data_sp[1] == 'sub' or data_sp[1] == 'ctg' or data_sp[1] == 'ctgss':
            tg_paginate(query, context, page=page, tur=data_sp[1])
        else:
            video_pag(query, context, page=page, tur=data_sp[1])

    elif data_sp[0] == 'del':

        if data_sp[0] == 'del' and data_sp[-1] == "ha":
            if data_sp[-2] == "sub":
                Course.objects.get(pk=data_sp[1]).delete()
                query.message.reply_text("Course o'chirildi!\nEndi nma qilamiz 😌")
                query.message.delete()
            elif data_sp[-2] == "cur":
                Sub.objects.get(pk=data_sp[1]).delete()
                query.message.reply_text("Yunalish o'chirildi!\nEndi nma qilamiz 😌")
                video_pag(query, context, tur=data_sp[-2])
                return 0
            elif data_sp[-2] == "ctgss":
                Categoryy.objects.get(pk=data_sp[1]).delete()
                query.message.reply_text("Kategoriya o'chirildi!\nEndi nma qilamiz 😌")
                query.message.delete()
                return 0
            elif data_sp[-2] == "vid":
                Videos.objects.get(pk=data_sp[1]).delete()
                query.message.reply_text("Video o'chirildi!\nEndi nma qilamiz 😌")
                video_pag(query, context, tur=data_sp[-2])
                query.message.delete()
                return 0
            elif data_sp[-2] == "ctg":
                Category.objects.get(pk=data_sp[1]).delete()
                query.message.reply_text("Bo'lim o'chirildi!\nEndi nma qilamiz 😌")
                query.message.delete()
            try:
                tg_paginate(query, context, tur=data_sp[-2])
            except:
                tg_paginate(query, context, tur='ctg')
        elif data_sp[0] == 'del' and data_sp[-1] == "no":

            if data_sp[-2] == "vid" or data_sp[-2] == 'cur':
                video_pag(query, context, tur=data_sp[-2])
                return 0
            try:
                tg_paginate(query, context, tur=data_sp[-2])
            except:
                tg_paginate(query, context, tur='ctg')

        elif data_sp[-1] == 'back':

            if data_sp[-2] == "vid" or data_sp[-2] == 'cur':
                video_pag(query, context, tur=data_sp[-2])
                return 0
            try:
                tg_paginate(query, context, tur=data_sp[-2])
            except:
                tg_paginate(query, context, tur='ctg')
        else:
            print("asdfghjk", data_sp)
            if data_sp[2] == "ctg":
                root = Category.objects.get(pk=data_sp[1])
            elif data_sp[2] == "cur":
                root = Sub.objects.get(pk=data_sp[1])
            elif data_sp[2] == "vid":
                root = Videos.objects.get(pk=data_sp[1])
            elif data_sp[2] == "sub":
                root = Course.objects.get(pk=data_sp[1])
            elif data_sp[2] == "ctgss":
                root = Categoryy.objects.get(pk=data_sp[1])
            else:
                query.message.reply_text("Xatolik")
                return 0
            query.message.edit_text(
                text=f"Siz rostan ham <b>{root.name}</b> ni o'chirasizmi 🧐",
                reply_markup=admin_inline_btn("conf", ctg=root, tur=data_sp[2]),
                parse_mode="HTML"
            )

    elif data_sp[0] == "edit":
        if data_sp[2] == "ctg":
            if data_sp[-1] == "name":
                root = Category.objects.get(pk=data_sp[1])
                log['admin_state'] = 3
                log['edit_ctg_content_id'] = root.id
                query.message.reply_html(
                    f"Siz 👉 <b>{root.name}</b> bulimni o'zgartirmoqchisiz. Yangi nom kiriting !!!")
                tglog.messages = log
                tglog.save()

            elif data_sp[-1] == 'back':

                if data_sp[-2] == "vid" or data_sp[-2] == "cur":
                    video_pag(query, context, tur=data_sp[-2])
                    return 0
                tg_paginate(query, context, key=True)
            else:
                root = Category.objects.get(pk=data_sp[1])
                query.message.edit_text(
                    text=f"<b>{root.name}</b>ni o'zgartiramiz?",
                    reply_markup=admin_inline_btn("ctg_edit", ctg=root),
                    parse_mode="HTML"
                )
        elif data_sp[2] == "ctgss":

            root = Categoryy.objects.get(pk=data_sp[1])
            log['admin_state'] = 170
            log['categoryy_change_id'] = root.id
            query.message.delete()
            query.message.reply_html(
                f"Kategoriyani o'zgartirish uchun nom kiriting!!!!!")
            tglog.messages = log
            tglog.save()
            return 0

        elif data_sp[2] == "vid":
            if data_sp[-1] == "name":
                root = Videos.objects.get(pk=data_sp[1])
                log['admin_state'] = 705
                log['edit_video_id'] = root.id
                query.message.reply_html(
                    f"Siz 👉 <b>{root.name}</b> Video o'zgartirmoqchisiz. Yangi nom kiriting !!!")
                tglog.messages = log
                tglog.save()

            elif data_sp[-1] == 'back':
                video_pag(query, context, tur=data_sp[2])

            elif data_sp[-1] == "video":
                root = Videos.objects.get(pk=data_sp[1])
                log['admin_state'] = 708
                log['edit_video_id'] = root.id
                query.message.reply_html(
                    f"Siz 👉 <b>{root.name}</b> Video o'zgartirish uchun. Yangi video  kiriting !!!")
                tglog.messages = log
                tglog.save()
            else:
                root = Videos.objects.get(pk=data_sp[1])
                query.message.edit_text(
                    text=f"<b>{root.name}</b>ni o'zgartiramiz?",
                    reply_markup=video_inline_btn("vid", root=root, tur=data_sp[2]),
                    parse_mode="HTML"
                )

        elif data_sp[2] == "sub":
            if data_sp[-1] == "name":
                root = Course.objects.get(pk=data_sp[1])
                log['admin_state'] = 605
                log['edit_course_id'] = root.id
                query.message.reply_html(
                    f"Siz 👉 <b>{root.name}</b> Course o'zgartirmoqchisiz. Yangi nom kiriting !!!")
                tglog.messages = log
                tglog.save()
                print("b")
            elif data_sp[-1] == 'back':
                tg_paginate(query, context, tur="sub")
            else:
                root = Course.objects.get(pk=data_sp[1])
                query.message.edit_text(
                    text=f"<b>{root.name}</b>ni o'zgartiramizmi?",
                    reply_markup=admin_inline_btn("ctg_edit", ctg=root, tur=data_sp[2]),
                    parse_mode="HTML"
                )

        elif data_sp[2] == "cur":
            if data_sp[-1] == "name":
                root = Sub.objects.get(pk=data_sp[1])
                log['admin_state'] = 505
                log['edit_sub_id'] = root.id
                query.message.reply_html(
                    f"Siz 👉 <b>{root.name}</b> Yunalishini o'zgartirmoqchisiz. Yangi nom kiriting !!!")
                tglog.messages = log
                tglog.save()
                print("b")
            elif data_sp[-1] == 'back':
                video_pag(query, context, tur="cur")
            else:
                root = Sub.objects.get(pk=data_sp[1])
                query.message.edit_text(
                    text=f"<b>{root.name}</b>ni o'zgartiramizmi?",
                    reply_markup=admin_inline_btn("ctg_edit", ctg=root, tur=data_sp[2]),
                    parse_mode="HTML"
                )

    return 0


def rek_video(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    msg = update.message.video
    state = log.get('admin_state', 0)
    if state == 100:
        log['admin_state'] = 101
        log['message_id'] = update.message.message_id
        context.bot.forward_message(
            chat_id=user.id,
            message_id=update.message.message_id,
            from_chat_id=user.id
        )
        update.message.reply_text("Shu reklamani jo'natamizmi 🧐", reply_markup=admin_btn('conf'))
    elif state == 702:
        log['video_msg_id'] = update.message.message_id
        context.bot.forward_message(
            chat_id=user.id,
            message_id=update.message.message_id,
            from_chat_id=user.id
        )
        update.message.reply_text(f"Siz rostdan ham {log['sub_video_name']} Kursiga shu videoni qo'shmoqchimisz🧐",
                                  reply_markup=admin_btn('conf'))
    elif state == 708:
        root = Videos.objects.filter(pk=log['edit_video_id']).first()
        if not root:
            update.message.reply_text("video topilmadi \n/start")
            return 0
        root.video = update.message.message_id
        root.chat_id = user.id
        root.save()
        video_pag(update, context, key=False, tur='vid', dele=False)

    tglog.messages = log
    tglog.save()
    return 0


def rek_rasm(update, context):
    user = update.message.from_user
    tglog = Log.objects.filter(user_id=user.id).first()
    log = tglog.messages
    tg_user = User.objects.filter(user_id=user.id).first()
    state = log.get('admin_state', 0)

    if state == 100:
        log['admin_state'] = 101
        log['message_id'] = update.message.message_id
        context.bot.forward_message(
            chat_id=user.id,
            message_id=update.message.message_id,
            from_chat_id=user.id
        )
        update.message.reply_text("Shu reklamani jo'natamizmi 🧐", reply_markup=admin_btn('conf'))

    tglog.messages = log
    tglog.save()
    return 0
