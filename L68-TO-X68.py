"""
### .L68 to .X68
###
### Generates Easy68k .X68 source code file from .L68
###
### Handles errors and symbols on left of source code.
###
### Put .L68 file in same directory as this file. Run. Outputs .X68 file in same directory.

### Usage:

python L68-TO-X68.py "INPUT FILE.L68"

(Must use quotes if spaces exist in file name)

### Author:

Zach Graham
"""

import os, sys, re


class L68ToX68:

    NORMAL_START_LINE = 0
    NORMAL_START_LINE_INDEX = 40
    ERROR_START_LINE = 12
    ERROR_START_LINE_INDEX = 80

    def __init__(self):
        if len(sys.argv) is not 2:
            self.print_error_message()
            exit()

        file_path = os.path.dirname(os.path.abspath(__file__)) + "/" + sys.argv[1]

        if not os.path.isfile(file_path):
            self.print_error_message()
            exit()

        f_in = open(file_path, "r+")
        f_in_list = f_in.readlines()
        f_in_string = ''.join(str(e) for e in f_in_list)

        if re.search(r'(?i)line\s*\d*\s*(ERROR|WARNING)\s*:', f_in_string):
            output = self.handle_file(self.ERROR_START_LINE, f_in_list, True)
        else:
            output = self.handle_file(self.NORMAL_START_LINE, f_in_list, False)

        self.write_output_to_file(file_path, output)
        exit()

    def handle_file(self, start_line, f_in, is_error_file):
        output = ""

        if is_error_file:
            start_index = self.ERROR_START_LINE_INDEX
        else:
            start_index = self.NORMAL_START_LINE_INDEX

        for i in xrange(start_line, len(f_in)):
            trimmed_line = self.get_trimmed_line(f_in[i], start_index)
            if re.match(r'\s*END\s*START\s*', trimmed_line):
                output += trimmed_line
                break
            output += trimmed_line

        return output

    def get_trimmed_line(self, line, start_index):

        if re.search(r'v\d{0,2}.\d{0,2}.\d{0,2}', line):
            return ""

        output = ""
        for x in xrange(start_index, len(line)):
            output += line[x]

        return output

    def print_error_message(self):
        print "Must input a file name within quotes\ne.g. python l68-L68-TO-X68.py \"FILE NAME.L68\""

    def write_output_to_file(self, file_path, output):
        f_out_path = file_path.replace(".l68", "").replace(".L68", "") + ".X68"
        f_out = open(f_out_path, "w")
        f_out.write(output)
        f_out.close()
        print "Done! output file is at: " + f_out_path

start = L68ToX68()
