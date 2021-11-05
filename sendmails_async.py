import asyncio
from email.message import EmailMessage

import aiosmtplib
import aiosqlite3
from more_itertools import chunked

SERVER = {
    'hostname': '127.0.0.1',
    'port': 1025
}


async def db_connect():
    async with aiosqlite3.connect('contacts.db') as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT first_name || ' ' || last_name, email FROM contacts;")
            contacts_list = await cur.fetchall()
    return contacts_list


async def send_message(fio, email, **params):
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = email
    message["Subject"] = f"Hello {fio}!"
    message.set_content("Server root message")

    return await aiosmtplib.send(message, hostname=params.get('hostname'), port=params.get('port'))


async def main():
    persons = await db_connect()
    tasks = []
    for data_chunked in chunked(persons, 20):
        tasks = [asyncio.create_task(send_message(data[0], data[1], hostname='localhost', port=1025))
                 for data in data_chunked]

    for task in tasks:
        await task


asyncio.run(main())
