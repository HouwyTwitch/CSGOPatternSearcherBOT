import os
from tkinter import filedialog
import time
import psutil
import platform
import GPUtil
from hashlib import blake2b
import requests
import re
from steampy.guard import generate_one_time_code
import steam.webauth
import sys
from steampy.client import SteamClient
from tqdm import tqdm
import urllib.parse
from threading import Thread
from random import randint
from steampy.market import GameOptions
from steampy.market import Currency

def exit_by_timer(_time):
    for _ in tqdm(range(_time), desc="Exiting..."):
        time.sleep(1)
    sys.exit(0)

def coolprint(word, end='\n'):
    for i in range(len(word)+1):
        if i < len(word):
            print(word[:i], end="\r")
        else:
            print(word[:i], end=end)
        time.sleep(0.005)

def get_pc_uuid_hash_key(s, l, p, a, _s, k):
    _hash = blake2b()
    data = []
    for item in platform.uname():
        data.append(str(item))
    data.append(str(psutil.cpu_count(logical=False)))
    data.append(str(psutil.cpu_count(logical=True)))
    data.append(str(psutil.virtual_memory().total))
    for partition in psutil.disk_partitions():
        data.append(str(partition.fstype))
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            data.append(str(partition_usage.total))
        except PermissionError:
            break
        break
    for gpu in GPUtil.getGPUs():
        data.append(str(gpu.uuid))
        break
    for i in range(len(data)):
        data[i] = data[i].encode("utf-8")
    for item in data:
        _hash.update(item)
    _hash.update(s.encode("utf-8"))
    _hash.update(l.encode("utf-8"))
    _hash.update(p.encode("utf-8"))
    _hash.update(a.encode("utf-8"))
    _hash.update(_s.encode("utf-8"))
    _hash.update(k.encode("utf-8"))
    return _hash.hexdigest().upper()

def get_skin_info(a, l, d):
    _url = 'https://api.csgofloat.com/?m=' + l + '&a=' + a + '&d=' + d
    try:
        http_content = requests.get(_url).content.decode("utf-8")
        if ('"status":400' in http_content) or ("www.cloudflare.com" in http_content) or ('"paintindex"' not in http_content):
            raise IOError
        good_asset_id.append(a)
        good_pattern.append(http_content.split('"paintseed":')[1].split(',')[0])
    except:
        time.sleep(randint(1, 4)/2)
        get_skin_info(a, l, d)


try:
    coolprint("Accout information...", end='\r')
    f = open("UserData.json", "r", encoding="utf-8")
    file_content = f.read()
    f.close()
    steam_id = file_content.split('"SteamID": "')[1].split('"')[0]
    login = file_content.split('"Login": "')[1].split('"')[0]
    password = file_content.split('"Password": "')[1].split('"')[0]
    api_key = file_content.split('"APIKEY": "')[1].split('"')[0]
    shared_secret = file_content.split('"Shared_Secret": "')[1].split('"')[0]
    identity_secret = file_content.split('"Identity_Secret": "')[1].split('"')[0]
    print("Accout information ✓")
except FileNotFoundError:
    print("Accout informationа ×")
    coolprint("Let's setup!")
    coolprint("maFile...", end='\r')
    root = filedialog.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename(title="Open maFile", filetypes=(("maFiles", "*.maFile"), ("All Files", "*.*")))
    f = open(file_name, "r", encoding="utf-8")
    file_content = f.read()
    f.close()
    login = file_content.split('"account_name":"')[1].split('"')[0]
    shared_secret = file_content.split('"shared_secret":"')[1].split('"')[0]
    identity_secret = file_content.split('"identity_secret":"')[1].split('"')[0]
    steam_id = file_content.split('"SteamID":')[1].split('}')[0]
    print("maFile ✓")
    coolprint("Now enter API key and password!")
    api_key = input("API key: ")
    password = input("Password: ")
    coolprint("Saving...", end='\r')
    f = open("UserData.json", "w", encoding="utf-8")
    f.write("{\n" + f'\t"SteamID": "{steam_id}",\n\t"Login": "{login}",\n\t"Password": "{password}",\n\t"APIKEY": "{api_key}",\n\t"Shared_Secret": "{shared_secret}",\n\t"Identity_Secret": "{identity_secret}"\n' + "}")
    f.close()
    f = open(f"{steam_id}.json", "w", encoding="utf-8")
    f.write('{\n' + f'    "steamid": "{steam_id}",\n    "shared_secret": "{shared_secret}",\n    "identity_secret": "{identity_secret}"\n' + '}')
    f.close()
    print("Saving ✓")

license_data = []

coolprint("PC UUID...", end='\r')

