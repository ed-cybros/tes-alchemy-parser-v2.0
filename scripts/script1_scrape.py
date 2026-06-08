import json
import re
import time

import requests
from bs4 import BeautifulSoup as bs

# Url list for scraping:
urls = [
    "https://en.uesp.net/wiki/Lore:Alchemy_A",
    "https://en.uesp.net/wiki/Lore:Alchemy_B",
    "https://en.uesp.net/wiki/Lore:Alchemy_C",
    "https://en.uesp.net/wiki/Lore:Alchemy_D",
    "https://en.uesp.net/wiki/Lore:Alchemy_E",
    "https://en.uesp.net/wiki/Lore:Alchemy_F",
    "https://en.uesp.net/wiki/Lore:Alchemy_G",
    "https://en.uesp.net/wiki/Lore:Alchemy_H",
    "https://en.uesp.net/wiki/Lore:Alchemy_I",
    "https://en.uesp.net/wiki/Lore:Alchemy_J",
    "https://en.uesp.net/wiki/Lore:Alchemy_K",
    "https://en.uesp.net/wiki/Lore:Alchemy_L",
    "https://en.uesp.net/wiki/Lore:Alchemy_M",
    "https://en.uesp.net/wiki/Lore:Alchemy_N",
    "https://en.uesp.net/wiki/Lore:Alchemy_O",
    "https://en.uesp.net/wiki/Lore:Alchemy_P",
    "https://en.uesp.net/wiki/Lore:Alchemy_R",
    "https://en.uesp.net/wiki/Lore:Alchemy_S",
    "https://en.uesp.net/wiki/Lore:Alchemy_T",
    "https://en.uesp.net/wiki/Lore:Alchemy_U",
    "https://en.uesp.net/wiki/Lore:Alchemy_V",
    "https://en.uesp.net/wiki/Lore:Alchemy_W",
    "https://en.uesp.net/wiki/Lore:Alchemy_Y",
    "https://en.uesp.net/wiki/Lore:Alchemy_Z",
]


# Scrape each url and write into intermediary .json file:
dic = {}

for url in urls:

    r = requests.get(url)
    r.raise_for_status()
    
    soup = bs(r.content, "html.parser")
    
    class_names = re.compile(r"mw-headline|Effect(Pos|Neg|Mix|Other)")

    
    # Filter for specific data:
    tags = soup.find_all(
        lambda tag: (  
            any(class_names.search(cls) for cls in tag.get("class", [])) or  # Reagents and effects
            tag.name == "p"  # Descriptions
        )
    )

    # Retrieve text nodes from tags:
    for tag in tags:
        
        text = tag.get_text(separator="\n").strip()  # Separate text nodes
        for item in text.split("\n"):  # Split text nodes
            item = item.strip()  # Retrieve single node (reagent / effect name)
     
        if tag.get('class'):
            

            # Filter for reagents names:
            if "mw-headline" in tag['class']:
                
                current_reagent = item
                dic[current_reagent] = {}


            # Filter for effects names and polarity: 
            elif "EffectPos" in tag['class']:
                
                effects = dic[current_reagent].get("effects")
                if not effects:
                    dic[current_reagent]["effects"] = {}
                
                if "positive" not in dic[current_reagent]["effects"]:
                    dic[current_reagent]["effects"]["positive"] = []
                    
                if text not in dic[current_reagent]["effects"]["positive"]:
                    dic[current_reagent]["effects"]["positive"].append(item)
        
            elif "EffectNeg" in tag['class']:
                
                effects = dic[current_reagent].get("effects")
                if not effects:
                    dic[current_reagent]["effects"] = {}
                
                if "negative" not in dic[current_reagent]["effects"]:
                    dic[current_reagent]["effects"]["negative"] = []
                    
                if text not in dic[current_reagent]["effects"]["negative"]:
                    dic[current_reagent]["effects"]["negative"].append(item)
        
            elif "EffectMix" in tag['class']:
                
                effects = dic[current_reagent].get("effects")
                if not effects:
                    dic[current_reagent]["effects"] = {}
                
                if "mixed" not in dic[current_reagent]["effects"]:
                    dic[current_reagent]["effects"]["mixed"] = []
                    
                if text not in dic[current_reagent]["effects"]["mixed"]:
                    dic[current_reagent]["effects"]["mixed"].append(item)
        
            elif "EffectOther" in tag['class']:
                
                effects = dic[current_reagent].get("effects")
                if not effects:
                    dic[current_reagent]["effects"] = {}
                
                if "mixed" not in dic[current_reagent]["effects"]:
                    dic[current_reagent]["effects"]["other"] = []
                    
                if text not in dic[current_reagent]["effects"]["other"]:
                    dic[current_reagent]["effects"]["other"].append(item)
                    
    
        # Filter for reagent descriptions:
        else:
            bold = tag.find("b")
            #print("TAG:", tag)

            if bold:
                #print("BOLD:", bold)
                text = tag.get_text().strip()
                text = re.sub(r"[:\[\]\d]", "", text)  # Clean string data
                #print(text)
                dic[current_reagent]["description"] = text


    time.sleep(1.2)


# Write scraped data into intermediary .json file:
with open("data/01_alchemy_scraped.json", "w") as file:
    json.dump(dic, file, indent=4)