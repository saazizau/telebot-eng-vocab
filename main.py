import telebot
import json
import pandas as pd
import random
import EngVocab
from function import isCreated, isStarted, isAllAnswered, scoreData
random.seed(random.randint(0,100))

from telebot import types

# Read Environtment]============
json_file = 'env.json'
data = None;

def get_update(id):
    with open(json_file, 'r') as f:
        data = json.load(f) 
        for i, yours in enumerate(data['Games']):
            if(yours['Id'] == id):
                return yours
            
        data = {
            "Id":0,
            "Player":[],
            "Playing":0,
            "Score":[],
            "History": [{
                "Id":[],
                "Questions":[],
                "Answers":[],
                "Keys":[],
                "Scores":[]
            }]
        }
        return data

def set_update(id, data):
    database = None
    
    with open('env.json', 'r') as f:
        database = json.load(f)
    
    for i, yours in enumerate(database['Games']):
        if(yours['Id'] == id):
            database['Games'][i] = data
        elif i == len(database['Games'])-1:
            database['Games'].append(data)
    
    with open(json_file, 'w') as f:
        json.dump(database, f, indent=4)
        
def reset(id):
    with open(json_file, 'r') as f:
        data = json.load(f) 
        for i, yours in enumerate(data['Games']):
            if(yours['Id'] == id):
                del data['Games'][i]

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)       
#================================

bot = telebot.TeleBot("6614100466:AAG9wd4UYkESzlKywktzrl9q8CIgwZii9qw", parse_mode=None)

#===============[BOT UMUM]=====================
@bot.message_handler(commands=["help", "hello"])
def send_help_message(msg):
    bot.reply_to(msg, "Minta tolong?")
#==============================================

#===================[GAME]=====================
@bot.message_handler(commands=["create_eng_vocab"])
def send_start_message(msg):
    data = get_update(msg.chat.id)
    
    if(isCreated(data)):
        player = "";
        for i, value in enumerate(data['Player']):
            player += f"\n{i+1}. {value}"
            
        message = f"*GAME ENGLISH VOCAB*\n==============\n{player}\n\n==============\n/join_eng_vocab untuk bergabung!"
        bot.send_message(chat_id=msg.chat.id, text=message) 
        bot.reply_to(msg, f"Game sudah dibuat oleh {data['Player'][0]}\nUntuk bergabung silahkan ketik /join_eng_vocab")
        return
    
    data['Playing'] = 0
    data['Player'] = [msg.from_user.username]
    data['Score'] = [0]
    data['Id'] = msg.chat.id
    set_update(data['Id'], data)
    message = f"*GAME ENGLISH VOCAB*\n==============\n\nPlayer:\n1. {msg.from_user.username}\n\n==============\n/join_eng_vocab untuk bergabung!"
    bot.send_message(chat_id=msg.chat.id, text=message)
        

@bot.message_handler(commands=["join_eng_vocab"])
def send_start_message(msg):
    data = get_update(msg.chat.id)
    
    if(not isCreated(data)):
        bot.reply_to(msg, f"Silahkan buat ruang game terlebih dahulu!\n/create_eng_vocab")
        return    
    
    if (msg.from_user.username not in data["Player"]):
        data['Player'].append(msg.from_user.username)
        data['Score'].append(0)
        data['History'].append(
            {
                "Id":[],
                "Questions": [],
                "Answers": [],
                "Keys": [],
                "Scores": []
            }
        )
        set_update(data['Id'], data)
        
        player = "";
        for i, value in enumerate(data['Player']):
            player += f"\n{i+1}. {value}"
            
        message = f"*GAME ENGLISH VOCAB*\n==============\n{player}\n\n==============\n/join_eng_vocab untuk bergabung!"
        bot.send_message(chat_id=msg.chat.id, text=message)        
    else:
        bot.reply_to(msg, f"Anda sudah bergabung dalam game!")

