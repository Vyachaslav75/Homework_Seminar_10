import telebot
from telebot import types
# from keyboa import Keyboa

keys = [['7', '8', '9', 'C'],
        ['4', '5', '6', '/'],
        ['1', '2', '3', '+'],
        ['0', '.', '-', '*'],
        ['%', '//', '=']]

signs = ['C', '/', '+', '-', '*', '%', '//']  # , '=']
user_input1 = ''
user_input2 = ''
sign = ''
flag_num = 1
flag_compl = 0

bot = telebot.TeleBot("5897991903:AAF3jvA8gx6jOhtJrEVv1B6qboK_-Pgh63o")


@bot.message_handler(commands=['start'])  # вызов функции по команде в списке
def start(message):
    mrk = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    key1 = telebot.types.KeyboardButton("7")
    key2 = telebot.types.KeyboardButton("8")
    key3 = telebot.types.KeyboardButton("9")
    #key4 = telebot.types.KeyboardButton("C")
    key5 = telebot.types.KeyboardButton("4")
    key6 = telebot.types.KeyboardButton("5")
    key7 = telebot.types.KeyboardButton("6")
    key8 = telebot.types.KeyboardButton("/")
    key9 = telebot.types.KeyboardButton("1")
    key10 = telebot.types.KeyboardButton("2")
    key11 = telebot.types.KeyboardButton("3")
    key12 = telebot.types.KeyboardButton("+")
    #key13 = telebot.types.KeyboardButton("0")
    #key14 = telebot.types.KeyboardButton(".")
    #key15 = telebot.types.KeyboardButton("-")
    #key16 = telebot.types.KeyboardButton("*")
    mrk.add(key1, key2, key3) #, key4)
    mrk.add(key5, key6, key7, key8)
    mrk.add(key9, key10, key11, key12)
    #mrk.add(key13, key14, key15, key16)
    if flag_compl == 0:
        key13 = telebot.types.KeyboardButton("0")
        key14 = telebot.types.KeyboardButton(".")
        key15 = telebot.types.KeyboardButton("-")
        key16 = telebot.types.KeyboardButton("*")
        key17 = telebot.types.KeyboardButton("%")
        key18 = telebot.types.KeyboardButton("//")
        key19 = telebot.types.KeyboardButton("=")
        key20 = telebot.types.KeyboardButton("compl")
        mrk.add(key13, key14, key15, key16)
        mrk.add(key17, key18, key19, key20)
        bot.send_message(
        message.chat.id, "калькулятор вещественных чисел", reply_markup=mrk)
    else:
        key13 = telebot.types.KeyboardButton("0")
        key14 = telebot.types.KeyboardButton("(")
        key15 = telebot.types.KeyboardButton("-")
        key16 = telebot.types.KeyboardButton("*")
        key17 = telebot.types.KeyboardButton("j")
        key18 = telebot.types.KeyboardButton("=")
        key19 = telebot.types.KeyboardButton(")")
        key20 = telebot.types.KeyboardButton("float")
        mrk.add(key13, key14, key15, key16)
        mrk.add(key17, key18, key19, key20)
        bot.send_message(
        message.chat.id, "калькулятор комплексных чисел, числа вводятся в скобках", reply_markup=mrk)

    # mrk.add(key1, key2, key3, key4)
    # mrk.add(key5, key6, key7, key8)
    # mrk.add(key9, key10, key11, key12)
    # mrk.add(key13, key14, key15, key16)
    # mrk.add(key17, key18, key19, key20)
    #bot.send_message(
    #    message.chat.id, "калькулятор", reply_markup=mrk)
    #bot.register_next_step_handler(message, user_input)
    bot.register_next_step_handler(message, start_input)

def restart():
    global user_input1
    global user_input2
    global sign
    user_input1 = ''
    user_input2 = ''
    sign = ''
    
    

def controller(message):
    global user_input1
    global user_input2
    global sign
    global flag_num
    if flag_compl == 0:
        x = float(user_input1)
        y = float(user_input2)
    else:
        x = complex(user_input1[1:-1])
        y = complex(user_input2[1:-1])
    if sign == '+':
        res = x+y
    elif sign == '-':
        res = x-y
    elif sign == '*':
        res = x*y
    elif sign == '/':
        res = x/y
    elif sign == '//':
        res = x//y
    elif sign == '%':
        res = x % y
    with open('log.txt', 'a') as file:
        file.write(f'{user_input1} {sign} {user_input2} = {res} \n')
    user_input1 = ''
    user_input2 = ''
    sign = ''
    flag_num = 1
    bot.send_message(message.chat.id, text=str(res))


@bot.message_handler(content_types=['text'])
def start_input(message):
    if flag_compl == 1:
        user_input_complex(message)
    else:
        user_input(message)



def user_input(message):
    global user_input1
    global user_input2
    global sign
    global flag_num
    global flag_compl
    compl=['float', 'compl']
    if flag_num == 1 and message.text not in signs and message.text != '=' and message.text not in compl:
        user_input1 += message.text
        bot.send_message(message.chat.id, text=user_input1)
    elif message.text in signs:
        sign = message.text
        flag_num = 2
        bot.send_message(message.chat.id, text=user_input1+sign)
    elif flag_num == 2 and message.text not in signs and message.text != '=':
        user_input2 += message.text
        bot.send_message(message.chat.id, text=user_input1+sign+user_input2)
    elif len(user_input1) > 0 and len(user_input2) > 0 and len(sign) > 0 and message.text == '=':
        controller(message)
    if message.text == 'compl' and flag_compl == 0:
        flag_compl = 1
        restart()
        start(message)


def user_input_complex(message):
    global user_input1
    global user_input2
    global sign
    global flag_num
    global flag_compl
    compl=['float', 'compl']
    #if flag_num == 1 and message.text not in signs and message.text != '=' and message.text not in compl:
    if flag_num == 1 and user_input1[-1:]!=')' and message.text != '=' and message.text not in compl:
        user_input1 += message.text
        bot.send_message(message.chat.id, text=user_input1)
    elif message.text in signs and flag_num==1:
        sign = message.text
        #user_input1=user_input1[1:-1]
        flag_num = 2
        bot.send_message(message.chat.id, text=user_input1+sign)
    #elif flag_num == 2 and message.text not in signs and message.text != '=':
    elif flag_num == 2 and user_input2[-1:]!=')' and message.text != '=' and message.text not in compl:
        user_input2 += message.text
        bot.send_message(message.chat.id, text=user_input1+sign+user_input2)
    elif len(user_input1) > 0 and len(user_input2) > 0 and len(sign) > 0 and message.text == '=':
        controller(message)
    if message.text == 'float' and flag_compl == 1:
        flag_compl = 0
        restart()
        start(message)


bot.infinity_polling()
