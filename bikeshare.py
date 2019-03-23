import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ('monday','tuesday','wednesday','thursday','friday', 'saturday', 'sunday')
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\nWould you like to explore data for chicago, new york city or washington? please type the name of the city.')
    while True:
        city = input().lower().strip()
        if city == 'quit':
            quit()
        if city in CITY_DATA:
            break
        print('\nPlease enter a valid city name!\n ...or type \'quit\' to terminate program.')
    print('\nwould like to filter the data by month? please type \n\'january\', \n\'february\', \n\'march\', \n\'april\', \n\'may\', \n\'june\' \nor \'all\'')
    while True:
        month = input().lower().strip()
        if month == 'all':
            break
        elif month in set(months):
            break
        elif month == 'quit':
            quit()
        print('\nPlease type a valid month or \'all\'!\nOr, to terminate program, type \'quit\'.')
    print('\nwhould like to filter the data by day of the week? please type \n\'monday\', \n\'tuesday\', \n\'wednesday\', \n\'thursday\', \n\'friday\', \n\'saturday\', \n\'sunday\' \nor \'all\'')
    while True:
        day = input().lower().strip()
        if day == 'all':
            break
        if day in days:
            break
        if day == 'quit':
            quit()
        print('\nplease type a valid day of the week or \'all\'!\nOr, to terminate program, type \'quit\'.')
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def raw_data(df):
    """Displays five lines of raw data upon user request."""

    print('\nWould you like to see five lines of raw data prior to calculating statistics? Please type \'yes\' or \'no\'')
    n =5
    while True:
        y_n = input().lower().strip()
        if y_n == 'no':
            break
        elif y_n == 'yes':
            print(df.head(n))
            n += 5
            print('\nWould you like to see five more lines of data?')
        elif y_n != 'yes' or 'no':
            print('\nPlease enter \'yes\' or \'no\'')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].value_counts().idxmax()
    popular_month = months[popular_month-1]
    print('Busiest month on record:', popular_month)

    popular_day = df['day_of_week'].value_counts().idxmax()
    print('Busiest day of the week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    if popular_hour > 12:
        popular_hour = popular_hour - 12
        print('Most Frequent Start Hour:', popular_hour, 'pm')
    elif popular_hour == 12:
        print('Most Frequent Start Hour:', popular_hour, 'pm')
    elif popular_hour == 0:
        popular_hour = popular_hour + 12
        print('Most Frequent Start Hour:', popular_hour, 'am')
    else:
        print('Most Frequent Start Hour:', popular_hour, 'am')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most common start station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most common end station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    df['station_combo'] = 'START: ' + df['Start Station'] + ' END: ' + df['End Station']
    popular_station_combo = df['station_combo'].value_counts().idxmax()
    print('Most common combination of stations:', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = pd.to_datetime(int(df['Trip Duration'].sum()), unit='s')
    print('The total travel time for {} filtered by {} and {} is:'.format(city, month, day), str(total_time)[-8:], 'hrs')

    mean_time = pd.to_datetime(int(df['Trip Duration'].mean()), unit='s')
    print('The mean travel time for {} filtered by {} and {} is:'.format(city, month, day), str(mean_time)[-5:], 'hrs')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    type_count = df['User Type'].value_counts()
    print('The count of Users by type is:\n', type_count)

    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of Users by gender is:\n', gender_count)
    except KeyError:
        print('\nThere is no gender data.')

    try:
        print('\nThe earliest year of birth is:', int(df['Birth Year'].min()))
        print('\nThe most recent year of birth is:', int(df['Birth Year'].max()))
        print('\nThe most common year of birth is:', int(df['Birth Year'].mode()))
    except KeyError:
        print('\nThere is no birth year data.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, city, month, day)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
