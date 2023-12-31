from config import config  # pylint: disable=wrong-import-order
from helpers.general_helpers import key_join

r = config.redis


_NAMESPACE = "iv_scraper"

#######################
# BLACKLISTED OPTIONS #
#######################

_BLACKLIST_KEY = key_join(_NAMESPACE, "blacklist")


def blacklist_append(ticker, failure_count):
    return r.hincrby(_BLACKLIST_KEY, ticker, failure_count)


def blacklist_get_failure_count_for_ticker(ticker):
    return r.hget(_BLACKLIST_KEY, ticker)


def blacklist_all_failure_counts():
    return r.hgetall(_BLACKLIST_KEY)


def blacklisted_tickers():
    return list(blacklist_all_failure_counts().keys())


def blacklist_remove_ticker(ticker):
    return r.hdel(_BLACKLIST_KEY, ticker)


def blacklist_purge():
    return r.delete(_BLACKLIST_KEY)


###########################
# OPTION EXPIRATION DATES #
###########################

_EXPIRATION_DATE_KEY = key_join(_NAMESPACE, "expr")


def get_all_expr_dates():
    return r.hgetall(_EXPIRATION_DATE_KEY)


def get_expr_date(ticker):
    return r.hget(_EXPIRATION_DATE_KEY, ticker)


def set_expr_date(ticker, expr):
    return r.hset(_EXPIRATION_DATE_KEY, ticker, expr)


def purge_expr_dates():
    r.delete(_EXPIRATION_DATE_KEY)


#####################
# AUXILIARY HELPERS #
#####################


def purge_glob(glob):
    for k in r.keys(glob):
        r.delete(k)
