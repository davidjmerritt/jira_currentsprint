#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# <bitbar.title>JIRA Current Sprint</bitbar.title>
# <bitbar.version>v0.0.1</bitbar.version>
# <bitbar.author>David J Merritt</bitbar.author>
# <bitbar.author.github>davidjmerritt</bitbar.author.github>
# <bitbar.desc>Loads list of tickets that have comments directed to you</bitbar.desc>
# <bitbar.dependencies>python, requests, pyyaml</bitbar.dependencies>
# <bitbar.abouturl></bitbar.abouturl>


import os, calendar, time, json, subprocess, base64, random
from datetime import datetime
from dateutil import rrule
import yaml, pytz

try:
    import requests
    from requests.auth import HTTPBasicAuth
except:
    pass


APP_FILE                    = os.path.abspath(__file__)
APP_PATH                    = os.path.dirname(APP_FILE)+'/'
DATA_PATH                   = APP_PATH+'jira_todo/'
LOG_PATH                    = DATA_PATH+'jira_todo.log'
CONFIG_FILE                 = DATA_PATH+'jira_todo.yaml'
DEFAULT_CONFIG              = { "JIRA_URL": "", "JIRA_REST_URL": "/rest/api/2", "JIRA_PROJECT_ID": "", "JIRA_ADMIN_USERNAME": "", "JIRA_ADMIN_PASSWORD": "", "STORY_POINTS_FIELD_KEY": "customfield_10280", "SPRINT_FIELD_KEY": "customfield_13760" }
REQUIRED_PIP_PACKAGES       = 'python-dateutil PyYAML pytz requests'


def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    return output[:-1]


def yaml_to_dict(yaml_input):
    if os.path.exists(yaml_input):
        with open(yaml_input) as yaml_string:
            yaml_data = yaml.safe_load(yaml_string)
    else:
        yaml_data = False
    return yaml_data


def dict_to_yaml(dict_data,return_type='pretty'):
    if return_type == 'pretty':
        return yaml.dump(dict_data, width=50, indent=4, default_flow_style=False)
    elif return_type == 'raw':
        return yaml.dump(dict_data)


def config(key=None):
    config_data = yaml_to_dict(CONFIG_FILE)
    if key == None:
        results = config_data
    else:
        try:
            results = config_data[key]
        except KeyError:
            results = False
    return results


def write_config(config_data=DEFAULT_CONFIG):
    if os.path.isdir(DATA_PATH):
        yaml_string = dict_to_yaml(DEFAULT_CONFIG)
        results = file_write(CONFIG_FILE,yaml_string,kind="overwrite")
    else:
        results = False
    return results


def file_write(file_path,contents,kind='append'):
    if kind == 'append':
        kind = 'a'
    elif kind == 'overwrite':
        kind = 'w'
    with open(file_path, kind) as f:
        read_data = f.write(contents+"\n")
    return os.path.isfile(file_path)


def which(bin_name):
    binary = run_command('which '+bin_name)
    if binary == '':
        binary = False
    return binary


def install():
    file_write(LOG_PATH,run_command('mkdir ~/Documents/BitBarApp'))
    file_write(LOG_PATH,run_command('curl https://github.com/matryer/bitbar/releases/download/v1.9.2/BitBar-v1.9.2.zip -o ~/Documents/BitBarApp/BitBar-v1.9.2.zip'))
    file_write(LOG_PATH,run_command('unzip ~/Documents/BitBarApp/BitBar-v1.9.2.zip'))
    file_write(LOG_PATH,run_command('curl https://bootstrap.pypa.io/get-pip.py -o ~/Documents/BitBarApp/get-pip.py'))
    file_write(LOG_PATH,run_command('python ~/Documents/BitBarApp/get-pip.py'))
    file_write(LOG_PATH,run_command('rm ~/Documents/BitBarApp/get-pip.py'))
    file_write(LOG_PATH,run_command('pip install '+REQUIRED_PIP_PACKAGES))


def setup():
    install()
    prompt_for_config()


