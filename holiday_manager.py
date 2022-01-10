import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from functools import reduce
import os
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
   
    #Adds holiday to .innerHolidays parameter. Returns true or false if holiday added 
    #Inputs - new_holiday: Holiday Object
    def addHoliday(self,new_holiday):
        if isinstance(new_holiday,Holiday): #Checking new_holiday is a Holiday object
            if new_holiday not in self.innerHolidays: #checking if unique holiday
                self.innerHolidays.append(new_holiday)
                return True
            else:
                return False #This holiday is already in!
        else:
            return False #Not a Holiday object!
    
    #Outputs Holiday object from .innerHolidays. 
    #Inputs - HolidayName: str, Date: datetime.date.
    def findHoliday(self,HolidayName, Date): 
        for holiday in self.innerHolidays:
            if holiday.name==HolidayName and holiday.date==Date:
                return holiday

    #Removes holiday from .innerHolidays parameter. Returns true or false if holiday removed
    #Inputs - HolidayName: str, Date: datetime.date.
    def removeHoliday(self,HolidayName, Date): 
        try:
            self.innerHolidays.remove(self.findHoliday(HolidayName,Date))
            return True
        except:
            return False
    
    #Adds holidays into .innerHolidays from a file
    #Inputs - filelocation: str (a json file path)
    def read_json(self,filelocation): #default: holidays_output.json
        with open(filelocation,"r") as f:
            for holiday in json.loads(f.read())["holidays"]:
                self.addHoliday(Holiday(holiday["name"],datetime.date.fromisoformat(holiday["date"])))

    #Writes .innerHolidays parameter into a json file
    #inputs - filelocation: str (a json file path)
    def save_to_json(self,filelocation):
        with open(filelocation,"w") as f:
            holidays={"holidays":[]}
            for holiday in self.innerHolidays:
                holidays["holidays"].append(holiday.__dict__)
            f.write(json.dumps(holidays,indent=4,default=str))

    #Scrapes all Holidays 2 years ago, this year, and 2 years in the future from timeanddate.com and adds them into .innerHolidays
    def scrapeHolidays(self):
        this_year=datetime.date.today().year
        for year in range(this_year-2,this_year+2):
            html = requests.get(f"https://www.timeanddate.com/holidays/us/{year}").text
            soup = BeautifulSoup(html,"html.parser")
            for item in soup.find("table",attrs={"id":"holidays-table"}).find("tbody").find_all("tr"):
                try:
                    holiday_date=datetime.datetime.strptime(f"{item.find('th').get_text()} {year}","%b %d %Y").date()
                    holiday_name=item.find("td").next_sibling.get_text()
                    self.addHoliday(Holiday(holiday_name,holiday_date))
                except:
                    continue
    
    #Returns the total number of holidays in innerHolidays
    def numHolidays(self):
        return len(self.innerHolidays)    

    #Returns list of Holiday objects
    #Inputs: self.innerHolidays, the year and week_number to filter by
    def filter_holidays_by_week(self,year, week_number):
        return list(filter(lambda x: x.date.isocalendar().week==week_number and x.date.isocalendar().year==year, self.innerHolidays))

    #Returns list of dictionaries for a 7 day forecast starting from today
    def getWeather(self):
        try:
            url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
            querystring = {"q":"district of columbia","cnt":"7","units":"imperial"} #=================================================================================
            headers = { #=============================================================================================================================================
                "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
                "x-rapidapi-key": "3b625cacbemshf536c40263ff31ap18df15jsn4cb571e5ef73"
                }
            response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
            weatherstring={}
            for day in response["list"]:
                weatherstring[datetime.datetime.fromtimestamp(day["dt"]).date()]=day["weather"][0]["main"]
            return weatherstring
        except:
            return "Weather API not working" #========================================================================================================================

    #Sorts and prints a list of holidays. If withWeather is true, also prints weather data from getWeather()
    #Inputs - holidayList: list of Holiday objects, withWeather: boolean (default=False)
    def displayHolidaysInWeek(self,holidayList,withWeather=False): 
        sorted_list=[]
        while len(holidayList)>0: #Sorting the holidayList
            minimum_holiday = reduce(lambda x1,x2: x1 if x1<x2 else x2, holidayList)
            sorted_list.append(minimum_holiday)
            holidayList.remove(minimum_holiday)
        if withWeather:
            weather=self.getWeather()
            for holiday in sorted_list:
                try:
                    print(f"{holiday} - {weather[holiday.date]}")
                except: #Just in case the API breaks
                    print(f"{holiday} - ERROR")
                    print(weather)
        else:
            for holiday in sorted_list:
                print(holiday)

    #Filters the .innerHolidays for the current week (today -> 6 days from today) and prints it. If withWeather is true, also prints weather data
    #Inputs - withWeather: boolean (default=False)
    def viewCurrentWeek(self,withWeather=False):
        current_week=[datetime.date.today()]
        for i in range(1,7):
            current_week.append(current_week[0]+datetime.timedelta(days=i))
        holidays_this_week=list(filter(lambda x: x.date in current_week, self.innerHolidays))
        self.displayHolidaysInWeek(holidays_this_week,withWeather)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Functions
#Prints out title message from file
#Input - msg: str title description
def titlemsg(msg):
    with open(r'texts\menu-title.txt',"r") as f:
        print(f.read().format(title=msg))

#Prints out an error message from file
#Input - msg: str error description
def errormsg(msg):
    with open(r'texts\error.txt',"r") as f:
        print(f.read().format(desc=msg))

#Prints out a success message from file
#Input - msg: str success description
def successmsg(msg):
    with open(r'texts\success.txt',"r") as f:
        print(f.read().format(desc=msg))

