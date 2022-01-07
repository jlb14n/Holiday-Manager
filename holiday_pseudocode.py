import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

@dataclass
class Holiday:
    name: str
    date: datetime
    
    def __str__ (self):
        #output: Holiday Name (Date)
        pass

    def __gt__(self,other):
        #based on date
        pass

    def __ge__(self,other):
        #
        #based on date
        pass
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
        self.innerHolidays = [] #This will be a list of Holiday objects
   
    def addHoliday(self,holidayObj):
        # if holidayObj is an object:
            #insert object into innerHolidays list by using innerHolidays.append(holidayObj) #Maybe use insert and sort to create a sorted list?
            #print success statement
        #else:
            #print failure statement
        pass

    def findHoliday(self,HolidayName, Date):
        # Find Holiday in innerHolidays (loop with for loop, check with if statement)
        # Return Holiday
        pass

    def removeHoliday(self,HolidayName, Date):
        #if the Holiday __str__ can be used within innerHolidays.remove(value), 
            #use try: remove 
            #except: print failure
        #otherwise:
            # Find Holiday in innerHolidays by searching the name and date combination. (findHoliday(name,date))
            # remove the Holiday from innerHolidays (use innerHolidays.pop(index))
        # inform user you deleted the holiday (print success statement) return true
        #print failure statement if holiday not found return false
        pass

    def read_json(self,filelocation):
        # Read in things from json file location, make sure relative path
        # Use json.loads to make a list of dictionaries (each holiday is a dictionary)
        # Make each holiday item from dictionary to Holiday class
        # Use addHoliday function to add holidays to inner list.
        pass

    def save_to_json(self,filelocation):
        # Write out json file to selected file. (json.dumps())
        pass
        
    def scrapeHolidays(self):
        # Define years list (202,2021,2022,2023,2024)
        # use a for loop with the years list to get every year
            # Scrape Holidays from https://www.timeanddate.com/holidays/us/{year} 
                #Use a for loop to cycle through each <tr> (#in table id="holidays-table" #in <tbody>)
                    #<th> is the date, second <td> is the name of the holiday
                    # Check to see if name and date of holiday is in innerHolidays array (if findHoliday)
                    # Add non-duplicates to innerHolidays ()
        # Handle any exceptions.
        pass     

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays (len())
        pass
    
    def filter_holidays_by_week(self,year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
            #return list(filter(lambda x: x.date.isocalendar().week==week_number and x.date.isocalendar().year==year, innerHolidays))
        # return your holidays
        pass

    def displayHolidaysInWeek(self,holidayList,withWeather=False): 
        # Output formated holidays in the week. (sort by date using __gt__)
        # * Remember to use the holiday __str__ method. print(holiday)
        # If withWeather is true
            # weather=getWeather()
            # print(str(holiday) + " - " + weather[holiday.date])
        pass

    def getWeather(self):
        # https://rapidapi.com/community/api/open-weather-map
        # This API returns a 16 day forecast starting at the current day. Restrict this to return only 7 days.
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information as a dictionary {date1:'weather data', date2:'weather data', ...}and return weather string.
        pass

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week
            #datetime.now().isocalendar().week
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass

def menu(): #returns menu selection option
    #read in menu-title.txt and print it
    #read in menu.txt and print it
    #request user input
    #validate correct user input, continue to prompt if not valid
    #return input
    pass

def addHolidayMenu(): #returns true or false depending on if a holiday was added
    #read in menu-title.txt and print it
    #request user input for holiday and date
        #validate correct user input, continue to prompt if not valid
        #convert input to Holiday object
    #addHoliday(input)
    pass

def removeHolidayMenu(): #returns true or false depending on if a holiday was removed
    #read in menu-title.txt and print it
    #request user input for holiday and date
    #validate correct user input, continue to prompt if not valid
    #stay in loop until removeHoliday(name,date) succeeds
    #if it fails, add a way for user to escape loop if they no longer wish to remove a holiday
    pass

def saveHolidayMenu(): #returns true or false depending on if holidays were saved
    #read in menu-title.txt and print it
    #request user input y/n 
    #if y: request filename, save_to_json(filename)
    pass

def viewHolidayMenu():
    #read in menu-title.txt and print it
    #request user for year and week, check for valid responses (blank, 1-52)
    #if week is left blank, viewCurrentWeek()
    #else: displayHolidaysInWeek(filter_holidays_by_week(year,week_number))
    pass

def exitMenu(isSaved): #returns true or false depending on if user wants to exit
    #read in menu-title.txt and print it
    #change text depending on if isSaved is true or false
    #request input for wanting to leave
        #return true if yes
    pass

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
        #holidays=HolidayList()
    # 2. Load JSON file via HolidayList read_json function
        #holidays.readjson(file)
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
        #holidays.scrapeHolidays()
    # 4. Create isSaved variable, initialize as False
    # 5. Create while loop for user to keep adding or working with the Calender
        # 6. Display User Menu and take user input for their action based on Menu and check the user input for errors (menu()) 
        # 7. Run appropriate method from the HolidayList object depending on what the user input is (if, elif, ... statement)
            #use addHolidayMenu(),deleteHolidayMenu(),saveHolidayMenu(), viewHolidayMenu(), or exitMenu()
            #change isSaved based on the return of the functions
            #use break to exit the while loop when prompted
    pass

if __name__ == "__main__":
    main()


