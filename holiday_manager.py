import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from functools import reduce
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
                print("Inserted object!") #======================================================================================================================================
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
            print("Removed Holiday") #========================================================================================================================================
        except:
            print("Could not find Holiday") #=================================================================================================================================
    
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

holidayList=HolidayList()
holidayList.read_json("holidays.json")
holidayList.scrapeHolidays()
holidayList.save_to_json('holidays_output.json')
print(holidayList.numHolidays())
print(holidayList.filter_holidays_by_week(2022,4))
holidayList.displayHolidaysInWeek(holidayList.filter_holidays_by_week(2022,50))
holidayList.viewCurrentWeek(True)
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