#Returns menu selection after printing the menu and validating selection
def menu(): #returns menu selection option
    titlemsg("Holiday Menu")
    with open(r'texts\menu-options.txt',"r") as file:
        print(file.read())
    while True:
        selection=input("Menu selection: ")
        try:
            if int(selection)<=5:
                return int(selection)
            else:
                errormsg("Invalid selection: integer too large.")
        except:
            errormsg("Invalid input: not an integer.")

#Adds inputted holiday is added into holidayList. Returns true or false depending on whether holiday was added
#Input -  holidayList: HolidayList object
def addHolidayMenu(holidayList):
    titlemsg("Add a Holiday")
    holiday=input("Holiday: ")
    date=input("Date (yyyy-mm-dd): ")
    while True:
        try: 
            date=datetime.date.fromisoformat(date)
            break
        except: 
            errormsg("Invalid date. Please try again.")
            date=input("Date for {0} (yyyy-mm-dd): ".format(holiday))
    holiday_obj=Holiday(holiday,date)
    if holidayList.addHoliday(holiday_obj):
        successmsg(f"{holiday_obj} has been added to the holiday list.")
        return True
    else:
        errormsg(f"{holiday_obj} is already in the holiday list")
        return False

#Removes inputted holiday is added into holidayList. Returns true or false depending on whether holiday was removed
#Input -  holidayList: HolidayList object
def removeHolidayMenu(holidayList): #returns true or false depending on if a holiday was removed
    titlemsg("Remove a Holiday")
    while True:
        holiday=input("Holiday Name: ")
        date=input("Date (yyyy-mm-dd): ")
        while True:
            try: 
                date=datetime.date.fromisoformat(date)
                break
            except: 
                errormsg("Invalid date. Please try again.")
                date=input("Date for {0} (yyyy-mm-dd): ".format(holiday))
        if holidayList.removeHoliday(holiday,date):
            successmsg(f"{Holiday(holiday,date)} has been removed from the holiday list.")
            return True
        else:
            errormsg(f"{Holiday(holiday,date)} not found.")
            if input("Would you like to return to the main menu? (yes=1): ")=="1":
                return False
            print('')

#Saves holidayList to a json file as requested. Returns true or false depending on if the holidays were saved
#Input -  holidayList: HolidayList object
def saveHolidayMenu(holidayList):
    titlemsg("Saving Holiday List")
    while True:
        selection=input("Are you sure you want to save your changes? [y/n]: ")
        if selection.lower()=='y':
            filename=input("Input desired file name (leave blank for 'holidays_output.json'): ")
            if filename == "":
                filename="holidays_output.json"
            holidayList.save_to_json(filename)
            successmsg("Your changes have been saved.")
            print("There are {0} holidays stored in {1}".format(holidayList.numHolidays(),filename))
            return True
        elif selection.lower()=='n':
            print("Canceled:")
            print("Holiday list file save canceled.")
            return False
        else:
            errormsg("Not a valid input. Please try again.")

#Print a week of holidays based on year or week. Can also print this week's with weather
#Input -  holidayList: HolidayList object
def viewHolidayMenu(holidayList):
    titlemsg("View Holidays")
    while True:
        year=input("Which year?: ")
        try: 
            year=int(year)
            break
        except: errormsg("Invalid input: not an integer.")
    while True:
        if year==datetime.date.today().year:
            week=input("Which week? #[1-52, Leave blank for the current week]: ")
        else:
            week=input("Which week? #[1-52]: ")
        try:
            if week=="" and year==datetime.date.today().year:
                while True:
                    selection=input("Would you like to see this week's weather? [y/n]: ")
                    if selection.lower() == "y":
                        print("\nThese are the holidays for this week:")
                        holidayList.viewCurrentWeek(True)
                        return
                    elif selection.lower() == "n":
                        print("\nThese are the holidays for this week:")
                        holidayList.viewCurrentWeek(False)
                        return
                    else:
                        errormsg("Not a valid input. Please try again.")
            elif int(week)>0 and int(week)<53:
                print(f"\nThese are the holidays for {year} week #{week}:")
                holidayList.displayHolidaysInWeek(holidayList.filter_holidays_by_week(year,int(week)))
                return
            else:
                errormsg("Invalid input: integer not between 1 and 52. Please try again.")
        except:
            errormsg("Invalid input: not an integer.")

#Exits the program. Returns true or false depending if the user wishes to exit. Changes text depending on if changes have been saved.
#Input - isSaved: boolean
def exitMenu(isSaved): #returns true or false depending on if user wants to exit
    titlemsg("Exit")
    print("Are you sure you want to exit?")
    if not isSaved:
        print("Your changes will be lost.")
    while True:
        selection=input("[y/n] ")
        if selection.lower()=="y":
            return True
        elif selection.lower()=="n":
            return False
        else:
            errormsg("Not a valid input. Please try again.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Main function
def main():
    titlemsg("Holiday Management")
    holidays=HolidayList()
    holidays.read_json("holidays.json")
    print("There are {0} holidays stored in holidays.json.".format(holidays.numHolidays()))
    holidays.scrapeHolidays()
    isSaved=False
    while True:
        selection=menu()
        if selection==1:
            if addHolidayMenu(holidays):
                isSaved=False
        if selection==2:
            if removeHolidayMenu(holidays):
                isSaved=False
        if selection==3:
            if saveHolidayMenu(holidays):
                isSaved=True
        if selection==4:
            viewHolidayMenu(holidays)
        if selection==5:
            if exitMenu(isSaved):
                break

if __name__ == "__main__":
    main()





