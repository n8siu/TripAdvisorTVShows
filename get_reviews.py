import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# returns new url to go to (for iterating through pages of reviews)
def reformat_url(orig_url, num):
    insert_pos = orig_url.find("-Reviews-")
    new_str = orig_url[:insert_pos] + "-Reviews-" + "or" + str(num) + "-" + orig_url[insert_pos+9:]
    return new_str


# takes in name of restaurant and TripAdvisor link as two strings separated by comma)
def run(rest_name, rest_link):

    driver.get(rest_link)

    time.sleep(2)

    # open the file to save the review
    csvFile = open("/Users/nathansiu/BigData_Final/BTIEA_reviews/{}_reviews.csv".format(rest_name), 'a')
    csvWriter = csv.writer(csvFile)

    # get num of pages
    if (check_exists_by_xpath("//div[@class='pageNumbers']")):
        p1 = driver.find_elements_by_xpath("//div[@class='pageNumbers']")
        p2 = p1[0].find_elements_by_xpath("//div[@class='pageNumbers']")
        p3 = p2[0].find_element_by_xpath(".//a[contains(@class,'last')]").get_attribute("data-page-number")
    else:
        p3 = 1

    print("range: " + str(p3))

    for i in range(0, int(p3)+1):

        if (check_exists_by_xpath("//span[@class='taLnk ulBlueLinks']")):
            # to expand the review
            driver.find_element_by_xpath("//span[@class='taLnk ulBlueLinks']").click()
            time.sleep(5)

        container = driver.find_elements_by_xpath("//div[@class='review-container']")
        num_page_items = len(container)

        for j in range(num_page_items):
            # gets the star rating of the restaurant
            string = container[j].find_element_by_xpath(
                ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class")
            data = string.split("_")

            # gets the date of review
            string_date = container[j].find_element_by_xpath(".//span[@class='ratingDate']").text

            # saves star rating, review text, and date of review in a CSV
            csvWriter.writerow(
                [data[3].encode('ascii', 'ignore'), container[j].find_element_by_xpath(".//p[@class='partial_entry']")
                    .text.replace("\n", "").encode('ascii', 'ignore'), string_date.encode('ascii', 'ignore')])

        # to change the page
        new_page = (i-1) * 10
        driver.get(reformat_url(rest_link, new_page))
        time.sleep(5)


    # driver.close()


if __name__ == '__main__':
    # uses ChromeDriver from the Chromium Driver for Selenium WebDriver
    driver = webdriver.Chrome("/Users/nathansiu/Downloads/chromedriver")

    f = open('/Users/nathansiu/Downloads/BestThingIEverAte.csv')
    csv_f = csv.reader(f)

    resto_name = ''
    resto_link = ''
    for row in csv_f:
        resto_name = row[0]
        print(resto_name)
        resto_link = row[1]
        print(resto_link)
        run(resto_name, resto_link)
