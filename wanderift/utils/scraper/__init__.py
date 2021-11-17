from .skyscanner import Skyscanner


KINDS = {
    "skyscanner": Skyscanner
}


def get_scraper_class(kind):
    return KINDS[kind]