def prompt_for_config():
    prompt_text_jira_url = 'What is yur JIRA host URL? For example:\nhttps://jira.COMPANY_NAME.com\nhttps://COMPANY_NAME.jira.com'
    jira_url_command = """osascript -e 'Tell application "System Events" to display dialog \"""" + prompt_text_jira_url + """\" default answer ""' buttons {"Cancel", "Submit"} default button 2 -e 'text returned of result'"""
    jira_url = run_command(jira_url_command)
    if 'User canceled' in jira_url:
        return False
    else:
        jira_url = jira_url.split('text returned:')[1]

    prompt_text_username = 'Enter Your JIRA Username:'
    username_command = """osascript -e 'Tell application "System Events" to display dialog \"""" + prompt_text_username + """\" default answer ""' buttons {"Cancel", "Submit"} default button 2 -e 'text returned of result'"""
    username = run_command(username_command)
    if 'Not authorized to send Apple events' in username:
        run_command('tccutil reset AppleEvents; tccutil reset SystemPolicyAllFiles')
        return False
    if 'User canceled' in username:
        return False
    else:
        username = username.split('text returned:')[1]

    prompt_text_password = 'Enter Your JIRA Password:'
    password_command = """osascript -e 'Tell application "System Events" to display dialog \"""" + prompt_text_password + """\" with hidden answer default answer ""' buttons {"Cancel", "Submit"} default button 2 -e 'text returned of result'"""
    password = run_command(password_command)
    if 'User canceled' in password:
        return False
    else:
        password = password.split('text returned:')[1]

    prompt_text_display_name = 'How is your name displayed in JIRA (e.g. Jack White, Immortan Joe, Cher, Ruth Bader Ginsberg, Hunter S. Thompson):'
    display_name_command = """osascript -e 'Tell application "System Events" to display dialog \"""" + prompt_text_display_name + """\" default answer ""' buttons {"Cancel", "Submit"} default button 2 -e 'text returned of result'"""
    display_name = run_command(display_name_command)
    if 'User canceled' in display_name:
        return False
    else:
        display_name = display_name.split('text returned:')[1]

    prompt_text_jira_project_id = 'What is your JIRA project ID? (e.g. GEGSOL, VMNW, MEW):'
    jira_project_id_command = """osascript -e 'Tell application "System Events" to display dialog \"""" + prompt_text_jira_project_id + """\" default answer ""' buttons {"Cancel", "Submit"} default button 2 -e 'text returned of result'"""
    jira_project_id = run_command(jira_project_id_command)
    if 'User canceled' in jira_project_id:
        return False
    else:
        jira_project_id = jira_project_id.split('text returned:')[1]

    config_data = DEFAULT_CONFIG
    config_data['JIRA_BASIC_AUTH'] = base64.b64encode(username+':'+password)
    config_data['JIRA_USER_ID'] = username
    config_data['JIRA_DISPLAY_NAME'] = display_name
    config_data['JIRA_URL'] = jira_url
    config_data['JIRA_PROJECT_ID'] = jira_project_id

    return write_config(config_data)


if os.path.isdir(DATA_PATH) == False:
    os.mkdir(DATA_PATH)

if os.path.isfile(CONFIG_FILE) == False:
    write_config()


JIRA_URL                    = config('JIRA_URL')
JIRA_REST_URL               = JIRA_URL+config('JIRA_REST_URL')
JIRA_PROJECT_ID             = config('JIRA_PROJECT_ID')
JIRA_USER_ID                = config('JIRA_USER_ID')
JIRA_DISPLAY_NAME           = config('JIRA_DISPLAY_NAME')
JIRA_BASIC_AUTH             = config('JIRA_BASIC_AUTH')
STORY_POINTS_FIELD_KEY      = config('STORY_POINTS_FIELD_KEY')
SPRINT_FIELD_KEY            = config('SPRINT_FIELD_KEY')


JIRA_ICON_BASE64 = 'iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RkQ0NTVGRUEyQjQ0MTFFN0JCRkNBOURGNEFERjU0REEiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RkQ0NTVGRUIyQjQ0MTFFN0JCRkNBOURGNEFERjU0REEiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpGRDQ1NUZFODJCNDQxMUU3QkJGQ0E5REY0QURGNTREQSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpGRDQ1NUZFOTJCNDQxMUU3QkJGQ0E5REY0QURGNTREQSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pu4ccU0AAAFkSURBVHjaYvj//z8DCOMBWkDcDsRSuBTAzcBimAgQ5yFp3glSD8RToHwdIM4GYk5iDJsD1bwayi+F8gOg/ItQfhm6YUxYXH0RSt+C0t1AzAjEG6D8S1D6BrpGRpirGBkZ5aCaHjIQD5ShLruL6l8Ghnyo83cBsSNUMTcQywAxF5RmhYqHAPFJqPpp2MLMDCoJw3xAzAHEv6H8R1CDTJDUfAbiaFwRsBNJ4Vao2CQoPwPKv4KkZiYQM+MyzBLNde1QcTcovQRJ7gcQKxBKGnVoBpZAxSeiiccTk85AYBFauJwB4n9IYq3E5gAY2IzmEhieTEp2Qgbr0QxaT2rehAE2KL0DybAX2DI8MYZ9gwY6CFxGMnAnqYZlImkGpXYeNO+6YTOMCUdYRSKxNYD4CxBPQBKLwl+wIYA41Iv/oclBHipui+SyB9jMYMFi/k8gng7E0tDiBlaKgNJaJxArQrMUBgAIMAAoPyG09TgH1QAAAABJRU5ErkJggg=='



