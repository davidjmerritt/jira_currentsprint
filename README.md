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

#### Download and Install [BitBar](https://github.com/matryer/bitbar/releases/tag/v1.9.2)
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

#### Configure JIRA
Click on the JIRA icon in your memnu bar and select "Configure". Fill in the missing data points.  Save the file. Click to the JIRA icon in the menu bar and select "Refresh".  You should now see Current Sprint data loaded when you Click the JIRA icon.


## Testing
```
cd ~/Documents/BitBarPlugin
python jira_currentsprint.1h.py test
```
This will return a pretty-printed json payload or an error message if the configuration is incorrect.
