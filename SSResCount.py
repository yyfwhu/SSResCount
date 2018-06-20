#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import os
import argparse


def main():

    print("*****************************************")
    print("SSCount by Yiming Tang @ Fudan")

    usage = "Usage: " + sys.argv[0] + " -f input_file -o output_file_name"

    # Check arguments
    if not (len(sys.argv) == 5):
        print("ERROR: Wrong Number of Arguments Provided")
        print(usage)
        exit(1)

    input_file_name = ""
    output_file_name = ""

    # Get arguments
    arg_count = 1
    while arg_count < 5:
        if sys.argv[arg_count] == '-f':
            input_file_name = sys.argv[arg_count+1]
            arg_count += 1
        elif sys.argv[arg_count] == '-o':
            output_file_name = sys.argv[arg_count+1]
            arg_count += 1
        arg_count += 1

    if input_file_name == "" or output_file_name == "":
        print("ERROR: Input or Output File Name not Provided.")
        print(usage)
        exit(1)
    else:
        print("Will Read Secondary Structure From : " + input_file_name)
        print("Will Write Structure Count    To   : " + output_file_name)

    # Read Lines

    try:
        with open(input_file_name, "r") as inputFile:
            lines = inputFile.read().splitlines()

            # Pop Non-Important Lines
            while lines[0][0] != 's':
                lines.pop(0)

            while lines[0][0] != '/':
                lines.pop(0)

            while lines[0][0] != '"':
                lines.pop(0)


            # Set up Time_Count && Residue_Count
            residue_count = len(lines)
            time_count = len(lines[0])-3
            print("Identified Total Number of Residues: " + str(residue_count))
            print("Identified Total Number of Frames  : " + str(time_count))

            for residue in range(residue_count):
                if lines[residue][0] != '"':
                    print("ERROR: The " + str(residue + 1) + "Lines contains inadequate beginning.")
                    print(lines[residue])
                    exit(1)

            # Get Frame Counts

            print("*****************************************")

            # Get Processed Residues
            processed_all_flag = input("Use All Residues? [yes / no] (default yes) > ")

            if processed_all_flag == "" or processed_all_flag[0] == 'y' or processed_all_flag[0] == 'Y':
                residue_down_limit = 0
                residue_up_limit   = residue_count
            else:
                residue_up_limit     = residue_count - int(input("Use Residue From (Index starts from 1): ")) + 1
                residue_down_limit   = residue_count - int(input("Use Residue To   (Index starts from 1): "))

            # Read Through Lines and Count Secondary Structure

            count_coil     = [0] * time_count
            count_b_sheet  = [0] * time_count
            count_b_bridge = [0] * time_count
            count_bend     = [0] * time_count
            count_turn     = [0] * time_count
            count_a_helix  = [0] * time_count
            count_5_helix  = [0] * time_count
            count_3_helix  = [0] * time_count

            translines = list(zip(*lines))

            #print(translines[time_count])

            for time in range(time_count):
                # print("residue: " + str(residue))
                # print(lines[residue])
                # print(translines[time+1][residue_down_limit:residue_up_limit])
                count_coil[time]      = translines[time+1][residue_down_limit:residue_up_limit].count('~')
                count_b_sheet[time]   = translines[time+1][residue_down_limit:residue_up_limit].count('E')
                count_b_bridge[time]  = translines[time+1][residue_down_limit:residue_up_limit].count('B')
                count_bend[time]      = translines[time+1][residue_down_limit:residue_up_limit].count('S')
                count_turn[time]      = translines[time+1][residue_down_limit:residue_up_limit].count('T')
                count_a_helix[time]   = translines[time+1][residue_down_limit:residue_up_limit].count('H')
                count_3_helix[time]   = translines[time+1][residue_down_limit:residue_up_limit].count('I')
                count_5_helix[time]   = translines[time+1][residue_down_limit:residue_up_limit].count('G')
            # Output to File

            try:
                with open(output_file_name, "w+") as outputFile:

                    outputFile.writelines("time\tCoil\tB-Sheet\tB-Bridge\tBend\tTurn\tA-Helix\t3-Helix\t5-Helix\n")

                    for time in range(time_count):
                        outputFile.writelines("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n"
                                               % (time, count_coil[time], count_b_sheet[time],
                                                  count_b_bridge[time], count_bend[time], count_turn[time],
                                                  count_a_helix[time], count_3_helix[time], count_5_helix[time]))

            except FileNotFoundError:
                print("ERROR: \"" + output_file_name + "\" not found.")
                print(usage)
                exit(1)
    except FileNotFoundError:
        print("ERROR: \"" + input_file_name + "\" not found.")
        print(usage)
        exit(1)

    print("Mission Completed. Miao~")

main()


