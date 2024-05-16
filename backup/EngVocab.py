import pandas as pd 
import re
import random
random.seed(random.randint(0,100))

def getSoal():
    dataVocab = """ 
        02/02/24 23.14 - Kak Kurnia Setyanti: Trade | berdagang
        03/02/24 00.12 - Sabrina Aziz Aulia: burdensome | berat
        03/02/24 09.45 - Kak Kurnia Setyanti: Ignite | menyala
        03/02/24 09.57 - Sabrina Aziz Aulia: nudge | dorongan
        03/02/24 09.59 - Sabrina Aziz Aulia: deprive | mencabut
        03/02/24 09.59 - Sabrina Aziz Aulia: stance | pendirian
        03/02/24 12.07 - Sabrina Aziz Aulia: appeal | banding | appeal to : mengajukan banding ke
        03/02/24 21.14 - Sabrina Aziz Aulia: fainted | pingsan
        04/02/24 17.53 - Sabrina Aziz Aulia: gaze | tatapan
        04/02/24 21.01 - Kak Kurnia Setyanti: Prestige | martabat
        04/02/24 21.08 - Kak Kurnia Setyanti: Enormous | sangat besar
        04/02/24 21.09 - Kak Kurnia Setyanti: Sweltering | panas terik
        04/02/24 21.18 - Kak Kurnia Setyanti: Hazard | Bahaya
        04/02/24 21.18 - Kak Kurnia Setyanti: Whimsical | aneh
        04/02/24 21.32 - Kak Kurnia Setyanti: Leveraging | memanfaatkan
        04/02/24 22.34 - Kak Kurnia Setyanti: Reciting | membacakan
        05/02/24 10.06 - Kak Kurnia Setyanti: Terrific | hebat
        05/02/24 10.38 - Kak Kurnia Setyanti: Spotty | tidak rapi
        05/02/24 10.48 - Kak Kurnia Setyanti: Verve | semangat
        05/02/24 10.56 - Kak Kurnia Setyanti: Inhibit | mencegah
        05/02/24 10.56 - Kak Kurnia Setyanti: Embargo | larangan
        05/02/24 10.57 - Kak Kurnia Setyanti: Rigid | kaku
        05/02/24 11.23 - Kak Kurnia Setyanti: Predicaments | kondisi yang sulit
        05/02/24 11.24 - Kak Kurnia Setyanti: Reminiscent | mengingatkan
        22/02/24 13.08 - Kak Kurnia Setyanti: Retarded | terbelakang
        22/02/24 13.22 - Kak Kurnia Setyanti: Astringent | zat
        """.title()

    vocab_pra_clear = []

    pattern = r'(?<=: ).*?(?=\n|$)'

    matches = re.findall(pattern, dataVocab)

    vocab_pra_clear = []
    if matches:
        for i, match in enumerate(matches):
            vocab_pra_clear.append(match)
    else:
        print("No matches found.")

    vocab_clear = [[],[]]
    for i, value in enumerate(vocab_pra_clear):
        split = value.split(' | ')
        vocab_clear[0].append(split[0])
        vocab_clear[1].append(split[1])

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
    dataVocab = """ 
        02/02/24 23.14 - Kak Kurnia Setyanti: Trade | berdagang
        03/02/24 00.12 - Sabrina Aziz Aulia: burdensome | berat
        03/02/24 09.45 - Kak Kurnia Setyanti: Ignite | menyala
        03/02/24 09.57 - Sabrina Aziz Aulia: nudge | dorongan
        03/02/24 09.59 - Sabrina Aziz Aulia: deprive | mencabut
        03/02/24 09.59 - Sabrina Aziz Aulia: stance | pendirian
        03/02/24 12.07 - Sabrina Aziz Aulia: appeal | banding | appeal to : mengajukan banding ke
        03/02/24 21.14 - Sabrina Aziz Aulia: fainted | pingsan
        04/02/24 17.53 - Sabrina Aziz Aulia: gaze | tatapan
        04/02/24 21.01 - Kak Kurnia Setyanti: Prestige | martabat
        04/02/24 21.08 - Kak Kurnia Setyanti: Enormous | sangat besar
        04/02/24 21.09 - Kak Kurnia Setyanti: Sweltering | panas terik
        04/02/24 21.18 - Kak Kurnia Setyanti: Hazard | Bahaya
        04/02/24 21.18 - Kak Kurnia Setyanti: Whimsical | aneh
        04/02/24 21.32 - Kak Kurnia Setyanti: Leveraging | memanfaatkan
        04/02/24 22.34 - Kak Kurnia Setyanti: Reciting | membacakan
        05/02/24 10.06 - Kak Kurnia Setyanti: Terrific | hebat
        05/02/24 10.38 - Kak Kurnia Setyanti: Spotty | tidak rapi
        05/02/24 10.48 - Kak Kurnia Setyanti: Verve | semangat
        05/02/24 10.56 - Kak Kurnia Setyanti: Inhibit | mencegah
        05/02/24 10.56 - Kak Kurnia Setyanti: Embargo | larangan
        05/02/24 10.57 - Kak Kurnia Setyanti: Rigid | kaku
        05/02/24 11.23 - Kak Kurnia Setyanti: Predicaments | kondisi yang sulit
        05/02/24 11.24 - Kak Kurnia Setyanti: Reminiscent | mengingatkan
        22/02/24 13.08 - Kak Kurnia Setyanti: Retarded | terbelakang
        22/02/24 13.22 - Kak Kurnia Setyanti: Astringent | zat
        """.title()

    vocab_pra_clear = []

    pattern = r'(?<=: ).*?(?=\n|$)'

    matches = re.findall(pattern, dataVocab)

    vocab_pra_clear = []
    if matches:
        for i, match in enumerate(matches):
            vocab_pra_clear.append(match)
    else:
        print("No matches found.")

    vocab_clear = [[],[]]
    vocab = "Entire Vocab:"
    
    for i, value in enumerate(vocab_pra_clear):
        split = value.split(' | ')
        vocab_clear[0].append(split[0])
        vocab_clear[1].append(split[1])
        
    for i, value in enumerate(vocab_clear[0]):
        vocab += f"\n{i+1}. {vocab_clear[0][i]} | {vocab_clear[1][i]}"

    print(vocab_clear)
    return (vocab)    