@bot.message_handler(commands=["start_eng_vocab"])
def send_start_message(msg):
    data = get_update(msg.chat.id)
    
    if(not isCreated(data)):
        bot.reply_to(msg, f"Silahkan buat ruang game terlebih dahulu!\n/create_eng_vocab")
        return   
    
    if(isStarted(data)):
        bot.send_message(chat_id=msg.chat.id, text=f"Game sudah dimulai.\nSilahkan {data['Player'][0]} untuk bisa mengakhiri game terlebih dahulu! \n/end_eng_vocab")   
        return
    
    if (msg.from_user.username == data["Player"][0]):
        data['Playing'] = 1
        set_update(data['Id'],data)
        message = f"Game English Vocab telah dimulai\n1. /next_eng_vocab : Untuk pertanyaan selanjutnya.\n2. /score_eng_vocab : Untuk mengecek skor pemain.\n3. /rekap_eng_vocab : Untuk merekap pertanyaan dan jawaban anda sebelumnya.\nHave Fun! :D"
        bot.send_message(chat_id=msg.chat.id, text=message)        
    else:
        bot.send_message(chat_id=msg.chat.id, text=f"Hanya {data['Player'][0]} yang bisa memulai game")           

@bot.message_handler(commands=["end_eng_vocab"])
def send_end_message(msg):
    data = get_update(msg.chat.id)
    if(data['Playing'] == 1):
        if (msg.from_user.username == data["Player"][0]):
            winner = ""
            for i, value in enumerate(data['Player']):
                if(data['Score'][i] == max(data['Score'])):
                    winner += f"Selamat kepada pemenang! @{value} dengan perolehan poin {data['Score'][i]}."
            reset(data['Id'])
            message = f"Game telah diakhiri\n{winner}\nTerima kasih sudah bermain :D"
            bot.send_message(chat_id=msg.chat.id, text=message)        
        else:
            bot.send_message(chat_id=msg.chat.id, text=f"Hanya {data['Player'][0]} yang bisa mengakhiri game")         
    else:
        bot.send_message(chat_id=msg.chat.id, text=f"Game belum dimulai.\nSilahkan {data['Player'][0]} untuk bisa memulai game! \n/start_eng_vocab")
    
@bot.message_handler(commands=["next_eng_vocab"])
def send_next_message(msg):
    data = get_update(msg.chat.id)
    
    if(not isCreated(data)):
        bot.reply_to(msg, f"Silahkan buat ruang game terlebih dahulu!\n/create_eng_vocab")
        return 
      
    if(not isStarted(data)):
        bot.reply_to(msg, f"Game belum dimulai.\nSilahkan {data['Player'][0]} untuk dapat memulai game terlebih dahulu!\n/start_eng_vocab")
        return 
    
    if(not isAllAnswered(data)):
        bot.reply_to(msg, f"Semua player harus menjawab terlebih dahulu! ^_^")
        return 
    
    data_soal = EngVocab.getSoal()
    no_soal = random.randint(0, data_soal.shape[0]-1)
    
    soal = data_soal['Question Text'][no_soal]
    jawaban = random.randint(1,4)
    option = ["","","",""]
    
    inSoal = 1
    for i in range(0,4):
        if i == (jawaban-1):
            option[i] = data_soal['Option 4'][no_soal]
        else:
            option[i] = data_soal[f'Option {inSoal}'][no_soal]
            inSoal += 1
    
    for i, value in enumerate(data['History']):
        data['History'][i]['Id'].append(msg.id)
        data['History'][i]['Questions'].append(soal)
        data['History'][i]['Keys'].append(option[(jawaban-1)])
    
    set_update(data['Id'],data)
        
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(option[0], callback_data=option[0])
    btn2 = types.InlineKeyboardButton(option[1], callback_data=option[1])
    btn3 = types.InlineKeyboardButton(option[2], callback_data=option[2])
    btn4 = types.InlineKeyboardButton(option[3], callback_data=option[3])
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(chat_id=msg.chat.id, text=soal, reply_markup=markup)
    
    player = "";
    for i, value in enumerate(data['Player']):
        player += f"\n{i+1}. {value}\t (Belum)"
            
    bot.send_message(chat_id=msg.chat.id, text=f"Menunggu jawaban: {player}")

@bot.message_handler(commands=["score_eng_vocab"])
def send_score_message(msg):
    data = get_update(msg.chat.id)
    
    if(not isCreated(data)):
        bot.reply_to(msg, f"Silahkan buat ruang game terlebih dahulu!\n/create_eng_vocab")
        return   
    
    if(not isStarted(data)):
        bot.send_message(chat_id=msg.chat.id, text=f"Game belum dimulai.\nSilahkan {data['Player'][0]} untuk bisa memulai game terlebih dahulu! \n/start_eng_vocab")   
        return    
    
    bot.send_message(chat_id=msg.chat.id, text=scoreData(data, False))

