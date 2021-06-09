import sys

from relative_estimator.helpers import read_config, get_logger, arg_parse
from relative_estimator.connections import JiraConnectionGenerator, JiraREConnectionException
from relative_estimator.data_provider import DataProvider, JiraREDataProviderException
from relative_estimator.output_writer import JSONWriter
from relative_estimator.aggregator import aggregate_statistics

if __name__ == '__main__':
    execution_arguments = arg_parse(sys.argv[1:])
    logger = get_logger(execution_arguments)
    logger.info("Jira Relative Estimator just started for generation.")

    # get configuration
    logger.info("Reading config file...")
    config = read_config(execution_arguments.config_file)


    jira_connection_factory = JiraConnectionGenerator()
    try:
        jira_connection = jira_connection_factory.get_jira_connection(config)
    except JiraREConnectionException as connection_exception:
        logger.critical("Cannot create jira connection.")
        exit(1)

    data_provider = DataProvider(dict(config['FILTERS']), jira_connection)

    issues = data_provider.get_issues()

    file_writer = JSONWriter(dict(config['OUTPUT']))
    file_writer.write_to_file(issues)

    stats = aggregate_statistics(issues)

    my_issues = sorted(issues, key=lambda k: k['sp'])
    print("%100s:\t %4s\t %5s\t %4s" % ("summary", "SP", "time", "h/SP"))
    for issue in my_issues:
        print("%100s:\t %2.1f\t %3.2f\t %.1f" % (issue['summary'], issue['sp'], issue['time'], issue['time']/issue['sp']))

    print("\nStatistics:")
    print("Items count: %i, oldest: %s, newest: %s" %
          (stats.get('count', 0), stats.get('oldest', 'N/A'), stats.get('newest', 'N/A')))
