import pandas as pd 
import re
import random
import json
random.seed(random.randint(0,100))

def getSoal():
    json_file = "eng_vocab.json"
    with open(json_file, 'r') as f:
        vocab_clear = json.load(f)['data']

    data_quizizz = {
        'Question Text': [],
        'Option 1': [],
        'Option 2': [],
        'Option 3': [],
        'Option 4': [],
    }

    tipe_soal = random.randint(0,1)
    jawaban_soal = [None] * 3

    for i, value in enumerate(vocab_clear[0]):
        j = 0
        while j < 3:
            temp = random.randint(0,len(vocab_clear[0]) - 1)
            if (temp not in jawaban_soal) and (temp != i):
                jawaban_soal[j] = temp 
                j += 1
        data_quizizz['Question Text'].append(vocab_clear[1 - tipe_soal][i])
        data_quizizz['Option 1'].append(vocab_clear[tipe_soal][jawaban_soal[0]])
        data_quizizz['Option 2'].append(vocab_clear[tipe_soal][jawaban_soal[1]])
        data_quizizz['Option 3'].append(vocab_clear[tipe_soal][jawaban_soal[2]])
        data_quizizz['Option 4'].append(vocab_clear[tipe_soal][i])

    return pd.DataFrame(data_quizizz)

def getAllSoal():
    json_file = "eng_vocab.json"
    with open(json_file, 'r') as f:
        vocab_clear = json.load(f)['data']
        
    vocab = "Entire Vocab:"
        
    for i, value in enumerate(vocab_clear[0]):
        vocab += f"\n{i+1}. {vocab_clear[0][i]} | {vocab_clear[1][i]}"

    return (vocab)   

def storeSoal(dataVocab):
    dataVocab = dataVocab.title()

    vocab_pra_clear = []

    pattern = r'(?<=: ).*?(?=\n|$)'

    matches = re.findall(pattern, dataVocab)

    vocab_pra_clear = []
    if matches:
        for i, match in enumerate(matches):
            vocab_pra_clear.append(match)
    else:
        return "Harap masukkan sesuai format!\n[/store_eng_vocab : {English} | {Indonesia}]"

    vocab_clear = [[],[]]
    for i, value in enumerate(vocab_pra_clear):
        split = value.split(' | ')
        vocab_clear[0].append(split[0])
        vocab_clear[1].append(split[1])

    json_file = "eng_vocab.json"
    with open(json_file, 'r') as f:
        database = json.load(f)
    
    database['data'][0].append(vocab_clear[0][-1])
    database['data'][1].append(vocab_clear[1][-1])
      
    with open(json_file, 'w') as f:
        json.dump(database, f, indent=4)

    return f"Kosakata baru telah disimpan! [ {database['data'][0][-1]} | {database['data'][1][-1]} ]"