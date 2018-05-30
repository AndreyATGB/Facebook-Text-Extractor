import os, sys, time, random
"""
HTML Facebook log extractor
messages between <div><div></div><div> and </div><div></div><div>
user between <div class="_3-96 _2pio _2lek _2lel"> and </div><div class="_3-96 _2let">
"""
def findMsgs(filename, shuffle=False, debug=False):
    startTime = time.time()
    # Read in entire file after </style><title>
    entireFile = ''
    with open(filename, 'r', encoding="utf8") as f:
        entireFile = f.readline()
    
    # Split all messages
    allMsgs = entireFile.split('<div class="_3-96 _2pio _2lek _2lel">')
    del allMsgs[0] # remove participants
    if debug:
        with open(f'debug_{filename}.txt', 'w', encoding="utf8") as fw:
            for msg in allMsgs:
                fw.write(msg + "\n")

    msgDict = {}
    # Adding to dictionary is very slow. First we find all users.
    for msg in allMsgs:
        # Find who sent message
        usr1 = msg.split('<div class="_3-96 _2pio _2lek _2lel">')[0] 
        usr = usr1.split('</div><div class="_3-96 _2let">')[0]
        if (usr == ''):
            usr = 'Unknown'
        if usr not in msgDict.keys():
            msgDict[usr] = ''

    # Extract and add to string, much faster than dictionary.
    for usr in msgDict.keys():
        print(F"Extracting {usr}'s messages.")
        tmpStr = ''
        for msg in allMsgs:
            # Ignore non-message lines
            usr1 = msg.split('<div class="_3-96 _2pio _2lek _2lel">')[0] 
            usrF = usr1.split('</div><div class="_3-96 _2let">')[0]
            if usrF == usr:
                # Find beginning of message
                msg1 = msg.split('<div><div></div><div>')[1]
                # End of message
                onlyMsg = msg1.split('</div><div></div><div>')[0]
                # Replace trash HTML characters
                onlyMsg = onlyMsg.replace("&#039;", "'")
                onlyMsg = onlyMsg.replace("&quot;", '"')
                onlyMsg = onlyMsg.replace("&gt;", '>')
                onlyMsg = onlyMsg.replace("&lt;", '<')
                onlyMsg = onlyMsg.replace("&amp;", '&')
                onlyMsg = onlyMsg.replace("&#123;", '{')
                onlyMsg = onlyMsg.replace("&#125;", '}')
                onlyMsg = onlyMsg.replace("&#064;", '@')
                # Ignore empty messages
                if onlyMsg != '':
                    tmpStr += onlyMsg + '\n'
        msgDict[usr] = tmpStr

    # Write to file
    saveFolder = filename.replace('.html', '')
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)
    for usr in msgDict.keys():
        if shuffle:
            tmp = msgDict[usr].split('\n')
            random.shuffle(tmp)
            with open(f'{saveFolder}/{usr}_shuffled.txt', 'w', encoding="utf8") as fw:
                fw.write('\n'.join(tmp))
        # Save regular one anyway
        with open(f'{saveFolder}/{usr}.txt', 'w', encoding="utf8") as fw:
            fw.write(msgDict[usr])
    print(F"Extracted {filename} in {time.time()-startTime:.1f}s.")
    return

if __name__ == '__main__':
    print('This program extracts messages from all .html files in the same folder\nand creates seperate text files for everyone in the conversation.')
    shuffle = False
    if input('Do you want to shuffle messages (y/n)? ') == 'y':
        shuffle = True

    for filename in os.listdir():
        if filename.endswith('.html'):
            print(F"-----Extracting from {filename}-----")
            findMsgs(filename, shuffle, debug=False)
    input("Press any key that isn't space to exit")
    

