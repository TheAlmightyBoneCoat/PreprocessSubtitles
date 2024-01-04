from sys import argv
import spacy
import pdb
#nlp = spacy.load("en_core_web_sm")

lenCurseTag = 4

# Skip past newlines
def getNextWordIndex(doc, index, step=1):
    result = index + step
    if result == len(doc) or result < 0:
        return -1

    while doc[result].pos_ == "SPACE":
        result += step
        if result == len(doc) or result < 0:
            return -1

    return result

# Remove "[ __ ]" and do the following:
# 1. Before an adjective or noun, guess "fucking"
# 2. After "what the," guess whatThe
# 3. For "you ___", guess defaultInsult
# 4. Otherwise, guess defaultSwear
# Return: The guessed swear (str)
def guessSwear(doc, curseBeginIndex, whatThe="fuck", defaultSwear="shit",
    defaultInsult="bitch", holy="shit"):
    # YouTube transcript swear pattern is ["[", "_", "_", "]"]
    curseEndIndex = curseBeginIndex + lenCurseTag - 1

    if curseBeginIndex - 1 >= 0:
        prevWordIndex = getNextWordIndex(doc, curseBeginIndex, step=-1)
        if prevWordIndex != -1:
            if doc[prevWordIndex].text == "you":
                return defaultInsult

            if doc[prevWordIndex].text == "holy":
                return holy
    
    if curseEndIndex + 1 < len(doc):
        nextWordIndex = getNextWordIndex(doc, curseEndIndex)
        if nextWordIndex != -1:
            if (doc[nextWordIndex].pos_ == "ADJ" or 
                doc[nextWordIndex].pos_ == "NOUN"):
                return "fucking"

    if curseBeginIndex - 2 >= 0:
        theIndex = getNextWordIndex(doc, curseBeginIndex, step=-1)
        
        if theIndex != -1 and doc[theIndex].text == "the":
            whatIndex = getNextWordIndex(doc, theIndex, step=-1)
        
            if whatIndex != -1 and doc[whatIndex].text == "what":
                return whatThe


    return defaultSwear

def replaceSwearTags(instring):
    doc = nlp(instring)
    result = ""
    
    i = 0
    while i < len(doc) - lenCurseTag:
        if doc[i].text == "[" and doc[i + 1].text == "_":
            result += guessSwear(doc, i) + " "
            i += lenCurseTag

        else:
            result += doc[i].text_with_ws
            i += 1

    return result
 
if __name__ == "__main__":
    filename = argv[1]
    outname = (filename[:filename.rfind(".")] + "_explicit" +
        filename[filename.rfind("."):])
    transcript = ""
    with open(filename, "r") as infile:
        transcript = infile.read()
        
    result = replaceSwearTags(transcript)
  
    with open(outname, "w") as outfile:
        outfile.write(result)

