import nltk
import re

def readVocab(indo_vocab, sunda_vocab):
    indo_filename = 'indonesia.txt'
    sunda_filename = 'sunda.txt'
    indo_file = open(indo_filename, 'r')
    sunda_file = open(sunda_filename, 'r')
    indo_read = indo_file.readlines()
    sunda_read = sunda_file.readlines()
    indo_file.close()
    sunda_file.close()
    vocab1_sunda = []
    vocab2_sunda = []
    vocab3_sunda = []
    vocab1_indo = []
    vocab2_indo = []
    vocab3_indo = []
    vocab4_indo = []

    for line in sunda_read:
        vocab = []
        indo = ""
        sunda = ""
        token = nltk.word_tokenize(line)
        j = 0
        for i in range (len(token)):
            if (token[i] == "="):
                j = i
        if (j == 1):
            sunda += token[0]
            indo += token[2]
            if (len(token) > 3):
                for i in range(len(token) - 3):
                    indo += ' ' + token[i + 3]
            vocab.append(sunda)
            vocab.append(indo)
            vocab1_sunda.append(vocab)
        elif (j == 2):
            sunda += token[0] + ' ' + token[1]
            indo += token[3]
            if (len(token) > 4):
                for i in range(len(token) - 4):
                    indo += ' ' + token[i + 4]
            vocab.append(sunda)
            vocab.append(indo)
            vocab2_sunda.append(vocab)
        elif (j == 3):
            sunda += token[0] + ' ' + token[1] + ' ' + token[2]
            indo += token[4]
            if (len(token) > 5):
                for i in range(len(token) - 5):
                    indo += ' ' + token[i + 5]
            vocab.append(sunda)
            vocab.append(indo)
            vocab3_sunda.append(vocab)

    for line in indo_read:
        vocab = []
        indo = ""
        sunda = ""
        token = nltk.word_tokenize(line)
        j = 0
        for i in range (len(token)):
            if (token[i] == "="):
                j = i
        if (j == 1):
            indo += token[0]
            sunda += token[2]
            if (len(token) > 3):
                for i in range(len(token) - 3):
                    sunda += ' ' + token[i + 3]
            vocab.append(indo)
            vocab.append(sunda)
            vocab1_indo.append(vocab)
        elif (j == 2):
            indo += token[0] + ' ' + token[1]
            sunda += token[3]
            if (len(token) > 4):
                for i in range(len(token) - 4):
                    sunda += ' ' + token[i + 4]
            vocab.append(indo)
            vocab.append(sunda)
            vocab2_indo.append(vocab)
        elif (j == 3):
            indo += token[0] + ' ' + token[1] + ' ' + token[2]
            sunda += token[4]
            if (len(token) > 5):
                for i in range(len(token) - 5):
                    sunda += ' ' + token[i + 5]
            vocab.append(indo)
            vocab.append(sunda)
            vocab3_indo.append(vocab)
        elif (j == 4):
            indo += token[0] + ' ' + token[1] + ' ' + token[2] + ' ' + token[3]
            sunda += token[5]
            if (len(token) > 6):
                for i in range(len(token) - 6):
                    sunda += ' ' + token[i + 6]
            vocab.append(indo)
            vocab.append(sunda)
            vocab4_indo.append(vocab)

    indo_vocab.append(vocab1_indo)
    indo_vocab.append(vocab2_indo)
    indo_vocab.append(vocab3_indo)
    indo_vocab.append(vocab4_indo)
    sunda_vocab.append(vocab1_sunda)
    sunda_vocab.append(vocab2_sunda)
    sunda_vocab.append(vocab3_sunda)

def knuthMorrisPratt(text, pattern):
    n = 0
    string = text
    for i in range (len(text)):
        a = len(text[i])
        n +=a
    m = len(pattern)
    fail = computeFail(pattern)
    i = 0
    j = 0
    while (i < n):
        if (pattern[j] == string[i]):
            if (j == m-1):
                return (i - m +1)       # found match
            i +=1
            j +=1
        elif (j > 0):
            j = fail[j-1]
        else:
            i +=1
    return -1

def computeFail(pattern):
    m = len(pattern)
    fail = []
    for i in range (m):                 # initialization
        fail.append(0)
    j = 0
    i = 1
    while (i < m):
        if (pattern[j] == pattern[i]):
            fail[i] = j +1
            i +=1
            j +=1
        elif (j > 0):
            j = fail[j-1]
        else:
            fail[i] = 0
            i +=1
    return fail

