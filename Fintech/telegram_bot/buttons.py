from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import requests
from telegram_bot.models import *
from telegram_bot.services import get_videos


def btns_add_ctg(tur='ctg'):
    tur = 'Mentor' if tur == 'sub' else 'Yunalish' if tur == 'cur' else 'Video' if tur == 'vid' else 'Kategoriya' if tur == "ctgss" else 'Bulim'
    return ReplyKeyboardMarkup([
        [KeyboardButton(f"Yangi {tur} qo'shish")],
        [KeyboardButton("◀ Orqaga")],
    ], resize_keyboard=True)


def btns(type=None, msg="", sub_id=0, page=1, ctg=None, sub=None, video=None, teacher_id=None):
    btn = []

    # - Bepul bo'limi uchun
    if type == "manu1":
        btn = [
            [KeyboardButton("Kurslar 👨🏻‍💻"), KeyboardButton("Biz bilan bog'lanish 📞")],
            [KeyboardButton("Statistika 📊")],
        ]

    elif type == "ctgs":
        btn = []
        ctgs = Categoryy.objects.all()
        for i in range(1, len(ctgs), 2):
            btn.append([
                KeyboardButton(ctgs[i - 1].name), KeyboardButton(ctgs[i].name)
            ])
        if len(ctgs) % 2:
            btn.append([KeyboardButton(ctgs[len(ctgs) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    elif type == "mentor_uchun_ctg":
        btn = []
        ctgs = Category.objects.all()
        for i in range(1, len(ctgs), 2):
            btn.append([
                KeyboardButton(ctgs[i - 1].name), KeyboardButton(ctgs[i].name)
            ])
        if len(ctgs) % 2:
            btn.append([KeyboardButton(ctgs[len(ctgs) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    elif type == "coursee":
        btn = []
        ctgs = Categoryy.objects.filter(name=ctg).first()
        if not ctgs:
            return ReplyKeyboardMarkup([], resize_keyboard=True)

        coursee = Category.objects.filter(ctg=ctgs)
        if not coursee:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        for i in range(1, len(coursee), 2):
            btn.append([
                KeyboardButton(coursee[i - 1].name), KeyboardButton(coursee[i].name)
            ])
        if len(coursee) % 2:
            btn.append([KeyboardButton(coursee[len(coursee) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    elif type == "course":
        btn = []
        ctgs = Category.objects.filter(name=ctg).first()
        if not ctgs:
            return ReplyKeyboardMarkup([], resize_keyboard=True)

        course = Course.objects.filter(ctg=ctgs)
        if not course:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])

        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    elif type == "subfree":
        btn = []
        ctgs = Course.objects.filter(name=sub).first()
        if not ctgs:
            return ReplyKeyboardMarkup([], resize_keyboard=True)
        course = Sub.objects.filter(course=ctgs)

        if not course:
            return []
        for i in range(1, len(course), 2):
            btn.append([
                KeyboardButton(course[i - 1].name), KeyboardButton(course[i].name)
            ])
        if len(course) % 2:
            btn.append([KeyboardButton(course[len(course) - 1].name)])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    elif type == 'video_name':
        videos = get_videos(video, teacher=teacher_id)
        print("\n\n\n", videos, "\n\n\n\n")
        for j in range(len(videos)):
            avj = videos[j].copy()
            buj = videos[j]['name'].replace(" ", "").split("-")
            for k in range(j, len(videos)):
                avk = videos[k].copy()
                buk = videos[k]['name'].replace(" ", "").split("-")
                if int(buk[0]) < int(buj[0]):
                    videos[j], videos[k] = videos[k], videos[j]

        for i in range(1, len(videos), 2):
            btn.append([
                KeyboardButton(videos[i - 1]['name']), KeyboardButton(videos[i]['name']),
            ])

        if len(videos) % 2:
            btn.append([KeyboardButton(videos[- 1]['name'])])
        btn.append([KeyboardButton("🔙 Orqaga"), KeyboardButton("🔝 Bosh Menu")])

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def inline_btn(type, page=1, ctg_id=0, data=None):
    btn = []
    if type == "course":
        if not data:
            return []
        print(page)
        for i in range(page - 1, page):
            print(i)
            btn.append([
                InlineKeyboardButton("🔙 Ortga", callback_data=f"prev_{page}_{ctg_id}"),
                InlineKeyboardButton(f"{page}/{len(data)}", callback_data=f"pass"),
                InlineKeyboardButton("Keyingi 🔜", callback_data=f"next_{page}_{ctg_id}"),
            ])
            btn.append([InlineKeyboardButton("Kursni ko'rish",
                                             url=f"https://eduon.uz/chosenCourse/{data[i]['id']}")])
    return InlineKeyboardMarkup(btn)


def admin_btn(type=None):
    btn = []
    if type == "admin_menu":
        btn = [
            [KeyboardButton("Kategoriya"), KeyboardButton("Bo'lim"), KeyboardButton("Mentor")],
            [KeyboardButton("Yunalish"), KeyboardButton("Video")],
            [KeyboardButton("Reklama yuborish"), KeyboardButton("Users 👤")],
            [KeyboardButton("Botga qaytish 🏘")]
        ]
    elif type == 'conf':
        btn = [
            [KeyboardButton("Ha"), KeyboardButton("Yo'q")]
        ]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def admin_inline_btn(type, tur='ctg', page=1, len=1, ctg=None, video=None):
    btn = []

    if type == "pagination_ctg":
        btn = [
            [InlineKeyboardButton("Edit ⚙", callback_data=f"edit_{ctg.id}_{tur}"),
             InlineKeyboardButton("Delete ❌", callback_data=f"del_{ctg.id}_{tur}")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"prev_{tur}_{page}"),
             InlineKeyboardButton(f"{page}/{len}", callback_data=f"{page}_{ctg.id}"),
             InlineKeyboardButton("Keyingi🔜", callback_data=f"next_{tur}_{page}")]
        ]
    elif type == 'conf':
        btn = [
            [InlineKeyboardButton("Ha ✅", callback_data=f"del_{ctg.id}_{tur}_ha"),
             InlineKeyboardButton("Yo'q ❌", callback_data=f"del_{ctg.id}_{tur}_no")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"del_{ctg.id}_{tur}_back")],

        ]
    elif type == "ctg_edit":
        btn = [
            [InlineKeyboardButton("Edit name", callback_data=f"edit_{ctg.id}_{tur}_name")],
            [InlineKeyboardButton("🔙Orqaga", callback_data=f"edit_{ctg.id}_{tur}_back")],
        ]

    return InlineKeyboardMarkup(btn)


def inline_btns(type=None):
    btn = []
    if type == "reklama":
        btn = [
            [InlineKeyboardButton("FinTech Innovation Hub", callback_data="fintechhubuz",
                                  url="https://t.me/fintechhubuz")],
            [InlineKeyboardButton("Fintech - Jobs", callback_data="fintech_jobs",
                                  url="https://t.me/fintech_jobs")],
        ]
    return InlineKeyboardMarkup(btn)
