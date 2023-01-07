#!/usr/bin/env python

'''
projectMenu.py

Author(s): 
    Michael Janeway (1167994)
    Jake Goode (1202742)
    Shahmeer Shahid (1191616)
    Harsimran Ghuman Singh (1181018)

Project: CIS2250 W22 Project: COVID-19 Data Tracking
Date of Last Update: Mar 28, 2022.

Functional Summary
projectMenu.py contains the following function(s):
    createMenu():
        createMenu() uses the PyInquirer library to prompt the user
        with a menu that allows them to either update the project's data,
        or run one of the four question's functions

This file is a module file, it is not meant to be run
'''

# Project functions
from projectUtilities import buildData, cls, project_style
from projectQuestions import q1, q2, q3, q4

# User interface and experience libraries
from PyInquirer import prompt
from pyfiglet import Figlet
from termcolor import cprint
import os

def createMenu():
    file_names = ["hospitalizations-by-vaccination-status",
                  "licensed-child-care-settings-summary",
                  "long-term-care-home-summary",
                  "vaccine-data-by-age",
                  "radio-canada-international-data"]

    questions = [
        {
            'type': 'list',
            'name': 'user_option',
            'message': "Please choose an option:\n",
            'choices': ["Update Data",
                        "Question 1 - Hospitalizations by vaccination status",
                        "Question 2 - Cases in Long-term care and Child-care",
                        "Question 3 - Vaccinations by age group and dosage",
                        "Question 4 - Total cases and deaths between Canada and other countries",
                        "Exit"]
        }
    ]

    f = Figlet(font='lean')
    
    while True:
        cls()
        
        cprint(f.renderText('Canada') + f.renderText('Covid-19'), 'red')

        cprint("*" * os.get_terminal_size()[0], 'red')
        cprint("Welcome to S\u00E3o Paulo group's COVID-19 data analyzer tool", 'white')
        cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

        print("Menu Instructions:")
        print("\n--> Up and Down arrows to move\
               \n--> Enter to select\n")
        
        answers = prompt(questions, style=project_style)

        cls()
        
        if answers.get("user_option") == "Update Data":
            buildData(file_names)
        elif answers.get("user_option") == "Question 1 - Hospitalizations by vaccination status":
            q1()
        elif answers.get("user_option") == "Question 2 - Cases in Long-term care and Child-care":
            q2()
        elif answers.get("user_option") == "Question 3 - Vaccinations by age group and dosage":
            q3()
        elif answers.get("user_option") == "Question 4 - Total cases and deaths between Canada and other countries":
            q4()
        elif answers.get("user_option") == "Exit":
            print("Exiting.....")
            return