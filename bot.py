#!/usr/bin/env python3

import time, sys, telepot, subprocess
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton



TOKEN = ''
message_with_inline_keyboard = None
process= None

#choose form eth0/wlan0 or other interfaces

network_interface='eth0'

def connect(server_ip):
    global status
    global network_interface
    global connected
    global process
    if process != None:
        os.system('sudo killall -9 lan-play')
        process = None
    process = subprocess.Popen("sudo" + "  ./lan-play " + "--relay-server-addr " + server_ip + " --netif " + network_interface + " &", shell=True)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        bot.sendMessage(chat_id, text='Use /servers')
        return
    if msg['text'] == "/start":
        bot.sendMessage(chat_id, text='Hi, write /servers to list the servers.')
    command = msg['text']
    if command == '/servers':
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text='1)  35.236.10.223:11451 US 🇺🇸              ', callback_data='1')],
                     [InlineKeyboardButton(text='2)  nxlan.duckdns.org:11451 US 🇺🇸          ', callback_data='2')],
                     [InlineKeyboardButton(text='3)  switch.lan-play.com:11451 FR 🇫🇷        ', callback_data='3')],
                     [InlineKeyboardButton(text='4)  relay1.fadx.co.uk:11451 EU 🇬🇧          ', callback_data='4')],
                     [InlineKeyboardButton(text='5)  relay2.fadx.co.uk:11451  EU 🇬🇧         ', callback_data='5')],
                     [InlineKeyboardButton(text='6)  switch.glaciergaming.co.uk:11451 EU 🇬🇧 ', callback_data='6')],
                     [InlineKeyboardButton(text='7)  switch.homelab.tech:11451 EU 🇬🇧        ', callback_data='7')],
                     [InlineKeyboardButton(text='8)  bandits.duckdns.org:11451 EU 🇪🇺        ', callback_data='8')],
                     [InlineKeyboardButton(text='9)  memehouse.de:11451 EU 🇩🇪               ', callback_data='9')],
                     [InlineKeyboardButton(text='10) relay.it-cybergate.club:11451 EU 🇩🇪    ', callback_data='10')],
                     [InlineKeyboardButton(text='11) slp.rush-hour.wo.tc:11451 KR 🇰🇷        ', callback_data='11')],
                     [InlineKeyboardButton(text='12) lithium2g.ddns.net:11451 AU 🇦🇺         ', callback_data='12')],
                 ])
        global message_with_inline_keyboard
        message_with_inline_keyboard = bot.sendMessage(chat_id, 'Select server to connect:', reply_markup=markup)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)
    global status

    if data == '1':
        bot.sendMessage(from_id, text='Connected to 35.236.10.223:11451 US 🇺🇸')
        connect('35.236.10.223:11451')
    elif data == '2':
        bot.sendMessage(from_id, text='Connected to nxlan.duckdns.org:11451 US 🇺🇸')
        connect('nxlan.duckdns.org:11451')
    elif data == '3':
        bot.sendMessage(from_id, text='Connected to switch.lan-play.com:11451 FR 🇫🇷')
        connect('switch.lan-play.com:11451')
    elif data == '4':
        bot.sendMessage(from_id, text='Connected to relay1.fadx.co.uk:11451 EU 🇬🇧')
        connect('relay1.fadx.co.uk:11451')
    elif data == '5':
        bot.sendMessage(from_id, text='Connected to relay2.fadx.co.uk:11451  EU 🇬🇧')
        connect('relay2.fadx.co.uk:11451')
    elif data == '6':
        bot.sendMessage(from_id, text='Connected to switch.glaciergaming.co.uk:11451 EU 🇬🇧')
        connect('switch.glaciergaming.co.uk:11451')
    elif data == '7':
        bot.sendMessage(from_id, text='Connected to switch.homelab.tech:11451 EU 🇬🇧')
        connect('switch.homelab.tech:11451')
    elif data == '8':
        bot.sendMessage(from_id, text='Connected to bandits.duckdns.org:11451 EU 🇪🇺')
        connect('bandits.duckdns.org:11451')
    elif data == '9':
        bot.sendMessage(from_id, text='Connected to memehouse.de:11451 EU 🇩🇪')
        connect('memehouse.de:11451')
    elif data == '10':
        bot.sendMessage(from_id, text='Connected to relay.it-cybergate.club:11451 EU 🇩🇪')
        connect('relay.it-cybergate.club:11451')
    elif data == '11':
        bot.sendMessage(from_id, text='Connected to slp.rush-hour.wo.tc:11451 KR 🇰🇷')
        connect('slp.rush-hour.wo.tc:11451')
    elif data == '12':
        bot.sendMessage(from_id, text='Connected to lithium2g.ddns.net:11451 AU 🇦🇺')
        connect('lithium2g.ddns.net:11451')




bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  }).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
