from sys import argv
import spacy
#import pdb
nlp = spacy.load("en_core_web_sm")

MAX_LINE_LENGTH = 42

# Failsafe to stop a program from getting stuck at the very end
# If it keeps requesting a split at the same position over and over,
# it'll just auto-allow the split
lastSplitRequest = 0
splitRequestCounter = 0
MAX_SPLIT_REQUESTS = 3

# Given a place the program is thinking of splitting,
# returns the pos of 1. this split
# or 2. the latest appropriate split in this range
def splitLine(doc, beforeToken, lineStartPos, currentLineLen):
 #   pdb.set_trace()

    result = beforeToken.i

    if currentLineLen < MAX_LINE_LENGTH:
        return result

    global lastSplitRequest
    global splitRequestCounter
    if result == lastSplitRequest:
        splitRequestCounter += 1
        if splitRequestCounter > MAX_SPLIT_REQUESTS:
            return result

    else:
        lastSplitRequest = result

    # Don't separate an adjective from its noun
    for i in range(result - 1, lineStartPos, -1):
        if doc[i].pos_ == "ADJ":
            if doc[i].head.i > result:
                result = doc[i].i
            break

    # Don't separate a determiner from its noun
    for i in range(result - 1, lineStartPos, -1):
        if doc[i].pos_ == "DET":
            if doc[i].head.i > result:
                result = i
            break

    # See if we can put it before a preposition
    for i in range(result - 1, lineStartPos, -1):
        if doc[i].pos_ == "ADP":
            result = i
            break

    return result    

def split_group(instring, deleteRepeatedWords=True):
    result = []
    currentLine = ""
    lineStartIndex = 0

    doc = nlp(instring)
    
    i = 0
    lastWord = ""
    while i < len(doc):
        #pdb.set_trace()
        token = doc[i]
        word = doc[i].text_with_ws
        nextI = i + 1

        # Don't separate a word from its punctuation
        while nextI < len(doc) and not word[-1].isspace():
            word += doc[nextI].text_with_ws
            nextI += 1
        '''
        # Turn a contraction from 2 tokens into 1 word
        if i + 1 < len(doc) and doc[i + 1].text[0] == "'":
            word = doc[i].text + doc[i + 1].text_with_ws
            nextI += 1
        '''

        if deleteRepeatedWords and word.lower() == lastWord.lower():
            i = nextI
            continue

        # Before prepositions or conjunction
        #if (doc[i].pos_ == "ADP" or doc[i].pos_ == "CCONJ"
            #or doc[i].pos_ == "SCONJ"

        # At the end of a sentence
        if ((i > 0 and doc[i - 1].is_sent_end)
        
        # Respect max line length
            or len(currentLine) + len(word) > MAX_LINE_LENGTH):

            #pdb.set_trace()
            recalcWord = False
            iToSeparate = splitLine(doc, token, lineStartIndex, len(currentLine))
            if iToSeparate < token.i:
                currentLine.rstrip()
                for i in range(token.i - iToSeparate):
                    currentLine = currentLine[:currentLine.rfind(" ")]
                i = iToSeparate
                nextI = i + 1
                recalcWord = True
                token = doc[iToSeparate]
            
            if doc[iToSeparate - 1].is_sent_end:
                currentLine += "\n"

            currentLine += "\n"
            result.append(currentLine)
            
            if recalcWord:
                word = token.text_with_ws
                while nextI < len(doc) and not word[-1].isspace():
                    word += doc[nextI].text_with_ws
                    nextI += 1
            currentLine = word
            lineStartIndex = token.i


        else:
            currentLine += word

        i = nextI
        lastWord = word

    result.append(currentLine)
    return result
    
if __name__ == "__main__":
    filename = argv[1]
    outname = (filename[:filename.rfind(".")] + "_grouped" +
        filename[filename.rfind("."):])
    linesIn = []
    linesOut = []
    with open(filename, "r") as infile:
        linesIn = infile.readlines()
        
    for line in linesIn:
        linesOut.append(split_group(line))

    parity = 0
    with open(outname, "w") as outfile:
        for section in linesOut:
            for line in section:
                outfile.write(line)

                # If it's already the end of a sentence
                # (i.e. ends in two newlines)
                # reset the two-newlines counter
                if len(line) > 1 and line[-2] == "\n":
                    parity = 0
        
                if (parity % 3 == 2):
                    outfile.write("\n")
                parity += 1
