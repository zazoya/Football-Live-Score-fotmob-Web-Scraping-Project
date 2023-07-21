from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def user_info():
    while (True):
        datetype = input('Do you want the data for a-"Today" or b-"Specific day" (a/b):')
        datetype= datetype.lower()
        if  datetype =='a' or datetype=='b':
            break
        else:
            print("Please enter the type as formatted.")

    if datetype=='a':
        url="https://www.fotmob.com/"
    elif datetype=='b':
        while True:
            date_input = input("Please enter the date (YYYY-MM-DD):")
            try:
                x = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Please enter the date in the format YYYY-MM-DD.")
                continue
        x=str(x)
        x=x.replace("-",'')
        url=f"https://www.fotmob.com/?date={x}"

    return url

def find_page_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    '''
    If there is an issue with the code, 
    comment on this line "chrome_options.add_argument("--disable-gpu")" to ensure smooth execution,
    This line's significance is optimizing the rendering time of the code.
    '''

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.END)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content,'lxml')
    driver.quit()
    return soup

def scraper(soup):
    championships = soup.find_all("div", {"class": "e7pc1841"})
    match_details = []
    for championship in championships:
        champion_title = championship.contents[0].find("a").text
        all_matches = championship.find_all('a', {"class": "ew7iiy61"})
        for match in all_matches:
            teama = match.find_all("span", {"class": "e1o4kpy50"})[0].text
            if match.find("span", {"class": "css-g3e0pm-score"}) :
                score = match.find("span", {"class": "css-g3e0pm-score"}).text
            else : score= "Not played yet"
            teamb = match.find_all("span", {"class": "e1o4kpy50"})[1].text
            if match.find("span",{"class","css-asuic7-time"}):
                time = match.find("span",{"class","css-asuic7-time"}).text
            else : time ="Already played"
            if match.find("span",{"class","css-1dfww3s-live"}):
                live = "live now"
                timelive= match.find("span",{"class","css-1dfww3s-live"}).text
            else :
                live = "Not live"
                timelive= "Not live"
            match_details.append({"Champion title" : champion_title,"Team A":teama,"Score":score,"Team B":teamb,"Start time":time,"Live":live,"Live time":timelive})
    match_details=pd.DataFrame(match_details)
    return match_details

def create_csv(match_details):
    match_details.to_csv("match_details.csv",index=False)
    print("CSV file created...")

def main():
    url=user_info()
    soup= find_page_content(url)
    match_details=scraper(soup)
    create_csv(match_details)

if __name__ == "__main__":
     main()