#from fastpunct import FastPunct
from sys import argv
from math import ceil
#import pdb
from nemo.collections.nlp.models import PunctuationCapitalizationModel


LINES_PER_SECTION = 50
TOTAL_LINES = None
FUSE_LINES = True

def outfileSuffix(string):
    SUFFIX = "_out"
    DOT_INDEX = string.rfind(".")
    return string[:DOT_INDEX] + SUFFIX + string[DOT_INDEX:]

# lines - The list of unpunctuated lines.
# index - Our current index in the list
# Return - One beyond the last index of the section.
#          Returns None if line limit has been reached.
def getNextSection(lines, index):
    if (TOTAL_LINES and index >= TOTAL_LINES) or index >= len(lines):
        return None
    maxLines = len(lines) - index
    if TOTAL_LINES and TOTAL_LINES < maxLines + index:
        maxLines = TOTAL_LINES - index
    if (LINES_PER_SECTION and LINES_PER_SECTION < maxLines):
        maxLines = LINES_PER_SECTION

    return index + maxLines

def guessPunctuation(lines):
    bert = PunctuationCapitalizationModel.from_pretrained(
        "punctuation_en_bert")

    outlines = []
    lineIndex = 0
#            pdb.set_trace()
    sectionEndIndex = getNextSection(lines, lineIndex)
    #try:
    while sectionEndIndex:   
        lineSection = lines[lineIndex:sectionEndIndex] 
        if (FUSE_LINES):
            lineSection = [' '.join(lineSection)]
        #punctLines = fastpunct.punct(lineSection)
        punctLines = bert.add_punctuation_capitalization(lineSection)
        lineIndex = sectionEndIndex
        for punctLine in punctLines:
            outlines.append(punctLine)

#               pdb.set_trace()            
        sectionEndIndex = getNextSection(lines, lineIndex)
    
    return outlines

if __name__ == "__main__":
#    fastpunct = FastPunct()
    
    for fname in argv[1:]:
        with open(fname, "r") as infile:
            lines = infile.read().splitlines()
            
            outlines = guessPunctuation(lines)
            
            outFname = outfileSuffix(fname)

            with open(outFname, "w") as outfile:
                for line in outlines:
                    outfile.write(line)
                    outfile.write("\n\n")
