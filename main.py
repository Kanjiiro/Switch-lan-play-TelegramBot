import subprocess
import sys
import time
import threading
import random
import telepot
import json
import os
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent


message_with_inline_keyboard = None

servers = []




def refresh_servers():
    ok = False
    try:
        output = subprocess.check_output('python3 get_servers.py', shell=True)
    except subprocess.CalledProcessError:
        None
    finally:
        if output != "Done ":
            ok = True
        return ok


def make_makup():
    global servers
    if len(servers) == 0:
        with open('servers.json') as json_file:
            data = json.load(json_file)
            for p in data['server']:
                servers.append([InlineKeyboardButton(text='{0} {1} {2}'.format(
                    p['ip'], p['ping'], p['flag']), callback_data='{0}'.format(p['ip']))])
        servers.append([InlineKeyboardButton(
            text='Back', callback_data='back')])
    else:
        return


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    global message_with_inline_keyboard
    if content_type != 'text':
        return

    command = msg['text']

    if command == '/start':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text='Refresh', callback_data='refresh'),
             dict(text='Servers', callback_data='servers')],
        ])

        message_with_inline_keyboard = bot.sendMessage(
            chat_id, 'Hi, choose Refresh to update the servers online,or Servers to get them', reply_markup=markup)

def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

    global message_with_inline_keyboard
    if data == 'servers':
        make_makup()
        markup = InlineKeyboardMarkup(inline_keyboard=servers)
        bot.editMessageText(telepot.message_identifier(
            message_with_inline_keyboard), 'SERVER IP | PING | REGION', reply_markup=markup)
        
    elif data == 'back':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text='Refresh', callback_data='refresh'),
             dict(text='Servers', callback_data='servers')],
        ])
        bot.editMessageText(telepot.message_identifier(
            message_with_inline_keyboard), 'Hi, choose Refresh to update the servers online,or Servers to get them', reply_markup=markup)
    elif data == 'refresh':
        if refresh_servers() == True:
            markup = InlineKeyboardMarkup(inline_keyboard=[[dict(text='Servers', callback_data='servers')],
                                                           ])
            bot.editMessageText(telepot.message_identifier(
                message_with_inline_keyboard), 'Server list updated', reply_markup=markup)
    elif data=='disconnect':
        os.system('sudo killall lan-play-linux')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [ dict(text='Servers', callback_data='servers')],
        ])
        bot.editMessageText(telepot.message_identifier(
            message_with_inline_keyboard), 'Disconnected', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [dict(text='Disconnect', callback_data='disconnect'),
             dict(text='Servers', callback_data='servers')],
        ])
        
        subprocess.Popen(["sudo ./lan-play-linux --relay-server-addr {0}".format(data)], stdout=subprocess.PIPE,stderr=None,shell=True)
        bot.editMessageText(telepot.message_identifier(
            message_with_inline_keyboard),'You are connected',  reply_markup=markup)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(
        msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)

TOKEN=''
try:
    with open('token.txt','r+') as f:
        read=f.read()
        if len(read)<45:
            print('error')
        else:
            TOKEN=read[-45:]
except FileNotFoundError:
    with open("token.txt",'w+')as f:
        f.write("Token={0}".format(sys.argv[1]))
    TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
