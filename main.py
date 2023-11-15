import requests
import json

#получаем id первой тысяци приложений
def get_appids():
    url = f"https://steamspy.com/api.php?request=all&page=0"
    response = requests.get(url)
    data = response.json()
    appids = []

    for appid in data.keys():
        appids.append(appid)

    return appids

#получаем json по каждой отдельной игре
def get_game_data(appid):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    response = requests.get(url)
    data = response.json()
    return data

#сохраняем обработанные данные в json
def save_to_json(data):
    with open("game_info.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#получаем дитальную информацию о играх
def get_detailed_game_data(appids):
    game_info_list = []

    #оброрбатывем данные чтобы сохранить только интересующие нас параметры
    for appid in appids:
        game_data = get_game_data(appid)
        
        if game_data.get("name"):
            game_info = {
                "Название игры": game_data["name"],
                "Разработчик": game_data["developer"],
                "Издатель": game_data["publisher"],
                "Цена в США": float(game_data["initialprice"])/100,
                "Языки": game_data["languages"],
                "Жанры": game_data["genre"],
                
            }
            game_info_list.append(game_info)

    return game_info_list

def main():
    appids = get_appids()
    game_info_list = get_detailed_game_data(appids)
    save_to_json(game_info_list)
    print("Данные сохранены в файл game_info.json")

if __name__ == "__main__":
    main()
