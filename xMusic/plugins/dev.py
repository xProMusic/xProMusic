import sys
import traceback
import subprocess

from config import OWNER_ID
from xMusic import app

from re import split
from os import remove
from io import StringIO

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command("eval") & filters.user(OWNER_ID) & ~filters.forwarded)
async def executor(client, message):
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.reply_text("<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ?</b>")

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    evaluation = evaluation.strip()

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🗑 Close", callback_data=f"forceclose {message.from_user.id}"),
            ]
        ]
    )
    if len(evaluation) > 4000:
        with open("COMPLETED.txt", "w+", encoding="utf8") as out_file:
            out_file.write(f"⥤ ɪɴᴘᴜᴛ :\n\n{cmd}\n\n\n⥤ ʀᴇsᴜʟᴛ :\n\n{evaluation}")
        await message.reply_document(
            document="COMPLETED.txt",
            caption=f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<code>Attached Document</code>",
            quote=False,
            reply_markup=keyboard,
        )
        remove("COMPLETED.txt")
        await message.delete()
    else:
        final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n\n<pre language='python'>{evaluation}</pre>"
        await message.reply_text(final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    user_id = CallbackQuery.data.split(" ", 1)[1]
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("You're not allowed to close this.", show_alert=True)
        except:
            return
    await CallbackQuery.message.delete()


@app.on_message(filters.command("sh") & filters.user(OWNER_ID) & ~filters.forwarded)
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await message.reply_text("<b>Example :</b>\n/sh git pull")

    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await message.reply_text(f"<b>⥤ ᴇʀʀᴏʀ :</b>\n\n<pre>{str(err)}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(exc_type, value=exc_obj, tb=exc_tb)
            return await message.reply_text(f"<b>⥤ ᴇʀʀᴏʀ :</b>\n<pre>{''.join(errors)}</pre>")
        output = process.stdout.read()[:-1].decode("utf-8")

    if str(output) == "\n":
        output = None

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🗑 Close", callback_data=f"forceclose {message.from_user.id}"),
                ]
            ]
        )
    if output:
        if len(output) > 4000:
            with open("COMPLETED.txt", "w+") as file:
                file.write(output)
            await client.send_document(message.chat.id, "COMPLETED.txt", reply_to_message_id=message.id, caption="<code>Output</code>")
            remove("COMPLETED.txt")
            return
        await message.reply_text(f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n\n<pre>{output}</pre>", reply_markup=keyboard)
    else:
        await message.reply_text("<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<code>No output</code>", reply_markup=keyboard)
