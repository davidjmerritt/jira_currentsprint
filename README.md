# JIRA Current Sprint
[Bitbar](https://github.com/matryer/bitbar) plugin that loads current JIRA sprint details by project id
<br><br>
![Screen Capture](https://github.com/davidjmerritt/jira_currentsprint/blob/512db8f3c119958e8025bfb98e2419e1a24b95e7/jira_currentsprint_graphic.jpg?raw=true)

## Installation (OS X)

#### Install Python Package Index: [pip](https://pip.pypa.io/en/stable/installing/)
```
cd ~/Downloads
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

#### Install Python Package Dependencies
```
sudo pip install requests
```

#### Create Plugin folder
```
mkdir ~/Documents/BitBarPlugin
```

#### [Download](https://github.com/matryer/bitbar/releases/tag/v1.9.2) and Install BitBar App
- Double-click and open BitBar App
- Choose: "~/Documents/BitBarPlugin" folder when prompted 

#### Download [Latest Release](https://github.com/davidjmerritt/jira_currentsprint/releases/latest)
```
cd ~/Documents/BitBarPlugin
curl -O https://raw.githubusercontent.com/davidjmerritt/jira_currentsprint/master/jira_currentsprint.1h.py
```

#### Modify permissions of file to make it executable
```
chmod +x jira_currentsprint.1h.py
```

#### Modify the "# CONFIG" section of the jira_currentsprint.py file
```python
# CONFIG
JIRA_URL                    = 'http://myjiraurl.mysite.com'
JIRA_REST_URL               = JIRA_URL+'/rest/api/2'

JIRA_PROJECT_ID             = 'PJID' # ex. MEW
JIRA_ADMIN_USERNAME         = 'myusername'
JIRA_ADMIN_PASSWORD         = 'mypassword'
STORY_POINTS_FIELD_KEY      = 'customfield_9893' # ex. customfield_10280
SPRINT_FIELD_KEY            = 'customfield_12455' # ex. customfield_13760
```

#### Refresh BitBar 
Click on BitBar menu bar scroll to Preferences and selcted "Refresh all"

## Testing
```
cd ~/Documents/BitBarPlugin
python jira_currentsprint.1h.py test
```
This will return a pretty-printed json payload or an error message if the configuration is incorrect.
