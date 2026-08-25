from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)


@Client.on_message(filters.command(["start", "help"]))
async def start(_: Client, msg: Message) -> None:
    await msg.reply_text(
        "发送 `开始` 后发送要合并的媒体文件, 完成后发送 `结束` 即可",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("开始"), KeyboardButton("结束")]],
            resize_keyboard=True,
            is_persistent=True,
        ),
    )


@Client.on_message(filters.regex("^开始$"))
async def begin(_: Client, msg: Message) -> None:
    await msg.reply_text("请发送要合并的媒体文件, 完成后发送 `结束` 即可")


@Client.on_message(filters.regex("^结束$"))
async def end(cli: Client, msg: Message) -> None:
    await process_media(cli, msg)


async def process_media(cli: Client, msg: Message) -> None:
    chat = msg.chat
    if chat is None:
        return
    chat_id = chat.id
    if chat_id is None:
        return

    raw_msgs = await cli.get_messages(chat_id, range(msg.id - 100, msg.id)) or []
    filtered_msgs: list[Message] = []
    for m in reversed(raw_msgs):
        if m.text and m.text == "开始":
            break
        if m.text and m.text == "结束":
            await msg.reply("请先发送 `开始`")
            return
        if m.media in (
            MessageMediaType.AUDIO,
            MessageMediaType.VIDEO,
            MessageMediaType.DOCUMENT,
            MessageMediaType.PHOTO,
        ):
            filtered_msgs.append(m)
    # 遍历是逆序(新→旧)以便定位"开始"边界, 收集完成后反转恢复用户发送顺序(旧→新)
    filtered_msgs.reverse()

    if not filtered_msgs:
        await msg.reply("请先发送要合并的内容")
        return

    if len(filtered_msgs) == 1:
        await msg.reply("至少两个文件")
        return

    # 照片/视频可组成相册发送, 音频/文档无法组成相册, 逐个转发
    album_msgs = [
        m for m in filtered_msgs if m.media in (MessageMediaType.PHOTO, MessageMediaType.VIDEO)
    ]
    others = [
        m for m in filtered_msgs if m.media not in (MessageMediaType.PHOTO, MessageMediaType.VIDEO)
    ]
    for g in [album_msgs[i : i + 10] for i in range(0, len(album_msgs), 10)]:
        media = [m for m in (get_album_media(m) for m in g) if m is not None]
        if media:
            await msg.reply_media_group(media)
    for m in others:
        await m.copy(chat_id)


def get_album_media(msg: Message) -> InputMediaPhoto | InputMediaVideo | None:
    if msg.media == MessageMediaType.VIDEO:
        video = msg.video
        if video is None:
            return None
        return InputMediaVideo(
            media=video.file_id,
            duration=video.duration,
            width=video.width,
            height=video.height,
            supports_streaming=video.supports_streaming if video.supports_streaming is not None else True,
        )
    if msg.media == MessageMediaType.PHOTO:
        photo = msg.photo
        if photo is None:
            return None
        return InputMediaPhoto(media=photo.file_id)
    return None
