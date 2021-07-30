import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_dic = {'ch':'chicago', 'ny': 'new york city', 'wg': 'washington'}
    user_symbol = input("Enter a symbol from among the following:\n(<ch> for Chicago, <wg> for Washington, and <ny> for New York.)\nenter the symbol here:").lower() 
    
    #checking that the city entered by a user is in city dictionary
    while user_symbol not in city_dic:
        print("\nthis city is not found!")
        user_symbol = input("Re-enter a symbol from among the following:\n('ch' for Chicago, 'wg' for Washington, and 'ny' for New York.)\n").lower() 

    # get user input for month (all, january, february, ... , june)
    months_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    user_month = input("\nEnter a specific month like: 'may' or 'all' to display all months: ").lower()

    #checking that the month entered by a user is in months list
    while user_month not in months_list:
        print("\nincorrect month!")
        user_month = input("Re-enter a specific month like: 'may' or 'all' to display all months: ").lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    user_day = input("\nEnter a specific day like: 'monday' or 'all' to display all days: ").lower()

    #checking that the day entered by a user is in days list
    while user_day not in days_list:
        print("\nincorrect value for that day!")
        user_day = input("\nRe-enter a specific day like: 'monday' or 'all' to display all days: ").lower()
        
    print('-'*40)
    return city_dic[user_symbol], user_month, user_day

#/////////////////////////////////////////////////////////////////////////////////////////////////

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month #make a column called month that has all months in a numeric shape
    df['day_of_week'] = df['Start Time'].dt.weekday_name #make a column called day_of_week that has all days's names

    #checking that the user entered specific month to filter with it or not
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 #finds the value of the entered month!
        #january is 1 so we will get the index of it(0) and add 1 to it to become 1

        df = df[df['month'] == month] #df['month'] is a numeric month
        # the condition df['month'] == month finds the rows contain the month value like 3(march)

    if day != 'all':
        df = df[df['day_of_week'] == day.title()] # day.title() for example make the day from friday to Friday
        #to match .dt.weekday_name
    return df

#/////////////////////////////////////////////////////////////////////////////////////////////////

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    most_commen_month = df['month'].mode()[0]
    most_commen_day = df['day_of_week'].mode()[0]

    df['hour'] = df['Start Time'].dt.hour
    most_commen_hour = df['hour'].mode()[0]

    # display most commonly month, day, and hour
    print("The most commen month: ", most_commen_month)
    print("The most commen day: ", most_commen_day)
    print("The most commen hour: ", most_commen_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#/////////////////////////////////////////////////////////////////////////////////////////////////

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['commen'] = df['Start Station'] + "--" + df['End Station']
    most_frequent_combination = df['commen'].mode()[0]

    print("The most commen start station: ", most_start_station)
    print("The most commen end station: ", most_end_station)
    print("The most frequent combination: ", most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#/////////////////////////////////////////////////////////////////////////////////////////////////

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time: {0:.2f}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time: {0:.2f}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#/////////////////////////////////////////////////////////////////////////////////////////////////

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_of_user_types = df['User Type'].value_counts()
    print("The count of:\n{}".format(count_of_user_types))
    print('\n')

    # Display counts of gender
    #using try and except here beause that 'Washington' doesn't have data about Gender and Year Of Birth columns
    try:
        count_of_gender = df['Gender'].value_counts()
        print("The count of:\n{}".format(count_of_gender))
    except:
        print('the gender data is not found for "Washington" city')

    try:
        # Display earliest, most recent, and most common year of birth
        earliest_year = np.min(df['Birth Year'])
        most_recent_year = np.max(df['Birth Year'])
        most_commen_year = df['Birth Year'].mode()[0]

        print("\nThe earliest year is: ", int(earliest_year))
        print("The most recent year: ", int(most_recent_year))
        print("The most commen year: ", int(most_commen_year))
    except:
        print('the year of birth data is not found for "Washington" city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#/////////////////////////////////////////////////////////////////////////////////////////////////

def display_raw_data(city):
    print('\nDo you want to display raw data for {} as chunks? \n'.format(city))
    display_raw_data = input("enter 'yes' if you want that or 'no' if you don't want\n").lower()

    while display_raw_data not in ('yes', 'no'):
        print("That's invalid input, please enter your input again in between (yes, no)")
        display_raw_data = input("enter 'yes' if you want to show it or 'no' if you don't want\n").lower()
   
    while display_raw_data == 'yes':
        for rows in pd.read_csv(CITY_DATA[city], index_col = 0, chunksize = 5):
            print(rows)
            display_raw_data = input("enter 'yes' if you want to show it or 'no' if you don't want\n").lower()
            if display_raw_data != 'yes':
                print('you are finished displying the raw data.')
                print("thanks!")
                break
        break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
