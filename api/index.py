import json
import random
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


TITLE_ID = "AD8B8"
SECRET_KEY = "K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N"
API_KEY = "OC|9402735573162915|579ca4879c2f42ab3555a2a56efc407a"

def get_auth_headers():
    return {"Content-Type": "application/json", "X-SecretKey": SECRET_KEY}

@app.route("/api/FetchPoll", methods=["POST", "GET"])
def Tables_Fetch_Poll():
    global poll_shit

    whatsabool = request.get_json()

    TitleId = whatsabool.get("settings.TitleId")
    PlayFabId = whatsabool.get("PlayFabId")
    PlayFabTicket = whatsabool.get("PlayFabTicket")

    vote_stuff = [
        {
            "PollId": 2,
            "Question": "ARE U GAY?",
            "VoteOptions": ["YES", "NO"],
            "VoteCount": [],
            "PredictionCount": [],
            "StartTime": f"{date.today().strftime('%Y-%m-%d')}",
            "EndTime": "2025-08-17T17:00:00",
            "isActive": True
        },
        {
            "PollId": 3,
            "Question": "DO YOU LIKE THIS UPDATE?",
            "VoteOptions": ["YESSS", "NO!"],
            "VoteCount": [184439, 0],
            "PredictionCount": [102522, 110490],
            "StartTime": "2025-03-07T18:00:00",
            "EndTime": "2025-03-14T17:00:00",
            "isActive": False
        }
    ]

    poll_shit = vote_stuff

    return jsonify(vote_stuff), 200

@app.route("/api/Vote", methods=["POST"])
def Tippys_VoteApi():
    VOTING_WEBHOOK = "https://discord.com/api/webhooks/1397293276637298861/RBDnThMU9fFyaZOrnmeYsphmeHEuyC5JePCP9IYWBfw1fbb7OfyNr-HfaDkaJRUf37N8"

    get = request.get_json()

    PollId = get.get("PollId")
    TitleId = get.get("TitleId")
    PlayFabId = get.get("PlayFabId")
    OculusId = get.get("OculusId")
    UserNonce = get.get("UserNonce")
    UserPlatform = get.get("UserPlatform")
    OptionIndex = get.get("OptionIndex")
    IsPrediction = get.get("IsPrediction")
    PlayFabTicket = get.get("PlayFabTicket")
    AppVersion = get.get("AppVersion")

    if get is None:
        return jsonify({"Message": "Something Happened"}), 400

    find = next((p for p in poll_shit if p["PollId"] == PollId), None)

    if not find:
        return jsonify({"Message": "Poll not found"}), 404

    embed = {
        "embeds": [
            {
                "title": "** A PLAYER HAS VOTED 📝 **",
                "description": (
                    "\n\n**↓ Vote Details ↓**\n\n"
                    ""
                    f"VOTE QUESTION: {find['Question']}\n"
                    f"VOTING FOR: {find['VoteOptions'][OptionIndex]}\n"
                    f"PREDICTION: {str(IsPrediction)}\n"
                    f"PollId: {str(PollId)}\n"
                    "\n\n"
                    "**↓ Player Details ↓**\n\n"
                    f"USER ID: {str(PlayFabId)}\n"
                    f"OCULUS ID: {str(OculusId)}\n"
                    f"PLATFORM: {str(UserPlatform)}\n"
                    f"PlayFabTicket: {str(PlayFabTicket)}\n"
                    f"NONCE: {str(UserNonce)}\n"
                    f"APPVERSION: {str(AppVersion)}\n"
                    f"Finally, Game Is {str(setttings.TitleId)}"
                ),
                "color": 63488
            }
        ]
    }

    requests.post(url=VOTING_WEBHOOK, json=embed)

    return jsonify({"Message": "Yay Votes Are Fixed, Very Cool"}), 200


