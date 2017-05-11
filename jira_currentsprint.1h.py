#!/usr/bin/python

# -*- coding: utf-8 -*-
# <bitbar.title>JIRA Current Sprint</bitbar.title>
# <bitbar.version>v0.0.2</bitbar.version>
# <bitbar.author>David J Merritt</bitbar.author>
# <bitbar.author.github>davidjmerritt</bitbar.author.github>
# <bitbar.desc>Loads current sprint details from JIRA project id.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

# <bitbar.abouturl></bitbar.abouturl>

# CONFIG
JIRA_URL                    = '' # jira.mydomain.com
JIRA_REST_URL               = JIRA_URL+'/rest/api/2'

JIRA_PROJECT_ID             = '' # ex. MEW
JIRA_ADMIN_USERNAME         = ''
JIRA_ADMIN_PASSWORD         = ''
STORY_POINTS_FIELD_KEY      = '' # ex. customfield_10280
SPRINT_FIELD_KEY            = '' # ex. customfield_13760

JIRA_ICON_BASE64 = 'iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKE1hY2ludG9zaCkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RkQ0NTVGRUEyQjQ0MTFFN0JCRkNBOURGNEFERjU0REEiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RkQ0NTVGRUIyQjQ0MTFFN0JCRkNBOURGNEFERjU0REEiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpGRDQ1NUZFODJCNDQxMUU3QkJGQ0E5REY0QURGNTREQSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpGRDQ1NUZFOTJCNDQxMUU3QkJGQ0E5REY0QURGNTREQSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/Pu4ccU0AAAFkSURBVHjaYvj//z8DCOMBWkDcDsRSuBTAzcBimAgQ5yFp3glSD8RToHwdIM4GYk5iDJsD1bwayi+F8gOg/ItQfhm6YUxYXH0RSt+C0t1AzAjEG6D8S1D6BrpGRpirGBkZ5aCaHjIQD5ShLruL6l8Ghnyo83cBsSNUMTcQywAxF5RmhYqHAPFJqPpp2MLMDCoJw3xAzAHEv6H8R1CDTJDUfAbiaFwRsBNJ4Vao2CQoPwPKv4KkZiYQM+MyzBLNde1QcTcovQRJ7gcQKxBKGnVoBpZAxSeiiccTk85AYBFauJwB4n9IYq3E5gAY2IzmEhieTEp2Qgbr0QxaT2rehAE2KL0DybAX2DI8MYZ9gwY6CFxGMnAnqYZlImkGpXYeNO+6YTOMCUdYRSKxNYD4CxBPQBKLwl+wIYA41Iv/oclBHipui+SyB9jMYMFi/k8gng7E0tDiBlaKgNJaJxArQrMUBgAIMAAoPyG09TgH1QAAAABJRU5ErkJggg=='



import os, datetime, calendar, time, json
from dateutil import rrule
import requests


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


def business_days(epoch_start,epoch_end):
    start = time_translate_for_business_days(epoch_start)
    end = time_translate_for_business_days(epoch_end)
    a = datetime.datetime(start[0],start[1],start[2]) # 2011,8,1
    b = datetime.datetime(end[0],end[1],end[2]) # 2011,8,29
    return len(list(rrule.rrule(rrule.DAILY,
        dtstart=a,
        until=b - datetime.timedelta(days=1),
        byweekday=(rrule.MO, rrule.TU, rrule.WE, rrule.TH, rrule.FR))))


def dict_to_json(dict_data, return_type='pretty'):
    if return_type == 'pretty':
        return json.dumps(dict_data, sort_keys=True, indent=4, separators=(',', ': '))
    elif return_type == 'raw':
        return json.dumps(dict_data)


def jira_stamp_short_to_epoch(string_time):
    dt = datetime.datetime.strptime(string_time, '%Y-%m-%d')
    return calendar.timegm(dt.utctimetuple())


def jira_search(jql_string):
    jira_server = JIRA_REST_URL+'/search?jql='+jql_string
    r = requests.get(jira_server, auth=(JIRA_ADMIN_USERNAME, JIRA_ADMIN_PASSWORD))
    return r.json()


