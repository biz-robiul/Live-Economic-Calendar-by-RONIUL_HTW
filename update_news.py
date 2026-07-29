import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def update_news():
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    root = ET.fromstring(response.content)
    
    output = "//=====================================================================\n"
    output += "// 🟢 AUTO-GENERATED FOREX FACTORY NEWS DATA\n"
    output += "//=====================================================================\n\n"
    output += "type NewsEvent\n"
    output += "    int time_ms\n"
    output += "    string currency\n"
    output += "    string impact\n"
    output += "    string title\n\n"
    output += "var newsData = array.new<NewsEvent>()\n"
    output += "if barstate.isfirst\n"
    
    for event in root.findall('event'):
        title = event.find('title').text
        country = event.find('country').text
        date_str = event.find('date').text
        time_str = event.find('time').text
        impact = event.find('impact').text
        
        if not time_str or not date_str or not title:
            continue
            
        if "All Day" in time_str or "Tentative" in time_str:
            continue
            
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%m-%d-%Y %I:%M%p")
            title_safe = title.replace("'", "\\'")
            ts_str = f"timestamp('America/New_York', {dt.year}, {dt.month}, {dt.day}, {dt.hour}, {dt.minute})"
            output += f"    newsData.push(NewsEvent.new({ts_str}, '{country}', '{impact}', '{title_safe}'))\n"
        except Exception as e:
            continue

    # ফাইল সেভ করা হচ্ছে
    with open("pine_news_data.txt", "w", encoding="utf-8") as f:
        f.write(output)
    print("Data successfully generated and saved to pine_news_data.txt")

if __name__ == "__main__":
    update_news()
