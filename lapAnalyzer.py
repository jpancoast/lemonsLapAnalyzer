#!/usr/bin/env python

import sys

from race import race


def main(argv):

    (lapFile, carNumToLookFor) = getArgs(argv)

    raceObj = race(lapFile, carNumToLookFor)
    raceObj.processLapData()
    raceObj.analyzeStints()


def getArgs(arguments):
    if len(arguments) != 3:
        usage()
        exit(2)

    lapFile = arguments[1]

    try:
        carNumToLookFor = int(arguments[2])
    except ValueError:
        print "team number is not an integer"
        exit(2)

    return (lapFile, carNumToLookFor)


def usage():
    print "Usage: " + sys.argv[0] + " <lapFile.csv> <carNumber>"

if __name__ == "__main__":
    main(sys.argv)
