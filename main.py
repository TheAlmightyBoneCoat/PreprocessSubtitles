from sys import argv

# Steps:
# 1. Replace [ __ ] with curse words
# 2. Add auto-punctuation
# 3. Create caption groups

from guess_cursing import replaceSwearTags
from punctuation import guessPunctuation
from grouping import split_group

if __name__ == "__main__":
    filename = argv[1]
    outname = (filename[:filename.rfind(".")] + "_out" +
        filename[filename.rfind("."):])
    transcript = ""
    with open(filename, "r") as infile:
        transcript = infile.read()

    print("Guessing curse words...")        
    result = replaceSwearTags(transcript)

    print("Guessing punctuation...")
    result = result.splitlines()
    result = guessPunctuation(result)
    
    print("Creating caption groups...")
    grouped = []
    for line in result:
        grouped.append(split_group(line))
  
    parity = 0
    with open(outname, "w") as outfile:
        for section in grouped:
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

