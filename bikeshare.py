import time
import pandas as pd
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

fname = ""
separate = False

def log():
    """
    This is a logging function which will determine whether to log the information
    to a given file or output it to the console based on the arugments given
    when executing this file.
    """
    def log_func(func):
        def func_wrapper(*var):
            
            try:
                global fname
                if separate:
                    fname = func.__name__ + ".txt"
                #Will log to a file if the fname is not blank otherwise will 
                #go to the except block.
                with open(fname,"a") as f:
                    holder = sys.stdout
                    sys.stdout = f

                    if func.__name__ == "time_stats":
                        sys.stdout.write('\nCalculating The Most Frequent Times of Travel...\n')
                    elif func.__name__ == "station_stats":
                        sys.stdout.write('\nCalculating The Most Popular Stations and Trip...\n')
                    elif func.__name__ == "trip_duration_stats":
                        sys.stdout.write('\nCalculating Trip Duration...\n')
                    elif func.__name__ == "user_stats":
                        sys.stdout.write('\nCalculating User Stats...\n')
                    
                    start_time = time.time()
                    func(*var)                    
                    sys.stdout.write("\nThis took {0:.5f} seconds. \n".format(time.time() - start_time))
                        
                    sys.stdout.write("-"*40 + "\n")
                    sys.stdout = holder
                    f.close()
                    
            except Exception:
                #If no file is available to write to it will execute this code
                #and output the information to the console.
                if func.__name__ == "time_stats":
                    print('\nCalculating The Most Frequent Times of Travel...\n')
                elif func.__name__ == "station_stats":
                    print('\nCalculating The Most Popular Stations and Trip...\n')
                elif func.__name__ == "trip_duration_stats":
                    print('\nCalculating Trip Duration...\n')
                elif func.__name__ == "user_stats":
                    print('\nCalculating User Stats...\n')
                        
                start_time = time.time()
                func(*var)                    
                print("\nThis took {0:.5f} seconds. \n".format(time.time() - start_time))
                    
                print("-"*40 + "\n")
                
        return func_wrapper
    return log_func


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("What city would you like to explore: Chicago, New York,"+ 
                     "or Washington?\n").lower()
        
        if city in ('chicago', 'new york', 'washington'):
            break
        
        print("Sorry you chose a city with no data. Please try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        choice = input("\nWould you like data for a month, day, or both?\n").lower()
        
        if choice in ("month", "both"):
            while True:
                month = input("\nWhat month would you like data for: January, February,"+
                             "March, April, May, June, or all.\n").lower()
                
                if (month in ("january", "february", "march", "april", 
                                    "may", "june", "all")):
                    if choice == "month":
                        day = "all"
                    break
                
                print("Sorry you chose a month with no data. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
        if choice in ("day", "both"):
            while True:
                day = input("\nWhat day would you like data for: Monday, Tuesday, "+
                              "Wednesday, Thursday, Friday, Saturday, Sunday, or all \n").lower()
                
                if (day in ("monday", "tuesday", "wednesday", "thursday", 
                            "friday", "saturday", "sunday", "all")):
                    if choice == "day":
                        month == "all"
                    break
        
                print("\nSorry you chose an invalid day. Please try again.\n")
        if choice in ("day", "month", "both"):
            break
        
        print("\nInvalid choice Please try again.\n")
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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hours from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


@log()
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    
    # Most common month
    print("\nMost common month:")
    print(months[df['month'].mode()[0] - 1])

    # Most common day of week
    print("\nMost common day of week:")
    print(df['day_of_week'].mode()[0])

    # Most common start hour
    print("\nMost common start hour:")
    print(df['hour'].mode()[0])
    
    
@log()
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # Most commonly used start station
    print("\nMost commonly used start station:")
    print(df['Start Station'].value_counts().index[0])
    
    # Most commonly used end station
    print("\nMost commonly used end station:")
    print(df['End Station'].value_counts().index[0])

    # Most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] +", "+ df['End Station']
    print("\nMost frequent combination of start station and end station trip:")
    print(str(df['Station Combo'].value_counts().index[0]) + "\t" +str(df['Station Combo'].value_counts().max()))


@log()
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Total Travel Time
    print("\nTotal Travel Time:")
    print(str(df['Trip Duration'].sum()) + " seconds")

    # Mean Travel Time
    print("\nMean Travel Time:")
    print(str(df['Trip Duration'].mean()) + " seconds")

    
@log()
def user_stats(df):
    """Displays statistics on bikeshare users."""

    # Diplays the counts of each user type
    print("\nTypes of Users:")
    print(df['User Type'].value_counts())

    # Displays the number of each gender
    print("\nMakeup of individuals by Gender:")
    print(df['Gender'].value_counts())

    # Oldest Individuals
    print("\nOldest year of birth:")
    print(int(df['Birth Year'].min()))
    
    # Youngest individuals
    print("\nMost recent year of birth:")
    print(int(df['Birth Year'].max()))
    
    # Most common year of birth of individuals
    print("\nMost common year of birth:")
    print(int(df['Birth Year'].mode()[0]))
    

def get_args(arguments):
    """
    This function handles all arguments given when the file has been executed.
    
    additional options:
        -on
        -on 'filename'
        -on -s
        
    If there are no additional options given it will print everything to console.
    """
    global fname
    global separate
    
    if len(arguments) == 2:
        if arguments[1] == '-on':
            fname = "log.txt"
            print("\n\nPlease note that your output will be logged in file '{}'.\n".format(fname))
    elif len(arguments) == 3:
        if arguments[1] == '-on':
            if arguments[2] == '-s':
                separate = True
                print("\n\nPlease note that each function output will be logged separately.\n")
            else:
                fname = arguments[2]
                print("\n\nPlease note that your output will be logged in file '{}'.\n".format(fname))
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    get_args(sys.argv)
    main()
