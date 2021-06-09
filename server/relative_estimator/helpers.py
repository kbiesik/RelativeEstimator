import configparser
import argparse
import logging


def arg_parse(args_array):
    """
    Creates/sets up argparser instance
    """
    parser = argparse.ArgumentParser(description="""Automatic Jira Time Logger """,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', '--config', dest='config_file', default="config.ini",
                        help='parameters configuration file')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-d", "--debug", dest='debug', action="store_true",
                       help='Debug mode (includes verbose mode)', default=False)
    group.add_argument('-v', '--verbose', dest='verbose', action="store_true",
                       help='Verbose mode', default=False)

    return parser.parse_args(args_array)


def get_logger(args):
    format = '%(asctime)s\t%(levelname)s\t%(message)s'
    logging.basicConfig(format=format)
    logger = logging.getLogger()

    logger.setLevel(logging.WARNING)
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug("Args: %s", repr(args))
    return logger


def read_config(config_file_name):
    config = configparser.ConfigParser()
    config.read(config_file_name)
    return config
