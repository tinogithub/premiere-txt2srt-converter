# Name: Premiere subtitle/captions TXT2SRT converter
# Version: 1.0

# Description:
# Premiere doesn't support to re-import its TXT export of subtitles/captions.
# This script converts a TXT subtitle export to a readable SRT format

import sys, os 

def txt2srt(source_file, srt_file, framerate):
    with open(source_file, 'r', encoding='utf-8') as raw_input:
        lines = raw_input.readlines()

    with open(srt_file, 'w', encoding='utf-8') as srt_output:
        subtitle_count = 1
        for i in range(0, len(lines)):
            current_line = lines[i].strip()
            try:
                inPoint, outPoint = current_line.split(' - ')
                
                # SRT needs an incrementing number for every subtitle
                srt_output.write(str(subtitle_count) + '\n')

                # Convert the timecode into SRT formatlike 00:00:04,734 --> 00:00:06,132
                # First let's convert the first 2 timecode dividers into colons
                if inPoint[2] == ";":
                    # Dropframe-Timecode
                    TCstring = inPoint.replace(';', ':', 2) + ' --> ' + outPoint.replace(';', ':', 2)
                    # Now let's replace the last timecode divider into a comma
                    TCstring = TCstring.replace(';', ',', 2)
                else:
                    # Non-Dropframe-Timecode
                    inPoint = inPoint[:8] + ',' + inPoint[8+1:]
                    outPoint = outPoint[:8] + ',' + outPoint[8+1:]
                    TCstring = inPoint + ' --> ' + outPoint

                # Split the two inPoint and outPoint again to convert the framecount into milliseconds
                inPoint, outPoint = TCstring.split(' --> ')
                inPoint = inPoint.split(',')[0] + ',' + str(round(1000 / framerate * int(inPoint.split(',')[1])))
                outPoint = outPoint.split(',')[0] + ',' + str(round(1000 / framerate * int(outPoint.split(',')[1])))

                # Join everything
                TCstring = inPoint + ' --> ' + outPoint + '\n'

                srt_output.write(TCstring)
                subtitle_count += 1
            except:
                # Just write the existing line
                srt_output.write(lines[i])
                continue

source_file = sys.argv[1]
srt_file = os.path.splitext(sys.argv[1])[0]+'.srt'

print('Sourcefile: ' + str(source_file))
print('Enter framerate (i.e. 25, 30 or 29.97): ')
framerate = float(input())

txt2srt(source_file, srt_file, framerate)

print('Outputfile: ' + str(srt_file))
