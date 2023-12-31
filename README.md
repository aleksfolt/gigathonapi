<h1 align="center">Hi there, I'm <a href="https://github.com/aleksfolt" target="_blank">AleksFolt</a> 

# GigaChat Messenger Api 

This is not the official library for the gigachat.ru messenger. We are not responsible for this project for all your actions you are responsible if you use this library

# Authentication

1. Go to gigachat.ru
2. Register or log in to your existing account
3. Open developer console: F12 or Ctrl + Shift + C
4. Application → Cookies → https://gigachat.ru → Copy the value of <code>PHPSESSID</code> cookie.

# Install

<pre>$ pip install gigathon-api==0.0.1</pre> 

# Usage

Import:
<pre>
from gigachat-api import GigaChat
import asyncio

api_token = "your_token"

client = GigaChat(api_token, "leave it like that")
</pre>
Usage:
<pre>
async def main():
  last = None
  while True:
      messages = await client.get_messages(last=last)
      for message in messages:
          last = message
          if message[1] != last:
              if not message[1]:
                  continue
              prompt = message[1][1]
              if prompt == "":
                  continue
              response = prompt
              await client.send_message(response, message[0])
</pre>
and:
<pre>
if __name__ == "__main__":
    asyncio.run(main())
</pre>

# Authors

**Created a library and did all the routine: [Alekami649](https://github.com/alekami649)**

**Deployed to pypi, made a repository on github and came up with an idea (or maybe not): [AleksFolt](https://github.com/aleksfolt)**

**PyPi: https://pypi.org/project/gigathon-api/0.0.1/**

