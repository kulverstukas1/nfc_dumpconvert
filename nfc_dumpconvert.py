#!/usr/local/bin/python
'''
    Author: Kulverstukas
    Website: 9v.lt
    Description:
        Converts HEX into Integers, Binary and ASCII data for further investigation.
        Usage is controlled with params.
        Inspired by https://github.com/evilpete/flipper_toolbox/blob/main/nfc_hexdump.py
    Note:
        "Bare binary" was added as a helper to only output the binary values without
        prepending the original data. This is useful is you intend to print these
        values because it saves time removing original data to fit everything on a page.
'''

#---------------------------------------------------------------
import sys
import argparse
import os.path
import shutil
#---------------------------------------------------------------

parser = argparse.ArgumentParser(
                    prog=(sys.argv[0].split("/"))[-1],
                    description='''
Converts Flipper HEX data into Integers, Binary and ASCII data for further investigation.\n
If no optional arguments are given then data will be converted to Decimal format.\n
Existing output file or folder will be overwritten.''',
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog="Hack the Planet!")
parser.add_argument("inputname", help="Input source name. Can be single file or folder", metavar="filename|foldername")
parser.add_argument("-o", dest="output", help="Output name. Ignored if input is a folder", metavar="OUTFILE")
parser.add_argument("-c", dest="convert", help="Convert HEX into ASCII, Decimal, Binary or Bare binary (no original data). Defaults to Decimal.", choices=["ascii", "dec", "bin", "binb"], default="dec")

args = parser.parse_args()

#---------------------------------------------------------------

def convertToAscii(inFileObj):
    processedLines = []
    for line in inFileObj:
        lineParts = line.split()
        if lineParts[0] in ["Page", "Block"]:
            hex = [00 if x == '??' else int(x, 16) for x in lineParts[2:]]
            charVarF = ["-" if x < 32 or x > 126 else chr(x) for x in hex]
            fLine = " ".join(charVarF)
            processedLines.append(line.rstrip() + ' # ' + fLine)
        else:
            processedLines.append(line.rstrip())
    return "\n".join(processedLines)

#---------------------------------------------------------------

def convertToDec(inFileObj):
    processedLines = []
    for line in inFileObj:
        lineParts = line.split()
        if lineParts[0] in ["Page", "Block"]:
            hex = [00 if x == '??' else int(x, 16) for x in lineParts[2:]]
            decValF = [f"{x:3d}" for x in hex]
            fLine = " ".join(decValF)
            processedLines.append(line.rstrip() + ' # ' + fLine)
        else:
            processedLines.append(line.rstrip())
    return "\n".join(processedLines)

#---------------------------------------------------------------

def convertToBin(inFileObj, bare):
    processedLines = []
    for line in inFileObj:
        lineParts = line.split()
        if lineParts[0] in ["Page", "Block"]:
            hex = [00 if x == '??' else int(x, 16) for x in lineParts[2:]]
            binValF = [f"{x:0>8b}" for x in hex]
            fLine = " ".join(binValF)
            if (bare):
                processedLines.append(fLine)
            else:
                processedLines.append(line.rstrip() + ' # ' + fLine)
        else:
            processedLines.append(line.rstrip())
    return "\n".join(processedLines)

#---------------------------------------------------------------

if (not os.path.exists(args.inputname)):
    print("Input '%s' does't exist. Exiting." % args.inputname)
    exit()

fileArr = []
outPath = ""
if (os.path.isdir(args.inputname)):
    outPath = os.path.join(args.inputname, "out-%s" % args.convert)
    if (os.path.exists(outPath)):
        shutil.rmtree(outPath)
    os.mkdir(outPath)
    args.output = None
    for f in os.listdir(args.inputname):
        if ((os.path.splitext(f)[1] == ".nfc") and (os.path.isfile(os.path.join(args.inputname, f)))):
            fileArr.append(os.path.join(args.inputname, f))
else:
    fileArr.append(args.inputname)
    outPath = os.path.split(args.inputname)[0]

for file in fileArr:
    inFileObj = open(file, "r", encoding="utf-8")
    header = inFileObj.readline().strip()
    if (header != 'Filetype: Flipper NFC device'):
        print("Error: %s is not a 'Flipper NFC' sample file'" % os.path.split(file)[1])
        continue
    inFileObj.seek(0)

    rtn = ""
    if (args.convert == "ascii"):
        rtn = convertToAscii(inFileObj)
    elif (args.convert == "dec"):
        rtn = convertToDec(inFileObj)
    elif ((args.convert == "bin") or (args.convert == "binb")):
        rtn = convertToBin(inFileObj, ((args.convert == "binb")))
        
    if (not args.output):
        inFilename = os.path.split(file)
        inFilename = os.path.splitext(inFilename[1])[0]
        outFile = os.path.join(outPath, "out_%s_%s.nfc" % (inFilename, args.convert))

    with open(outFile, "w", encoding="utf-8") as outFileObj:
        outFileObj.write(rtn + "\n")

print("Done!")

#---------------------------------------------------------------
