from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pathlib
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
#from cairosvg import svg2png
import database
import keep_alive
# Create a new Client instance
ostrich = Client("ostrich",
                 
                 bot_token=os.environ['bot_token'],
                 api_id=os.environ['api_id'],
                 api_hash=os.environ['api_hash'])


@ostrich.on_message(filters.command(["start"]))
async def start(client, message):
    try:
        await message.reply_text(
            text=f"**Hi {message.chat.first_name} 👋 !"
            "\n\nHaving troubles with SVG?\nDon't worry I will convert it to easily viewable/usable file format."
            "\n\nCheck help to find out more about how to use me.**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("HELP", callback_data="getHelp"),
            ]]),
            reply_to_message_id=message.message_id)
    except:
        await message.reply_text(
            text=f"**Hi 👋 !"
            "\n\nHaving troubles with SVG?\nDon't worry I will convert it to easily viewable/usable file format."
            "\n\nCheck help to find out more about how to use me.**",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("HELP", callback_data="getHelp"),
            ]]),
            reply_to_message_id=message.id)
    database.scrape(message)


@ostrich.on_message(filters.command(["help"]))
async def assist(client, message):
    await message.reply_text(
        text=f"**Hello {message.chat.first_name}."
        "\nHere is a detailed guide to use me."
        "\n\nYou might have know about various file formats of an image like JPG,PNG. But you might not know/familiar with SVG type formatted files."
        "\n\nDon't worry I am here to help you with it.\n\nSend me any SVG files and I will convert it to other file formats.\n[Currently I support transferring SVG to PNG files]."
        "\n\nFor further information and guidance contact my developers at my support group.**",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("SUPPORT GROUP",
                                 url="https://t.me/ostrichdiscussion"),
        ]]),
        reply_to_message_id=message.id)


@ostrich.on_message(filters.private & filters.document)
async def noSVG(client, message):
    media = message

    msg = await client.send_message(
        chat_id=message.chat.id,
        text="**Downloading your file to server...**",
        reply_to_message_id=media.id)

    download_location = await client.download_media(message=media)
    filename = pathlib.Path(download_location).stem
    extention = pathlib.Path(download_location).suffix
    if extention == ".svg":
        drawing = svg2rlg(download_location)
        renderPM.drawToFile(drawing,f"{filename}.png")
        await client.send_photo(chat_id=msg.chat.id, photo=f"{filename}.png")
        os.remove(download_location)
        
        
        os.remove(f"{filename}.png")
    else:
        await msg.edit_text("**Send me any SVG files**")
        os.remove(download_location)
        


@ostrich.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    """Log Errors caused by Updates."""

    keyboard = [
        [
            InlineKeyboardButton("➰Channel", url="t.me/theostrich"),
            InlineKeyboardButton("👥Support Group",
                                 url="t.me/ostrichdiscussion"),
        ],
        [
            InlineKeyboardButton(
                "🔖Add Me In Group",
                url="https://t.me/iconrailsBot?startgroup=new")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
        "<b>Hello! My name is noSVGbot.</b>"
        "\nI can convert SVG files to PNG."
        "\n\n<b>About Me :</b>"
        "\n\n  - <b>Name</b>        : noSVGbot"
        "\n\n  - <b>Creator</b>      : @theostrich"
        "\n\n  - <b>Language</b>  : Python 3"
        "\n\n  - <b>Library</b>       : <a href=\"https://docs.pyrogram.org/\">Pyrogram</a>"
        "\n\nIf you enjoy using me and want to help me survive, do donate with the /donate command - my creator will be very grateful! Doesn't have to be much - every little helps! Thanks for reading :)",
        reply_markup=reply_markup,
        disable_web_page_preview=True)


@ostrich.on_message(filters.command(["donate"]))
async def donate(client, message):
    keyboard = [
        [
            InlineKeyboardButton("Contribute",
                                 url="https://github.com/theostrich"),
            InlineKeyboardButton("Paypal Us",
                                 url="https://paypal.me/donateostrich"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply_text(
        "Thank you for your wish to contribute. I hope you enjoyed using our services. Make a small donation/contribute to let this project alive.",
        reply_markup=reply_markup)


@ostrich.on_callback_query()
async def callback(client, query):
    if query.data == "getHelp":
        await query.answer()
        await query.message.edit_text(
            text=f"**Hello {query.message.chat.first_name}."
            "\nHere is a detailed guide to use me."
            "\n\nYou might have know about various file formats of an image like JPG,PNG. But you might not know/familiar with SVG type formatted files."
            "\n\nDon't worry I am here to help you with it.\n\nSend me any SVG files and I will convert it to other file formats.\n[Currently I support transferring SVG to PNG files]."
            "\n\nFor further information and guidance contact my developers at my support group.**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("SUPPORT GROUP",
                                     url="https://t.me/ostrichdiscussion"),
            ]]),
            disable_web_page_preview=True)
        return


keep_alive.keep_alive()
ostrich.run()
