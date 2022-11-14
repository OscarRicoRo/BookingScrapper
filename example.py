import Scrapper

print("Write the URL: ")
url = str(input())
print("Write the csv file name: ")
filename = str(input())
Scrapper.scrapper(url, filename)
