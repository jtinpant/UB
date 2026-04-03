import asyncio
from random import choice
from telethon import events, functions, types
from config import SUDO_USERS, hl
from AltBots.data import GROUP, PORMS

def register_spam(client):
    """
    This function attaches all spam handlers to a specific user's client session.
    Preserves: Spam (Text/Media), PornSpam, and Hang.
    """

    # --- INTERNAL HELPER FOR GIF SAVING ---
    async def gifspam(e, smex):
        try:
            await e.client(
                functions.messages.SaveGifRequest(
                    id=types.InputDocument(
                        id=smex.media.document.id,
                        access_hash=smex.media.document.access_hash,
                        file_reference=smex.media.document.file_reference,
                    ),
                    unsave=True,
                )
            )
        except Exception:
            pass

    # --- STANDARD SPAM ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%sspam(?: |$)(.*)" % hl))
    async def spam(event):
        if event.sender_id in SUDO_USERS:
            altron = event.text.split(" ", 2)
            mk = await event.get_reply_message()

            try:
                # Case 1: .spam <count> <message>
                if len(altron) == 3:
                    message = altron[2]
                    for _ in range(int(altron[1])):
                        if event.reply_to_msg_id:
                            await mk.reply(message)
                        else:
                            await event.client.send_message(event.chat_id, message)
                        await asyncio.sleep(0.2)

                # Case 2: .spam <count> (Replying to Media/GIF)
                elif event.reply_to_msg_id and mk.media:
                    for _ in range(int(altron[1])):
                        mk = await event.client.send_file(event.chat_id, mk, caption=mk.text)
                        await gifspam(event, mk) 
                        await asyncio.sleep(0.2)  

                # Case 3: .spam <count> (Replying to Text)
                elif event.reply_to_msg_id and mk.text:
                    message = mk.text
                    for _ in range(int(altron[1])):
                        await event.client.send_message(event.chat_id, message)
                        await asyncio.sleep(0.2)
                else:
                    await event.reply(f"😈 **Usage:**\n » {hl}spam 13 Smoker\n » {hl}spam 13 <reply to text>")

            except (IndexError, ValueError):
                await event.reply(f"😈 **Usage:**\n » {hl}spam 13 Smoker\n » {hl}spam 13 <reply to text>")
            except Exception as e:
                print(f"Spam Error: {e}")

    # --- PORN SPAM (PSPAN) ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%spspam(?: |$)(.*)" % hl))
    async def pspam(event):
        if event.sender_id in SUDO_USERS:
            # Check if group is protected
            if event.chat_id in GROUP:
                await event.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(event.text.split(" ", 2)[1])
                    for _ in range(counter):
                        porrn = choice(PORMS)
                        alt = await event.client.send_file(event.chat_id, porrn)
                        await gifspam(event, alt) 
                        await asyncio.sleep(0.2)
                except (IndexError, ValueError):
                    await event.reply(f"🔞 **Usage:** {hl}pspam 13")
                except Exception as e:
                    print(f"PSpam Error: {e}")

    # --- HANG (LAG SPAM) ---
    @client.on(events.NewMessage(incoming=True, pattern=r"\%shang(?: |$)(.*)" % hl))
    async def hang(e):
        if e.sender_id in SUDO_USERS:
            if e.chat_id in GROUP:
                await e.reply("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀʟᴛʀᴏɴ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            else:
                try:
                    counter = int(e.text.split(" ", 2)[1])
                    # Original "Hanging" character string
                    hang_msg = "😈" + "꙰" * 500 # Simplified representation for the script
                    for _ in range(counter):
                        await e.respond(hang_msg)
                        await asyncio.sleep(0.3)
                except (IndexError, ValueError):
                    await e.reply(f"😈 **Usage:** {hl}hang 10")
                except Exception as ex:
                    print(f"Hang Error: {ex}")
                  