def pad_string_with_spaces(string,max_chars):
    padded_string = string.upper()
    for i in xrange(0,max_chars):
        if len(padded_string) == max_chars:
            break
        else:
            padded_string += '\t'
    return padded_string+' - '+str(len(padded_string))


def progress_bar(per,top=100,empty=" ",fill=u"\u2588",scale=4):
        barlist = []
        for i in range(0,per/scale):
            barlist.append(fill)
        for i in range(per/scale,top/scale):
            barlist.append(empty)
        return barlist


def print_column_from_list(input_list,padding=4):
    col_width = max(len(word) for row in input_list for word in row) + padding
    for row in input_list:
        print "".join(word.ljust(col_width) for word in row)


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ''


def sort_dict_list(d,key_name=None):
    if key_name == None:
        result = d
    else:
        check = []
        for item in d:
            if key_name in item:
                check.append(True)
            else:
                check.append(False)
        if False in check:
            result = d
        else:
            result = sorted(d, key=lambda k: k[key_name])
    return result


def time_hr_short(epoch_time):
    return time.strftime('%a, %b %d', time.localtime( epoch_time ))


def time_translate_for_business_days(epoch_time):
    return (
        int(time.strftime('%Y', time.localtime( epoch_time ))),
        int(time.strftime('%m', time.localtime( epoch_time ))),
        int(time.strftime('%d', time.localtime( epoch_time )))
    )


def dict_to_json(dict_data, return_type='pretty'):
    if return_type == 'pretty':
        return json.dumps(dict_data, sort_keys=True, indent=4, separators=(',', ': '))
    elif return_type == 'raw':
        return json.dumps(dict_data)


def format_time(timezone):
    return datetime.now(pytz.timezone(timezone))


def hours_since_updated(updated_time):
    nowDatetimeFormat = '%Y-%m-%d %H:%M:%S' # 2020-01-23 01:02:13.085714-05:00
    stampDatetimeFormat = '%Y-%m-%dT%H:%M:%S' # 2020-01-21T11:49:52.000-0500
    duration = datetime.strptime(str(format_time('US/Eastern')).split('.')[0], nowDatetimeFormat) - datetime.strptime(updated_time.split('.')[0], stampDatetimeFormat)
    return convert_timedelta_to_hours(duration)


