# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:41:45 2020

@author: aesha
"""

###########################################################
    #Computer Project #9
    #   open_file function
    #   build_dictionary function
    #   top_affected_by_spread function
    #   top_affected_by_numbers function
    #   is_affected function
    #   plot_by_number function
    #   affected_states_in_country function
    #   printing all data through main function
###########################################################


import csv
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from operator import itemgetter


def open_file():
    ''' Prompting for a file, and opening file. Otherwise print error.'''
    while True:
        fp = input("Data file: ")
        try:
            fp = open(fp, "r")
            return fp    
        except: 
            if fp =='': #automatically open file if no input
                fp = open("ncov.csv", "r")
                return fp
            else:
                print("Error. Try again.")#display error if file doesn't exist
    pass      

def build_dictionary(fp):
    '''Building dictionary with a dictionary of the country and tuple value'''  
    reader = csv.reader(fp)
    fp.readline() #skip header
    master_dict = {} #build master_dict
    
    for line in reader: #create variables
        area_dict = {}
        country = line[2]
        area = line[1]
        last_up = line[3]
        cases = int(line[4])
        deaths = int(line[5])
        recovered = int(line[6])
        if area == '':
            area = 'N/A'    
            
        area_dict[area] = (last_up, cases, deaths, recovered)#define area_dict

        if country in master_dict:#add to master_dict
            master_dict[country].append(area_dict)
        else:
            master_dict[country] = [area_dict] 
    return master_dict

def top_affected_by_spread(master_dict):
    '''Create a descending list of top 10 countries with the most areas affected'''
    topten = []#create list
    for key,val in master_dict.items():#add to list
         countries = key
         areas = 0
         for line in val:
             areas += 1
         topten.append((countries,areas))
    
    topten = sorted(topten, key=itemgetter(0), reverse = False)#order list
    topten = sorted(topten, key=itemgetter(1), reverse = True)
    topten = topten[0:10]#print top ten only
    return topten

def top_affected_by_numbers(master_dict):
    '''Create a descending list of top 10 countries with the most people affected within every country'''
    topten = []#create list
    for key,val in master_dict.items():#add to list
        countries = key
        people = 0
        for line in val:
            for key,val in line.items():
                people = people + val[1]
        topten.append((countries,people))
    topten = sorted(topten, key=itemgetter(0), reverse = False)#order list
    topten = sorted(topten, key=itemgetter(1), reverse = True)
    topten = topten[0:10]#print top ten only
    return topten

def is_affected(master_dict, country):
    '''Identifying affected countries'''
    for key,val in master_dict.items():
        if key.lower() == country.lower():
            return True #affected countries
    return False #otherwise unaffected

def plot_by_numbers(list_of_countries, list_of_numbers):
    '''
        This function plots the number of areas/people inffected by country.
        
        parameters: 
            list_of_countries: list of countries
            list_of_numbers: list of the number of areas/people inffected
            
        Returns: None
    '''
    fig, ax = plt.subplots()
    
    x_pos = [i for i, _ in enumerate(list_of_countries)]
    
    ax.barh(x_pos, list_of_numbers, align='center', color='red')
    ax.set_yticks(x_pos)
    ax.set_yticklabels(list_of_countries)
    ax.invert_yaxis()
    ax.set_xlabel('Count')
    ax.set_title('Novel Coronavirus statistics')
    
    plt.show()


def affected_states_in_country(master_dict, country):
    '''Returns a set of affected areas within a country'''
    states_set = set()#create set
    for line in master_dict.items():#add to set
        state = str(line[0])
        state = state.lower()
        if state == country:
            for i in line[1]:
                for j in i.keys():
                    states_set.add(j)
    if states_set == set():#identify if country exists
        print("Error. Country not found.")
        states_set = {}
    return states_set

def main():
    
    BANNER = '''
.__   __.   ______   ______   ____    ____
|  \ |  |  /      | /  __  \  \   \  /   /
|   \|  | |  ,----'|  |  |  |  \   \/   / 
|  . `  | |  |     |  |  |  |   \      /  
|  |\   | |  `----.|  `--'  |    \    /   
|__| \__|  \______| \______/      \__/  
    '''
    print(BANNER)
    
    fp = open_file() #call file pointer
    
    MENU = ''' 
[1] Countries with most areas infected
[2] Countries with most people affected
[3] Affected areas in a country
[4] Check if a country is affected
[5] Exit

Choice: '''
    
    master_dict = build_dictionary(fp) #return master_dict
    choice = input(MENU) #prompt for user option
    
    while choice != "5":
        country = []
        areas = []
        people = []
        if choice == '1': #print top ten areas affected
            print("{:<20s} {:15s}".format("Country", "Areas affected"))
            print("-"*40)
            for line in top_affected_by_spread(master_dict):
                print("{:<20s} {:5d}".format(*line))
            plot = input('Plot? (y/n) ') #prompt for user to plot
            if plot.lower() == 'y':
                for line in top_affected_by_spread(master_dict)[0:5]:
                    country.append(line[0])
                    areas.append(line[1])
                plot_by_numbers(country,areas)
            else:
                pass
        if choice == '2': #print top countries with msot people affected
            print("{:<20s} {:15s}".format("Country", "People affected"))
            print("-"*40)
            for line in top_affected_by_numbers(master_dict):
                print("{:<20s} {:5d}".format(*line))
            plot = input('Plot? (y/n) ') #prompt for user to plot
            if plot.lower() == 'y':
                for line in top_affected_by_numbers(master_dict)[1:6]:
                    country.append(line[0])
                    people.append(line[1])
                plot_by_numbers(country,people)
            else:
                pass
        if choice == '3': #prints affected areas in the given country
            affected = False
            country_in = input("Country name: ").lower()
            print("-"*30)
            for line in master_dict.keys():
                if country_in in line.lower():
                    affected = True
            if affected:
                print("{:<30s}".format("Affected area"))
                print("-"*30)
            for key,val in enumerate(sorted(affected_states_in_country(master_dict,country_in)),1) :   
                print("[{:02d}] {:<30s}".format(key,val))
        if choice == '4':
            country_in = input("Country name: ").lower()
            print("-"*30)
            if is_affected(master_dict,country_in):
                print("{} is affected.".format(country_in))
            else:
                print("{} is not affected.".format(country_in))
        if choice == '5':
            break
        if choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5': #print error if choice does not exist
            print("Error. Try again.")
        choice = input(MENU)
    print("Stay at home. Protect your community against COVID-19") #If option 5, program ends, prints farewell
        
    
if __name__ == "__main__":    
    main()