from .worker import *


async def up(event):
    if not event.is_private:
        return
    stt = dt.now()
    ed = dt.now()
    v = ts(int((ed - uptime).seconds) * 1000)
    ms = (ed - stt).microseconds / 1000
    p = f"💥Pɪɴɢ = {ms}ms"
    await event.reply(v + "\n" + p)


async def start(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`\nThis Encoder Bot Belongs To @OngoingAnimess",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("OngoingAnimess", url="https://t.me/OngoingAnimess"),
            ],
        ],
    )


async def help(event):
    await event.reply(
        "**🌐 This Bot Is Not Public**\n\n✔️Only Authenticated Users Will Use This Bot"
    )


async def ihelp(event):
    await event.edit(
        "**🌐 This Bot Is Not Public**\n\n✔️Only Authenticated Users Will Use This Bot",
        buttons=[Button.inline("BACK", data="beck")],
    )


async def beck(event):
    await event.edit(
        f"Hi `{event.sender.first_name}`\nThis Encoder Bot Belongs To @OngoingAnimess",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("OngoingAnimess", url="https://t.me/OngoingAnimess"),
            ],
        ],
    )