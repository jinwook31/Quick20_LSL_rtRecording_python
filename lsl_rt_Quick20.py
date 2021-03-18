#!/usr/bin/env python
from pylsl import StreamInlet, resolve_stream
import csv, time, datetime
import numpy as np
import pandas as pd
import threading

now = datetime.datetime.now()
startExpTime = now.strftime("%y_%m_%d_%H_%M_%S")

# first resolve an EEG stream on the lab network
print("looking for an EEG and Marker stream...")
streamsEEG = resolve_stream('type', 'EEG')
streamsMarker = resolve_stream('type', 'Markers')

inletEEG = StreamInlet(streamsEEG[0])
inletMarker = StreamInlet(streamsMarker[0])


#####################
#  Marker Receiver  #
#####################
marker = 0

def getMarker():
    while True:
        markers, timestamp = inletMarker.pull_sample()
        global marker
        marker = markers[0]

        if marker == 'end':
            break

t = threading.Thread(target=getMarker)
t.start()


#####################
#   Data Receiver   #
#####################
elapTime = 1   # ms
result = []

while True:
    # get a new sample (you can also omit the timestamp part if you're not interested in it)
    chunk, timestamps = inletEEG.pull_chunk()

    # Check Marker
    if marker == 'end':
        break
    elif marker == 0:
        continue

    if timestamps:
        #print(timestamps, chunk)
        for idx in range(0, len(chunk)):
            ts = timestamps[idx]  # UTC time
            sample = [elapTime, ts, marker]
            sample.extend(chunk[idx])
            elapTime += 1
            result.append(sample)
            print(sample)


#######################
#  Generate CSV file  #
#######################
def saveData2CSV(result):
    # Datastamp | timestamp | Marker | EEG Channels (20)
    csvFile = open(startExpTime+'_eeg.csv', 'w', newline="")

    header = ["Datastamp","timestamp", "Marker"]
    for channel in range(1, len(result[0]) - 2):
        header.append("Channel_"+str(channel))

    csvwriter = csv.writer(csvFile)
    csvwriter.writerow(header)
    for row in result:
        csvwriter.writerow(row)

    csvFile.close()

