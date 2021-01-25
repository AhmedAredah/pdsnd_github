import time
import pandas as pd
import numpy as np

#define the city data along with their file names
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# define months and their abbreviation
Month_list = {  'all':0, 'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7,
                'auguest':8, 'september':9, 'october':10, 'november':11, 'december':12,
                'jan':1, 'feb':2 , 'mar':3 , 'apr':4, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12 }

# define a list of all days              
DAY_LIST = [    'all', 'sunday', 'monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('Select a city to explore with among "'"chicago, new york city, washington"'"')
        city = input().lower().strip()
        #check if city is entered correctly
        if city in CITY_DATA:
            print('{} has been selected...\n'.format(city))
            break
        else:
            print('make sure you spelled the city name correctly!')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        
        print('select a month [str] to filter data with.\nAll, January, February, ... December')
        month = input().strip()

        #check if month name is entered correctly
        if month.lower() not in Month_list: print('make sure you spelled month name correctly!'); continue

        #print the selected month
        if month.lower() == 'all': 
            print('All months have been selected\n')
        else: 
            print('Month \"{}\" has been selected\n'.format(month))
        
        break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('select a day to filter data with.\nAll, Sunday, Monday, ... Saturday')
        day = input().strip()

        # check if day name is entered correctly
        if day.lower() not in DAY_LIST: print('make sure you spelled day name correctly!'); continue

        #print the selected day
        # adjust the printed statment to the user filter
        if day.lower() != 'all':
            print('Day "{}" has been selected\n'.format(day))
            break
        else:
            print('All days have been selected\n')
            break

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
    #try loading the database
    try:
        df = pd.read_csv(CITY_DATA[city])
    except:
        # Pandas could not be installed on PC
        print('Could not find the database file \"{}\" or pandas library is not installed'.format(CITY_DATA[city]))
        raise SystemExit
    
    # convert date columns from str type to date type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #extract month and day of the week  to new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # convert month name to month number
    month_value = int(Month_list[month])

    #apply the filters to selected month and day
    if month_value != 0:
        df = df[df['month'] == month_value]

    if day.lower() != 'all':
        df = df[df['day_of_week'].str.lower() == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # calculate the most common month
    popular_month = df['month'].mode()[0]

    # calculate the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    # calculate the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    #print statistics
    print('The most frequent time data is as below:\nMonth:{}\nDay of the week:{}\nHour:{}\n'.format(popular_month, popular_day,popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # calculate most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # calculate most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # calculate most frequent combination of start station and end station trip
    df['start_dest'] = df['Start Station'].astype(str) + ' - to - ' + df['End Station'].astype(str)
    popular_start_end_station = df['start_dest'].mode()[0]

    # print statstics
    print('The most frequent station data is as below:\nStart Station:{}\nDestination Station:{}\nStart-Destination Station Combination:{}\n'.format(popular_start_station, popular_end_station,popular_start_end_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = df['Trip Duration'].sum()

    # Calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # print statstics
    print('Statistics on total and average trip duration:\nTotal travel time(sec)={}\nmean travel time(sec)={}\n'.format(total_travel_time, mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts of user types
    count_user_type = df['User Type'].value_counts()
    print('frequency table of users by user type:\n{}'.format(count_user_type))

    # Calculate counts of gender
    if 'Gender' in df.columns:
        count_user_gender = df['Gender'].value_counts()
        print('\nfrequency table of users by gender:\n{}\n'.format(count_user_gender))
    else:
        print('*No Gender data for this city\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        print('Oldest user\'s birth year is {}\nYoungest user\'s birth year is {}\n'.format(oldest_user,youngest_user))
    else:
        print('*No birth data for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Dsiplay top 5 rows of the selected dataframe

    Parameters
    ----------
    df : Datafram
        Dataframe of the selected city.

    """
    while True:
        print('Do you wish to view top 5 rows of the row data? (yes or no)')
        respond = input().lower().strip()
        if respond == 'yes':
            print(df.head(5))
            break
        elif respond != 'no':
            print('Check your spelling, yes or no only?\n')
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
