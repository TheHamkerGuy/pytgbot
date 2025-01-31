
[![PyPi Package Version](https://img.shields.io/pypi/v/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/pyTelegramBotAPI)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/pyTelegramBotAPI)
[![Documentation Status](https://readthedocs.org/projects/pytba/badge/?version=latest)](https://pytba.readthedocs.io/en/latest/?badge=latest)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyTelegramBotAPI.svg)](https://pypi.org/project/pyTelegramBotAPI/)
[![PyPi status](https://img.shields.io/pypi/status/pytelegrambotapi.svg?style=flat-square)](https://pypi.python.org/pypi/pytelegrambotapi)

# <p align="center">pytgbot

<p align="center">A simple, but extensible Python implementation for the <a href="https://core.telegram.org/bots/api">Telegram Bot API</a>.</p>
<p align="center">Both synchronous and asynchronous.</p>

## <p align="center">Supported Bot API version: <a href="https://core.telegram.org/bots/api#january-1-2025"><img src="https://img.shields.io/badge/Bot%20API-8.2-blue?logo=telegram" alt="Supported Bot API version"></a>

<h2><a href='https://pytba.readthedocs.io/en/latest/index.html'>Official documentation</a></h2>
<h2><a href='https://pytba.readthedocs.io/ru/latest/index.html'>Official ru documentation</a></h2>
	
## Contents

  * [Getting started](#getting-started)
  * [Writing your first bot](#writing-your-first-bot)
    * [Prerequisites](#prerequisites)
    * [A simple echo bot](#a-simple-echo-bot)
  * [General API Documentation](#general-api-documentation)
    * [Types](#types)
    * [Methods](#methods)
    * [General use of the API](#general-use-of-the-api)
      * [Message handlers](#message-handlers)
      * [Edited Message handler](#edited-message-handler)
      * [Channel Post handler](#channel-post-handler)
      * [Edited Channel Post handler](#edited-channel-post-handler)
      * [Callback Query handlers](#callback-query-handler)
      * [Shipping Query Handler](#shipping-query-handler)
      * [Pre Checkout Query Handler](#pre-checkout-query-handler)
      * [Poll Handler](#poll-handler)
      * [Poll Answer Handler](#poll-answer-handler)
      * [My Chat Member Handler](#my-chat-member-handler)
      * [Chat Member Handler](#chat-member-handler)
      * [Chat Join request handler](#chat-join-request-handler)
    * [Inline Mode](#inline-mode)
      * [Inline handler](#inline-handler)
      * [Chosen Inline handler](#chosen-inline-handler)
      * [Answer Inline Query](#answer-inline-query)
    * [Additional API features](#additional-api-features)
      * [Middleware handlers](#middleware-handlers)
      * [Custom filters](#custom-filters)
      * [pytgbot](#pytgbot)
      * [Reply markup](#reply-markup)
  * [Advanced use of the API](#advanced-use-of-the-api)
    * [Using local Bot API Server](#using-local-bot-api-sever)
    * [Asynchronous Pytgbot](#asynchronous-pytgbot)
    * [Sending large text messages](#sending-large-text-messages)
    * [Controlling the amount of Threads used by pytgbot](#controlling-the-amount-of-threads-used-by-pytgbot)
    * [The listener mechanism](#the-listener-mechanism)
    * [Using web hooks](#using-web-hooks)
    * [Logging](#logging)
    * [Proxy](#proxy)
    * [Testing](#testing)
  * [API conformance limitations](#api-conformance-limitations)
  * [AsyncPytgbot](#asyncpytgbot)
  * [F.A.Q.](#faq)
    * [How can I distinguish a User and a GroupChat in message.chat?](#how-can-i-distinguish-a-user-and-a-groupchat-in-messagechat)
    * [How can I handle reocurring ConnectionResetErrors?](#how-can-i-handle-reocurring-connectionreseterrors)
  * [The Telegram Chat Group](#the-telegram-chat-group)
  * [Telegram Channel](#telegram-channel)
  * [More examples](#more-examples)
  * [Code Template](#code-template)
  * [Bots using this library](#bots-using-this-library)

## Getting started

This API is tested with Python 3.9-3.13 and Pypy 3.
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
$ pip install pytgbot
```
* Installation from source (requires git):

```
$ pip install git+https://github.com/TheHamkerGuy/pytgbot.git
```

It is generally recommended to use the first option.

*While the API is production-ready, it is still under development and it has regular updates, do not forget to update it regularly by calling*
```
pip install pytgbot --upgrade
```

## Writing your first bot

### Prerequisites

It is presumed that you [have obtained an API token with @BotFather](https://core.telegram.org/bots#botfather). We will call this token `TOKEN`.
Furthermore, you have basic knowledge of the Python programming language and more importantly [the Telegram Bot API](https://core.telegram.org/bots/api).

### A simple echo bot

The pytgbot class (defined in \__init__.py) encapsulates all API calls in a single class. It provides functions such as `send_xyz` (`send_message`, `send_document` etc.) and several ways to listen for incoming messages.

Create a file called `echo_bot.py`.
Then, open the file and create an instance of the TeleBot class.
```python
import pytgbot

bot = pytgbot.pytgbot("TOKEN", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
```
*Note: Make sure to actually replace TOKEN with your own API token.*

After that declaration, we need to register some so-called message handlers. Message handlers define filters which a message must pass. If a message passes the filter, the decorated function is called and the incoming message is passed as an argument.

Let's define a message handler which handles incoming `/start` and `/help` commands.
```python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
```
A function which is decorated by a message handler __can have an arbitrary name, however, it must have only one parameter (the message)__.

Let's add another handler:
```python
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
```
This one echoes all incoming text messages back to the sender. It uses a lambda function to test a message. If the lambda returns True, the message is handled by the decorated function. Since we want all messages to be handled by this function, we simply always return True.

*Note: all handlers are tested in the order in which they were declared*

We now have a basic bot which replies a static message to "/start" and "/help" commands and which echoes the rest of the sent messages. To start the bot, add the following to our source file:
```python
bot.infinity_polling()
```
Alright, that's it! Our source file now looks like this:
```python
import pytgbot

bot = pytgbot.pytgbot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()
```
To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! Test it by sending commands ('/start' and '/help') and arbitrary text messages.

## General API Documentation

### Types

All types are defined in types.py. They are all completely in line with the [Telegram API's definition of the types](https://core.telegram.org/bots/api#available-types), except for the Message's `from` field, which is renamed to `from_user` (because `from` is a Python reserved token). Thus, attributes such as `message_id` can be accessed directly with `message.message_id`. Note that `message.chat` can be either an instance of `User` or `GroupChat` (see [How can I distinguish a User and a GroupChat in message.chat?](#how-can-i-distinguish-a-user-and-a-groupchat-in-messagechat)).

The Message object also has a `content_type`attribute, which defines the type of the Message. `content_type` can be one of the following strings:
`text`, `audio`, `document`, `animation`, `game`, `photo`, `sticker`, `video`, `video_note`, `voice`, `location`, `contact`, `venue`, `dice`, `new_chat_members`, `left_chat_member`, `new_chat_title`, `new_chat_photo`, `delete_chat_photo`, `group_chat_created`, `supergroup_chat_created`, `channel_chat_created`, `migrate_to_chat_id`, `migrate_from_chat_id`, `pinned_message`, `invoice`, `successful_payment`, `connected_website`, `poll`, `passport_data`, `proximity_alert_triggered`, `video_chat_scheduled`, `video_chat_started`, `video_chat_ended`, `video_chat_participants_invited`, `web_app_data`, `message_auto_delete_timer_changed`, `forum_topic_created`, `forum_topic_closed`, `forum_topic_reopened`, `forum_topic_edited`, `general_forum_topic_hidden`, `general_forum_topic_unhidden`, `write_access_allowed`, `user_shared`, `chat_shared`, `story`.

You can use some types in one function. Example:

```content_types=["text", "sticker", "pinned_message", "photo", "audio"]```

### Methods

All [API methods](https://core.telegram.org/bots/api#available-methods) are located in the TeleBot class. They are renamed to follow common Python naming conventions. E.g. `getMe` is renamed to `get_me` and `sendMessage` to `send_message`.

### General use of the API

Outlined below are some general use cases of the API.

#### Message handlers
A message handler is a function that is decorated with the `message_handler` decorator of a pytgbot instance. Message handlers consist of one or multiple filters.
Each filter must return True for a certain message in order for a message handler to become eligible to handle that message. A message handler is declared in the following way (provided `bot` is an instance of pytgbot):
```python
@bot.message_handler(filters)
def function_name(message):
	bot.reply_to(message, "This is a message handler")
```
`function_name` is not bound to any restrictions. Any function name is permitted with message handlers. The function must accept at most one argument, which will be the message that the function must handle.
`filters` is a list of keyword arguments.
A filter is declared in the following manner: `name=argument`. One handler may have multiple filters.
TeleBot supports the following filters:

|name|argument(s)|Condition|
|:---:|---| ---|
|content_types|list of strings (default `['text']`)|`True` if message.content_type is in the list of strings.|
|regexp|a regular expression as a string|`True` if `re.search(regexp_arg)` returns `True` and `message.content_type == 'text'` (See [Python Regular Expressions](https://docs.python.org/2/library/re.html))|
|commands|list of strings|`True` if `message.content_type == 'text'` and `message.text` starts with a command that is in the list of strings.|
|chat_types|list of chat types|`True` if `message.chat.type` in your filter|
|func|a function (lambda or function reference)|`True` if the lambda or function reference returns `True`|
	
Here are some examples of using the filters and message handlers:

```python
import pytgbot
bot = pytgbot.pytgbot("TOKEN")

# Handles all text messages that contains the commands '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	pass

# Handles all text messages that match the regular expression
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
	pass

# Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
	pass

# Which could also be defined as:
def test_message(message):
	return message.document.mime_type == 'text/plain'

@bot.message_handler(func=test_message, content_types=['document'])
def handle_text_doc(message):
	pass

# Handlers can be stacked to create a function which will be called if either message_handler is eligible
# This handler will be called if the message starts with '/hello' OR is some emoji
@bot.message_handler(commands=['hello'])
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == SOME_FANCY_EMOJI)
def send_something(message):
    pass
```
**Important: all handlers are tested in the order in which they were declared**

#### Edited Message handler
Handle edited messages
`@bot.edited_message_handler(filters) # <- passes a Message type object to your function`

#### Channel Post handler
Handle channel post messages
`@bot.channel_post_handler(filters) # <- passes a Message type object to your function`

#### Edited Channel Post handler
Handle edited channel post messages
`@bot.edited_channel_post_handler(filters) # <- passes a Message type object to your function`

#### Callback Query Handler
Handle callback queries
```python
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    logger.info(call)
```

#### Shipping Query Handler
Handle shipping queries
`@bot.shipping_query_handler() # <- passes a ShippingQuery type object to your function`

#### Pre Checkout Query Handler
Handle pre checkout queries
`@bot.pre_checkout_query_handler() # <- passes a PreCheckoutQuery type object to your function`

#### Poll Handler
Handle poll updates
`@bot.poll_handler() # <- passes a Poll type object to your function`

#### Poll Answer Handler
Handle poll answers
`@bot.poll_answer_handler() # <- passes a PollAnswer type object to your function`

#### My Chat Member Handler
Handle updates of a the bot's member status in a chat
`@bot.my_chat_member_handler() # <- passes a ChatMemberUpdated type object to your function`

#### Chat Member Handler
Handle updates of a chat member's status in a chat
`@bot.chat_member_handler() # <- passes a ChatMemberUpdated type object to your function`
*Note: "chat_member" updates are not requested by default. If you want to allow all update types, set `allowed_updates` in `bot.polling()` / `bot.infinity_polling()` to `util.update_types`*

#### Chat Join Request Handler	
Handle chat join requests using:
`@bot.chat_join_request_handler() # <- passes ChatInviteLink type object to your function`

### Inline Mode

More information about [Inline mode](https://core.telegram.org/bots/inline).

#### Inline handler

Now, you can use inline_handler to get inline queries in telebot.

```python

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    # Query message is text
```

#### Chosen Inline handler

Use chosen_inline_handler to get chosen_inline_result in telebot. Don't forget to add the /setinlinefeedback
command for @Botfather.

More information : [collecting-feedback](https://core.telegram.org/bots/inline#collecting-feedback)

```python
@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    # Process all chosen_inline_result.
```

#### Answer Inline Query

```python
@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

```

### Additional API features

#### Middleware Handlers

A middleware handler is a function that allows you to modify requests or the bot context as they pass through the 
Telegram to the bot. You can imagine middleware as a chain of logic connection handled before any other handlers are
executed. Middleware processing is disabled by default, enable it by setting `apihelper.ENABLE_MIDDLEWARE = True`. 

```python
apihelper.ENABLE_MIDDLEWARE = True

@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message):
    # modifying the message before it reaches any other handler 
    message.another_text = message.text + ':changed'

@bot.message_handler(commands=['start'])
def start(message):
    # the message is already modified when it reaches message handler
    assert message.another_text == message.text + ':changed'
```
There are other examples using middleware handler in the [examples/middleware](examples/middleware) directory.

#### Class-based middlewares
There are class-based middlewares. 
Basic class-based middleware looks like this:
```python
class Middleware(BaseMiddleware):
    def __init__(self):
        self.update_types = ['message']
    def pre_process(self, message, data):
        data['foo'] = 'Hello' # just for example
        # we edited the data. now, this data is passed to handler.
        # return SkipHandler() -> this will skip handler
        # return CancelUpdate() -> this will cancel update
    def post_process(self, message, data, exception=None):
        print(data['foo'])
        if exception: # check for exception
            print(exception)
```
Class-based middleware should have two functions: post and pre process.
So, as you can see, class-based middlewares work before and after handler execution.
	
#### Custom filters
Also, you can use built-in custom filters. Or, you can create your own filter.
	
Also, we have examples on them. Check this links:
	
You can check some built-in filters in source [code](https://github.com/TheHamkerGuy/pytgbot/blob/master/pytgbot/custom_filters.py)
	
If you want to add some built-in filter, you are welcome to add it in custom_filters.py file.
	
Here is example of creating filter-class:
	
```python
class IsAdmin(pytgbot.custom_filters.SimpleCustomFilter):
    # Class will check whether the user is admin or creator in group or not
    key='is_chat_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']
	
# To register filter, you need to use method add_custom_filter.
bot.add_custom_filter(IsAdmin())
	
# Now, you can use it in handler.
@bot.message_handler(is_chat_admin=True)
def admin_of_group(message):
	bot.send_message(message.chat.id, 'You are admin of this group!')

```
	

#### pytgbot
```python
import pytgbot

TOKEN = '<token_string>'
tb = pytgbot.pytgbot(TOKEN)	#create a new Telegram Bot object

# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - interval: int (default 0) - The interval between polling requests
# - timeout: integer (default 20) - Timeout in seconds for long polling.
# - allowed_updates: List of Strings (default None) - List of update types to request 
tb.infinity_polling(interval=0, timeout=20)

# getMe
user = tb.get_me()

# setWebhook
tb.set_webhook(url="http://example.com", certificate=open('mycert.pem'))
# unset webhook
tb.remove_webhook()

# getUpdates
updates = tb.get_updates()
# or
updates = tb.get_updates(1234,100,20) #get_Updates(offset, limit, timeout):

# sendMessage
tb.send_message(chat_id, text)

# editMessageText
tb.edit_message_text(new_text, chat_id, message_id)

# forwardMessage
tb.forward_message(to_chat_id, from_chat_id, message_id)

# All send_xyz functions which can take a file as an argument, can also take a file_id instead of a file.
# sendPhoto
photo = open('/tmp/photo.png', 'rb')
tb.send_photo(chat_id, photo)
tb.send_photo(chat_id, "FILEID")

# sendAudio
audio = open('/tmp/audio.mp3', 'rb')
tb.send_audio(chat_id, audio)
tb.send_audio(chat_id, "FILEID")

## sendAudio with duration, performer and title.
tb.send_audio(CHAT_ID, file_data, 1, 'eternnoir', 'pyTelegram')

# sendVoice
voice = open('/tmp/voice.ogg', 'rb')
tb.send_voice(chat_id, voice)
tb.send_voice(chat_id, "FILEID")

# sendDocument
doc = open('/tmp/file.txt', 'rb')
tb.send_document(chat_id, doc)
tb.send_document(chat_id, "FILEID")

# sendSticker
sti = open('/tmp/sti.webp', 'rb')
tb.send_sticker(chat_id, sti)
tb.send_sticker(chat_id, "FILEID")

# sendVideo
video = open('/tmp/video.mp4', 'rb')
tb.send_video(chat_id, video)
tb.send_video(chat_id, "FILEID")

# sendVideoNote
videonote = open('/tmp/videonote.mp4', 'rb')
tb.send_video_note(chat_id, videonote)
tb.send_video_note(chat_id, "FILEID")

# sendLocation
tb.send_location(chat_id, lat, lon)

# sendChatAction
# action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
# 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
tb.send_chat_action(chat_id, action_string)

# getFile
# Downloading a file is straightforward
# Returns a File object
import requests
file_info = tb.get_file(file_id)

file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))


```
#### Reply markup
All `send_xyz` functions of pytgbot take an optional `reply_markup` argument. This argument must be an instance of `ReplyKeyboardMarkup`, `ReplyKeyboardRemove` or `ForceReply`, which are defined in types.py.

```python
from pytgbot import types

# Using the ReplyKeyboardMarkup class
# It's constructor can take the following optional arguments:
# - resize_keyboard: True/False (default False)
# - one_time_keyboard: True/False (default False)
# - selective: True/False (default False)
# - row_width: integer (default 3)
# row_width is used in combination with the add() function.
# It defines how many buttons are fit on each row before continuing on the next row.
markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('a')
itembtn2 = types.KeyboardButton('v')
itembtn3 = types.KeyboardButton('d')
markup.add(itembtn1, itembtn2, itembtn3)
tb.send_message(chat_id, "Choose one letter:", reply_markup=markup)

# or add KeyboardButton one row at a time:
markup = types.ReplyKeyboardMarkup()
itembtna = types.KeyboardButton('a')
itembtnv = types.KeyboardButton('v')
itembtnc = types.KeyboardButton('c')
itembtnd = types.KeyboardButton('d')
itembtne = types.KeyboardButton('e')
markup.row(itembtna, itembtnv)
markup.row(itembtnc, itembtnd, itembtne)
tb.send_message(chat_id, "Choose one letter:", reply_markup=markup)
```
The last example yields this result:

![ReplyKeyboardMarkup](https://farm3.staticflickr.com/2933/32418726704_9ef76093cf_o_d.jpg "ReplyKeyboardMarkup")

```python
# ReplyKeyboardRemove: hides a previously sent ReplyKeyboardMarkup
# Takes an optional selective argument (True/False, default False)
markup = types.ReplyKeyboardRemove(selective=False)
tb.send_message(chat_id, message, reply_markup=markup)
```

```python
# ForceReply: forces a user to reply to a message
# Takes an optional selective argument (True/False, default False)
markup = types.ForceReply(selective=False)
tb.send_message(chat_id, "Send me another word:", reply_markup=markup)
```
ForceReply:

![ForceReply](https://farm4.staticflickr.com/3809/32418726814_d1baec0fc2_o_d.jpg "ForceReply")


### Working with entities
This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.
Attributes:
* `type`
* `url`
* `offset`
* `length`
* `user`


**Here's an Example:**`message.entities[num].<attribute>`<br>
Here `num` is the entity number or order of entity in a reply, for if incase there are multiple entities in the reply/message.<br>
`message.entities` returns a list of entities object. <br>
`message.entities[0].type` would give the type of the first entity<br>
Refer [Bot Api](https://core.telegram.org/bots/api#messageentity) for extra details

## Advanced use of the API

### Using local Bot API Sever
Since version 5.0 of the Bot API, you have the possibility to run your own [Local Bot API Server](https://core.telegram.org/bots/api#using-a-local-bot-api-server).
pyTelegramBotAPI also supports this feature.
```python
from pytgbot import apihelper

apihelper.API_URL = "http://localhost:4200/bot{0}/{1}"
```
**Important: Like described [here](https://core.telegram.org/bots/api#logout), you have to log out your bot from the Telegram server before switching to your local API server. in pyTelegramBotAPI use `bot.log_out()`**

*Note: 4200 is an example port*

### Asynchronous pytgbot
New: There is an asynchronous implementation of pytgbot.
To enable this behaviour, create an instance of AsyncPytgbot instead of pytgbot.
```python
tb = pytgbot.AsyncPytgbot("TOKEN")
```
Now, every function that calls the Telegram API is executed in a separate asynchronous task.
Using AsyncPytgbot allows you to do the following:
```python
import pytgbot

tb = pytgbot.AsyncPytgbot("TOKEN")

@tb.message_handler(commands=['start'])
async def start_message(message):
	await bot.send_message(message.chat.id, 'Hello!')

```

### Sending large text messages
Sometimes you must send messages that exceed 5000 characters. The Telegram API can not handle that many characters in one request, so we need to split the message in multiples. Here is how to do that using the API:
```python
from pytgbot import util
large_text = open("large_text.txt", "rb").read()

# Split the text each 3000 characters.
# split_string returns a list with the splitted text.
splitted_text = util.split_string(large_text, 3000)

for text in splitted_text:
	tb.send_message(chat_id, text)
```

Or you can use the new `smart_split` function to get more meaningful substrings:
```python
from pytgbot import util
large_text = open("large_text.txt", "rb").read()
# Splits one string into multiple strings, with a maximum amount of `chars_per_string` (max. 4096)
# Splits by last '\n', '. ' or ' ' in exactly this priority.
# smart_split returns a list with the splitted text.
splitted_text = util.smart_split(large_text, chars_per_string=3000)
for text in splitted_text:
	tb.send_message(chat_id, text)
```
### Controlling the amount of Threads used by TeleBot
The pytgbot constructor takes the following optional arguments:

 - threaded: True/False (default True). A flag to indicate whether
   pytgbot should execute message handlers on it's polling Thread.

### The listener mechanism
As an alternative to the message handlers, one can also register a function as a listener to TeleBot.

NOTICE: handlers won't disappear! Your message will be processed both by handlers and listeners. Also, it's impossible to predict which will work at first because of threading. If you use threaded=False, custom listeners will work earlier, after them handlers will be called. 
Example:
```python
def handle_messages(messages):
	for message in messages:
		# Do something with the message
		bot.reply_to(message, 'Hi')

bot.set_update_listener(handle_messages)
bot.infinity_polling()
```

### Using web hooks
When using webhooks telegram sends one Update per call, for processing it you should call process_new_messages([update.message]) when you recieve it.

### Logging
You can use the pytgbot module logger to log debug info about pytgbot. Use `pytgbot.logger` to get the logger of the pytgbot module.
It is possible to add custom logging Handlers to the logger. Refer to the [Python logging module page](https://docs.python.org/2/library/logging.html) for more info.

```python
import logging

logger = pytgbot.logger
pytgbot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
```

### Proxy
For sync:

You can use proxy for request. `apihelper.proxy` object will use by call `requests` proxies argument.

```python
from pytgbot import apihelper

apihelper.proxy = {'http':'http://127.0.0.1:3128'}
```

If you want to use socket5 proxy you need install dependency `pip install requests[socks]` and make sure, that you have the latest version of `gunicorn`, `PySocks`, `pytgbot`, `requests` and `urllib3`.

```python
apihelper.proxy = {'https':'socks5://userproxy:password@proxy_address:port'}
```

For async:
```python
from pytgbot import asyncio_helper

asyncio_helper.proxy = 'http://127.0.0.1:3128' #url
```


### Testing
You can disable or change the interaction with real Telegram server by using
```python
apihelper.CUSTOM_REQUEST_SENDER = your_handler
```
parameter. You can pass there your own function that will be called instead of _requests.request_.

For example:
```python
def custom_sender(method, url, **kwargs):
    print("custom_sender. method: {}, url: {}, params: {}".format(method, url, kwargs.get("params")))
    result = util.CustomRequestResponse('{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}')
    return result
```

Then you can use API and proceed requests in your handler code.
```python
apihelper.CUSTOM_REQUEST_SENDER = custom_sender
tb = pytgbot("test")
res = tb.send_message(123, "Test")
```

Result will be:

`custom_sender. method: post, url: https://api.telegram.org/botololo/sendMessage, params: {'chat_id': '123', 'text': 'Test'}`



## API conformance limitations
* ➕ [Bot API 4.5](https://core.telegram.org/bots/api-changelog#december-31-2019) - No nested MessageEntities and Markdown2 support
* ➕ [Bot API 4.1](https://core.telegram.org/bots/api-changelog#august-27-2018)   - No Passport support
* ➕ [Bot API 4.0](https://core.telegram.org/bots/api-changelog#july-26-2018)     - No Passport support


## AsyncPytgbot
### Asynchronous version of pytgbot
We have a fully asynchronous version of pytgbot.
This class is not controlled by threads. Asyncio tasks are created to execute all the stuff.

### EchoBot
Echo Bot example on AsyncPytgbot:
	
```python
# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

from pytgbot.async_pytgbot import AsyncPytgbot
import asyncio
bot = AsyncPytgbot('TOKEN')



# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


asyncio.run(bot.polling())
```
As you can see here, keywords are await and async. 
	
### Why should I use async?
Asynchronous tasks depend on processor performance. Many asynchronous tasks can run parallelly, while thread tasks will block each other.

### Differences in AsyncPytgbot
AsyncPytgbot is asynchronous. It uses aiohttp instead of requests module.

## F.A.Q.

### How can I distinguish a User and a GroupChat in message.chat?
Telegram Bot API support new type Chat for message.chat.

- Check the ```type``` attribute in ```Chat``` object:
```python
if message.chat.type == "private":
    # private chat message

if message.chat.type == "group":
	# group chat message

if message.chat.type == "supergroup":
	# supergroup chat message

if message.chat.type == "channel":
	# channel message

```

### How can I handle reocurring ConnectionResetErrors?

Bot instances that were idle for a long time might be rejected by the server when sending a message due to a timeout of the last used session. Add `apihelper.SESSION_TIME_TO_LIVE = 5 * 60` to your initialisation to force recreation after 5 minutes without any activity. 

## The Telegram Chat Group

Get help. Discuss. Chat.

* Join the [pyTelegramBotAPI Telegram Chat Group](https://telegram.me/joinchat/Bn4ixj84FIZVkwhk2jag6A)
	
## Telegram Channel

Join the [News channel](https://t.me/pyTelegramBotAPI). Here we will post releases and updates.

**Want to have your bot listed here? Just make a pull request. Only bots with public source code are accepted.**
