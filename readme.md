# how to download google configuration files

```
Go to the Google Cloud Console https://console.cloud.google.com/ and create a new project.
Enable the Google Drive API for your project by following these steps:
    Click on the "APIs & Services" -> "Library" menu on the left sidebar.
    Search for "Google Drive API" and click on it.
    Click the "Enable" button.
Create credentials for your project by following these steps:
    (note if you just created the project you need to:configure the OAuth consent screen with information about your application.
            by clicking the "Configure consent screen" button and add your email in the "Test users" TAP!)
    Click on the "APIs & Services" -> "Credentials" menu on the left sidebar.
    Click the "Create Credentials" and choose "OAuth client ID."
    application type "Desktop App"
    Click the "Continue" button.
Download The JSON file and save it as "credentials.json".


if you have an exist project 
go to "APIs & Services" -> "Credentials"
select a "OAuth 2.0 Client IDs"
find the download button
```


# installation

```bash
pip install virtualenv
virtualenv env
env\Scripts\activate  or source env/bin/activate
env\Scripts\pip.exe install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2

if on linux 
install 7zip
```

# How it works
```
main.py // start the upload changes to drive

sync.py // downloads changes
```
