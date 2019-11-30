#!/usr/bin/env python
# coding: utf-8import os
import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ["January", "February", "March", "April", "May", "June"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_city():
    """Asks the user to choose one city and returns the city"""
    while True:
        try:
            city = input("Let us explore the bikeshare data.\nChoose one of the three cities: ")
            city=city.lower().rstrip()
            if city in CITY_DATA:
                print(" Great...We will explore the bikeshare data for %s " %city.title())
                break
        except KeyboardInterrupt:
            print("Good bye!")
    return city

def select_option(option, options):
    """ Asks user to select an option and returns the chosen option.
    Args: 
        (str) option is either day of the week or month
        (List) options a list of days of the week or months
    Returns:
        (str) choice
    """
    
    while True:
        try:
            choice = input("Choose a {} or enter b  to go back: ".format(option))
            choice = choice.title().rstrip()
            if choice in options:
                break
            elif  choice == "B":
                choice = get_filter(option,options)
                break
        except KeyboardInterrupt:
            print("Good bye!")
            break

    return choice
def get_filter(option, options):
    """This function asks  users whether they to want to filter data by option.
    If yes, the user is asked to give the chosen option which is then returned.
    If not, the function returns 'all'
    Args: 
        (str) option 
        (List) options 
    Returns:
        (str) choice
        """
    while True:
        try:
            byoption = input("Do you want to filter by {} ? [y/n] ".format(option))
            byoption = byoption.lower().rstrip()
            if byoption =='yes' or byoption == 'y':
                choice = select_option(option,options)
                break
            elif byoption == 'no' or byoption == 'n':
                choice = 'all'
                break        
        except: 
            print("Good bye!")
            break
    return choice    

def load_data(city, month, day):
    """
     Loads data for the specified city and filters by month and day if applicable.
    Args:
         (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
     """
    
    # load data file into a dataframe
    filename = CITY_DATA.get(city)     
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of week'] = df['Start Time'].dt.day_name() #prefer using dt.day_name
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month']== month]

    # filter by day of week if applicable
    if day != 'all':
        #filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day]
    return df



def yes_or_no(request, message):
    
    """ Asks a yes/no question, prints a message in case the user answers no and also
    returns a string that helps keep track of the user's answer.
    Args:
    (str) request
    (str) message
    """
    while True:
        try:
            choice = input("Do you want to {}? [y/n]".format(request)).lower().rstrip()
            if choice == 'yes' or choice == 'y':
                print(message)
                report = 'proceed'
                break
            elif choice ==  'no' or choice == 'n':
                report = 'end'
                break
        except: 
            break
    return report
        


def stream_data(size, df):
    """A generator that streams chunks of the data as prompted by the user
    Args:
        (int) size - number of lines of data that are shown each time
        (pandas data frame) df 
    """
    start = 0; end = size
    i= 0
    while start <= len(df):
        if i == 0:
            x = yes_or_no('see some few lines of the data',df[start: min(end,len(df)+1)])
            yield x
        else:
            x =  yes_or_no('see more',df[start: min(end,len(df)+1)])
            yield x
        if x == 'end':
            break
        start = end
        end += size
        i += 1
        



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    popular_month = df['Month'].mode().values[0]
    #check if all data from the same day
    if not (df['Month']==df['Month'].iloc[0]).all():
        print("The most popular month is %s."% popular_month)
        month_filtered = False
    else:
        month_filtered =  True
    # display the most common day of week
    popular_day = df['Day of week'].mode().values[0]
    #check if all data from the same day- the else statement
    if not (df['Day of week']==df['Day of week'].iloc[0]).all():
        print("The most popular day of week is %s ." % popular_day)
        day_filtered = False
    else:
        day_filtered = True

    # display the most common start hour
    hour = df['Start Time'].dt.hour
    popular_hour = hour.mode().values[0]
    #when day or month is filtered, the message for hour mention the day or the month.
    if day_filtered and month_filtered:
        message = "On "+ popular_day + 's'+ " of " +  popular_month+', ' +\
            "the most popular start hour is "   + str(popular_hour)+ " o' clock."
    elif day_filtered and (not month_filtered):
        message = "On "+ popular_day + 's, ' + \
                           "the most popular start hour is "+ str(popular_hour)+ " o' clock."
    elif (not day_filtered) and month_filtered:
        message = "In "+ popular_month + "," + "the most popular start hour is " + str(popular_hour)
    else: message = "The most popular start hour is " + str(popular_hour)+ " o' clock."
    

    print(message)
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode().values[0]
    print("The most commonly used start station is %s ."%popular_start )


    # display most commonly used end station
    popular_end = df['End Station'].mode().values[0]
    print("The most commonly used end station is %s ."%popular_end )


    # display most frequent combination of start station and end station trip
    combined = pd.concat([df['Start Station'],df['End Station']])
    popular_station = combined.mode().values[0]
    print("The most commonly used station is %s ."%popular_station )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration = sum(df['Trip Duration'])
    duration_h = duration //3600
    duration_m = (duration//60)%60
    duration_s = (duration%60)
    print("The total travel time is {} hours {} minutes and {} seconds.".format(duration_h,duration_m, duration_s))
    # display mean travel time
    mean_duration = np.mean(df['Trip Duration'])
    mduration_m = (mean_duration//60)
    mduration_s = (mean_duration%60)
    print("The mean travel time is {} minutes and {} seconds.".format(mduration_m, mduration_s))
     
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("The counts of user types are the following:\n {}\n".format(user_type))
    
    #Barplot of user_type
    #df['User Type'].value_counts().plot.bar()
    
    # Draw a histogram of Trip Duration for suscribers and for customers
    #df.hist('Trip Duration', by='User Type',range=[0, 5000],bins=30)

    # Display counts of gender
    if 'Gender'in df.columns:
        freq_gender = df['Gender'].value_counts()
        print("The counts of user gender are the following:\n {}\n".format(freq_gender))
        
    #Bar plot of Gender
    #df['Gender'].value_counts().plot.bar()
    # Display earliest, most recent, and most common year of birth
    
    if 'Birth Year' in df.columns:        
        birth_year = df['Birth Year']
        oldest = int(min(birth_year))
        youngest = int(max(birth_year))
        common = int(birth_year.mode().values[0])
        
        print("The eldest user was born in {} .\n".format(oldest))
        print("The youngest user was born in {}.\n".format(youngest))
        print("Most commonly, users were born in {}.\n".format(common))
        
        print("Humm..., what do you think about the birth year of the eldest users?")
        time.sleep(3)

        #Surprisingly some users are born before 1890. Look at this closer.
        if oldest < 1920:
            print("Let us see how old they were when they went for a ride ")
            riding_age = pd.to_datetime(df['Start Time']).dt.year - df['Birth Year']
            oldest_riding_age = riding_age[birth_year==oldest]
            #Name the series
            oldest_riding_age.rename('Age At Riding Time', inplace=True)
            
            oldest_ride = df[['Start Time','Trip Duration','Birth Year']][df['Birth Year']==oldest]
            oldest_ride = pd.concat([oldest_ride, oldest_riding_age], axis=1)
            print(oldest_ride)
            time.sleep(3)
        print("The most advanced age at riding time is %s years?" %max(riding_age))
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        df = load_data(get_city(),get_filter('month', months), get_filter('day',days))
        df = df.drop('Unnamed: 0', axis=1)
        #
        data_stream = stream_data(5,df)
        for data in data_stream:
            while True:
                try:
                    next(data_stream)
                except:
                    break
                    
                    
        input("Press Enter to see some statistics about riding times")
        time_stats(df)
        
        input("Press Enter to see some statistics about Stations")
        station_stats(df)
        
        input("Press Enter to see some statistics about Trip duration")
        trip_duration_stats(df)
        
        input("Press Enter to see some statistics about the users")
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            break

            
if __name__ == "__main__":
    main()
# In[ ]:
