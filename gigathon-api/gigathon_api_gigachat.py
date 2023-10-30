import time

import aiohttp
from bs4 import BeautifulSoup


HTTP_ENDPOINT = "https://gigachat.ru"
AUTH_HEADER_NAME = "PHPSESSID"

SEND_MESSAGE_ENDPOINT = "ajax.php"

GET_MESSAGES_ENDPOINT = "ajax.php?companions=true"

LISTEN_MESSAGES_ENDPOINT = "ajax.php?companion_name={0}&update=true"

"""
'<div class="user companion">AleksFolt</div><div class="user companion">admin</div><div class="user companion">alekami649</div><div class="user companion">самим собой</div><div class="user companion">Folt</div><div class="user companion">ChatGPT</div><div class="user companion">thekami649</div><div class="user companion">Привет! Чем могу помочь?</div><div class="user companion">Здраво! Како можам да бидам од помош?</div>'
div
"""



class GigaChat():
    listen = True

    def __init__(self, session_id: str, skip_browser_warning: str) -> None:
        self.session_id: str = session_id
        self.skip_browser_warning: str = skip_browser_warning

    async def send_message(self, text: str, receiver: str) -> None:
        url = f"{HTTP_ENDPOINT}/{SEND_MESSAGE_ENDPOINT}"
        data = {
            "message": text,
            "companion_name": receiver.strip(),
            "save": "true"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.8,ru-RU;q=0.5,ru;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://gigachat.ru",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": f"PHPSESSID={self.session_id}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "ngrok-skip-browser-warning": f"{self.skip_browser_warning}",
            "TE": "trailers"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                print(await response.text())

    async def get_last_message(self, user: str, last = None) -> tuple[str, str]:
        message = await self._get_message_from_conversation(user, last=last)
        return message

    async def listen_for_messages(self, user: str) -> None:
        last = None
        while self.listen:
            message = await self._get_message_from_conversation(user, last=last)
            if message and message != last:
                print(message)
                last = message
            time.sleep(0.1)

    async def _get_message_from_conversation(self, user: str, last: list[tuple[str, str]] = None) -> tuple[
                                                                                                         str, str] | None:
        url = f"{HTTP_ENDPOINT}/{LISTEN_MESSAGES_ENDPOINT.format(user.strip())}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.8,ru-RU;q=0.5,ru;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://gigachat.ru",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": f"PHPSESSID={self.session_id}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "ngrok-skip-browser-warning": f"{self.skip_browser_warning}",
            "TE": "trailers"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()
                conversation: list[tuple[str, str]] = self._parse_conversation(text)
                if len(conversation) > 1:
                    return conversation[-1] if conversation != last else None
                return None

    def _parse_conversation(self, conversation_html: str) -> list[tuple[str, str]]:
        soup = BeautifulSoup(conversation_html, "html.parser")
        messages = soup.find_all("div", class_="friend-message")
        result = []

        for message in messages:
            text = message.text
            if "my-message" in message.attrs["class"]:
                continue
            result.append(("aaa", text))

        return result

    async def get_conversations(self):
        url = f"{HTTP_ENDPOINT}/{GET_MESSAGES_ENDPOINT}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.8,ru-RU;q=0.5,ru;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://gigachat.ru",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": f"PHPSESSID={self.session_id}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "ngrok-skip-browser-warning": f"{self.skip_browser_warning}",
            "TE": "trailers"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                text = await response.text()
                return self._parse_conversations(text)

    def _parse_conversations(self, conversations_html):
        soup = BeautifulSoup(conversations_html, "html.parser")
        conversations = soup.find_all("div", class_="user companion")
        result = []

        for conversation in conversations:
            result.append(conversation.text)

        return result

    async def get_messages(self, last=None):
        conversations = await self.get_conversations()
        result = []

        for conversation in conversations:
            last_message = await self.get_last_message(conversation)
            if last_message != last:
                result.append((conversation, last_message))

        return result
