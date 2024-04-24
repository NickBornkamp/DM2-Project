from scrapfly import ScrapflyClient, ScrapeConfig
import scrapfly
import re
import json
import sys
import csv
import random
import time


client = ScrapflyClient(key="scp-live-5354c81c729c491397f8fd8fb5c77644")
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

companies = [
            #('eBay', '7853'), 
            #('Amazon', '6036'), 
            # ('Meta', '40772'),
            #('Target', '194'),
            #('Google', '9079'),
            #('Netflix', '11891'),
            #('Tesla', '43129'),
            #('Microsoft', '1651'),
            ('Apple', '1138')
            ]

pageNum = 2
#url = f"https://www.glassdoor.com/Overview/Working-at-{company_name}-EI_IE{company_id}.htm"




with open('database.csv', 'w', encoding='utf-8', newline='') as file:
    file.flush()
    writer = csv.writer(file)
    field = ["Company", "Job Title", "Employement Level", 'Review Title', 'Pros', 'Cons', 'Rating']
    writer.writerow(field)

    employer = ["MANAGER", "PRESIDENT", "DIRECTOR", "SUPERVISOR", "EXECUTIVE", "OVERSEER"]
    employee = ["ENGINEER", "SCIENTIST", "STAFF", "ENTRY", "INTERN"]


    for company_name, company_id in companies:
        i = 0
        print("Scraping ", company_name)
        while i < 101:
            pageNum = str(i+2) #starts on Page 2
            url = f"https://www.glassdoor.com/Reviews/{company_name}-Reviews-E{company_id}_P{pageNum}.htm?filter.iso3Language=eng"
            #print(url)
                #https://www.glassdoor.com/Reviews/eBay-Reviews-E7853_P2.htm?filter.iso3Language=eng
            
            time.sleep(random.random() * 4 + 2)
            print("Scraping Page ", pageNum)
            result = None
            
            result = client.scrape(ScrapeConfig(url, country="US", asp=True, retry=True, cookies={"tldp": "1)"}))
            
        
            


            #["Company", "Job Title", "Employement Level", 'Review Title', 'Pros', 'Cons', 'Rating']
            prosText = result.selector.css("div[id*=Review] span[data-test*=review-text-pros] ::text").getall()
            consText = result.selector.css("div[id*=Review] span[data-test*=review-text-cons] ::text").getall()
            ratingsText =  result.selector.css("div[id*=Review] span[class*=review-details_overallRating] ::text").getall()
            titleText =  result.selector.css("div[id*=Review] a[class*=review-details_title] ::text").getall()
            employeeText =  result.selector.css("div[id*=Review] span[class*=review-details_employee] ::text").getall()
            if len(employeeText) == 0:
                print("Page ", pageNum, " failed for ", company_name)
                
                continue
            elif len(titleText) != 10:
                print("No title on ", pageNum, " for ", company_name)
                i += 1
                continue
            #print("Scrape Success")
            for j in range(10):
                jobTitle = employeeText[j]
                if jobTitle == "Anonymous Employee":
                    continue
                level = 1 if any(emp in jobTitle.upper() for emp in employer) else 0

                
                
                entry = [company_name, jobTitle, level, titleText[j], prosText[j], consText[j], int(ratingsText[j][0])]

                #print(entry)
                writer.writerow(entry)
                file.flush()
            i += 1
            

    #outputFile.write(text)



