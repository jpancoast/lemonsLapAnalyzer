#!/usr/bin/python


import datetime


'''
TODO:
#    Figure out how to split the days
#
#    What do I do if there are two pit laps in a row?

    print out:
        overall average lap time
#        fastest lap of the race, lap number, stint number
#        slowest lap of the race, lap number, stint number
    
    Also some data for in and out laps, but separate
    
    'analyzeStints' should just save the data into a dict or something. (self.analyzedData = {})
    write another method to output the data

    Make a website out of it...
    
#    Convert to a python module
'''


class race():

    def __init__(self, lapFile, carNum=999999, debug=False):
        self.lapData = {}
        self.analyzedData = {}

        print "carNum:" + str(carNum)
        self.stints = []

        self.lapFile = lapFile
        self.carNum = str(carNum)
        self.debug = debug

        if int(carNum) == 999999:
            self.__load_new_format()
        else:
            self.__loadLapData()

    def getAnalyzedData(self):
        return self.analyzedData

    def analyzeStints(self):

        fastestLapOfRaceInSeconds = 99999.9
        slowestLapOfRaceInSeconds = 0.0
        fastestLapOfRaceLapNum = 9999999
        slowestLapOfRaceLapNum = 0.0

        slowestStint = 99999
        fastestStint = 99999

        stintCount = 0

        for stint in self.stints:
            fastestLapInSeconds = 9999.9
            slowestLapInSeconds = 0.0
            stintCount += 1

            averageLapTime = 0.0
            totalTime = 0.0
            count = 0
            numLapsToAverage = 0

            numLaps = len(stint)

            if self.debug:
                print stint

            print "Stint Number: " + str(stintCount)
            print "Number of Laps this Stint: " + str(numLaps)

            for lap in stint:
                if self.debug:
                    print lap

                if (count != 0 and count != (numLaps - 1)) or ('firstLapOfDay' in lap and lap['firstLapOfDay']):
                    if lap['lapTimeInSeconds'] < fastestLapOfRaceInSeconds:
                        fastestLapOfRaceInSeconds = lap['lapTimeInSeconds']
                        fastestLapOfRaceLapNum = lap['laps']
                        fastestStint = stintCount

                    if lap['lapTimeInSeconds'] > slowestLapOfRaceInSeconds:
                        slowestLapOfRaceInSeconds = lap['lapTimeInSeconds']
                        slowestLapOfRaceLapNum = lap['laps']
                        slowestStint = stintCount

                    if lap['lapTimeInSeconds'] < fastestLapInSeconds:
                        fastestLapInSeconds = lap['lapTimeInSeconds']
                        fastestLap = lap['lapTime']
                        fastestLapNumber = lap['laps']

                    if lap['lapTimeInSeconds'] > slowestLapInSeconds:
                        slowestLapInSeconds = lap['lapTimeInSeconds']
                        slowestLap = lap['lapTime']
                        slowestLapNumber = lap['laps']

                    totalTime = totalTime + lap['lapTimeInSeconds']
                    numLapsToAverage += 1
                else:
                    if self.debug:
                        print "Not counting this lap: " + lap['laps']

                count += 1

            if numLapsToAverage == 0:
                print "Not enough actual laps to do anything.  Probably two pit laps in a row or something"
            else:
                averageLapTime = totalTime / numLapsToAverage

                print "Fastest Lap: " + str(fastestLap) + ", lap Number: " + str(fastestLapNumber)
                print "Slowest Lap: " + str(slowestLap) + ", lap Number: " + str(slowestLapNumber)
                print "Average Lap Time: " + str(self.__convertSecondsToTime(averageLapTime))

            print "----------------------"

            numLapsToAverage = 0

        print "Overall race Info:"
        print "Fastest Lap: " + self.__convertSecondsToTime(fastestLapOfRaceInSeconds) + " on lap: " + str(fastestLapOfRaceLapNum) + ", stint Number: " + str(fastestStint)
        print "Slowest Lap: " + self.__convertSecondsToTime(slowestLapOfRaceInSeconds) + " on lap: " + str(slowestLapOfRaceLapNum) + ", stint Number: " + str(slowestStint)

    def processLapData(self):
        stint = []

        newStint = False
        prevLap = 999999
        endOfDay = False
        lastLapOfDay = None

        if str(self.carNum) in self.lapData:
            for lap in self.lapData[str(self.carNum)]:
                if lap['lapTime'] != '':

                    if prevLap == lap['laps']:
                        endOfDay = True

                    if lap['laps'] == '1':
                        lap['firstLapOfDay'] = True

                    if not endOfDay:
                        stint.append(lap)

                    if endOfDay and lap['laps'] > prevLap:
                        temp = lap
                        temp['firstLapOfDay'] = True
                        lastLapOfDay = temp
                        newStint = True
                        endOfDay = False

                    if str(lap['laps']).startswith('P'):
                        newStint = True

                    if newStint:
                        self.stints.append(stint)
                        stint = []
                        newStint = False

                        if lastLapOfDay is not None:
                            stint.append(lastLapOfDay)
                            lastLapOfDay = None

                    prevLap = lap['laps']

        else:
            print "No data for Car Number: " + str(self.carNum)

    def __convertTimeToSeconds(self, lapTime):
        l = lapTime.split(':')

        if len(l) == 3:
            # probably not useful for lap times...
            return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
        elif len(l) == 2:
            return float(l[0]) * 60.0 + float(l[1])
        else:
            return None

    def __convertSecondsToTime(self, seconds):
        return str(datetime.timedelta(seconds=seconds))

    '''
    Lap,Lead Lap,Lap Time,Difference w/ fast lap,Difference w/ best lap,Speed
1,1,02:47.0,0.000,47.159,47.437
    '''
    def __load_new_format(self):
        carNum = self.carNum
        print "__load_new_format"
        with open(self.lapFile) as f:
            for line in f:
                recordLine = line.rstrip().split(',')

                if carNum not in self.lapData:
                    self.lapData[carNum] = []

                record = {}
                record['carClass'] = "dummy class"
                record['teamName'] = "fuck if I know"
                record['laps'] = recordLine[0]
                record['lapTime'] = recordLine[2]
                record['lapTimeInSeconds'] = self.__convertTimeToSeconds(
                    recordLine[2])

                #print record
                self.lapData[carNum].append(record)




    def __loadLapData(self):

        with open(self.lapFile) as f:
            for line in f:
                recordLine = line.rstrip().split(',')

                carNum = recordLine[1]

                if carNum not in self.lapData:
                    self.lapData[carNum] = []

                record = {}
                record['carClass'] = recordLine[2]
                record['teamName'] = recordLine[3]
                record['laps'] = recordLine[4]
                record['lapTime'] = recordLine[5]
                record['lapTimeInSeconds'] = self.__convertTimeToSeconds(
                    recordLine[5])

                self.lapData[carNum].append(record)
