# kube-sso

The kube_sso.py script gets a user's credentials, connects to an IDP server and updates the token in kubectl config.
When running the script you need to provide the following arguments:
* idp server_url
* realm
* client_id

For example:
```kube_sso.py https://keycloak.elminda.com elminda k8s-on-prem```