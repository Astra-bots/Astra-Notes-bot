import os

from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from storage import (
    add_note,
    get_notes,
    delete_note,
    delete_all_notes,
    edit_note,
    search_notes
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


MENU = 0
ADD = 1
DELETE = 2
EDIT_SELECT = 3
EDIT_TEXT = 4
SEARCH = 5


edit_index = {}


keyboard = [

    ["📝 افزودن یادداشت"],

    ["📋 یادداشت‌ها"],

    ["✏️ ویرایش", "🗑 حذف"],

    ["🔍 جستجو"],

    ["❌ حذف همه"]

]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "📝 به Astra Notes خوش آمدی.\n\n"
        "از منوی زیر گزینه موردنظر را انتخاب کن.",

        reply_markup=reply_markup

    )

    return MENU

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📝 افزودن یادداشت":

        await update.message.reply_text(

            "متن یادداشت را ارسال کن."

        )

        return ADD



    if text == "📋 یادداشت‌ها":

        notes = get_notes(update.effective_user.id)

        if not notes:

            await update.message.reply_text(

                "یادداشتی وجود ندارد."

            )

        else:

            message = ""

            for i, note in enumerate(notes, 1):

                message += f"{i}. {note}\n\n"

            await update.message.reply_text(message)

        return MENU



    if text == "🗑 حذف":

        notes = get_notes(update.effective_user.id)

        if not notes:

            await update.message.reply_text(

                "یادداشتی وجود ندارد."

            )

            return MENU

        message = ""

        for i, note in enumerate(notes, 1):

            message += f"{i}. {note}\n"

        message += "\nشماره یادداشت را ارسال کن."

        await update.message.reply_text(message)

        return DELETE



    if text == "✏️ ویرایش":

        notes = get_notes(update.effective_user.id)

        if not notes:

            await update.message.reply_text(

                "یادداشتی وجود ندارد."

            )

            return MENU

        message = ""

        for i, note in enumerate(notes, 1):

            message += f"{i}. {note}\n"

        message += "\nشماره یادداشت را ارسال کن."

        await update.message.reply_text(message)

        return EDIT_SELECT



    if text == "🔍 جستجو":

        await update.message.reply_text(

            "کلمه موردنظر را ارسال کن."

        )

        return SEARCH



    if text == "❌ حذف همه":

        delete_all_notes(update.effective_user.id)

        await update.message.reply_text(

            "همه یادداشت‌ها حذف شدند."

        )

        return MENU



    return MENU

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_note(

        update.effective_user.id,

        update.message.text

    )

    await update.message.reply_text(

        "✅ یادداشت ذخیره شد."

    )

    return MENU




async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        index = int(update.message.text) - 1

    except ValueError:

        await update.message.reply_text(

            "❌ لطفاً فقط شماره یادداشت را وارد کن."

        )

        return DELETE


    if delete_note(update.effective_user.id, index):

        await update.message.reply_text(

            "🗑 یادداشت حذف شد."

        )

    else:

        await update.message.reply_text(

            "❌ شماره نامعتبر است."

        )

    return MENU




async def edit_select(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        index = int(update.message.text) - 1

    except ValueError:

        await update.message.reply_text(

            "❌ شماره معتبر وارد کن."

        )

        return EDIT_SELECT


    notes = get_notes(update.effective_user.id)

    if index < 0 or index >= len(notes):

        await update.message.reply_text(

            "❌ شماره نامعتبر است."

        )

        return MENU


    edit_index[update.effective_user.id] = index

    await update.message.reply_text(

        "✏️ متن جدید را ارسال کن."

    )

    return EDIT_TEXT




async def edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    index = edit_index.get(update.effective_user.id)

    if index is None:

        return MENU


    edit_note(

        update.effective_user.id,

        index,

        update.message.text

    )

    del edit_index[update.effective_user.id]

    await update.message.reply_text(

        "✅ یادداشت ویرایش شد."

    )

    return MENU




async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    result = search_notes(

        update.effective_user.id,

        update.message.text

    )

    if not result:

        await update.message.reply_text(

            "هیچ نتیجه‌ای پیدا نشد."

        )

        return MENU


    message = ""

    for index, note in result:

        message += f"{index + 1}. {note}\n\n"

    await update.message.reply_text(message)

    return MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "❌ عملیات لغو شد.",

        reply_markup=reply_markup

    )

    return MENU





def main():

    app = Application.builder().token(TOKEN).build()



    conversation = ConversationHandler(

        entry_points=[

            CommandHandler(
                "start",
                start
            )

        ],


        states={


            MENU: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    menu
                )

            ],



            ADD: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    add
                )

            ],



            DELETE: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    delete
                )

            ],



            EDIT_SELECT: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_select
                )

            ],



            EDIT_TEXT: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_text
                )

            ],



            SEARCH: [

                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    search
                )

            ]

        },


        fallbacks=[

            CommandHandler(
                "cancel",
                cancel
            )

        ]

    )



    app.add_handler(conversation)



    print("Astra Notes Started 📝")



    app.run_polling()





if __name__ == "__main__":

    main()
