import json
import logging
import re
import statistics

from relative_estimator import JiraRelativrEstimatorException


class JiraREDataProviderException(JiraRelativrEstimatorException):
    pass


class DataProvider:

    def __init__(self, configuration, jira_connection):
        self.__config = configuration
        self.__jira = jira_connection

        self.__logger = logging.getLogger(__name__)
        self.__explode_config()

    def __explode_config(self):
        self.__logger.debug(repr(self.__config['project_codes']))
        self._projects = json.loads(self.__config['project_codes'])
        self._exclude_labels = json.loads(self.__config['exclusion_labels'])
        self._oldest_results = self.__config['oldest_results']
        self._max_results = int(self.__config['max_results'])

    def get_issues(self):
        jql = self.__build_query()

        self.__logger.debug("JQL:\n%s", jql)
        jira_issues = self.__jira.search_issues(jql,
                                                fields=["customfield_10800", 'summary', 'description',
                                                        'customfield_10002', 'aggregatetimespent', 'labels',
                                                        'resolutiondate'],
                                                maxResults=self._max_results,
                                                expand='renderedFields')

        my_issues = []
        sprints = {}
        for issue in jira_issues:
            if (issue.fields and issue.fields.customfield_10800 and len(issue.fields.customfield_10800) <= 2) \
                     or (issue.fields and not issue.fields.customfield_10800):
                if issue.fields.customfield_10800 and len(issue.fields.customfield_10800) == 1 and issue.fields.aggregatetimespent:
                    sprint_name = re.findall(r"name=([^,(]*)", str(issue.fields.customfield_10800[0]))[0]
                    if 'ICE' not in sprint_name:  # due to common reporting code between ICE and FIRE
                        continue
                    if sprint_name in sprints:
                        sprints[sprint_name]['time_spent'] = issue.fields.aggregatetimespent + sprints[sprint_name]['time_spent']
                        sprints[sprint_name]['sp'] = issue.fields.customfield_10002 + sprints[sprint_name]['sp']
                    else:
                        sprints[sprint_name] = {'time_spent': issue.fields.aggregatetimespent,
                                                'sp': issue.fields.customfield_10002}
                        # sprints[sprint_name] = {'sp': issue.fields.customfield_10002}
                if issue.fields.resolutiondate < '2022-03-31 00:00:00':
                    sp = int((issue.fields.aggregatetimespent if issue.fields.aggregatetimespent else 0) / 3600 * 0.24)
                else:
                    sp = float(issue.fields.customfield_10002)
                my_issue = {
                    'no_of_active_sprints': len(issue.fields.customfield_10800) if issue.fields.customfield_10800 else 0,
                    'key': issue.key,
                    'summary': self.__clear_field(issue.fields.summary),
                    'description': self.__clear_field(issue.renderedFields.description),
                    'sp': sp,
                    'time': float(issue.fields.aggregatetimespent if issue.fields.aggregatetimespent else 0) / 3600,
                    'labels': issue.fields.labels,
                    'resolutiondate': issue.fields.resolutiondate
                }
                my_issues.append(my_issue)
        for sprint_name, sprint in sprints.items():
            sprint['sph'] = round(sprint['sp']/sprint['time_spent']*3600, 3)
            print(f'{sprint_name}: {round(sprint["time_spent"]/3600)} h; {sprint}')
            sprints[sprint_name] = sprint
        median_velocity = round(statistics.median([sprint['sph'] for sprint in sprints.values()][:6]), 3)
        print(sprints)
        print(median_velocity)
        my_final_issues = []

        for issue in my_issues:
            if issue['no_of_active_sprints'] > 1:
                issue['sp'] = round(issue['time'] * median_velocity,1)
            my_final_issues.append(issue)

        return my_final_issues, sprints

    def __build_query(self):
        jql_arr = [
            # "sprint in closedSprints()",
            # "Sprint not in openSprints()",
            "\"Story Points\"  is not EMPTY",
            "status IN (Resolved, Closed)",
            "project IN (%s)" % (", ".join(self._projects)),
            "resolved >= %s" % self._oldest_results
        ]
        if len(self._exclude_labels):
            jql_arr.append(" (labels not in (%s) OR labels is EMPTY)" % (", ".join(self._exclude_labels)))
        jql = " AND ".join(jql_arr) + " ORDER BY resolutiondate DESC"
        return jql

    def __clear_field(self, val):
        return val.replace('\r', '').replace('\n', '').replace('"', '')