http_content = requests.get("https://github.com/HouwyTwitch/CSGOPatternSearcherBOT/blob/master/licence.key").content.decode("utf8")
regex = r"(?:class\=\"blob-code blob-code-inner js-file-line\"\>)([^<]+)(?:\<\/td\>)"
matches = re.finditer(regex, http_content, re.MULTILINE)
for matchNum, match in enumerate(matches, start=1):
    for groupNum in range(len(match.groups())):
        groupNum += 1
        license_data.append(str(match.group(groupNum)))
programm_key = get_pc_uuid_hash_key(steam_id, login, password, api_key, shared_secret, identity_secret)
if programm_key in license_data:
    f = open("Good Skins.log", "w", encoding="utf-8")
    f.close()
    count = 0
    license_data = []
    print("PC UUID ✓")
    coolprint("Steam Guard...", end='\r')
    one_time_authentication_code = generate_one_time_code(shared_secret)
    print("Steam Guard ✓")
    coolprint("Skin search service...", end='\r')
    user = steam.webauth.WebAuth(login, password)
    user.login(twofactor_code=one_time_authentication_code)
    print("Skin search service ✓")
    coolprint("Skin buying service...", end="\r")
    for _ in range(6):
        time.sleep(1)
        print("Skin buying service —", end="\r")
        time.sleep(1)
        print("Skin buying service \\", end="\r")
        time.sleep(1)
        print("Skin buying service |", end="\r")
        time.sleep(1)
        print("Skin buying service /", end="\r")
        time.sleep(1)
        print("Skin buying service —", end="\r")
    steam_client = SteamClient(api_key)
    while True:
        try:
            steam_client.login(login, password, f"{steam_id}.json")
            break
        except ConnectionAbortedError:
            print("Captcha!")
            exit(1)
        except:
            print("Skin buying service ×", end="\r")
            for _ in range(6):
                time.sleep(1)
                print("Skin buying service —", end="\r")
                time.sleep(1)
                print("Skin buying service\\", end="\r")
                time.sleep(1)
                print("Skin buying service |", end="\r")
                time.sleep(1)
                print("Skin buying service /", end="\r")
                time.sleep(1)
                print("Skin buying service —", end="\r")
    print("Skin buying service ✓")
    global quality
    quality = [" (Battle-Scarred)", " (Well-Worn)", " (Field-Tested)", " (Minimal Wear)", " (Factory New)"]
    coolprint("="*60)
    file_names = []
    for r, d, f in os.walk(os.getcwd() + "\\PatternDB\\"):
        for file in f:
            if ".ptn" in file:
                file_names.append(file.replace(".ptn", "").replace(";", " | "))
    for i in range(len(file_names)):
        print(f"{i+1}) {file_names[i]}")
    coolprint("="*60)
    choose = int(input("Choose the skin: "))
    main_skin_name = file_names[choose-1]
    global good_asset_id
    global good_pattern
    pattern = []
    description = []
    price = []
    f = open(os.getcwd() + "\\PatternDB\\" + main_skin_name.replace(" | ", ";") + ".ptn", "r", encoding="utf-8")
    for line in f:
        pattern.append(line.split(":")[0])
        description.append(line.split(":")[1])
        price.append(int(line.split(":")[2].replace("\n", "")))
    f.close()
    start_time = time.time()
    while True: 
        try:
            balance = int(steam_client.get_wallet_balance()*100)  
            good_asset_id = []
            good_pattern = []
            skin_price = []
            skin_price_fee = []
            total_pages = []
            url = []
            url_line = []
            asset_id = []
            listing_id = []
            d_num = []
            skin_price_without_fee = []
            skin_pattern = []
            default_price = []
            time_total_pages = []
            time_default_prices = []
            time_quality = [] 
            while True:
                try:
                    http_content = user.session.get(f"https://steamcommunity.com/market/search/render/?query={urllib.parse.quote(main_skin_name)}&start=0&count=10&search_descriptions=0&sort_column=name&sort_dir=asc&appid=730").content.decode("utf-8")
                    regex = r"(?:data-hash-name=\\\"" + main_skin_name.replace("|", "\\|") + r")([^\\]+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        time_quality.append(match.group(1))
                    regex = r"(?:data-price=\\\")(\d+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        time_default_prices.append(int(match.group(1)))
                    regex = r"(?:data-qty=\\\")(\d+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        time_total_pages.append(int(match.group(1))//100+1)
                    for i in range(len(quality)):
                        total_pages.append(time_total_pages[time_quality.index(quality[i])])
                        default_price.append(time_default_prices[time_quality.index(quality[i])])
                    break
                except:
                    time.sleep(10)
                    time_quality = []
                    time_default_prices = []
                    time_total_pages = []
                    total_pages = []
                    default_price = []
            for i in range(len(quality)):
                for k in range(total_pages[i]):
                    url = "https://steamcommunity.com/market/listings/730/" + urllib.parse.quote(main_skin_name + quality[i]) + f"/render/?query=&start={k*100}&count=100&country=RU&language=russian&currency=5"
                    http_content = user.session.get(url).content.decode("utf-8")
                    regex = r"(?:\"asset\":{\"currency\":\d+,\"appid\":\d+,\"contextid\":\"\d+\",\"id\":\")(\d+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        asset_id.append(match.group(1))
                    regex = r"(?:{\"listingid\":\")(\d+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        listing_id.append(match.group(1))
                    regex = r"(?:\%listingid\%A\%assetid\%D)(\d+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        d_num.append(match.group(1))
                    regex = r"(?:\\\"market_listing_price market_listing_price_with_fee\\\">[^\d]+)([^\s]+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        try:
                            skin_price.append(int(float(match.group(1).replace(",", "."))*100))
                        except ValueError:
                            skin_price.append(int(0))
                    regex = r"(?:\\\"market_listing_price market_listing_price_without_fee\\\">[^\d]+)([^\s]+)"
                    matches = re.finditer(regex, http_content, re.MULTILINE)
                    for _, match in enumerate(matches, start=1):  
                        try:
                            skin_price_without_fee.append(int(float(match.group(1).replace(",", "."))*100))
                        except ValueError:
                            skin_price_without_fee.append(int(0))
                    for n in range(len(skin_price)):
                        skin_price_fee.append(skin_price[n] - skin_price_without_fee[n])
                    threads = []
                    for n in range(len(asset_id)):
                        threads.append(Thread(target=get_skin_info, args=(asset_id[n], listing_id[n], d_num[n])))
                    for thr in threads:
                        thr.start()
                    for thr in threads:
                        thr.join()
                    for n in range(len(asset_id)):
                        skin_pattern.append(good_pattern[good_asset_id.index(asset_id[n])])
                    with open("Good Skins.log", "r", encoding="utf-8") as f:
                        file_content = f.read()
                    f = open("Good Skins.log", "a", encoding="utf-8")
                    for n in range(len(asset_id)):
                        if skin_pattern[n] in pattern:
                            if f"{main_skin_name}{quality[i]} | Pattern: {pattern[pattern.index(skin_pattern[n])]} ({description[pattern.index(skin_pattern[n])]}) |  Index on Market: {n} | Price: {skin_price[n]/100}\n" not in file_content:
                                f.write(f"{main_skin_name}{quality[i]} | Pattern: {pattern[pattern.index(skin_pattern[n])]} ({description[pattern.index(skin_pattern[n])]}) |  Index on Market: {n} | Price: {skin_price[n]/100}\n")
                            if (skin_price[n]<=default_price[i]*((100+price[pattern.index(skin_pattern[n])])/100)) and (skin_price[n] != 0) and (skin_price[n]<=balance):
                                try:
                                    response = steam_client.market.buy_item(f'{main_skin_name}{quality[i]}', listing_id[n], skin_price[n], skin_price_fee[n], GameOptions.CS, Currency.RUB)
                                except:
                                    pass
                                balance = int(steam_client.get_wallet_balance()*100)
                    f.close()
                    count += len(asset_id)
                    os.system('cls')
                    coolprint(f"{count} skins has been checked!")
                    current_time = round(time.time() - start_time)
                    coolprint(f"Bot working for {current_time//3600} hours {current_time%3600//60} minutes {current_time%60} seconds!")
                    coolprint(f"Speed - {round(count/current_time*60, 2)} skins per minute!")
                    skin_price_fee = []
                    skin_price_without_fee = []
                    threads = []
                    good_asset_id = []
                    good_pattern = []
                    skin_pattern = []
                    time_total_pages = []
                    time_default_prices = []
                    time_quality = []
                    asset_id = []
                    listing_id = []
                    d_num = []
                    time.sleep(1)
                    try:
                        if max(skin_price)>default_price[i]*((100+max(price))/100):
                            skin_price = []
                            break
                    except:
                        skin_price = []
                        break
                    skin_price = []
        except:
            while True:
                try:
                    coolprint("Session has been ended!")
                    user = 0
                    try:
                        steam_client.logout()
                    except:
                        pass
                    time.sleep(120)
                    one_time_authentication_code = generate_one_time_code(shared_secret)
                    user = steam.webauth.WebAuth(login, password)
                    user.login(twofactor_code=one_time_authentication_code)
                    time.sleep(30)
                    steam_client = SteamClient(api_key)
                    while True:
                        try:
                            steam_client.login(login, password, f"{steam_id}.json")
                            break
                        except:
                            time.sleep(30)
                    break
                except:
                    pass
else:
    license_data = []
    print("PC UUID ×")
    coolprint("PC UUID key has been saved in program folder!")
    coolprint("Send it to developer and you will get the access.")
    f = open("licence.key", "w", encoding="utf-8")
    f.write(programm_key)
    f.close()
    exit_by_timer(5)
