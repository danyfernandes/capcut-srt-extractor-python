#!/usr/bin/env python3
"""
Capcut SRT Extractor.
This script extracts auto captions from a Capcut application project file into a .srt subtitle file.
Capcut generates a "draft_info.json" in Mac OS X and Linux OS systems.
Capcut generates a "draft_content.json" in Microsoft Windows OS systems.
On Mac OS X, this file can be found
/Users/[user]]/Movies/CapCut/User Data/Projects/com.lveditor.draft/[id]/draft_info.json
"""

__author__ = "Daniel Fernandes"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import json
import os

from datetime import timedelta

def check_file(filename):
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError("{0} does not exist".format(filename))
    if not filename.endswith(".json"):
        raise argparse.ArgumentTypeError("{0} has not .json extension".format(filename))
    return filename

def parseJSON(filename):
    if not filename.endswith(".json"):
        print("parseJSON: Filename has not JSON extension")
        exit(-1)
    file = open(filename, "r")
    data = json.load(file)
    file.close()

    return data

def formatTimeToSrt(timeInMicroSeconds):
    # Will be formatted in HH:MM:SS.yyyyyy
    timeFormatted = str(timedelta(microseconds=timeInMicroSeconds))

    listTimeFormatted = timeFormatted.split('.')

    if len(listTimeFormatted) <= 1:
        listTimeFormatted[0] = listTimeFormatted[0] + '.000'
    elif len(listTimeFormatted[1]) > 3:
        listTimeFormatted[1] = listTimeFormatted[1][:3]

    return '.'.join(listTimeFormatted).replace('.', ',')

def writeToSrtFile(filename, lines):
    file = open(filename, "w", encoding="utf-8")
    file.writelines(lines)
    file.close()

def process(input, output):
    data = parseJSON(input)

    # Get materials and tracks
    materials = data['materials']
    tracks = data['tracks']

    # Get texts and segments
    texts = materials['texts']
    segments = []

    # Take the track with attribute=0
    for track in tracks:
        if track['attribute'] == 0:
            # Take the track has more than 1 segment
            if 'segments' in track and len(track['segments']) > 1:
                segments = track['segments']
                break

    # Counter to be incremented for each subtitle
    sub_counter = 0

    # Final list of subtitles formated:
    # 1
    # 00:00:05,326 --> 00:00:06,001
    # Some Text
    # 2
    # .....
    listOfSubtitles = []

    for text in texts:
        for segment in segments:
              if text['id'] == segment['material_id']:
                subtitleSentence = ''.join(text['words']['text'])
                startSubtitleTime = segment['target_timerange']['start']
                subtitleDuration = segment['target_timerange']['duration']
                endSubtitleTime = startSubtitleTime + subtitleDuration

                strStartSubtitle = formatTimeToSrt(startSubtitleTime)
                strEndSubtitle = formatTimeToSrt(endSubtitleTime)

                sub_counter = sub_counter + 1
                srtTiming = f'{strStartSubtitle} --> {strEndSubtitle}'

                listOfSubtitles.append(f'{sub_counter}\n{srtTiming}\n{subtitleSentence}\n\n')
                break

    writeToSrtFile(output, listOfSubtitles)

        
def main():
    parser = argparse.ArgumentParser(description="Capcut SRT Extraction")
    parser.add_argument("-i", "--input", dest="filename", required=True, type=check_file, help="Path to 'draft_content.json' file on Windows or 'draft_info.json' file on Mac OS X and Linux.", metavar="JSON File")
    parser.add_argument("-o", "--output", dest="output", required=False, default="out.srt", help="Path to output SRT file.", metavar="SRT File")
    args = parser.parse_args()

    process(args.filename, args.output)

if __name__ == "__main__":
    main()