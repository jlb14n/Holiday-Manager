import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class Holiday:
    name: str
    date: datetime.date
    
    def __str__ (self): #outputs: Holiday Name (Date)
        return f"{self.name} ({str(self.date)})"

    def __gt__(self,other):
        return self.date>other.date

    def __ge__(self,other):
        return self.date>=other.date

#This will be a list of Holiday objects
@dataclass
class HolidayList:
    def __init__(self):
        self.innerHolidays = [] 
   
    #Adds holiday to .innerHolidays parameter.
    #Inputs - new_holiday: Holiday Object
    def addHoliday(self,new_holiday):
        if isinstance(new_holiday,Holiday): #Checking new_holiday is a Holiday object
            if new_holiday not in self.innerHolidays: #checking if unique holiday
                self.innerHolidays.append(new_holiday)
                print("Inserted object!") #=================================================================================================================================
            else:
                print("This holiday is already in!") #=================================================================================================================================
        else:
            print("Not a Holiday object!") #============================================================================================================================================
    
    #Outputs Holiday object from .innerHolidays
    #Inputs - HolidayName: str, Date: datetime.date.
    def findHoliday(self,HolidayName, Date): 
        for holiday in self.innerHolidays:
            if holiday.name==HolidayName and holiday.date==Date:
                return holiday

    #Removes holiday from .innerHolidays parameter. 
    #Inputs - HolidayName: str, Date: datetime.date.
    def removeHoliday(self,HolidayName, Date): 
        try:
            self.innerHolidays.remove(self.findHoliday(HolidayName,Date))
            print("Removed Holiday") #=================================================================================================================================
        except:
            print("Could not find Holiday") #=================================================================================================================================
    
    #Adds holidays into .innerHolidays from a file
    #Inputs - filelocation: str (a json file path)
    def read_json(self,filelocation): #default: holidays_output.json
        with open(filelocation,"r") as f:
            for holiday in json.loads(f.read())['holidays']:
                self.addHoliday(Holiday(holiday['name'],datetime.date.fromisoformat(holiday['date'])))

    #Writes .innerHolidays parameter into a json file
    #inputs - filelocation: str (a json file path)
    def save_to_json(self,filelocation):
        with open(filelocation,"w") as f:
            holidays={"holidays":[]}
            for holiday in self.innerHolidays:
                holidays["holidays"].append(holiday.__dict__)
            f.write(json.dumps(holidays,indent=4,default=str))

holidayList=HolidayList()
holidayList.read_json("holidays.json")
holidayList.addHoliday(100)
holidayList.save_to_json('holidays_output.json')

    # def scrapeHolidays(self):
    #     # Define years list (202,2021,2022,2023,2024)
    #     # use a for loop with the years list to get every year
    #         # Scrape Holidays from https://www.timeanddate.com/holidays/us/{year} 
    #             #Use a for loop to cycle through each <tr> (#in table id="holidays-table" #in <tbody>)
    #                 #<th> is the date, second <td> is the name of the holiday
    #                 # Check to see if name and date of holiday is in innerHolidays array (if findHoliday)
    #                 # Add non-duplicates to innerHolidays ()
    #     # Handle any exceptions.
    #     pass     

    # def numHolidays(self):
    #     # Return the total number of holidays in innerHolidays (len())
    #     pass
    
    # def filter_holidays_by_week(self,year, week_number):
    #     # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
    #         #return list(filter(lambda x: x.date.isocalendar().week==week_number and x.date.isocalendar().year==year, innerHolidays))
    #     # return your holidays
    #     pass

    # def displayHolidaysInWeek(self,holidayList,withWeather=False): 
    #     # Output formated holidays in the week. (sort by date using __gt__)
    #     # * Remember to use the holiday __str__ method. print(holiday)
    #     # If withWeather is true
    #         # weather=getWeather()
    #         # print(str(holiday) + " - " + weather[holiday.date])
    #     pass

    # def getWeather(self):
    #     # https://rapidapi.com/community/api/open-weather-map
    #     # This API returns a 16 day forecast starting at the current day. Restrict this to return only 7 days.
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # Format weather information as a dictionary {date1:'weather data', date2:'weather data', ...}and return weather string.
    #     pass

    # def viewCurrentWeek(self):
    #     # Use the Datetime Module to look up current week
    #         #datetime.now().isocalendar().week
    #     # Use your filter_holidays_by_week function to get the list of holidays 
    #     # for the current week/year
    #     # Use your displayHolidaysInWeek function to display the holidays in the week
    #     # Ask user if they want to get the weather
    #     # If yes, use your getWeather function and display results
    #     pass
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Create isSaved variable, initialize as False
        # 4. Display User Menu and take user input for their action based on Menu and check the user input for errors (menu()) 
        # 5. Run appropriate method from the HolidayList object depending on what the user input is
        # 6. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
            #selection=menu():
                #if menu==selection:
                    #if addHolidayMenu():
                        #isSaved=False
                #if menu==selection:
                    #if removeHolidayMenu():
                        #isSaved=False
                #if menu==selection:
                    #if saveHolidayMenu():
                        #isSaved=True
                #if menu==selection:
                    #viewHolidayMenu()
                #if menu==selection:
                    #if exitMenu(saved)
                        #break
                    
    pass

if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