@bot.message_handler(commands=["recap_eng_vocab"])
def send_recap_message(msg):
    data = get_update(msg.chat.id)
    
    if(not isCreated(data)):
        bot.reply_to(msg, f"Silahkan buat ruang game terlebih dahulu!\n/create_eng_vocab")
        return   
    
    if(not isStarted(data)):
        bot.send_message(chat_id=msg.chat.id, text=f"Game belum dimulai.\nSilahkan {data['Player'][0]} untuk bisa memulai game terlebih dahulu! \n/start_eng_vocab")   
        return

    recap = ""
    username = msg.from_user.username
    for i, value in enumerate(data['Player']):
        if(username == value):
            recap += f"Rekap dari @{username}:\n"
            for j in range(0, len(data['History'][i]['Questions'])):
                recap += f"\n{j+1}. Q: {data['History'][i]['Questions'][j]} J: {data['History'][i]['Answers'][j]} K: {data['History'][i]['Keys'][j]} S: {data['History'][i]['Scores'][j]}"
            recap += "\n\nKeterangan:\nQ: Pertanyaan.\nJ: Jawaban anda.\nK: Kunci jawaban.\nS: Skor anda."
            recap += f"\n===========================\nTotal skor: {sum(data['History'][i]['Scores'])}"
            
    bot.send_message(chat_id=msg.chat.id, text=recap)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    id_game = call.message.json['chat']['id']
    id_pertanyaan = call.message.id
    username = call.from_user.username
    
    data = get_update(id_game)
    
    for i, value in enumerate(data['Player']):
        if(username == value):
            if(len(data['History'][i]['Answers']) == len(data['History'][i]['Id'])):
                bot.send_message(chat_id=id_game, text=f"@{username} anda sudah menjawab, tidak bisa diubah")
                return
    
    player = ""
    done = True
     
    for i, value in enumerate(data['Player']):
        if(username == value):
            data['History'][i]['Answers'].append(call.data)
            
            data = set_update(id_game, data)
            data = get_update(id_game)
            
            skor_temp = 0
            if(data['History'][i]['Answers'][-1] == data['History'][i]['Keys'][-1]):
                skor_temp = 1
            data['History'][i]['Scores'].append(skor_temp)
            data['Score'][i] += skor_temp
            
    data = set_update(id_game, data)
    data = get_update(id_game)
    
    for i, value in enumerate(data['History']):
        no_soal = len(value['Questions'])-1
        if(len(value['Answers'])-1 != no_soal):
            done = False
            player += f"\n{i+1}. {data['Player'][i]}\t (Belum)"
            continue
        player += f"\n{i+1}. {data['Player'][i]}\t (Sudah)"
    
    data = set_update(id_game, data)
    data = get_update(id_game)
    
    bot.edit_message_text(text=f"Menyimpan jawaban {username}",chat_id=id_game, message_id=(id_pertanyaan+1), reply_markup=None)
    bot.edit_message_text(text=f"Menunggu jawaban: {player}",chat_id=id_game, message_id=(id_pertanyaan+1), reply_markup=None)
    
    if(done):
        bot.send_message(chat_id=id_game, text=f"Jawabannya adalah {data['History'][0]['Keys'][-1]}")
        bot.send_message(chat_id=id_game, text=scoreData(data, True))
        
@bot.message_handler(commands=["show_eng_vocab"])
def send_show_message(msg):
    bot.send_message(chat_id=msg.chat.id, text=EngVocab.getAllSoal())

@bot.message_handler(commands=["store_eng_vocab"])
def send_show_message(msg):
    bot.send_message(chat_id=msg.chat.id, text=EngVocab.storeSoal(msg.json['text']))
                    
@bot.message_handler(commands=["test"])
def handle_test(msg):
    id_msg = msg.id
    id_chat = msg.chat.id
    print(id_msg, " ", id_chat)
    bot.send_message(chat_id=msg.chat.id, text="MANTAP")
    bot.edit_message_text(text="Edited",chat_id=id_chat, message_id=824, reply_markup=None)
#==============================================
print("Running...")
bot.polling()