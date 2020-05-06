import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTH_LIST = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'All']

DAYS_LIST = {'Sunday',
             'Monday',
             'Tuesday',
             'Wednesday',
             'Thursday',
             'Friday',
             'Saturday',
             'Sunday',
             'All'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Please enter a city to analyze (Chicago, New York City, or Washington): ').title()

    while city not in CITY_DATA :
        city = input('Invalid city. Please input a valid city selection: ').title()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('Please select a month to analyze (input January - June or \'All\'): ').title()

    while month not in MONTH_LIST :
        month = input('Invalid. Please input a valid selection: ').title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please select a weekday to analyze (input weekday or \'All\'): ').title()

    while day not in DAYS_LIST :
        day = input('Invalid. Please input a valid selection: ').title()


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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All' :
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
        df = df.loc[df['month'] == month]

    if day != 'All' :
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df,city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month_num = df['month'].mode().values[0]
    popular_month = MONTH_LIST[popular_month_num-1].title()
    print('The most popular month for {} is: {}'.format(city, popular_month))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most popular weekday for {} is: {}'.format(city, popular_day_of_week))

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('The most popular starting hour for {} is: {}'.format(city, popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    pop_start_station = df['Start Station'].mode().values[0]
    print('The most common start station is: {}'.format(pop_start_station))

    #display most commonly used end station

    pop_end_station = df['End Station'].mode().values[0]
    print('The most common end station is: {}'.format(pop_end_station))

    # display most frequent combination of start station and end station trip

    df['routes'] = df['Start Station']+' '+df['End Station']
    common_route_combo = df['routes'].mode().values[0]
    print('The most common start and end station combination is: {}'.format(common_route_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time

    sum_travel_time = df['duration'].sum()
    print('The total travel time for this period is: {}'.format(str(sum_travel_time)))

    # display mean travel time

    avg_travel_time = df['duration'].mean()
    print('The average travel time for this period is: {}'.format(str(avg_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('Counts by user type:')
    print(df['User Type'].value_counts())

    # Display counts of gender

    if city != 'Washington' :
        print('\nCounts by gender:')
        print(df['Gender'].value_counts())

     # Display earliest, most recent, and most common year of birth

        print('\nThe youngest customer was born in: {}'.format(
            str(int(df['Birth Year'].min()))))

        print('\nThe oldest customer was born in: {}'.format(
            str(int(df['Birth Year'].max()))))

        print('\nThe most common customer birth year is: {}'.format(
            str(int(df['Birth Year'].mode().values[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    start_loc = 0
    end_loc = 5

    display_csv = input("Do you want to see the raw data? (yes/no): ").lower()

    if display_csv == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Display additional data? (yes/no): ").lower()
            if end_display == 'no':
                break

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? (yes/no): ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
