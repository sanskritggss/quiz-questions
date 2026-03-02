import json

links = [
    {
        "section": "XII",
        "url": "https://sacred-texts.com/hin/m03/m03012.htm"
    },
    {
        "section": "XIII",
        "url": "https://sacred-texts.com/hin/m03/m03013.htm"
    },
    {
        "section": "XIV",
        "url": "https://sacred-texts.com/hin/m03/m03014.htm"
    },
    {
        "section": "XV",
        "url": "https://sacred-texts.com/hin/m03/m03015.htm"
    },
    {
        "section": "XVI",
        "url": "https://sacred-texts.com/hin/m03/m03016.htm"
    },
    {
        "section": "XVII",
        "url": "https://sacred-texts.com/hin/m03/m03017.htm"
    },
    {
        "section": "XVIII",
        "url": "https://sacred-texts.com/hin/m03/m03018.htm"
    },
    {
        "section": "XIX",
        "url": "https://sacred-texts.com/hin/m03/m03019.htm"
    },
    {
        "section": "XX",
        "url": "https://sacred-texts.com/hin/m03/m03020.htm"
    },
    {
        "section": "XXI",
        "url": "https://sacred-texts.com/hin/m03/m03021.htm"
    },
    {
        "section": "XXII",
        "url": "https://sacred-texts.com/hin/m03/m03022.htm"
    },
    {
        "section": "XXIII",
        "url": "https://sacred-texts.com/hin/m03/m03023.htm"
    },
    {
        "section": "XXIV",
        "url": "https://sacred-texts.com/hin/m03/m03024.htm"
    },
    {
        "section": "XXV",
        "url": "https://sacred-texts.com/hin/m03/m03025.htm"
    },
    {
        "section": "XXVI",
        "url": "https://sacred-texts.com/hin/m03/m03026.htm"
    },
    {
        "section": "XXVII",
        "url": "https://sacred-texts.com/hin/m03/m03027.htm"
    },
    {
        "section": "XXVIII",
        "url": "https://sacred-texts.com/hin/m03/m03028.htm"
    },
    {
        "section": "XXIX",
        "url": "https://sacred-texts.com/hin/m03/m03029.htm"
    },
    {
        "section": "XXX",
        "url": "https://sacred-texts.com/hin/m03/m03030.htm"
    },
    {
        "section": "XXXI",
        "url": "https://sacred-texts.com/hin/m03/m03031.htm"
    },
    {
        "section": "XXXII",
        "url": "https://sacred-texts.com/hin/m03/m03032.htm"
    },
    {
        "section": "XXXIII",
        "url": "https://sacred-texts.com/hin/m03/m03033.htm"
    },
    {
        "section": "XXXIV",
        "url": "https://sacred-texts.com/hin/m03/m03034.htm"
    },
    {
        "section": "XXXV",
        "url": "https://sacred-texts.com/hin/m03/m03035.htm"
    },
    {
        "section": "XXXVI",
        "url": "https://sacred-texts.com/hin/m03/m03036.htm"
    },
    {
        "section": "XXXVII",
        "url": "https://sacred-texts.com/hin/m03/m03037.htm"
    },
]

new_data = []

link_map = {link["section"]: link["url"] for link in links}

with open("quiz_pratibha_2026.json", "r") as f:
    data = json.load(f)

    data = list(data)

    print(len(data))

    for question in data:
        
        if question.get("url") is None:
            section = question["section"] 

            if section in link_map:
                question["url"] = link_map[section]

        new_data.append(question)
              

print(len(new_data))

with open("quiz_pratibha_2026_updated.json", "w") as file:
    json.dump(new_data, file, indent=4, ensure_ascii=False)
