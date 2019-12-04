from datetime import datetime, timedelta
import os

CALENDAR = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December']
SHOWS = ['DinersDriveInsAndDives.csv', 'ManVsFood.csv', 'BestThingIEverAte.csv']
DAYS = 365


# get list of file names for all csv files in the folder; ignores non csv files
def matchlist_iter(folder_path):
    files = [file_path for file_path in os.listdir(folder_path) if file_path.endswith('.csv')]
    return files


# creates dictionary with the name of the restaurant as the key and the air date as the values
def get_air_dates(filename):
    with open(filename) as restFile:
        dict = {}
        for rows in restFile:
            array = rows.split(',')
            date = array[2].split('\n')
            restaurant = array[0].replace('&', '_').replace("'s","_s")
            dict[restaurant] = date[0]
        dict.pop('rest_name')
        return dict


# calculates average rating from specified time period before and after air date
# we calculated the average rating of all reviews one year after and one year before air date
def find_average_rating(filename, AIR_DATE):
    with open(filename, "r") as file:
        before = []
        after = []
        for line in file:
            index=line.find('Reviewed',-30)
            data = line[index+9:-2].strip("'")
            if 'yesterday' in data:
                date = datetime.now() - timedelta(days=1)
            elif 'today' in data:
                date = datetime.now() 
            elif 'days' in data:
                num = int(data[0])
                date = datetime.now() - timedelta(days=num)
            elif 'week' in data:
                num = int(data[0]) * 7
                date = datetime.now() - timedelta(days=num)
            else:
                data = data.replace(',', '').split(' ')
                if data[0] in CALENDAR:
                    date = datetime(int(data[2]), int(CALENDAR.index(data[0])), int(data[1]))
                else:
                    return [0, 0]

            # date is more recent than AIR_DATE but not by more than a year
            if date > AIR_DATE and date < (AIR_DATE + timedelta(days= DAYS)):
                if line[2].isdigit():
                    after.append(int(line[2]))

            # date is before AIR_DATE but not by more than a year
            elif date < AIR_DATE and date > (AIR_DATE - timedelta(days= DAYS)):
                if line[2].isdigit():
                    before.append(int(line[2]))

        # averages the ratings
        if len(before)>0 and len(after)>0:
            avg_before = sum(before) / len(before)
            avg_after = sum(after) / len(after)
        else:
            return [0,0]
            
        return [avg_before, avg_after]
    

# finds the average number of reviews from a specified time period before and after air date
# we calculated the number of reviews one year after and one year before air date
def find_num_reviews(filename, AIR_DATE):
    with open(filename, "r") as file:
        before = 0
        after = 0
        for line in file:
            index=line.find('Reviewed',-30)
            data = line[index+9:-2].strip("'")

            # format the date
            if 'yesterday' in data:
                date = datetime.now() - timedelta(days=1)
            elif 'today' in data:
                date = datetime.now() 
            elif 'days' in data:
                num = int(data[0])
                date = datetime.now() - timedelta(days=num)
            elif 'week' in data:
                num = int(data[0]) * 7
                date = datetime.now() - timedelta(days=num)
            else:
                data = data.replace(',', '').split(' ')
                if data[0] in CALENDAR:
                    date = datetime(int(data[2]), int(CALENDAR.index(data[0])), int(data[1]))
                else:
                    return [0, 0]

            # date is more recent than AIR_DATE but not by more than a year
            if date > AIR_DATE and date < (AIR_DATE + timedelta(days= DAYS)):
                after += 1

            # date is before AIR_DATE but not by more than a year
            elif date < AIR_DATE and date > (AIR_DATE - timedelta(days= DAYS)):
                before += 1

        # returns the total number of reviews for these conditions
        return [before, after]


# helper function to run data analysis on all csv files
def collect_data(CSVs, ManVsFood, manvsfood_CSV):
    average_rating = []
    num_reviews = []
    
    for csv in CSVs:
        infile = '../Big Data Webscraping/' +  manvsfood_CSV + '/' + csv
        if csv[:-12] in ManVsFood: 
            AIR_DATE = ManVsFood[csv[:-12]].split('/')
            AIR_DATE = datetime(int(AIR_DATE[2]), int(AIR_DATE[0]), int(AIR_DATE[1]))

            average_rating.append(find_average_rating(infile, AIR_DATE))
            num_reviews.append(find_num_reviews(infile, AIR_DATE))
    
    return average_rating, num_reviews


# calculates the average rating from total rating
def analyze_ratings(average_rating):
    before = []
    after = []
    for rating in average_rating:
        if rating[0] > 0 and rating[1] > 0:  # filter out the errors
            before.append(rating[0])
            after.append(rating[1])
    
    if len(before) > 0 and len(after) > 0:
        avg_before = sum(before) / len(before)
        avg_after = sum(after) / len(after)
    print('','before:',round(avg_before,3))
    print('','after:',round(avg_after,3))
    
    return round(avg_before,3), round(avg_after,3)
    

# calculates the average number of reviews from total number
def analyze_reviews(num_reviews):
    before = []
    after = []
    for review in num_reviews:
        before.append(review[0])
        after.append(review[1])
    avg_before = sum(before) / len(before)
    avg_after = sum(after) / len(after)
    print('','before:',round(avg_before,3))
    print('','after:',round(avg_after,3))
    
    return round(avg_before,3), round(avg_after,3)


# main: find the average number and average rating of reviews 1yr before and 1yr after the airdate for all given restaurants
if __name__ == "__main__":
    ddd_CSVs = matchlist_iter('../Big Data Webscraping/DinersDriveInsAndDives_CSV')
    manvfood_CSVs = matchlist_iter('../Big Data Webscraping/manvsfood_CSV')
    bestthingieverate_CSV = matchlist_iter('../Big Data Webscraping/BestThingIEverAte_CSV')

    DinersDriveInsAndDives = get_air_dates(SHOWS[0])
    ManVsFood = get_air_dates(SHOWS[1])
    bestthingieverate = get_air_dates(SHOWS[2])

    ddd_average_rating, ddd_num_reviews = collect_data(ddd_CSVs, DinersDriveInsAndDives, 'DinersDriveInsAndDives_CSV')
    manvfood_average_rating, manvfood_num_reviews = collect_data(manvfood_CSVs, ManVsFood, 'manvsfood_CSV')
    bestthing_average_rating, bestthing_num_reviews = collect_data(bestthingieverate_CSV, bestthingieverate,
                                                                   'bestthingieverate_CSV')

    print('\t', 'Diners, Drive ins, and Dives: ')
    print('Average Rating:')
    analyze_ratings(ddd_average_rating)
    print('Number of Reviews:')
    analyze_reviews(ddd_num_reviews)
    print('')
    print('\t', 'Man vs. Food: ')
    print('Average Rating:')
    analyze_ratings(manvfood_average_rating)
    analyze_reviews(manvfood_num_reviews)
    print('')
    print('\t', 'Best Thing I Ever Ate: ')
    print('Average Rating:')
    analyze_ratings(bestthing_average_rating)
    print('Number of Reviews:')
    analyze_reviews(bestthing_num_reviews)