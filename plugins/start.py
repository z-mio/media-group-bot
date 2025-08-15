from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import (
    Message,
    BotCommand,
    ReplyKeyboardMarkup as Rkm,
    KeyboardButton as Kb,
    InputMediaAudio,
    InputMediaVideo,
    InputMediaDocument,
    InputMediaPhoto,
)

from utils.filters import is_admin


@Client.on_message(filters.command(["start", "help"]))
async def start(_, msg: Message):
    await msg.reply_text("发送 `开始` 后发送要合并的媒体文件, 完成后发送 `结束` 即可")


@Client.on_message(filters.command("menu") & is_admin)
async def set_menu(cli: Client, msg: Message):
    commands = {"start": "开始", "help": "帮助"}
    await cli.set_bot_commands(
        [BotCommand(command=k, description=v) for k, v in commands.items()]
    )
    await msg.reply(
        "👌",
        reply_markup=Rkm(
            [[Kb("开始"), Kb("结束")]], resize_keyboard=True, is_persistent=True
        ),
    )


@Client.on_message(filters.regex("^开始$"))
async def begin(_, msg: Message):
    await msg.reply_text("请发送要合并的媒体文件, 完成后发送 `结束` 即可")


@Client.on_message(filters.regex("^结束$"))
async def end(_, msg: Message):
    await process_media(_, msg)


async def process_media(cli: Client, msg: Message):
    msgs = await cli.get_messages(msg.chat.id, range(msg.id - 100, msg.id))
    filtered_msgs = []
    for m in reversed(msgs):
        if m.text and m.text == "开始":
            break
        if m.text and m.text == "结束":
            await msg.reply("请先发送 `开始`")
            return
        if m.media in [
            MessageMediaType.AUDIO,
            MessageMediaType.VIDEO,
            MessageMediaType.DOCUMENT,
            MessageMediaType.PHOTO,
        ]:
            filtered_msgs.append(m)

    if not filtered_msgs:
        await msg.reply("请先发送要合并的内容")
        return

    if len(filtered_msgs) == 1:
        await msg.reply("至少两个文件")

    groups = [filtered_msgs[i : i + 10] for i in range(0, len(filtered_msgs), 10)]
    for g in groups:
        await msg.reply_media_group([get_media(m) for m in g])


def get_media(msg: Message):
    match msg.media:
        case MessageMediaType.AUDIO:
            return InputMediaAudio(
                media=msg.audio.file_id,
                duration=msg.audio.duration,
                title=msg.audio.title,
                performer=msg.audio.performer,
            )
        case MessageMediaType.VIDEO:
            return InputMediaVideo(
                media=msg.video.file_id,
                duration=msg.video.duration,
                width=msg.video.width,
                height=msg.video.height,
                supports_streaming=msg.video.supports_streaming,
            )
        case MessageMediaType.DOCUMENT:
            return InputMediaDocument(
                media=msg.document.file_id,
            )
        case MessageMediaType.PHOTO:
            return InputMediaPhoto(
                media=msg.photo.file_id,
            )
        case _:
            return None
