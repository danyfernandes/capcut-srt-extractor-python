# capcut-srt-extractor-python

Capcut SRT Extractor written in Python language

## Introduction

When using Capcut application, sometimes we need to export SRT files for some videos make with this software. Capcut does not include the possibility to export a SRT file. It generates the subtitles (auto-caption) for a video, but not export the SRT file.

Capcut generates a JSON file in the project user data folder. In Mac OS and Linux based systems, this file is named draft_info.json. For Microsoft Windows systems, this file is named draft_content.json.

This script takes this file as an input and will generates the subtitles in a SRT file.

## Execution

To run and get its options, simply run:

```console
python3 main.py -h
```

What you should see:

```shell
usage: main.py [-h] -i JSON File [-o SRT File]

Capcut SRT Extraction

options:
-h, --help show this help message and exit
-i JSON File, --input JSON File
Path to 'draft_content.json' file on Windows or 'draft_info.json' file on Mac OS X and Linux.
-o SRT File, --output SRT File
Path to output SRT file.
```

To run the program, simply run:

```console
python3 main.py -i PATH/TO/draft\_[info|content].json -o mySrt.srt
```

If no parameter is specified specified for the output, the program will export automatically a out.srt file at the root of the project folder.

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details
