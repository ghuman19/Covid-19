#!/usr/bin/env python

'''
projectQuestions.py

Author(s): 
    Michael Janeway (1167994)
    Jake Goode (1202742)
    Shahmeer Shahid (1191616)
    Harsimran Ghuman Singh (1181018)

Project: CIS2250 W22 Project: COVID-19 Data Tracking
Date of Last Update: Mar 28, 2022.

Functional Summary
projectQuestions.py contains the following function(s):
    q1():
        q1() allows the user to interactively make the graph related to
        our project's first question.

    q2():
        q2() allows the user to interactively make the graph related to
        our project's second question.

    q3():
        q3() allows the user to interactively make the graph related to
        our project's third question.

    q4():
        q4() allows the user to interactively make the graph related to
        our project's fourth question.

This file is a module file, it is not meant to be run
'''

# Data management and graphing libraries
import os
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools
import matplotlib.backends.backend_pdf

# User interface and experience libraries
from PyInquirer import prompt
from termcolor import cprint

from projectUtilities import getDateRange, convertList, project_style



# =======================================================================
# Question 1 - Hospitalizations by vaccination status
# =======================================================================
def q1():
    # Prints title
    cprint("=" * os.get_terminal_size()[0], 'blue')
    cprint("Question 1 - Hospitalizations by vaccination status", 'white')
    cprint("=" * os.get_terminal_size()[0], 'blue', end="\n\n")
    
    # Open and read file if it exists, if not prompt user and return
    try:
        df = pd.read_csv("data/hospitalizations-by-vaccination-status/{}".format(os.listdir("data/hospitalizations-by-vaccination-status")[0]))
    except FileNotFoundError:
        input("File not found, please Update Data and try again\nPress ENTER to return to menu")
        return

    # Set the date column to datetime objects
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

    # Sort dataframe based on date
    df = df.sort_values(by=['date'])

    # Get start and end dates for data sorting
    start_date, end_date = getDateRange(df.iloc[0]['date'], df.iloc[-1]['date'])

    # Inclusively slices between the start and end dates
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Makes the totals into columns as well
    df["Total ICU"] = df["icu_unvac"] + df["icu_partial_vac"] + df["icu_full_vac"]
    df["Total Non-ICU"] = df["hospitalnonicu_unvac"] + df["hospitalnonicu_partial_vac"] + df["hospitalnonicu_full_vac"]
    df["Full Total"] = df["Total Non-ICU"] + df["Total ICU"]

    # Rename columns to increase readability
    df = df.rename(columns={
        "icu_unvac": "ICU un-vaccinated",
        "icu_partial_vac": "ICU partial vaccinated",
        "icu_full_vac": "ICU fully vaccinated",
        "hospitalnonicu_unvac": "Non-ICU un-vaccinated",
        "hospitalnonicu_partial_vac": "Non-ICU partial vaccinated",
        "hospitalnonicu_full_vac": "Non-ICU fully vaccinated",
    })

    # Pyinquirer questions
    questions = [
        {
            'type': 'checkbox',
            'name': 'user_input',
            'message': "Enter options:\n",
            'choices': convertList(list(df)[1:], 'name'),
        }
    ]

    # Introduce user to checkboxes
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection", 'white')
    print("Choose the data lines to graph using the following checkbox:")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")
    
    print("Checkbox navigation:")
    print("\n--> Up and Down arrows to move\
           \n--> Space to select\
           \n--> A to toggle all\
           \n--> I to invert selection(s)\
           \n--> Enter to enter selection(s)\n")

    # Prompt user with questions
    answers = prompt(questions, style=project_style)
    while answers['user_input'] == []:
        cprint("No options selected, please try again", 'red')
        answers = prompt(questions, style=project_style)

    # Completion of data selection
    # Shows user what was entered by them
    print("")
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection completed successfully\nThe following data lines will be output:", 'white')
    for entry in answers['user_input']:
        cprint(entry, 'blue')
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Slice dataframme to only the user inputted and date columns
    df = df[answers['user_input'] + ['date']]

    # Flips the data from columns to rows with date as index to enable plotting
    df = df.melt("date", var_name="cols", value_name="cases")
    
    # Create and customize graph
    fig = plt.figure()
    ax = sns.lineplot(x="date", y="cases", hue="cols", data=df)
    ax.xaxis.set_major_locator(ticktools.MaxNLocator(5))
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.legend(loc="upper right")
    plt.xticks(rotation = 45, ha = 'right')
    plt.title("Hospitalizations per Vaccination Status\n({} to {})".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    
    # Export to pdf
    fig.savefig("data/output/Q1.pdf", bbox_inches="tight")

    # Graph completion message
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Graph successfully created!\nLocated at 'data/output/Q1.pdf'")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Return to menu
    print("Press enter to return to menu...")
    input("")



# =======================================================================
# Question 2 - Cases in Long-term care and Child-care
# =======================================================================
def q2():
    # Prints title
    cprint("=" * os.get_terminal_size()[0], 'blue')
    cprint("Question 2 - Cases in Long-term care and Child-care", 'white')
    cprint("=" * os.get_terminal_size()[0], 'blue', end="\n\n")
    
    # Open and read files if they exist, if not prompt user to update and return
    try:
        # Open and read files
        lcc_df = pd.read_csv("data/licensed-child-care-settings-summary/{}".format(os.listdir("data/licensed-child-care-settings-summary")[0]))
        ltc_df = pd.read_csv("data/long-term-care-home-summary/{}".format(os.listdir("data/long-term-care-home-summary")[0]))
    except FileNotFoundError:
        input("Files not found, please Update Data and try again\nPress ENTER to return to menu")
        return

    # Slice data columns
    lcc_df = lcc_df[["reported_date", 
                     "current_lcc_centres_w_cases",
                     "new_lcc_related_child_cases"]]
    ltc_df = ltc_df[["Report_Data_Extracted", 
                     "LTC_Homes_with_Active_Outbreak",
                     "Confirmed_Active_LTC_Resident_Cases"]]

    # Rename date columns to 'date' to allow concatenation
    lcc_df.set_index('reported_date')
    lcc_df = lcc_df.rename(columns={"reported_date":"date"})
    ltc_df.set_index('Report_Data_Extracted')
    ltc_df = ltc_df.rename(columns={"Report_Data_Extracted":"date"})
    
    # Concatenate DataFrames into one
    df = pd.concat([lcc_df, ltc_df])

    # Set the date column to datetime objects
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

    # Sort dataframe based on date
    df = df.sort_values(by=['date'])

    # Get start and end dates for data sorting
    start_date, end_date = getDateRange(df.iloc[0]['date'], df.iloc[-1]['date'])

    # Inclusively slices between the start and end dates
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Rename columns to increase readability
    df = df.rename(columns={
        "current_lcc_centres_w_cases": "Child care centres with cases",
        "new_lcc_related_child_cases": "Confirmed child cases",
        "LTC_Homes_with_Active_Outbreak": "Long term care homes with cases",
        "Confirmed_Active_LTC_Resident_Cases": "Confirmed resident cases",
    })

    # Pyinquirer questions
    questions = [
        {
            'type': 'checkbox',
            'name': 'user_input',
            'message': "Enter options:\n",
            'choices': convertList(list(df)[1:], 'name'),
        }
    ]

    # Introduce user to checkboxes
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection", 'white')
    print("Choose the data lines to graph using the following checkbox:")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")
    
    print("Checkbox navigation:")
    print("\n--> Up and Down arrows to move\
           \n--> Space to select\
           \n--> A to toggle all\
           \n--> I to invert selection(s)\
           \n--> Enter to enter selection(s)\n")

    # Prompt user with questions
    answers = prompt(questions, style=project_style)
    while answers['user_input'] == []:
        cprint("No options selected, please try again", 'red')
        answers = prompt(questions, style=project_style)

    # Completion of data selection
    # Shows user what was entered by them
    print("")
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection completed successfully\nThe following data lines will be output:", 'white')
    for entry in answers['user_input']:
        cprint(entry, 'blue')
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Slice dataframme to only the user inputted and date columns
    df = df[answers['user_input'] + ['date']]
    
    # Flips the data from columns to rows with date as index to enable plotting
    df = df.melt("date", var_name="cols", value_name="cases")

    # Create and customize graph
    fig = plt.figure()
    ax = sns.lineplot(x="date", y="cases", hue="cols", data=df)
    ax.xaxis.set_major_locator(ticktools.MaxNLocator(5))
    ax.set_xlim(start_date, end_date)
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.legend(loc="upper right")
    plt.xticks(rotation = 45, ha = 'right')
    plt.title("COVID-19 Cases in Childcare and Long-term Care Centres\n({} to {})".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

    # Export to pdf
    fig.savefig("data/output/Q2.pdf", bbox_inches="tight")

    # Graph completion message
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Graph successfully created!\nLocated at 'data/output/Q2.pdf'")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Return to menu
    print("Press enter to return to menu...")
    input("")


# Chart 1 - 1 dose
# Chart 2 - Fully vaccinated (2 doses)
# Chart 3 - 3 doses
# =======================================================================
# Question 3 - Vaccinations by age group and dosage
# =======================================================================
def q3():
    # Prints title
    cprint("=" * os.get_terminal_size()[0], 'blue')
    cprint("Question 3 - Vaccinations by age group and dosage", 'white')
    cprint("=" * os.get_terminal_size()[0], 'blue', end="\n\n")
    
    # Open and read file if it exists, if not prompt user to update and return
    try:
        df = pd.read_csv("data/vaccine-data-by-age/{}".format(os.listdir("data/vaccine-data-by-age")[0]))
    except FileNotFoundError:
        input("File not found, please Update Data and try again\nPress ENTER to return to menu")
        return

    # Fill empty second dose data with fully vaccinated data, as it switches over around Jan 2022
    df["Second_dose_cumulative"] = df["Second_dose_cumulative"].fillna(df["fully_vaccinated_cumulative"])

    # Rename columns to increase readability of titles
    df = df.rename(columns={"Date":"date", 
                            "At least one dose_cumulative":"At least one dose cumulative",
                            "Second_dose_cumulative":"Fully vaccinated (2 doses)",
                            "third_dose_cumulative":"Third Dose Cumulative"})

    # Slice the dataframe to only have the necessary columns 
    df = df[["date",
             "Agegroup",
             "At least one dose cumulative",
             "Fully vaccinated (2 doses)",
             "Third Dose Cumulative"]]
    
    # Set the date column to datetime objects
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

    # Sort dataframe based on date
    df = df.sort_values(by=['date', 'Agegroup'])

    # Get start and end dates for data sorting
    start_date, end_date = getDateRange(df.iloc[0]['date'], df.iloc[-1]['date'])

    # Inclusively slices between the start and end dates
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    removed_rows = ['Adults_18plus',
                    'Ontario_12plus',
                    'Undisclosed_or_missing',
                    'Ontario_5plus']
    
    df = df[~df['Agegroup'].isin(removed_rows)]

    questions = [
        {
            'type': 'checkbox',
            'name': 'user_input',
            'message': "Enter options:\n",
            'choices': convertList(df['Agegroup'].unique(), 'name'),
        }
    ]

    # Introduce user to checkboxes
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection", 'white')
    print("Choose the data lines to graph using the following checkbox:")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")
    
    print("Checkbox navigation:")
    print("\n--> Up and Down arrows to move\
           \n--> Space to select\
           \n--> A to toggle all\
           \n--> I to invert selection(s)\
           \n--> Enter to enter selection(s)\n")

    # Prompt user with questions
    answers = prompt(questions, style=project_style)
    while answers['user_input'] == []:
        cprint("No options selected, please try again", 'red')
        answers = prompt(questions, style=project_style)

    # Completion of data selection
    # Shows user what was entered by them
    print("")
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection completed successfully\nThe following data lines will be output:", 'white')
    for entry in answers['user_input']:
        cprint(entry, 'blue')
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Slices dataframe to match user input
    df = df[df.Agegroup.isin(answers['user_input'])]

    # Create a pdf page to hold all the charts
    pdf = matplotlib.backends.backend_pdf.PdfPages("data/output/Q3.pdf")
    
    all_titles = list(df)[2:]
    fig = plt.figure()
    
    for i in all_titles:
        # Create and customize graph
        plt.clf()
        ax = sns.lineplot(x="date", y=i, hue="Agegroup", data=df)
        ax.xaxis.set_major_locator(ticktools.MaxNLocator(5))
        ax.set_xlim([start_date, end_date])
        plt.xlabel("Date")
        plt.ylabel("Number of People")
        plt.legend(loc="upper right")
        plt.xticks(rotation = 45, ha = 'right')
        plt.title(i + "\n({} to {})".format(start_date.strftime("%Y-%m-%d"),
                                          end_date.strftime("%Y-%m-%d")))
        pdf.savefig(fig, bbox_inches="tight")

    # Export to pdf
    pdf.close()

    # Graph completion message
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Graph successfully created!\nLocated at 'data/output/Q3.pdf'")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Return to menu
    print("Press enter to return to menu...")
    input("")

# =======================================================================
# Question 4 - Total confirmed cases and deaths between Canada and other countries
# =======================================================================
def q4():
    # Prints title
    cprint("=" * os.get_terminal_size()[0], 'blue')
    cprint("Question 4 - Total confirmed cases and deaths between Canada and other countries", 'white')
    cprint("=" * os.get_terminal_size()[0], 'blue', end="\n\n")
    
    # Initialize variables
    country1, country2, user_input = "", "", ""

    # Open and read file if it exists, if not prompt user to update and return
    try:
        df = pd.read_csv("data/radio-canada-international-data/{}".format(os.listdir("data/radio-canada-international-data")[0]), header=6, usecols=range(4), index_col=False)
    except FileNotFoundError:
        input("File not found, please Update Data and try again\nPress ENTER to return to menu")
        return

    # Fix date column name
    df = df.rename(columns={"Date":"date"})
    
    # Set the date column to datetime objects
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

    # Sort dataframe based on date and country
    df = df.sort_values(['Geo', 'date'])
        
    # Get start and end dates for data sorting
    start_date, end_date = getDateRange(df.iloc[0]['date'], df.iloc[-1]['date'])

    # User data selection
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection ", 'white', end='')
    cprint("(CASE SENSITIVE)", 'blue')
    print("Choose the ", end='')
    cprint("TWO", 'blue', end='')
    print(" country data lines to graph using the following input fields:")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")
    
    # Ask if user wants to view country list
    while user_input not in ["y", "n"]:
        user_input = input("Would you like to view a list of the countries available? (y/n): ").lower()
    if user_input == 'y':
        for country in [*df["Geo"].unique()]:
            cprint(country, 'blue', sep="\n")
        
    # Get country1
    while not country1 in df["Geo"].unique():
        country1 = input("Enter country 1/2 (Press Enter to view country list): ")
        
        if country1 == '':
            for country in [*df["Geo"].unique()]:
                cprint(country, 'blue', sep="\n")
        elif not country1 in df["Geo"].unique():
            cprint("{} is not in the country list, please try again".format(country1), 'red')

    # Inform the user of their choice
    cprint("{} is in the country list.\n{} COVID-19 data will be graphed".format(country1, country1), 'green')

    
    # Get country2
    while not country2 in df["Geo"].unique():
        country2 = input("Enter country 2/2 (Press Enter to view country list): ")
        
        if country2 == '':
            for country in [*df["Geo"].unique()]:
                cprint(country, 'blue', sep="\n")
        elif not country2 in df["Geo"].unique():
            cprint("{} is not in the country list, please try again".format(country2), 'red')

    # Inform the user of their choice
    cprint("{} is in the country list.\n{} COVID-19 data will be graphed".format(country2, country2), 'green')

    # Completion of data selection
    # Shows user what was entered by them
    print("")
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Data selection completed successfully\nThe following data lines will be output:", 'white')
    for entry in [country1, country2]:
        cprint(entry, 'blue')
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Slice the dataframe to just country1 and country2 entries
    df = df.loc[(df['Geo'] == country1) | (df['Geo'] == country2)]

    # Inclusively slices between the start and end dates
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Create a pdf page to hold the charts
    pdf = matplotlib.backends.backend_pdf.PdfPages("data/output/Q4.pdf")
    all_titles = list(df)[2:4]

    # Create and customize graph, then add it to the pdf page
    fig = plt.figure()
    for i in all_titles:
        plt.clf()
        ax = sns.lineplot(x="date", y=i, hue="Geo", data=df)
        ax.xaxis.set_major_locator(ticktools.MaxNLocator(7))
        plt.xlabel("Date")
        plt.legend(loc="upper right")
        plt.xticks(rotation = 45, ha = 'right')
        plt.title(i + "\n({} to {})".format(start_date.strftime("%Y-%m-%d"),
                                            end_date.strftime("%Y-%m-%d")))
        pdf.savefig(fig, bbox_inches="tight")

    # Export to pdf
    pdf.close()

    # Graph completion message
    cprint("*" * os.get_terminal_size()[0], 'red')
    cprint("Graph successfully created!\nLocated at 'data/output/Q4.pdf'")
    cprint("*" * os.get_terminal_size()[0], 'red', end="\n\n")

    # Return to menu
    print("Press enter to return to menu...")
    input("")