@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    data = request.get_json()
    oculus_id = data.get("OculusId", "Null")
    nonce = data.get("Nonce", "Null")
    platform = data.get("Platform", "Null")

    login_req = requests.post(
        url=f"https://{TITLE_ID}.playfabapi.com/Server/LoginWithServerCustomId",
        json={
            "ServerCustomId": f"OCULUS{oculus_id}",
            "CreateAccount": True
        },
        headers=get_auth_headers()
    )

    if login_req.status_code == 200:
        rjson = login_req.json().get('data', {})
        session_ticket = rjson.get('SessionTicket')
        playfab_id = rjson.get('PlayFabId')
        entity = rjson.get('EntityToken', {})
        entity_token = entity.get('EntityToken')
        entity_id = entity.get('Entity', {}).get('Id')
        entity_type = entity.get('Entity', {}).get('Type')

        
        requests.post(
            url=f"https://{TITLE_ID}.playfabapi.com/Client/LinkCustomID",
            json={"CustomID": f"OCULUS{oculus_id}", "ForceLink": True},
            headers={
                "content-type": "application/json",
                "x-authorization": session_ticket
            }
        )

        return jsonify({
            "PlayFabId": playfab_id,
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "EntityId": entity_id,
            "EntityType": entity_type,
            "Nonce": nonce,
            "OculusId": oculus_id,
            "Platform": platform
        }), 200
    else:
        ban_info = login_req.json()
        if ban_info.get("errorCode") == 1002:
            details = ban_info.get("errorDetails", {})
            ban_reason = next(iter(details.keys()), "Banned")
            ban_time = details.get(ban_reason, ["Indefinite"])[0]
            return jsonify({
                "BanMessage": ban_reason,
                "BanExpirationTime": ban_time,
            }), 403
        return jsonify({"Message": "Login failed"}), 403
        

@app.route("/api/CheckForBadName", methods=["POST"])
def check_for_bad_name():
    rjson = request.get_json().get("FunctionResult")
    name = rjson.get("name").upper()

    if name in ["KKK", "PENIS", "NIGG", "NEG", "NIGA", "MONKEYSLAVE", "SLAVE", "FAG",
        "NAGGI", "TRANNY", "QUEER", "KYS", "DICK", "PUSSY", "VAGINA", "BIGBLACKCOCK",
        "DILDO", "HITLER", "KKX", "XKK", "NIGA", "NIGE", "NIG", "NI6", "PORN",
        "JEW", "JAXX", "TTTPIG", "SEX", "COCK", "CUM", "FUCK", "PENIS", "DICK",
        "ELLIOT", "JMAN", "K9", "NIGGA", "TTTPIG", "NICKER", "NICKA",
        "REEL", "NII", "@here", "!", " ", "JMAN", "PPPTIG", "CLEANINGBOT", "JANITOR", "K9",
        "H4PKY", "MOSA", "NIGGER", "NIGGA", "IHATENIGGERS", "@everyone", "TTT"]:
        return jsonify({"result": 2})
    else:
        return jsonify({"result": 0})

@app.route("/api/CachePlayFabId", methods=["POST"])
def cache_playfab_id():
    data = request.get_json()
    session_ticket = data.get("SessionTicket")
    if session_ticket:
        playfab_id = session_ticket.split("-")[0]
        return jsonify({"Message": "Authed", "PlayFabId": playfab_id}), 200
    return jsonify({"Message": "Try Again Later."}), 404



@app.route("/api/TitleData", methods=["POST", "GET"])
def title_data():
    return jsonify({
      "MOTD": "[ <color=red>W</color><color=red></color><color=orange>E</color><color=yellow>L</color><color=green>C</color><color=green>O</color><color=blue>M</color>E <color=red>T</color><color=orange>O </color><color=yellow>H</color><color=green>Y</color><color=green>P</color><color=blue>ER</color> T<color=red>A</color><color=orange>G</color><color=green></color><color=blue></color><color=red>S</color> ]\n<color=green>DISCORD.GG/HYPERTAG</color>\n<color=red>CURRENT UPDATE: METRO 2024!!!</color>\n<color=orange>IF YOU BOOST THE DISCORD SERVER YOU GET EVERY SINGLE COSMETICS, EXECPT STAFF COSMETICS!!</color>\<color=yellow>MAIN OWNER: RAIDER</color>\n<color=purple>CREDITS: BXT & NEVA, TABLE</color>",
      "BundleBoardSign": "discord.gg/hypertag",
      "BundleKioskButton": "discord.gg/hypertag",
      "BundleKioskSign": "discord.gg/hypertag",
      "BundleLargeSign": "discord.gg/hypertag",
      "SeasonalStoreBoardSign": "discord.gg/hypertag",
      "GorillanalyticsChance": 4320,
      "EmptyFlashbackText": "discord.gg/hypertag",
      "UseLegacyIAP": False,
      "TOTD": [
        {
          "PedestalID": "CosmeticStand1",
          "ItemName": "LBAFA.",
          "StartTimeUTC": "2025-02-28T22:00:00.000Z",
          "EndTimeUTC": "2025-03-07T22:00:00.000Z"
        },
        {
          "PedestalID": "CosmeticStand2",
          "ItemName": "LBAFB.",
          "StartTimeUTC": "2025-02-28T22:00:00.000Z",
          "EndTimeUTC": "2025-03-07T22:00:00.000Z"
        },
        {
          "PedestalID": "CosmeticStand3",
          "ItemName": "LBAFC.",
          "StartTimeUTC": "2025-02-28T22:00:00.000Z",
          "EndTimeUTC": "2025-03-07T22:00:00.000Z"
        }
      ],
      "AllowedClientVersions": {
        "clientVersions": [
          "beta1.1.1.95",
          "live1.1.1.95",
          "beta1.1.1.99",
          "live1.1.1.99",
          "beta1.1.1.100",
          "live1.1.1.100",
          "beta1.1.1.101",
          "live1.1.1.101",
          "beta1.1.1.51",
          "beta1.1.1.80"
        ]
      },
      "AutoMuteCheckedHours": {
        "hours": 169
      },
      "AutoName_Adverbs": [
        "Cool",
        "Fine",
        "Bald",
        "Bold",
        "Half",
        "Only",
        "Calm",
        "Fab",
        "Ice",
        "Mad",
        "Rad",
        "Big",
        "New",
        "Old",
        "Shy"
      ],
      "AutoName_Nouns": [
        "Gorilla",
        "Chicken",
        "Darling",
        "Sloth",
        "King",
        "Queen",
        "Royal",
        "Major",
        "Actor",
        "Agent",
        "Elder",
        "Honey",
        "Nurse",
        "Doctor",
        "Rebel",
        "Shape",
        "Ally",
        "Driver",
        "Deputy"
      ],
      "BacktraceSampleRate": 0.001,
      "BundleBoardSafeAccountSign": "EVERY DAY YOU VISIT GORILLA WORLD YOU WILL GET 100 SHINY ROCKS",
      "BundleBoardSign_SafeAccount": "EVERY DAY YOU VISIT GORILLA WORLD YOU WILL GET 100 SHINY ROCKS",
      "BundleData": {
        "Items": [
          {
            "isActive": False,
            "skuName": "2025_bear_hug_pack",
            "shinyRocks": 0,
            "playFabItemName": "LSABX.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 99,
            "displayName": "Bear Hug Pack"
          },
          {
            "isActive": False,
            "skuName": "2025_brass_funke_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABW.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 97,
            "displayName": "Brass Funke Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_holiday_blast_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABV.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 95,
            "displayName": "Holiday Blast Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_dragon_armor_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABU.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 93,
            "displayName": "Dragon Armor Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_headless_nightmare_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABT.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 91,
            "displayName": "Headless Nightmare Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_pumpkin_patch_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABS.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 90,
            "displayName": "Pumpkin Patch Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_monkes_wild_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABR.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 89,
            "displayName": "Monkes Wild Pack"
          },
          {
            "isActive": False,
            "skuName": "CLIMBSTOPPERSBUN",
            "shinyRocks": 10000,
            "playFabItemName": "CLIMBSTOPPERSBUN",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 0,
            "displayName": "CLIMB STOPPERS BUNDLE"
          },
          {
            "isActive": False,
            "skuName": "GLAMROCKERBUNDLE",
            "shinyRocks": 10000,
            "playFabItemName": "GLAMROCKERBUNDLE",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 0,
            "displayName": "GLAM ROCKER BUNDLE"
          },
          {
            "isActive": False,
            "skuName": "2024_cyber_monke_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABP.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 87,
            "displayName": "Cyber Monke Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_splash_dash_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABO.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 85,
            "displayName": "Splash and Dash Pack"
          },
          {
            "isActive": False,
            "skuName": "2024_shiny_rock_special",
            "shinyRocks": 2200,
            "playFabItemName": "LSABN.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 83,
            "displayName": "Shiny Rock Special"
          },
          {
            "isActive": False,
            "skuName": "2024_climb_stoppers_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABM.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 82
          },
          {
            "isActive": True,
            "skuName": "2024_glam_rocker_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABL.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 80
          },
          {
            "isActive": False,
            "skuName": "2024_monke_monk_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABK.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 78
          },
          {
            "isActive": False,
            "skuName": "2024_leaf_ninja_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABJ.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 76
          },
          {
            "isActive": False,
            "skuName": "2024_gt_monke_plush",
            "shinyRocks": 0,
            "playFabItemName": "LSABI.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 73
          },
          {
            "isActive": False,
            "skuName": "2024_beekeeper_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABH.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 73
          },
          {
            "isActive": False,
            "skuName": "2024_i_lava_you_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABG.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 71
          },
          {
            "isActive": False,
            "skuName": "2024_mad_scientist_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABF.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 69
          },
          {
            "isActive": False,
            "skuName": "2023_holiday_fir_pack",
            "shinyRocks": 10000,
            "playFabItemName": "LSABE.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 63
          },
          {
            "isActive": False,
            "skuName": "2023_spider_monke_bundle",
            "shinyRocks": 10000,
            "playFabItemName": "LSABD.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 59
          },
          {
            "isActive": False,
            "skuName": "2023_caves_bundle",
            "shinyRocks": 10000,
            "playFabItemName": "LSABC.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 54
          },
          {
            "isActive": False,
            "skuName": "2023_summer_splash_bundle",
            "shinyRocks": 10000,
            "playFabItemName": "LSABA.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 46
          },
          {
            "isActive": False,
            "skuName": "2023_march_pot_o_gold",
            "shinyRocks": 5000,
            "playFabItemName": "LSAAU.",
            "majorVersion": 1,
            "minorVersion": 1,
            "minorVersion2": 39
          },
          {
            "skuName": "2023_sweet_heart_bundle",
            "playFabItemName": "LSAAS.",
            "shinyRocks": 0,
            "isActive": False
          },
          {
            "skuName": "2022_launch_bundle",
            "playFabItemName": "LSAAP2.",
            "shinyRocks": 10000,
            "isActive": False
          },
          {
            "skuName": "early_access_supporter_pack",
            "playFabItemName": "Early Access Supporter Pack",
            "shinyRocks": 0,
            "isActive": False
          }
        ]
      },
      "BundleLargeSafeAccountSign": " ",
      "BundleLargeSign_SafeAccount": " ",
      "CreditsData": [
        {
          "Title": "DEV TEAM",
          "Entries": [
            "BXT",
            "NEVA",
            "JITNY"
          ]
        },
        {
          "Title": "SPECIAL THANKS",
          "Entries": [
            "Meta",
            "The \"Sticks\""
          ]
        },
        {
          "Title": "MUSIC BY",
          "Entries": [
            "Stunshine",
            "Jaguar Jen",
            "Audiopfeil",
            "Owlobe"
          ]
        }
      ],
      "DeployFeatureFlags": {
        "flags": [
          {
            "name": "2024-05-ReturnCurrentVersionV2",
            "value": 0,
            "valueType": "percent"
          },
          {
            "name": "2024-05-ReturnMyOculusHashV2",
            "value": 0,
            "valueType": "percent"
          },
          {
            "name": "2024-05-TryDistributeCurrencyV2",
            "value": 0,
            "valueType": "percent"
          },
          {
            "name": "2024-05-AddOrRemoveDLCOwnershipV2",
            "value": 0,
            "valueType": "percent"
          },
          {
            "name": "2024-05-BroadcastMyRoomV2",
            "value": 0,
            "valueType": "percent"
          },
          {
            "name": "2024-06-CosmeticsAuthenticationV2",
            "value": 100,
            "valueType": "percent"
          },
          {
            "name": "2024-08-KIDIntegrationV1",
            "value": 0,
            "valueType": "percent",
            "alwaysOnForUsers": [
              ""
            ]
          }
        ]
      },
      "EnableCustomAuthentication": True,
      "MOTDDeprecation": "WELCOME TO HYPERY TAG! WE HAVE MADE AN NEW PLAYFAB BECAUSE OF THE BUG! JOIN THE DISCORD: discord.gg/hypertag\n\nCREDITS TO BXT FOR SIGMA SKIBIDI METHODS",
      "MuteThresholds": {
        "thresholds": [
          {
            "name": "low",
            "threshold": 20
          },
          {
            "name": "high",
            "threshold": 50
          }
        ]
      },
      "VStumpDiscord": "discord.gg/luckytag",
      "VStumpFeaturedMaps": "4641648,4733024,4475071",
      "Bundle1TryOnDesc": "discord.gg/hypertag",
      "Bundle1TryOnPurchaseBtn": "discord.gg/hypertag",
      "TOBAlreadyOwnCompTxt": "YOU OWN THE BUNDLE ALREADY! THANK YOU!",
      "TOBAlreadyOwnPurchaseBtnTxt": "-",
      "TOBDefCompTxt": "PLEASE SELECT A PACK TO TRY ON AND BUY",
      "TOBDefPurchaseBtnDefTxt": "SELECT A PACK",
      "TOBSafeCompTxt": "PURCHASE ITEMS IN YOUR CART AT THE CHECKOUT COUNTER",
      "PromoHutSignText": "discord.gg/hypertag",
      "VStumpMOTD": "WELCOME TO HYPER TAG! WE HAVE MADE AN NEW PLAYFAB BECAUSE OF THE BUG! JOIN THE DISCORD: discord.gg/hypertag\n\nCREDITS TO BXT FOR SIGMA SKIBIDI METHODS",
      "GTBlackFridayPromo": "discord.gg/hypertag",
      "AllActiveQuests": {
        "DailyQuests": [
          {
            "selectCount": 1,
            "name": "Gameplay",
            "quests": [
              {
                "disable": False,
                "questID": 11,
                "weight": 1,
                "questName": "Play Infection",
                "questType": "gameModeRound",
                "questOccurenceFilter": "INFECTION",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "forest",
                  "canyon",
                  "beach",
                  "mountain",
                  "skyJungle",
                  "cave",
                  "Metropolis",
                  "bayou",
                  "rotating",
                  "none"
                ]
              },
              {
                "disable": True,
                "questID": 19,
                "weight": 1,
                "questName": "Play Paintbrawl",
                "questType": "gameModeRound",
                "questOccurenceFilter": "PAINTBRAWL",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "forest",
                  "canyon",
                  "beach",
                  "mountain",
                  "skyJungle",
                  "cave",
                  "Metropolis",
                  "bayou",
                  "rotating",
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 13,
                "weight": 1,
                "questName": "Play Freeze Tag",
                "questType": "gameModeRound",
                "questOccurenceFilter": "FREEZE TAG",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "forest",
                  "canyon",
                  "beach",
                  "mountain",
                  "skyJungle",
                  "cave",
                  "Metropolis",
                  "bayou",
                  "rotating",
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 1,
                "weight": 1,
                "questName": "Play Guardian",
                "questType": "gameModeRound",
                "questOccurenceFilter": "GUARDIAN",
                "requiredOccurenceCount": 5,
                "requiredZones": [
                  "forest",
                  "canyon",
                  "beach",
                  "mountain",
                  "cave",
                  "Metropolis",
                  "bayou",
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 4,
                "weight": 1,
                "questName": "Tag players",
                "questType": "misc",
                "questOccurenceFilter": "GameModeTag",
                "requiredOccurenceCount": 2,
                "requiredZones": [
                  "none"
                ]
              }
            ]
          },
          {
            "selectCount": 3,
            "name": "Exploration",
            "quests": [
              {
                "disable": False,
                "questID": 5,
                "weight": 1,
                "questName": "Ride the shark",
                "questType": "grabObject",
                "questOccurenceFilter": "ReefSharkRing",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 9,
                "weight": 1,
                "questName": "Play the piano",
                "questType": "tapObject",
                "questOccurenceFilter": "Piano_Collapsed_Key",
                "requiredOccurenceCount": 10,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 14,
                "weight": 1,
                "questName": "Throw snowballs",
                "questType": "launchedProjectile",
                "questOccurenceFilter": "SnowballProjectile",
                "requiredOccurenceCount": 10,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 15,
                "weight": 1,
                "questName": "Go for a swim",
                "questType": "swimDistance",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 200,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 21,
                "weight": 1,
                "questName": "Climb the tallest tree",
                "questType": "enterLocation",
                "questOccurenceFilter": "TallestTree",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "forest"
                ]
              },
              {
                "disable": False,
                "questID": 22,
                "weight": 1,
                "questName": "Complete the obstacle course",
                "questType": "enterLocation",
                "questOccurenceFilter": "ObstacleCourse",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 23,
                "weight": 1,
                "questName": "Swim under a waterfall",
                "questType": "enterLocation",
                "questOccurenceFilter": "UnderWaterfall",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 24,
                "weight": 1,
                "questName": "Sneak upstairs in the store",
                "questType": "enterLocation",
                "questOccurenceFilter": "SecretStore",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 25,
                "weight": 1,
                "questName": "Climb into the crow's nest",
                "questType": "enterLocation",
                "questOccurenceFilter": "CrowsNest",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 26,
                "weight": 1,
                "questName": "Go for a walk",
                "questType": "moveDistance",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 500,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 28,
                "weight": 1,
                "questName": "Get small",
                "questType": "misc",
                "questOccurenceFilter": "SizeSmall",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 29,
                "weight": 1,
                "questName": "Get big",
                "questType": "misc",
                "questOccurenceFilter": "SizeLarge",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              }
            ]
          },
          {
            "selectCount": 1,
            "name": "Social",
            "quests": [
              {
                "disable": False,
                "questID": 2,
                "weight": 1,
                "questName": "High Five Players",
                "questType": "triggerHandEffect",
                "questOccurenceFilter": "HIGH_FIVE",
                "requiredOccurenceCount": 10,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 3,
                "weight": 1,
                "questName": "Fist Bump Players",
                "questType": "triggerHandEffect",
                "questOccurenceFilter": "FIST_BUMP",
                "requiredOccurenceCount": 10,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 16,
                "weight": 1,
                "questName": "Find something to eat",
                "questType": "eatObject",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 30,
                "weight": 1,
                "questName": "Make a friendship bracelet",
                "questType": "misc",
                "questOccurenceFilter": "FriendshipGroupJoined",
                "requiredOccurenceCount": 1,
                "requiredZones": [
                  "none"
                ]
              }
            ]
          }
        ],
        "WeeklyQuests": [
          {
            "selectCount": 1,
            "name": "Gameplay",
            "quests": [
              {
                "disable": False,
                "questID": 17,
                "weight": 1,
                "questName": "Play Infection",
                "questType": "gameModeRound",
                "questOccurenceFilter": "INFECTION",
                "requiredOccurenceCount": 5,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": True,
                "questID": 20,
                "weight": 1,
                "questName": "Play Paintbrawl",
                "questType": "gameModeRound",
                "questOccurenceFilter": "PAINTBRAWL",
                "requiredOccurenceCount": 5,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 8,
                "weight": 1,
                "questName": "Play Freeze Tag",
                "questType": "gameModeRound",
                "questOccurenceFilter": "FREEZE TAG",
                "requiredOccurenceCount": 5,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 10,
                "weight": 1,
                "questName": "Play Guardian",
                "questType": "gameModeRound",
                "questOccurenceFilter": "GUARDIAN",
                "requiredOccurenceCount": 25,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 12,
                "weight": 1,
                "questName": "Tag players",
                "questType": "triggerHandEffect",
                "questOccurenceFilter": "THIRD_PERSON",
                "requiredOccurenceCount": 10,
                "requiredZones": [
                  "none"
                ]
              }
            ]
          },
          {
            "selectCount": 1,
            "name": "Exploration and Social",
            "quests": [
              {
                "disable": False,
                "questID": 6,
                "weight": 1,
                "questName": "Throw Snowballs",
                "questType": "launchedProjectile",
                "questOccurenceFilter": "SnowballProjectile",
                "requiredOccurenceCount": 50,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 7,
                "weight": 1,
                "questName": "Go for a long swim",
                "questType": "swimDistance",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 1000,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 18,
                "weight": 1,
                "questName": "Eat food",
                "questType": "eatObject",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 25,
                "requiredZones": [
                  "none"
                ]
              },
              {
                "disable": False,
                "questID": 27,
                "weight": 1,
                "questName": "Go for a long walk",
                "questType": "moveDistance",
                "questOccurenceFilter": "",
                "requiredOccurenceCount": 2500,
                "requiredZones": [
                  "none"
                ]
              }
            ]
          }
        ]
      },
      "ArenaForestSign": "discord.gg/hypertag",
      "ArenaRulesSign": "discord.gg/hypertag",
      "LBDMakeshipPromo": "discord.gg/hypertag"
    }), 200


@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    data = request.get_json()
    access_token = data.get("userToken")
    user_id = data.get("userID")
    nonce = data.get("nonce")
    sku = data.get("sku")

    response = requests.post(
        url=f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={API_KEY}",
        headers={"content-type": "application/json"}
    )

    if response.json().get("success"):
        return jsonify({"result": True})
    return jsonify({"error": True})


@app.route("/api/photon", methods=["POST"])
def photonauth():
    print(f"Received {request.method} request at /api/photon")
    getjson = request.get_json()
    Ticket = getjson.get("Ticket")
    Nonce = getjson.get("Nonce")
    Platform = getjson.get("Platform")
    UserId = getjson.get("UserId")
    nickName = getjson.get("username")
    if request.method.upper() == "GET":
        rjson = request.get_json()
        print(f"{request.method} : {rjson}")

        userId = Ticket.split('-')[0] if Ticket else None
        print(f"Extracted userId: {UserId}")

        if userId is None or len(userId) != 16:
            print("Invalid userId")
            return jsonify({
                'resultCode': 2,
                'message': 'Invalid token',
                'userId': None,
                'nickname': None
            })

        if Platform != 'Quest':
            return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}),403

        if Nonce is None:
            return jsonify({'Error': 'Bad request', 'Message': 'Not Authenticated!'}),304

        req = requests.post(
            url=f"https://{TITLE_ID}.playfabapi.com/Server/GetUserAccountInfo",
            json={"PlayFabId": userId},
            headers={
                "content-type": "application/json",
                "X-SecretKey": SECRET_KEY
            })

        print(f"Request to PlayFab returned status code: {req.status_code}")

        if req.status_code == 200:
            nickName = req.json().get("UserInfo",
                                      {}).get("UserAccountInfo",
                                              {}).get("Username")
            if not nickName:
                nickName = None

            print(
                f"Authenticated user {userId.lower()} with nickname: {nickName}"
            )

            return jsonify({
                'resultCode': 1,
                'message':
                f'Authenticated user {userId.lower()} title {TITLE_ID.lower()}',
                'userId': f'{userId.upper()}',
                'nickname': nickName
            })
        else:
            print("Failed to get user account info from PlayFab")
            return jsonify({
                'resultCode': 0,
                'message': "Something went wrong",
                'userId': None,
                'nickname': None
            })

    elif request.method.upper() == "POST":
        rjson = request.get_json()
        print(f"{request.method} : {rjson}")

        ticket = rjson.get("Ticket")
        userId = ticket.split('-')[0] if ticket else None
        print(f"Extracted userId: {userId}")

        if userId is None or len(userId) != 16:
            print("Invalid userId")
            return jsonify({
                'resultCode': 2,
                'message': 'Invalid token',
                'userId': None,
                'nickname': None
            })

        req = requests.post(
             url=f"https://{TITLE_ID}.playfabapi.com/Server/GetUserAccountInfo",
             json={"PlayFabId": userId},
             headers={
                 "content-type": "application/json",
                 "X-SecretKey": SECRET_KEY
             })

        print(f"Authenticated user {userId.lower()}")
        print(f"Request to PlayFab returned status code: {req.status_code}")

        if req.status_code == 200:
             nickName = req.json().get("UserInfo",
                                       {}).get("UserAccountInfo",
                                               {}).get("Username")
             if not nickName:
                 nickName = None
             return jsonify({
                 'resultCode': 1,
                 'message':
                 f'Authenticated user {userId.lower()} title {TITLE_ID.lower()}',
                 'userId': f'{userId.upper()}',
                 'nickname': nickName
             })
        else:
             print("Failed to get user account info from PlayFab")
             successJson = {
                 'resultCode': 0,
                 'message': "Something went wrong",
                 'userId': None,
                 'nickname': None
             }
             authPostData = {}
             for key, value in authPostData.items():
                 successJson[key] = value
             print(f"Returning successJson: {successJson}")
             return jsonify(successJson)
    else:
         print(f"Invalid method: {request.method.upper()}")
         return jsonify({
             "Message":
             "Use a POST or GET Method instead of " + request.method.upper()
         })


def ReturnFunctionJson(data, funcname, funcparam={}):
    print(f"Calling function: {funcname} with parameters: {funcparam}")
    rjson = data.get("FunctionParameter", {})
    userId = rjson.get("CallerEntityProfile",
                       {}).get("Lineage", {}).get("TitlePlayerAccountId")

    print(f"UserId: {userId}")

    req = requests.post(
        url=f"https://{TITLE_ID}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": userId,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers={
            "content-type": "application/json",
            "X-SecretKey": SECRET_KEY
        })

    if req.status_code == 200:
        result = req.json().get("data", {}).get("FunctionResult", {})
        print(f"Function result: {result}")
        return jsonify(result), req.status_code
    else:
        print(f"Function execution failed, status code: {req.status_code}")
        return jsonify({}), req.status_code


@app.route("/", methods=["GET"])
def home():
    return "mama said i special"


if __name__ == "__main__":
    app.run(debug=True)
