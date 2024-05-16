
def isCreated(data):
    if(data['Id'] != 0):
        return True
    return False

def isStarted(data):
    if(data['Playing'] == 1):
        return True
    return False

def isAllAnswered(data):
    for i, value in enumerate(data['History']):
        no_soal = len(value['Questions'])-1
        if(len(value['Answers'])-1 != no_soal):
            return False
    return True

def scoreData(data, semua): 
    player = ""
    for i, value in enumerate(data['Player']):
        temp = f"+{data['History'][i]['Scores'][-1]}" if semua else ""
        player += f"\n{i+1}. {value} {temp} ({data['Score'][i]})"
    return f"Perolehan poin: {player}\n\nPertanyaan selanjutnya: /next_eng_vocab"                        

        
        