import requests
from bs4 import BeautifulSoup
import pandas as pd

event_links = []

# Scrape the list page
for page_num in range(1, 6):  # Assuming there are 41 pages
    url = f"https://visitseattle.org/events/page/{page_num}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Extract the url in href of a tags to the event detail page
    a_tags = soup.select("div.search-result-preview > div > h3 > a")
    event_links.extend([a['href'] for a in a_tags])

# Print the event links
print(event_links)


import csv

# Create a list to store the event details
event_details = []

# Loop through the event links
for event_link in event_links:
    # HTTP GET the detail page HTML
    res = requests.get(event_link)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Extract the event details
    name = soup.select_one("div.medium-6.columns.event-top > h1")
    date = soup.select_one("div.medium-6.columns.event-top > h4 > span:nth-child(1)")
    location = soup.select_one("div.medium-6.columns.event-top > h4 > span:nth-child(2)")
    event_type = soup.select_one("div.medium-6.columns.event-top > a:nth-child(3)")
    region = soup.select_one("div.medium-6.columns.event-top > a:nth-child(4)")
    
    # Check if the elements exist before accessing their text attribute
    if name is not None:
        name = name.text.strip()
    if date is not None:
        date = date.text.strip()
    if location is not None:
        location = location.text.strip()
    if event_type is not None:
        event_type = event_type.text.strip()
    if region is not None:
        region = region.text.strip()
    
    # Append the event details to the list
    event_details.append([name, date, location, event_type, region])

# Store the event details as CSV
with open("events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Date", "Location", "Type", "Region"])  # Write the header
    writer.writerows(event_details)  # Write the event details

import csv

# Create a list to store the event details
event_details = []

# Loop through the event links
for event_link in event_links:
    # HTTP GET the detail page HTML
    res = requests.get(event_link)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Extract the event details
    name = soup.select_one("div.medium-6.columns.event-top > h1")
    date = soup.select_one("div.medium-6.columns.event-top > h4 > span:nth-child(1)")
    location = soup.select_one("div.medium-6.columns.event-top > h4 > span:nth-child(2)")
    event_type = soup.select_one("div.medium-6.columns.event-top > a:nth-child(3)")
    region = soup.select_one("div.medium-6.columns.event-top > a:nth-child(4)")
    
    # Check if the elements exist before accessing their text attribute
    if name is not None:
        name = name.text.strip()
    if date is not None:
        date = date.text.strip()
    if location is not None:
        location = location.text.strip()
    if event_type is not None:
        event_type = event_type.text.strip()
    if region is not None:
        region = region.text.strip()
    
    # Append the event details to the list
    event_details.append([name, date, location, event_type, region])

# Store the event details as CSV
with open("events.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Date", "Location", "Type", "Region"])  # Write the header
    writer.writerows(event_details)  # Write the event details

def get_seattle_weather_forecast():
   
    seattle_lat = '47.6062'
    seattle_lon = '-122.3321'
    return get_latest_weather_forecast(seattle_lat, seattle_lon)


base_url = "https://visitseattle.org/events/page/"
num_pages = 46
events = []
for page in range (0,num_pages):
    url = base_url + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    selector = 'div.search-result-preview > div > h3 > a'
    a_eles=soup.select(selector)
    events = events + [x['href'] for x in a_eles]

events

eventdata = []

for event in events:
    res = requests.get(event)

    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        
        name = soup.select_one('div.medium-6.columns.event-top > h1')
        date_time = soup.select_one('div.medium-6.columns.event-top > h4 > span:nth-child(1)')
        location = soup.select_one('div.medium-6.columns.event-top > h4 > span:nth-child(2)')
        event_type = soup.select_one('div.medium-6.columns.event-top > a:nth-child(3)')
        region = soup.select_one('div.medium-6.columns.event-top > a:nth-child(4)')

        eventdata.append({
            "Name": name.get_text(strip=True) if name else "Not found",
            "Date & Time": date_time.get_text(strip=True) if date_time else "Not found",
            "Location": location.get_text(strip=True) if location else "Not found",
            "Type": event_type.get_text(strip=True) if event_type else "Not found",
            "Region": region.get_text(strip=True) if region else "Not found"
        })


df = pd.DataFrame(eventdata)
df.to_csv("events.csv")

# Read CSV file
csv_file = 'events.csv' 
df = pd.read_csv(csv_file)

# Adding new columns for latitude and longitude
df['Latitude'] = None
df['Longitude'] = None

for index, row in df.iterrows():
    lat, lon = get_lat_lon(row['Location'])
    if lat is not None and lon is not None:
        df.at[index, 'Latitude'] = lat
        df.at[index, 'Longitude'] = lon
    else:
        # Handle cases where coordinates are not found or invalid
        print(f"Coordinates not found or invalid for location: {row['Location']}")

# Save the updated DataFrame to a new CSV file
df.to_csv('events_with_LongLat.csv', index=False)

csv_file = 'events_with_LongLat.csv'
df = pd.read_csv(csv_file)

# Adding new columns for weather details
df['weather'] = None
df['temperature'] = None
df['wind_speed'] = None
df['wind_direction'] = None

for index, row in df.iterrows():
    lat = row.get('Latitude')
    lon = row.get('Longitude')
    date_str = row['Date & Time'].split(' ')[0]

    if pd.notna(lat) and pd.notna(lon):
        try:
            if date_str.lower() == 'now' or date_str.lower() == 'ongoing':
                weather_info = get_latest_weather_forecast(lat, lon)
            else:
                event_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                weather_info = get_weather_forecast(lat, lon, event_date)

            # Check if weather info is not returned
            if not all(weather_info):
                weather_info = get_seattle_weather_forecast()  # Default to Seattle weather
        except Exception:
            weather_info = get_seattle_weather_forecast()  # Default to Seattle weather
    else:
        weather_info = get_seattle_weather_forecast()  # Default to Seattle weather

    # Update the DataFrame with the weather information
    df.at[index, 'weather'], df.at[index, 'temperature'], df.at[index, 'wind_speed'], df.at[index, 'wind_direction'] = weather_info

# Export the updated dataframe to a CSV file
df.to_csv('Seattle_Events_Detail_Forcast.csv', index=False)
