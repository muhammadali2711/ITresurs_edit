from django.core.management import BaseCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from Fintech.settings import TOKEN

from telegram_bot.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(TOKEN)

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.video, video_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
        updater.start_polling()
        updater.idle()