def current_sprint_bitbar(mode='prod'):
    search_results = jira_search('project='+JIRA_PROJECT_ID+'+and+sprint+in+openSprints()+order+by+assignee&startAt=0&maxResults=200&fields=summary,project,assignee,issuetype,subtask,status,'+STORY_POINTS_FIELD_KEY+','+SPRINT_FIELD_KEY)
    issues = search_results['issues']

    if mode == 'test':
        print dict_to_json(search_results)
        exit()

    issue_count = 0
    point_count = 0
    complete_point_count = 0

    for issue in issues:
        sprint_id = find_between(issue['fields'][SPRINT_FIELD_KEY][0],'id=',',rapidViewId=')
        sprint_title = find_between(issue['fields'][SPRINT_FIELD_KEY][0],'name=',',startDate=')
        sprint_start = jira_stamp_short_to_epoch(find_between(find_between(issue['fields'][SPRINT_FIELD_KEY][0],'startDate=',',endDate='),'','T'))
        sprint_end = jira_stamp_short_to_epoch(find_between(find_between(issue['fields'][SPRINT_FIELD_KEY][0],'endDate=',',completeDate='),'','T'))
        if type(issue['fields'][STORY_POINTS_FIELD_KEY]) is float:
            point_count += issue['fields'][STORY_POINTS_FIELD_KEY]
            if issue['fields']['status']['name'] == 'Complete':
                complete_point_count += issue['fields'][STORY_POINTS_FIELD_KEY]
        if issue['fields']['issuetype']['subtask'] == False:
            issue_count += 1
    users = []
    for issue in issues:
        if issue['fields']['assignee'] == None:
            user, _id = "_Unassigned", "_Unassigned"
        else:
            user = issue['fields']['assignee']['displayName']
            _id = issue['fields']['assignee']['name']
        if {'_id':_id,'name':user,'issues':[],'issue_count':0,'point_count':0.0,'complete_points':0.0,'complete_issues':0} not in users:
            users.append({'_id':_id,'name':user,'issues':[],'issue_count':0,'point_count':0.0,'complete_points':0.0,'complete_issues':0})

    for user in users:
        user['statusTypes'] = []
        for issue in issues:
            summary = issue['fields']['summary']
            key = issue['fields']['project']['key']
            issue_number = issue['key'].replace(key+'-','')
            project_name = issue['fields']['project']['name']
            subtask = issue['fields']['issuetype']['subtask']
            points = issue['fields'][STORY_POINTS_FIELD_KEY]
            status = issue['fields']['status']['name']
            statusColor = 'black'
            if status == 'Blocked':
                statusColor = 'red'
            elif status == 'In Progress' or status == 'In Progress (DEV)' or status == 'In Progress (QA)':
                statusColor = 'blue'
            elif status == 'Ready for Work' or status == 'To Do':
                statusColor = 'green'
            elif status == 'Complete':
                statusColor = 'gray'
            if points is None:
                points = 0.0
            if issue['fields']['assignee'] == None:
                search_name = '_Unassigned'
            else:
                search_name = issue['fields']['assignee']['displayName']
            if search_name == user['name']:
                user['statusTypes'].append(status)
                if type(issue['fields'][STORY_POINTS_FIELD_KEY]) is float:
                    user['point_count'] += points
                    if status == 'Complete':
                        user['complete_points'] += points
                        user['complete_issues'] += 1
                if subtask: #and search_name != '_Unassigned':
                    user['issues'].append({
                        'text':'--'+' [ '+status+' ] '+issue_number+' - '+summary+' ('+str(points)+')'+'|size=12 href='+JIRA_URL+'/browse/'+key+'-'+issue_number+' color='+statusColor,
                        'status':status
                    })
                else:
                    user['issue_count'] += 1
                    user['issues'].append({
                        'text':'[ '+status+' ] '+issue_number+' - '+summary+' ('+str(points)+')'+'|size=12 href='+JIRA_URL+'/browse/'+key+'-'+issue_number+' color='+statusColor,
                        'status':status
                    })

    print '|color=black templateImage='+JIRA_ICON_BASE64
    # print 'Current Sprint ('+project_name+')'
    print '---'
    print project_name+' ('+JIRA_PROJECT_ID+') // '+sprint_title+'|color=black href='+JIRA_URL+'/secure/RapidBoard.jspa?projectKey='+JIRA_PROJECT_ID+'&view=planning.nodetail&epics=visible'

    # days_left_in_sprint = round((((sprint_end)-(time.time()))/3600)/24,2)
    days_total_in_sprint = business_days(sprint_start,sprint_end)
    days_left_in_sprint = business_days(time.time(),sprint_end)
    if days_left_in_sprint < 0:
        days_left_in_sprint = 0
    if days_left_in_sprint == 1:
        days_remaining_text = 'business day'
    else:
        days_remaining_text = 'business days'
    print time_hr_short(sprint_start)+' to '+time_hr_short(sprint_end)+' ('+str(days_left_in_sprint)+'/'+str(days_total_in_sprint)+' '+days_remaining_text+' remaining)'+'|size=10'
    print '---'
    sorted_users = sort_dict_list(users,key_name='_id')

    # print dict_to_json(sorted_users)
    # exit()

    # print 'Completed Issues|color=black'
    print 'Name\t\t\t\t\tIssues\t\t\tPoints|size=11'
    max_len_name = 18
    for user in sorted_users:
        # user['name'] = user['name'].split(' ')[0]
        if len(user['name']) < max_len_name:
            diff = max_len_name - len(user['name'])
            spaces = '                              '
            user['name'] = user['name']+spaces[:diff]
            tabs = '\t\t\t'
        else:
            user['name'] = user['name'][:max_len_name]+'..'
            tabs = '\t\t\t'
        if 'Blocked' in user['statusTypes']:
            print user['name']+tabs+str(user['complete_issues'])+'/'+str(user['issue_count'])+'\t\t\t\t'+str(user['complete_points'])+'/'+str(user['point_count'])+'|size=12 color=red'
        else:
            print user['name']+tabs+str(user['complete_issues'])+'/'+str(user['issue_count'])+'\t\t\t\t'+str(user['complete_points'])+'/'+str(user['point_count'])+'|size=12'
        issues = user['issues'] #sort_dict_list(user['issues'],key_name='status')
        for issue in issues:
            print '--'+issue['text']
    print '---'
    print 'Total\t\t\t\t\t'+str(issue_count)+'\t\t\t\t'+str(complete_point_count)+'/'+str(point_count)+'|size=14'
    print '[ '+''.join(progress_bar(int((complete_point_count/point_count)*100),top=100,empty=" ",fill='l',scale=1))+'l '+str(int((complete_point_count/point_count)*100))+'% Complete ]'+'|size=10 href='+JIRA_URL+'/secure/RapidBoard.jspa?projectKey='+JIRA_PROJECT_ID+'&view=reporting&chart=burndownChart&sprint='+sprint_id

if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        try:
            current_sprint_bitbar()
        except Exception as e:
            print 'Current Sprint (Unknown)'
            print '---'
            print 'Error loading sprint...'
    else:
        if sys.argv[1] == 'test':
            current_sprint_bitbar('test')
