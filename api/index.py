from flask import Flask, request, jsonify
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json
import os
import requests

titleider = "AD8B8"
SecretKey = "K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N"

app_id_2 = '9402735573162915'
app_secret_2 = 'K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N'

app_id_3 = 'OC|9402735573162915|579ca4879c2f42ab3555a2a56efc407a'
app_secret_3 = 'K1PTADUY6T63TAKKS6O1NEHYBMU9U53YXH38YX9G8EMMJHIZ9N'

headers = {'Content-Type': 'application/json', 'X-SecretKey': SecretKey}

app = Flask(__name__)

def send_to_discord(message):
    webhook_url = 'https://discord.com/api/webhooks/1402736443784429679/Tt4LGmSUlttI5nKW0tkiPkio8ofKCJrJ2raEnYPhO93H13YOLG9YJG0ZX50lXwvaDev8'
    headers = {'Content-Type': 'application/json'}
    data = {
        'content': message,
    }
    requests.post(webhook_url, headers=headers, json=data)
    
def validate_oculus(OrgScopedIdServer, OculusId):
    og_url_2 = f"https://graph.oculus.com/{OculusId}?access_token=OC|{app_id_2}|{app_secret_2}&fields=org_scoped_id"
    og_url_3 = f"https://graph.oculus.com/{OculusId}?access_token=OC|{app_id_3}|{app_secret_3}&fields=org_scoped_id"

    headers = {"Content-Type": "application/json"}

    def get_valid(url) -> bool:
        try:
            result = requests.get(url=url, headers=headers)
            result.raise_for_status()
            json_result = result.json()
            if 'org_scoped_id' in json_result and json_result['org_scoped_id'] == OrgScopedIdServer:
                return True
            else:
                print(f'Warning: org_scoped_id not in data for {OculusId}')
                return False
        except Exception as e:
            print(f'Error checking Oculus ID validity: {e}')
            return False

    og_2_valid = get_valid(og_url_2)
    og_3_valid = get_valid(og_url_3)

    if og_2_valid or og_3_valid:
        return True
    else:
        return False


def validate_nonce(user_id, nonce):
    og_url_2 = f"https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={user_id}&access_token=OC|{app_id_2}|{app_secret_2}"
    og_url_3 = f"https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={user_id}&access_token=OC|{app_id_3}|{app_secret_3}"
    og_2 = {
        "access_token": f"OC|{app_id_2}|{app_secret_2}",
        "user_id": f"{user_id}"
    }
    og_3 = {
        "access_token": f"OC|{app_id_3}|{app_secret_3}",
        "user_id": f"{user_id}"
    }
    headers = {}

    def get_valid(url, json) -> bool:
        try:
            result = requests.post(url=url, json=json, headers=headers)
            json_result = result.json()
            if 'is_valid' in json_result:
                return json_result['is_valid']
            else:
                print('Warning: is_valid not in data')
                return False
        except Exception as e:
            print(f'Error checking nonce validity: {e}')
            return False

    og_2_valid = get_valid(og_url_2, og_2)
    og_3_valid = get_valid(og_url_3, og_3)

    if og_2_valid or og_3_valid:
        return True
    else:
        return False


@app.route('/ogapi/PlayFabAuthentication', methods=['POST'])
def playfabauth():
    data = request.json
    required_fields = [
        'CustomId', 'AppId', 'Nonce', 'OculusId', 'Platform', 'AppVersion'
    ]
    platform = data.get('Platform')
    appid = data.get('AppId')
    custom_id = data.get('CustomId')
    oculus_id = data.get('OculusId')
    scopedid = custom_id.split("OCULUS")[1] if "OCULUS" in custom_id else None
    nonce = data.get('Nonce')
    
    print("Received data at /api/PlayFabAuthentication:", data)

    accepted_versions = ["2022.3.2f1", "2019.3.15f1"]

    user_agent = request.headers.get('User-Agent', '')
    unity_version = request.headers.get('X-Unity-Version', '')

    if not any(
            version in user_agent for version in accepted_versions
    ) or "UnityPlayer" not in user_agent or unity_version not in accepted_versions:
        return jsonify({
            "Error": "BadRequest",
            "Message": "BadRequest-InvalidRequest"
        }), 400

    missing_fields = [
        field for field in required_fields
        if field not in data or data.get(field) is None
    ]

    if missing_fields:
        return jsonify({
            "Error": "BadRequest",
            "Message": "BadRequest-InvalidRequest"
        }), 400

    #custom ids that can bypass auth
    if custom_id != "BYPASSERCUSTOMID" and custom_id != "BYPASSERCUSTOMID":
        if not validate_nonce(data['OculusId'], data['Nonce']):
            return jsonify({
                'Error': 'Bad Request',
                'Message': 'BadRequest-InvalidRequest'
            }), 400

        if not validate_oculus(scopedid, oculus_id):
            return jsonify({
                'Error': 'Bad Request',
                'Message': 'BadRequest-InvalidRequest'
            }), 400

    if platform != "Quest" or appid != titleider:
        return jsonify({
            'Error': "BadRequest",
            'Message': 'BadRequest-InvalidRequest'
        }), 400

    login_endpoint = f"https://{titleider}.playfabapi.com/Server/LoginWithServerCustomId"
    login_payload = {
        'TitleId': titleider,
        'ServerCustomId': custom_id,
        'CreateAccount': True
    }
    login_response = requests.post(login_endpoint,
                                   headers=headers,
                                   json=login_payload)

    if login_response.status_code == 200:
        response_data = login_response.json()["data"]
        playfab_id = response_data['PlayFabId']
        session_ticket = response_data['SessionTicket']

        entityId = response_data['EntityToken']['Entity']['Id']
        entityType = response_data['EntityToken']['Entity']['Type']
        entityToken = response_data['EntityToken']['EntityToken']

        return jsonify({
            'SessionTicket': session_ticket,
            'PlayFabId': playfab_id,
            'EntityId': entityId,
            'EntityType': entityType,
            'EntityToken': entityToken,
            'KidAccessToken': None,
            'KidRefreshToken': None,
            'KidUrlBasePath': None,
            'LocationCode': None
        }), 200

    elif login_response.status_code == 403:
        ban_info = login_response.json()
        if ban_info.get('errorCode') == 1002:
            ban_details = ban_info.get('errorDetails', {})
            ban_expiration_key = next(iter(ban_details.keys()), None)
            ban_expiration_list = ban_details.get(ban_expiration_key, [])
            ban_expiration = ban_expiration_list[0] if len(
                ban_expiration_list) > 0 else "No expiration date provided."
            print(ban_info)
            return jsonify({
                'BanMessage': ban_expiration_key,
                'BanExpirationTime': ban_expiration
            }), 403
        else:
            error_message = ban_info.get('errorMessage', 'No ban information')
            return jsonify({
                'Error': 'PlayFab Error',
                'Message': error_message
            }), 403

    else:
        playfab_error = login_response.json().get("error", {})
        error_message = playfab_error.get("errorMessage", "Login Failed")
        return jsonify({
            'Error': 'PlayFab Error',
            'Message': error_message,
            'PlayFabError': playfab_error
        }), login_response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
