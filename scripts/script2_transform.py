import json

# Load intermediary file with scraped data:
with open('data/01_alchemy_scraped.json', 'r') as file:
    dic = json.load(file)


# Dictionary with old names as keys, new names as values:
with open("data/mapping_dic.json") as mapping_data:
    mapping_dic = json.load(mapping_data)


# Replace effect names:
for key in dic:

    effects = dic[key].get("effects")
    
    if effects:
        #print(key, "\n", "   BEFORE", dic[key]['effects'])  # Print Debugging
        for polarity, effect_list in effects.items():
            
            new_effect_list = []
            
            for effect in effect_list:
                
                final_name = mapping_dic.get(effect, effect)
                
                if final_name not in new_effect_list:
                    new_effect_list.append(final_name)
            dic[key]['effects'][polarity] = new_effect_list

        #print("   AFTER", dic[key]['effects'])  # Sanity check



# Write transformed data into final .json file:
with open("data/02_alchemy_transformed.json", "w") as file:
    json.dump(dic, file, indent=4)