def convert_timedelta_to_hours(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours


def hr_time_diff(updated_time):
    nowDatetimeFormat = '%Y-%m-%d %H:%M:%S' # 2020-01-23 01:02:13.085714-05:00
    stampDatetimeFormat = '%Y-%m-%dT%H:%M:%S' # 2020-01-21T11:49:52.000-0500
    duration = datetime.strptime(str(format_time('US/Eastern')).split('.')[0], nowDatetimeFormat) - datetime.strptime(updated_time.split('.')[0], stampDatetimeFormat)

    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    weeks = days // 7
    months = days // 30

    if days > 60:
        return str(months)+' months'
    else:
        if days >= 14:
            return str(weeks)+' weeks'
        else:
            if days >= 3 :
                return str(days)+' days'
            else:
                if hours > 0:
                    return str(hours)+' hours'
                else:
                    return str(minutes)+' mins.'


def jira_stamp_short_to_epoch(string_time):
    dt = datetime.strptime(string_time, '%Y-%m-%d')
    return calendar.timegm(dt.utctimetuple())


def jira_search(jql_string):
    jira_server = JIRA_REST_URL+'/search?jql='+jql_string
    r = requests.get(jira_server, headers={'Authorization': 'Basic '+JIRA_BASIC_AUTH})
    return r.json()


def issue_comments(issue_id):
    jira_server = JIRA_REST_URL+'/issue/'+issue_id+'/comment'
    r = requests.get(jira_server, headers={'Authorization': 'Basic '+JIRA_BASIC_AUTH})
    return r.json()


def main(mode='prod'): #+and+sprint+in+openSprints() #+and+sprint+not+in+closedsprints()
    search_results = jira_search('project='+JIRA_PROJECT_ID+'&startAt=0&maxResults=999999&fields=summary,project,priority,assignee,issuetype,status,comment,'+STORY_POINTS_FIELD_KEY+','+SPRINT_FIELD_KEY)
    issues = search_results['issues']

    print '@mentions|color=black templateImage='+JIRA_ICON_BASE64
    # print 'Current Sprint ('+project_name+')'
    print '---'

    #sprint_title = issues[0]['fields'][SPRINT_FIELD_KEY][0].split(',')[3].split('=')[1]
    project_name = issues[0]['fields']['project']['name']
    print project_name+' ('+JIRA_PROJECT_ID+')' + ' - Issues you have been @mentioned in latest comment.' #+' - Sprint: '+sprint_title+'|color=black href='+JIRA_URL+'/secure/RapidBoard.jspa?rapidView=2164&projectKey='+JIRA_PROJECT_ID
    print '---'

    issues_with_comments_for_me = []
    for issue in issues:
        comments = issue['fields']['comment']['comments']
        status = issue['fields']['status']['name']
        try:
            if JIRA_USER_ID.upper() is issue['fields']['assignee']['key'].upper():
                assigned_to_me = True
            else:
                assigned_to_me = False
        except:
            assigned_to_me = False

        if len(comments) > 0:
            last_comment = comments[-1]
            if JIRA_USER_ID.upper() in last_comment['body'].upper() or JIRA_DISPLAY_NAME.upper() in last_comment['body'].upper() or assigned_to_me:
                issue_key = int(issue['key'].split('-')[1])
                if issue_key >= 0 and issue_key < 10:
                    issue_key = "    "+str(issue_key)
                elif issue_key >= 10 and issue_key < 100:
                    issue_key = "   "+str(issue_key)
                elif issue_key >= 100 and issue_key < 1000:
                    issue_key = "  "+str(issue_key)
                elif issue_key >= 1000 and issue_key < 10000:
                    issue_key = ""+str(issue_key)
                issue_summary = issue['fields']['summary'].replace('"','') [0:50]+'...'
                comment_author = last_comment['author']['name'].upper() #[0:5].upper()
                comment_updated = last_comment['updated']
                comment_body = last_comment['body'].replace('"','').split('\r')[0][0:30]+'...'
                priority = issue['fields']['priority']['name']
                priority_id = int(issue['fields']['priority']['id'])
                if priority in ['Blocker','Critical']:
                    color = 'red'
                elif priority in ['Major']:
                    color = 'black'
                else:
                    color = 'gray'


                # if status in ['Complete']:
                #     status_icon = ':white_check_mark:'
                # else:
                hours_since_comment = hours_since_updated(comment_updated)
                if hours_since_comment >= 30*24: # 1 month
                    # status_icon = ":ghost:"
                    status_icon = ":disappointed:"
                elif hours_since_comment >= 14*24 : # 2 weeks
                    status_icon = ":sleeping:"
                elif hours_since_comment >= 3*24: # 3 days
                    status_icon = ":sleepy:"
                elif hours_since_comment > 36: # 36 hours
                    # status_icon = ":hourglass:"
                    status_icon = ":grimacing:"
                else:
                    # status_icon = ":new:"
                    status_icon = ":smile:"

                status_icon +=  ' '+str(hr_time_diff(comment_updated))

                if status in ['Ready','Ready for Work','Acceptance Review']:
                    # status = ':checkered_flag:'
                    # status = ':microscope:'
                    status = ':mag:'

                elif status in ['Blocked']:
                    status = ':no_entry_sign:'
                elif status in ['In Progress']:
                    status = ':construction:'
                elif status in ['Complete']:
                    status = ':white_check_mark:'
                else: #,'To Do'
                    # status = ':arrow_right:'
                    status = ':new:'

                summary = '\t'.join([
                    # status,
                    status+status_icon,
                    # priority,
                    '  '+comment_author,
                    '  '+issue_key,
                    issue_summary
                ])
                issues_with_comments_for_me.append({
                    'sort_key': hours_since_comment,
                    'data': summary + '|size=13 color='+color+' href='+JIRA_URL+'/browse/'+issue['key'],
                    'comment': comment_body + '|size=11 color=black href='+JIRA_URL+'/browse/'+issue['key']
                })

    sorted_issues = sort_dict_list(issues_with_comments_for_me,key_name='sort_key')

    if len(sorted_issues) > 0:
        print '\t'.join([
            # '',
            'Status',
            # '\tLast Updated',
            # 'Priority'
            '                  Mention by',
            '   Id',
            '        Summary'
        ]) + '|size=12'
        print '-|size=1'
        for issue in sorted_issues:
            print issue['data']
            # print '-- '+ issue['comment']
    else:
        print 'Nothing to do...'


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        try:
            main()
            print '---'
            print 'Refresh|refresh=true'
            print '---'
            print 'Setup|bash='+which('python')+' param1='+APP_FILE+' param2=config terminal=false'
        except Exception as e:
            print '|color=red templateImage='+JIRA_ICON_BASE64
            print '---'
            print 'Refresh|refresh=true'
            print '---'
            print 'Setup|bash='+which('python')+' param1='+APP_FILE+' param2=config terminal=false'
    else:
        if sys.argv[1] == 'test':
            main('test')
        elif sys.argv[1] == 'config':
            setup()
