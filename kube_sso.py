#!/usr/bin/env python
import fileinput
import getpass
import os
import sys
import requests

if len(sys.argv) != 4:
    raise SystemExit('usage: kube_sso.py idp_server_url realm client_id\nfor example: kube_sso.py https://keycloak.example.com my-realm k8s-on-prem')

idp = sys.argv[1]
realm = sys.argv[2]
client_id = sys.argv[3]
grant_type = "password"
scope = "openid"
welcome_prompt = "Let's login into the cluster"
kube_config = "~/.kube/config"


def get_token(username, password):
    '''
    Gets a token from the IDP server
    '''

    token_dict = {}
    r = requests.post(idp + "/auth/realms/{}/protocol/openid-connect/token".format(realm),
    data={'client_id': client_id, 
    'username': username, 
    'password': password, 
    'grant_type': grant_type, 
    'scope': scope})

    token_dict['client_secret'] = r.json()['session_state']
    token_dict['id_token'] = r.json()['id_token']
    token_dict['refresh_token'] = r.json()['refresh_token']

    return token_dict


def update_kube_config(token_dict):
    '''
    Updates ~/.kube/config with the token
    '''

    for line in fileinput.input(os.path.expanduser(kube_config), inplace=1, backup=".bak"):
        if "client-secret" in line:
            print("        client-secret: " + token_dict['client_secret'])
        elif "id-token" in line:
            print("        id-token: " + token_dict['id_token'])
        elif "refresh-token" in line:
            print("        refresh-token: " + token_dict['refresh_token'])
        else:
            print(line.strip("\n"))


if __name__ == "__main__":
    print(welcome_prompt)
    print("=" * len(welcome_prompt))
    username = raw_input("username > ")
    password = getpass.getpass("password > ")

    token = get_token(username, password)
    update_kube_config(token)
