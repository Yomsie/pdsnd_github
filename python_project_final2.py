#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). Using a while loop to handle invalid inputs
    error_count=0
    while True:
        city=input('please select city you wish to explore\n\nnew york city, chicago, washington\n').lower()
        if city not in CITY_DATA:
            print('\ncity name not recognised, please try again')
            error_count+=1
            if error_count>2:
                print('Invalid entry for city..error will occur')
                break
            else:
                continue
        else:
            print('\nThanks! you\'ve  selected {}'.format(city))
            #break

    # get user input for month (all, january, february, ... , june)
        valid_months=['all','january','february','march','april','may','june']

        month = input('\nplease input month (only January to June) you will like to explore: type "all" for no filter\n').lower()

        if month not in valid_months:
            print('\nmonth name not recognised, please try again...restarting')
            continue
        else:
            print('\nThanks! you\'ve  selected: {}'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)

        valid_days=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = input('\nplease input name of day you will like to explore: type "all" for no filter\n').lower()

        if day not in valid_days:
            print('\name of day not recognised, please try again...restarting')
            continue
        else:
            print('\nThanks! you\'ve selected: {}'.format(day))

        print('-'*40)

        return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    week_days=list(["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"])

    with open('new_york_city.csv') as f1:
        ny=pd.read_csv(f1)
    with open('washington.csv') as f2:
        ws=pd.read_csv(f2)
    with open('chicago.csv') as f3:
        ch=pd.read_csv(f3)
    file_data1=pd.DataFrame(ny)
    file_data1['City']='New York City'
    file_data2=pd.DataFrame(ws)
    file_data2['Gender']=None
    file_data2['Birth Year']=None
    file_data2['City']='Washington'
    file_data3=pd.DataFrame(ch)
    file_data3['City']='Chicago'
    file_data=file_data1
    file_data=file_data.append(file_data2)
    file_data=file_data.append(file_data3)
    dfs = pd.DataFrame(file_data)
    dfs=dfs.rename(columns = {'Unnamed: 0': 'User_ID'})
    dfs['Start Time']=pd.to_datetime(dfs['Start Time'])
    dfs['Months']=dfs['Start Time'].dt.month_name()
    dfs['Weekday']=dfs['Start Time'].dt.weekday
    for i in range(7):
        dfs['Weekday']=dfs['Weekday'].replace(i,week_days[i])
    df_filter1 = dfs[dfs.City.eq(city.title())]
    # ignore filter when month selected is "all"
    if month=='all':
        df_filter2=df_filter1
    else:
        df_filter2 = df_filter1[df_filter1.Months.eq(month.title())]
    # ignore filter when day selected is "all"
    if day == 'all':
        df_filter3=df_filter2
    else:
        df_filter3 = df_filter2[df_filter2.Weekday.eq(day.title())]

    df = pd.DataFrame(df_filter3)

    #insert zeros for all NaN
    df=df.fillna(0)

    #viewing DataFrame for debugging
    print(df.head(10))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode=df['Months'].mode()[0]
    print('\nMost common month:{}'.format(month_mode))

    # display the most common day of week
    week_mode=df['Weekday'].mode()[0]
    print('\nMost common weekday:{}'.format(week_mode))

    # display the most common start hour
    df['Start_hr']=df['Start Time'].dt.hour
    strt_hr_mode=df['Start_hr'].mode()[0]

    print('\nMost common start hour:{}'.format(strt_hr_mode))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    strt_sttn_mode=df['Start Station'].mode()[0]
    print('\nThe Most Popular Start Station is\n{}'.format(strt_sttn_mode))

    # display most commonly used end station
    end_sttn_mode=df['End Station'].mode()[0]
    print('\nThe Most Popular End Station is\n{}'.format(end_sttn_mode))

    # display most frequent combination of start station and end station trip
    df['Start_Stop']=df['Start Station']+" to "+df['End Station']
    strt_stop_mode=df['Start_Stop'].mode()[0]
    print('\nThe Most Popular Start/End Station is\n{}'.format(strt_stop_mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    ttl_trvl_time=df['Trip Duration'].sum()/3600
    print('Total travel time in hrs is {}'.format(ttl_trvl_time))

    # display mean travel time
    mean_trvl_time=df['Trip Duration'].mean()/3600
    print('Average travel time in hrs is {}'.format(mean_trvl_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    cnt_user_typs=df.groupby(['User Type'])['User Type'].count()
    print('Current user types are: {}'.format(cnt_user_typs))

    # display counts of gender
    gender_typs=df.groupby(['Gender'])['Gender'].count()
    print('Current genders are: {}'.format(gender_typs))

    # display earliest, most recent, and most common year of birth
    most_recent_birth_yr=df['Birth Year'].max()
    print('Most recent Birth Year is: {}'.format(int(most_recent_birth_yr)))

    most_common_birth_yr=df['Birth Year'].mode()[0]
    print('Most common Birth Year is: {}'.format(int(most_common_birth_yr)))

    earliest_birth_yr=df['Birth Year'].min()
    print('The earliest Birth Year is: {}'.format(int(earliest_birth_yr)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nPlease note: All NaN data are converted to zero (0)!!')
    print('='*50)

def view_lines(df):
    """Displays few lines in trip database on user request."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # display few lines for user's satisfaction

    view_data = input('\n\n\nWould you like to view a few rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 5
    while view_data == 'yes': #(?????):
        print(df.iloc[:start_loc]) #(df.iloc[????:????]
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data != 'yes':
            break
        else:
            continue

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_lines(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThanks for exploring our US bikeshare data!!!')
            print('\n Bye'*10)
            break
if __name__ == "__main__":
	main()



# In[ ]:
