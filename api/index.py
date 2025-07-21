import requests
import random
from flask import Flask, jsonify, request
# This can do any update up to prop haunt * i havent tested lastest *
# IF YOU USE THIS PUT FATE IN YOU MOTD!
# discord.gg/apkland

class GameInfo:

    def __init__(self):
        self.TitleId: str = "AD8B8"
        self.SecretKey: str = "K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N"
        self.ApiKey: str = "9402735573162915"

    def get_auth_headers(self):
        return {
            "content-type": "application/json",
            "X-SecretKey": self.SecretKey
        }


settings = GameInfo()
app = Flask(__name__)
playfab_cache = {}
mute_cache = {}

settings.TitleId = "AD8B8"
settings.SecretKey = "K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N"
settings.ApiKey = "9402735573162915"


def return_function_json(data, funcname, funcparam={}):
    user_id = data["FunctionParameter"]["CallerEntityProfile"]["Lineage"][
        "TitlePlayerAccountId"]

    response = requests.post(
        url=
        f"https://{settings.TitleId}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": user_id,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers=settings.get_auth_headers())

    if response.status_code == 200:
        return jsonify(response.json().get("data").get(
            "FunctionResult")), response.status_code
    else:
        return jsonify({}), response.status_code


def get_is_nonce_valid(nonce, oculus_id):
    response = requests.post(
        url=
        f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculus_id}&access_token={settings.ApiKey}',
        url1=
        f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculus_id}&access_token={settings.ApiKey1}',
        headers={"content-type": "application/json"})
    return response.json().get("is_valid")


@app.route("/", methods=["POST", "GET"])
def main():
    return "tickel my buthole"


@app.route("/api/CachePlayFabId", methods=["GET", "POST"])
def cacheplayfabid():

  left_pocket_dog_shit = request.get_json()

  plat = left_pocket_dog_shit.get("Platform")
  plat_userId = left_pocket_dog_shit.get("PlatformUserId")
  session_ticket = left_pocket_dog_shit.get("SessionTicket")
  playfab_id = left_pocket_dog_shit.get("PlayFabId")
  title_id = left_pocket_dog_shit.get("TitleId")

  return jsonify({
    "Message": "Yay Your Authed",
    "PlayFabId": playfab_id,
    "KidAccessToken": left_pocket_dog_shit.get("KidAccessToken"),
    "KidRefreshToken": left_pocket_dog_shit.get("KidRefreshToken"),
    "KidUrlBasePath": left_pocket_dog_shit.get("KidUrlBasePath"),
    "LocationCode": left_pocket_dog_shit.get("LocationCode")
  }), 200


@app.route("/api/PlayFabAuthentication", methods=["POST","GET"])
def skibidi():
    pluh = request.get_json()
    app_id = pluh.get('AppId')
    app_version = pluh.get('AppVersion')
    nonce = pluh.get('Nonce')
    oculus_id = pluh.get('OculusId')
    platform = pluh.get('Platform')
    age_catagory = pluh.get('AgeCategory')
    mother_token = pluh.get('MothershipToken')
    mother_shipid = pluh.get('MothershipId')

    login_req = requests.post(
        url = f'https://{settings.TitleId}.playfabapi.com/Server/LoginWithServerCustomId',
        json = {
            'ServerCustomId': "OCULUS" + oculus_id,
            'CreateAccount': True
        },
        headers = {
            'X-SecretKey': settings.SecretKey,
            'Content-Type': 'application/json'
        })

    if login_req.status_code == 200:
        rjson = login_req.json()

        session_ticket = rjson.get('data').get('SessionTicket')
        entity_token = rjson.get('data').get('EntityToken').get('EntityToken')
        playfab_id = rjson.get('data').get('PlayFabId')
        entity_id = rjson.get('data').get('EntityToken').get('Entity').get('Id')
        entity_type = rjson.get('data').get('EntityToken').get('Entity').get('Type')
        kid_access_token = rjson.get('data').get('KidAccessToken')
        kid_refresh_token = rjson.get('data').get('KidRefreshToken')
        kid_url_base_path = rjson.get('data').get('KidUrlBasePath')
        location_code = rjson.get('data').get('LocationCode')

        link_req = requests.post(
            url = f'https://{settings.TitleId}.playfabapi.com/Client/LinkCustomID',
            json = {
                'PlayFabId': playfab_id,
                'CustomId': "OCULUS" + oculus_id,
                'ForceLink': True
            },
            headers = {
                'X-Authorization': session_ticket,
                'Content-Type': 'application/json'
            })

        return jsonify({
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "PlayFabId": playfab_id,
            "EntityId": entity_id,
            "EntityType": entity_type,
            "KidAccessToken": kid_access_token,
            "KidRefreshToken": kid_refresh_token,
            "KidUrlBasePath": kid_url_base_path,
            "LocationCode": location_code
        }), 200
    else: 
        ban_info = login_req.json()
        if ban_info.get("errorCode") == 1002:
            ban_message = ban_info.get("errorMessage", "No ban message provided.")
            ban_details = ban_info.get("errorDetails", {})
            ban_expiration_key = next(iter(ban_details.keys()), None)
            ban_expiration_list = ban_details.get(ban_expiration_key, [])
            ban_expiration = (
                ban_expiration_list[0]
                if len(ban_expiration_list) > 0
                else "Indefinite"
            )
            return (
                jsonify(
                    {
                        "BanMessage": ban_expiration_key,
                        "BanExpirationTime": ban_expiration,
                    }
                ),
                403
            )

@app.route('/api/TitleData', methods=['POST'])
def titled_data():
    return jsonify({"MOTD": "<color=ORANGE>WELCOME TO HYPER TAG</color>\n\n<color=red>UPDATE:BACKTOSCHOOL 2023, HAVE AN UPDATE THAT YOU WANT? REQUEST IT IN THE DISCORD!</color>\n\n<color=blue>DISCORD: https://discord.gg/V6gbz7Vn4j</color>\n\n<color=orange>OWNER/FOUNDER:RAIDER/CO OWNER:MINTY</color>"})

    if req.status_code == 200:
        return jsonify(req.json().get("data").get("Data"))
    else:
        return jsonify({})

@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()

    access_token = rjson.get("userToken")
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")

    response = requests.post(
        url=
        f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"})

    if response.json().get("success"):
        return jsonify({"result": True})
    else:
        return jsonify({"error": True})
        
@app.route("/api/ConsumeCodeItem", methods=["POST"])
def consume_code_item():
    rjson = request.get_json()
    code = rjson.get("itemGUID")
    playfab_id = rjson.get("playFabID")
    session_ticket = rjson.get("playFabSessionTicket")

    if not all([code, playfab_id, session_ticket]):
        return jsonify({"error": "Missing parameters"}), 400

    raw_url = f"" 
    response = requests.get(raw_url)

    if response.status_code != 200:
        return jsonify({"error": "GitHub fetch failed"}), 500

    lines = response.text.splitlines()
    codes = {split[0].strip(): split[1].strip() for line in lines if (split := line.split(":")) and len(split) == 2}

    if code not in codes:
        return jsonify({"result": "CodeInvalid"}), 404

    if codes[code] == "AlreadyRedeemed":
        return jsonify({"result": codes[code]}), 200

    grant_response = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Admin/GrantItemsToUsers",
        json={
            "ItemGrants": [
                {
                    "PlayFabId": playfab_id,
                    "ItemId": item_id,
                    "CatalogVersion": "DLC"
                } for item_id in ["dis da cosmetics", "anotehr cposmetic", "anotehr"]
            ]
        },
        headers=settings.get_auth_headers()
    )


    if grant_response.status_code != 200:
        return jsonify({"result": "PlayFabError", "errorMessage": grant_response.json().get("errorMessage", "Grant failed")}), 500

    new_lines = [f"{split[0].strip()}:AlreadyRedeemed" if split[0].strip() == code else line.strip() 
             for line in lines if (split := line.split(":")) and len(split) >= 2]

    updated_content = "\n".join(new_lines).strip()

    return jsonify({"result": "Success", "itemID": code, "playFabItemName": codes[code]}), 200

@app.route("/api/CheckForBadName", methods=["POST", "GET"])
def checkforbadname():
    rjson = request.get_json() 
    function_result = rjson["FunctionArgument"]
    playfab_id = rjson["CallerEntityProfile"]["Lineage"]["MasterPlayerAccountId"]
    name = function_result["name"].upper()
    forRoom = function_result["forRoom"]

    if forRoom == True:
        return jsonify({"result": 0})

    link_response = requests.post(
        url=f"https://{settings.titleid}.playfabapi.com/Admin/UpdateUserTitleDisplayName",
        json={
            "DisplayName": name,
            "PlayFabId": playfab_id,
        },
        headers=settings.get_auth_headers(),
    ).json()
    return jsonify({"result": 0})

@app.route("/api/GetAcceptedAgreements", methods=["POST", "GET"])
def get_accepted_agreements():
    rjson = request.get_json()["FunctionResult"]
    return jsonify(rjson)

@app.route("/api/SubmitAcceptedAgreements", methods=["POST", "GET"])
def submit_accepted_agreements():
    rjson = request.get_json()["FunctionResult"]
    return jsonify(rjson)

@app.route("/api/ReturnMyOculusHashV2")
def return_my_oculus_hash_v2():
    return return_function_json(request.get_json(), "ReturnMyOculusHash")

@app.route("/api/ReturnCurrentVersionV2", methods=["POST", "GET"])
def return_current_version_v2():
    return return_function_json(request.get_json(), "ReturnCurrentVersion")

@app.route("/api/TryDistributeCurrencyV2", methods=["POST", "GET"])
def try_distribute_currency_v2():
    return return_function_json(request.get_json(), "TryDistributeCurrency")

@app.route("/api/BroadCastMyRoomV2", methods=["POST", "GET"])
def broadcast_my_room_v2():
    return return_function_json(request.get_json(), "BroadCastMyRoom",
                                request.get_json()["FunctionParameter"])

@app.route("/api/ShouldUserAutomutePlayer", methods=["POST", "GET"])
def should_user_automute_player():
    return jsonify(mute_cache)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1416)


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
            url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
            json={"PlayFabId": userId},
            headers={
                "content-type": "application/json",
                "X-SecretKey": settings.SecretKey
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
                f'Authenticated user {userId.lower()} title {settings.TitleId.lower()}',
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
             url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
             json={"PlayFabId": userId},
             headers={
                 "content-type": "application/json",
                 "X-SecretKey": settings.SecretKey
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
                 f'Authenticated user {userId.lower()} title {settings.TitleId.lower()}',
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