def buildLast(pattern):
    last = []
    for i in range(128):
        last.append(-1)
    for i in range (len(pattern)):
        last[ord(pattern[i])] = i
    return last

def boyerMoore(text, pattern):
    n = 0
    string = text
    for i in range(len(text)):
        a = len(text[i])
        n +=a
    last = buildLast(pattern)
    m = len(pattern)
    i = m - 1
    if (i > n - 1):
        return -1
    else:
        j = m -1
        while (i <= n - 1):
            if (pattern[j] == string[i]):
                if (j == 0):
                    return i
                else:
                    i -= 1
                    j -= 1
            else:
                lo = last[ord(string[i])]
                i = i + m - min(j, 1 +lo)
                j = m - 1
        return -1

def regex(text, pattern):
    string = text
    pattern_input = '(' + pattern + ')'
    s = -1
    for match in re.finditer(pattern, text):
        s = match.start()
        e = match.end()
    if (s > -1):
        return s
    else:
        return -1


def translate(m, n, teks, indo_vocab, sunda_vocab):

    # untuk menerjemahkan kalimat bahasa Sunda ke bahasa Indonesia,
    # seluruh kata 'teh' akan di abaikan
    if (n == 1):
        teks = teks.replace(' teh ', ' ')

    teks_tokenized = nltk.word_tokenize(teks)
    new_text = teks
    length = 0

    # untuk menerjemahkan kalimat bahasa Indonesia ke bahasa Sunda,
    # kata 'teh' ditambahkan setelah 'saya', 'dia', dan 'kamu' dengan
    # syarat tidak berada pada akhir kalimat
    if (n == 2):
        i = 0
        found= False
        while (i < (len(teks_tokenized) - 1)) and (not(found)):
            current_word = teks_tokenized[i]
            if (boyerMoore(current_word, "saya") == 0 and len(current_word) == len("saya")) or (boyerMoore(current_word, "kamu") == 0 and len(current_word) == len("kamu")) or (boyerMoore(current_word, "dia") == 0 and len(current_word) == len("dia")):
                found = True
                sisa = []
                a = i + 1
                while (a < len(teks_tokenized)):
                    sisa.append(teks_tokenized[a])
                    a += 1
                teks_tokenized[i + 1] = "teh"
                teks_tokenized.append("a")
                b = 0
                while (b < len(sisa)):
                    teks_tokenized[i + 2 + b] = sisa[b]
                    b += 1
            else:
                i +=1
        new_text = teks_tokenized[0]
        c = 1
        while (c < (len(teks_tokenized))):
            new_text += ' ' + teks_tokenized[c]
            c +=1
                
    # MENERJEMAHKAN BAHASA SUNDA --> BAHASA INDONESIA
    if (n == 1):
        while (length < len(teks_tokenized)):
            cur_text = teks_tokenized[length]
            found3 = False
            found2 = False
            found = False

            # pengecekan dimulai dari 3 kata pertama
            # apabila 3 kata pertama memiliki arti dalam kamus bahasa sunda,
            # pengecekan dilanjutkan di kata ke 4
            if (length + 2 < len(teks_tokenized)):
                for i in range (2):
                    cur_text += ' ' + teks_tokenized[length + i + 1]
                i = 0
                while (i < len(sunda_vocab[2])) and not(found3):
                    sunda = sunda_vocab[2][i][0]
                    indo = sunda_vocab[2][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, sunda) == 0):
                            found3 = True
                            length += 3
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, sunda) == 0):
                            found3 = True
                            length += 3
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, sunda) == 0):
                            found3 = True
                            length += 3
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1

            # 3 kata pertama tidak memiliki arti dalam kamus bahasa sunda, 
            # pengecekan dilakukan di 2 kata pertama                          
            if not(found3) and (length + 1 < len(teks_tokenized)):
                cur_text = teks_tokenized[length] + ' ' + teks_tokenized[length + 1]
                i = 0
                found2 = False
                while (i < len(sunda_vocab[1])) and not(found2):
                    sunda = sunda_vocab[1][i][0]
                    indo = sunda_vocab[1][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, sunda) == 0) and (len(cur_text) == len(sunda)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, sunda) == 0) and (len(cur_text) == len(sunda)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, sunda) == 0) and (len(cur_text) == len(sunda)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1

            # 2 kata pertama tidak memiliki arti dalam kamus bahasa sunda, 
            # pengecekan dilakukan di kata pertama    
            if not(found3) and not(found2) and (length < len(teks_tokenized)):
                cur_text = teks_tokenized[length]
                i = 0
                found = False
                while (i < len(sunda_vocab[0])) and not(found):
                    sunda = sunda_vocab[0][i][0]
                    indo = sunda_vocab[0][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, sunda) == 0)and (len(cur_text) == len(sunda)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, sunda) == 0) and (len(cur_text) == len(sunda)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, sunda) == 0) and (len(cur_text) == len(sunda)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, indo)
                        else:
                            i += 1

                # kata pertama tidak memiliki arti dalam kamus bahasa sunda, 
                # pengecekan dilakukan di kata selanjutnya    
                if not(found):
                    length += 1

    
    # MENERJEMAHKAN BAHASA INDONESIA --> BAHASA SUNDA
    elif (n == 2):
        while (length < len(teks_tokenized)):
            cur_text = teks_tokenized[length]
            found4 = False
            found3 = False
            found2 = False
            found = False

            # pengecekan dimulai dari 4 kata pertama
            # apabila 4 kata pertama memiliki arti dalam kamus bahasa indonesia,
            # pengecekan dilanjutkan di kata ke 5
            if (length + 3 < len(teks_tokenized)):
                for i in range (3):
                    cur_text += ' ' + teks_tokenized[length + i + 1]
                i = 0
                while (i < len(indo_vocab[3])) and not(found3):
                    indo = indo_vocab[3][i][0]
                    sunda = indo_vocab[3][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found4 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found4 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found4 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1

            # 4 kata pertama tidak memiliki arti dalam kamus bahasa indonesia, 
            # pengecekan dilakukan di 3 kata pertama 
            if not(found4) and (length + 2 < len(teks_tokenized)):
                for i in range (2):
                    cur_text += ' ' + teks_tokenized[length + i + 1]
                i = 0
                while (i < len(indo_vocab[2])) and not(found3):
                    indo = indo_vocab[2][i][0]
                    sunda = indo_vocab[2][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found3 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found3 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found3 = True
                            length += 3
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1

            # 3 kata pertama tidak memiliki arti dalam kamus bahasa indonesia, 
            # pengecekan dilakukan di 2 kata pertama 
            if not(found4) and not(found3) and (length + 1 < len(teks_tokenized)):
                # cek 2
                cur_text = teks_tokenized[length] + ' ' + teks_tokenized[length + 1]
                i = 0
                found2 = False
                while (i < len(indo_vocab[1])) and not(found2):
                    indo = indo_vocab[1][i][0]
                    sunda = indo_vocab[1][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found2 = True
                            length += 2
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1

            # 2 kata pertama tidak memiliki arti dalam kamus bahasa sunda, 
            # pengecekan dilakukan di kata pertama 
            if not(found4) and not(found3) and not(found2) and (length < len(teks_tokenized)):
                # cek 1
                cur_text = teks_tokenized[length]
                # print(cur_text)
                i = 0
                found = False
                while (i < len(indo_vocab[0])) and not(found):
                    indo = indo_vocab[0][i][0]
                    sunda = indo_vocab[0][i][1]
                    if (m == 1):
                        if (boyerMoore(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 2):
                        if (knuthMorrisPratt(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1
                    elif (m == 3):
                        if (regex(cur_text, indo) == 0) and (len(cur_text) == len(indo)):
                            found = True
                            length += 1
                            new_text = new_text.replace(cur_text, sunda)
                        else:
                            i += 1

                # kata pertama tidak memiliki arti dalam kamus bahasa sunda, 
                # pengecekan dilakukan di kata selanjutnya
                if not(found):
                    length += 1
                    
    return new_text


        

                

# indo_vocab = []
# sunda_vocab = []
# readVocab(indo_vocab, sunda_vocab)

# print("Pilih Metode Pencocokkan String :")
# print("1. Boyer Moore")
# print("2. Knuth Morris Pratt")
# print("3. Regular Expression")
# m = int(input("Nomor Metode yang dipilih = "))

# print("Pilih Mode Translate :")
# print("1. Sunda --> Indonesia")
# print("2. Indonesia --> Sunda")
# n = int(input("Nomor mode yang dipilih = "))

# teks = str(input("Masukkan kalimat yang ingin di-translate = "))
# # # m= 1
# # # n= 1
# # teks = "nami rai anjeun teh saha?"
# print(translate(m, n, teks, indo_vocab, sunda_vocab))

