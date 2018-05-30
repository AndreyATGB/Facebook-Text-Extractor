import os, sys, time, random
"""
HTML Facebook log extractor
message starts at <div class="message_header"> with usr who sent it.
messages between <p> and </p>
user between <span class="user"> and </span>
"""
def findMsgs(filename, shuffle=False, debug=False):
    startTime = time.time()
    # Read in entire file after </style><title>
    entireFile = ''
    with open(filename, 'r', encoding="utf8") as f:
        startRead = False
        for line in f:
            if line.startswith('</style><title>'):
                startRead = True
            if startRead:
                entireFile += line.replace('\n', '')
    
    # Split all messages
    allMsgs = entireFile.split('<span class="user">')
    if debug:
        with open(f'debug_{filename}.txt', 'w', encoding="utf8") as fw:
            for msg in allMsgs:
                fw.write(msg + "\n")

    # Adding to dictionary is very slow. First we find all users.
    tmpStr = ''
    for msg in allMsgs:
        # Ignore non-message lines
        if not (msg.startswith('</style>')):
            # Find who sent message
            usr = msg.split('</span>')[0] 
            if (usr == ''):
                usr = 'Unknown'
            # Only first names
            usr = usr.split(' ')[0]
            # Find beginning of message
            msg1 = msg.split('<p>')[1]
            # End of message
            onlyMsg = msg1.split('</p>')[0]
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
                tmpStr += usr + ": " + onlyMsg + '\n'

    # Write to file
    saveFolder = filename.replace('.html', '')
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)
    if shuffle:
        tmp = tmpStr.split('\n')
        random.shuffle(tmp)
        with open(f'{saveFolder}/{saveFolder}_shuffled.txt', 'w', encoding="utf8") as fw:
            fw.write('\n'.join(tmp))
    # Save regular one anyway
    with open(f'{saveFolder}/{saveFolder}.txt', 'w', encoding="utf8") as fw:
        fw.write(tmpStr)
    print(F"Extracted {filename} in {time.time()-startTime:.1f}s.")
    return

if __name__ == '__main__':
    print('This program extracts messages from all .html files in the same folder\nand creates one text file, everyone has their first name before their message.')
    shuffle = False
    if input('Do you want to shuffle messages (y/n)? ') == 'y':
        shuffle = True

    for filename in os.listdir():
        if filename.endswith('.html'):
            print(F"-----Extracting from {filename}-----")
            findMsgs(filename, shuffle)
    

