#!/usr/bin/env python

'''
main.py

Author(s): 
    Michael Janeway (1167994)
    Jake Goode (1202742)
    Shahmeer Shahid (1191616)
    Harsimran Ghuman Singh (1181018)

Project: CIS2250 W22 Project: COVID-19 Data Tracking
Date of Last Update: Mar 28, 2022.

Functional Summary
main.py contains the following function(s):
    main():
        main() calls the createMenu() function, starting the program

This file is the only file meant to be ran for this project
To use enter "python main.py" when in the project's directory
'''

from projectMenu import createMenu
    
def main():
    createMenu()
    
# References:

# To use .melt to make the pandas dataframe plotable
# https://stackoverflow.com/questions/44941082/plot-multiple-columns-of-pandas-dataframe-using-seaborn

# To have multiple pdf pages
# https://stackoverflow.com/questions/17788685/python-saving-multiple-figures-into-one-pdf-file

main()