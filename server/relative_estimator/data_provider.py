import logging
import json

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
        for issue in jira_issues:
            if len(issue.fields.customfield_10800) == 1:
                my_issue = {
                    'key': issue.key,
                    'summary': self.__clear_field(issue.fields.summary),
                    'description': self.__clear_field(issue.renderedFields.description),
                    'sp':  float(issue.fields.customfield_10002),
                    'time': float(issue.fields.aggregatetimespent if issue.fields.aggregatetimespent else 0)/3600,
                    'labels': issue.fields.labels,
                    'resolutiondate': issue.fields.resolutiondate
                }
                my_issues.append(my_issue)
        return my_issues

    def __build_query(self):
        jql_arr = ["sprint in closedSprints()",
                   "Sprint not in openSprints()",
                   "\"Story Points\"  is not EMPTY",
                   "status IN (Resolved, Closed)",
                   "project IN (%s)" % (", ".join(self._projects)),
                   "resolved > %s" % self._oldest_results
                   ]
        if len(self._exclude_labels):
            jql_arr.append(" (labels not in (%s) OR labels is EMPTY)" % (", ".join(self._exclude_labels)))
        jql = " AND ".join(jql_arr) + " ORDER BY resolutiondate DESC"
        return jql


    def __clear_field(self, val):
        return val.replace('\r', '').replace('\n', '').replace('"', '')