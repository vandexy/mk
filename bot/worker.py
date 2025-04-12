from .FastTelethon import download_file, upload_file
from .funcn import *


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        ans = f"Original File Size:\n{ov}\n\nCurrent Encoding File Size:\n{ot}"
        await e.answer(ans, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        await e.answer("❌Someting Went Wrong❌\nResend Media\nMaybe Server Restart", cache_time=0, alert=True)


async def dl_link(event):
    if not event.is_private:
        return
    if str(event.sender_id) not in OWNER:
        return
    link, name = "", ""
    try:
        link = event.text.split()[1]
        name = event.text.split()[2]
    except BaseException:
        pass
    if not link:
        return
    if WORKING or QUEUE:
        QUEUE.update({link: name})
        return await event.reply(f"Added {link} in QUEUE")
    WORKING.append(1)
    s = dt.now()
    xxx = await event.reply("`⬇️Downloading⬇️`")
    try:
        dl = await fast_download(xxx, link, name)
    except Exception as er:
        WORKING.clear()
        LOGS.info(er)
        return
    es = dt.now()
    kk = dl.split("/")[-1]
    aa = kk.split(".")[-1]
    rr = "encode"
    bb = kk.replace(f".{aa}", " Encode.mkv")
    out = f"{rr}/{bb}"
    dtime = ts(int((es - s).seconds) * 1000)
    hehe = f"{out};{dl};0"
    wah = code(hehe)
    nn = await xxx.edit(
        "`Encoding Your Video Now`",
        buttons=[
            [Button.inline("█ ▆Current Encoding Stats▆ █", data=f"stats{wah}")],
            [Button.inline("█ ▆Cancel▆ █", data=f"skip{wah}")],
        ],
    )
    cmd = FFMPEG.format(dl, out)
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    er = stderr.decode()
    try:
        if er:
            await xxx.edit(str(er) + "\n\n**ERROR**")
            WORKING.clear()
            os.remove(dl)
            return os.remove(out)
    except BaseException:
        pass
    ees = dt.now()
    ttt = time.time()
    await nn.delete()
    nnn = await xxx.client.send_message(xxx.chat_id, "`⬆️Uploading⬆️`")
    with open(out, "rb") as f:
        ok = await upload_file(
            client=xxx.client,
            file=f,
            name=out,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, nnn, ttt, "⬆️Uploading⬆️")
            ),
        )
    ds = await xxx.client.send_file(
        xxx.chat_id, file=ok, force_document=True
    )
    await nnn.delete()
    org = int(Path(dl).stat().st_size)
    com = int(Path(out).stat().st_size)
    pe = 100 - ((com / org) * 100)
    per = str(f"{pe:.2f}") + "%"
    eees = dt.now()
    x = dtime
    xx = ts(int((ees - es).seconds) * 1000)
    xxx = ts(int((eees - ees).seconds) * 1000)
    a1 = await info(dl, xxx)
    a2 = await info(out, xxx)
    dk = await ds.reply(
        f"Original Size : {hbs(org)}\nEncoded Size : {hbs(com)}\nEncoded Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}",
        link_preview=False,
    )
    os.remove(dl)
    os.remove(out)
    WORKING.clear()


async def encod(event):
    try:
        if not event.is_private:
            return
        if str(event.sender_id) not in OWNER:
            return
        if not event.media:
            return
        if hasattr(event.media, "document"):
            if not event.media.document.mime_type.startswith(
                ("video", "application/octet-stream")
            ):
                return
        else:
            return
        try:
            oc = event.fwd_from.from_id.user_id
            occ = (await event.client.get_me()).id
            if oc == occ:
                return await event.reply("`😶This Video File is Already Encoded😶`")
        except BaseException:
            pass
        if WORKING or QUEUE:
            xxx = await event.reply("`Adding To Queue`")
            # id = pack_bot_file_id(event.media)
            doc = event.media.document
            if doc.id in list(QUEUE.keys()):
                return await xxx.edit("`(⌐⊙_⊙)This File Is Already In Queue(⌐⊙_⊙)`")
            name = event.file.name
            if not name:
                name = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            QUEUE.update({doc.id: [name, doc]})
            return await xxx.edit("`✔️Added This File In Queue✔️`")
        WORKING.append(1)
        xxx = await event.reply("`⬇️Downloading⬇️`")
        s = dt.now()
        ttt = time.time()
        dir = f"downloads/"
        try:
            if hasattr(event.media, "document"):
                file = event.media.document
                filename = event.file.name
                if not filename:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                dl = dir + filename
                with open(dl, "wb") as f:
                    ok = await download_file(
                        client=event.client,
                        location=file,
                        out=f,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                xxx,
                                ttt,
                                "⬇️Downloading⬇️",
                            )
                        ),
                    )
            else:
                dl = await event.client.download_media(
                    event.media,
                    dir,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, xxx, ttt, "⬇️Downloading⬇️")
                    ),
                )
        except Exception as er:
            WORKING.clear()
            LOGS.info(er)
            return os.remove(dl)
        es = dt.now()
        kk = dl.split("/")[-1]
        aa = kk.split(".")[-1]
        rr = f"encode"
        bb = kk.replace(f".{aa}", " Encoded.mkv")
        out = f"{rr}/{bb}"
        dtime = ts(int((es - s).seconds) * 1000)
        e = xxx
        hehe = f"{out};{dl};0"
        wah = code(hehe)
        nn = await e.edit(
            "`Encoding Your Video Now`",
            buttons=[
                [Button.inline("█ ▆Current Encoding Stats▆ █", data=f"stats{wah}")],
                [Button.inline("█ ▆Cancel▆ █", data=f"skip{wah}")],
            ],
        )
        cmd = FFMPEG.format(dl, out)
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        er = stderr.decode()
        try:
            if er:
                await e.edit(str(er) + "\n\n**ERROR**")
                WORKING.clear()
                os.remove(dl)
                return os.remove(out)
        except BaseException:
            pass
        ees = dt.now()
        ttt = time.time()
        await nn.delete()
        nnn = await e.client.send_message(e.chat_id, "`⬆️Uploading⬆️`")
        with open(out, "rb") as f:
            ok = await upload_file(
                client=e.client,
                file=f,
                name=out,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, nnn, ttt, "⬆️Uploading⬆️")
                ),
            )
        ds = await e.client.send_file(
            e.chat_id, file=ok, force_document=True
        )
        await nnn.delete()
        org = int(Path(dl).stat().st_size)
        com = int(Path(out).stat().st_size)
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}") + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        a1 = await info(dl, e)
        a2 = await info(out, e)
        dk = await ds.reply(
            f"Original Size : {hbs(org)}\nEncoded Size : {hbs(com)}\nEncoded Percentage : {per}\n\nMediainfo: [Before]({a1})//[After]({a2})\n\nDownloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}",
            link_preview=False,
        )
        os.remove(dl)
        os.remove(out)
        WORKING.clear()
    except BaseException as er:
        LOGS.info(er)
        WORKING.clear()
