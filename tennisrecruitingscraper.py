import bs4
import re
import requests
import pandas as pd 
google_search =  "https://google.com/search?q="
players = pd.read_csv(r"C:\\Users\\rvand\Downloads\\toy_dataset_scrape_trainer.csv")
def scraper(players):
    player_to_location_map = {}
    for i in players:
        j+=1
        final_url = google_search+f"{i}"+" tennisrecruiting"
        search_results = requests.get(final_url)
        soup = bs4.BeautifulSoup(search_results.text, 
                            "html.parser")
        links = soup.find_all('a')
        target_url = ""
        for link in links:
            list_matches = re.findall("https:\/\/www.tennisrecruiting\.net\/player\/[^&]*", str(link))
            if len(list_matches) > 0:
                target_url = list_matches[0]
        if target_url == "":
            print('No target URL for this player')
            player_to_location_map[i] = 'No tennis recruiting info on this player'
        else:
            player_id = re.findall("[0-9]{4,}", target_url)[0]
            player_url = "https://www.tennisrecruiting.net/player.asp?id="+player_id
            second_request = requests.get(player_url)
            second_bowl = bs4.BeautifulSoup(second_request.text, "html.parser")
            tennis_recruiting_location = second_bowl.find_all('div', {'class': 'lrg'})
            if len(tennis_recruiting_location) == 0:
                tennis_recruiting_location = second_bowl.find_all('meta', {'name': 'twitter:description'})
                if len(tennis_recruiting_location) == 0:
                    player_to_location_map[i] = 'No tennis recruiting info on this player'
                    continue
                tennis_string = str(tennis_recruiting_location[0])
                first_comp = tennis_string.split('.')[0]
                loc_list = re.findall("([A-Z]{1}[a-z]+\,\s[\w]+)|([A-Z]{1}[a-z]+\s[\w]+\,\s[\w]+)", first_comp)
                if len(loc_list) == 0:
                    player_to_location_map[i] = 'No tennis recruiting info on this player'
                    continue
                location_index = 0
                for k in range(len(loc_list[0])):
                    if loc_list[0][k] == '':
                        continue
                    else:
                        location_index = k
                player_to_location_map[i] = loc_list[0][location_index]      
            else:
                player_to_location_map[i] = tennis_recruiting_location[0].getText()
    return player_to_location_map

results = scraper(players['column_2'][:501])
results