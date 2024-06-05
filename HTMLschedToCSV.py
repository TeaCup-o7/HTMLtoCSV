from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import pyperclip as pc

def main():
    #read clipboard
    html_content = pc.paste()

    #parse html
    soup = BeautifulSoup(html_content, 'html.parser')
    date = soup.find_all('h4')
    range = date[8].get_text().split(" Week of ")[1].split('                            ')
    rangeSplit = range[0].split(' –\n')
    range = [rangeSplit[0], range[1]] #why is this format such a mess? # provides [[month day], [month day year]]
    table = soup.find_all("div", {"class": "schedule-grid"})
    times = table[0].find_all("p", {"class": "shiftTimes"})
    i = 0
    schedule = ['', '', '', '', '', '', ''] 

    #parse table for dates and times
    for day in times:
        hours = day.get_text()
        if hours != "No Shifts":
            hours = hours.split(" - ")
            #print(hours)
        schedule[i] = hours
        i = i + 1
    
    #create dataframe
    days = []
    starts = []
    ends = []
    d = {"Subject": "H-E-B", "Start Date": days, "Start Time" : starts, 'End Time': ends, 'Description': "Auto Generated via Pyhon"}
    endTime = dt.datetime.strptime(range[1], "%b %d, %Y")
    y = 6
    #if schedule exists for day we format each for dataframe
    for day in schedule:
          if schedule[y] != 'No Shifts':
                  days.append(dt.datetime.strftime(endTime, "%m/%d/%Y"))
                  starts.append(schedule[y][0])
                  ends.append(schedule[y][1])
          
                
          y = y - 1
          endTime = endTime - dt.timedelta(days=1)
    d = pd.DataFrame.from_dict(d)
    d = d.set_index('Subject')
    print(d)
    d.to_csv("ScheduleWeekOf{}.csv".format(range[1]))

main()

