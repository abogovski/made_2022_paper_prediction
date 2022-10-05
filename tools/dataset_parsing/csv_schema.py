CSV_SCHEMA = {
    'paper': [
        ('paper_id',    int),
        ('_id',         str),
        ('title',       str),
        ('abstract',    str),
        ('lang',        str),
        ('pdf',         str),
        ('doi',         str),
        ('isbn',        str),
        ('issn',        str),
        ('issue',       str),
        ('volume',      str),
        ('year',        str),
        ('page_start',  str),
        ('page_end',    str),
        ('n_citation',  int),
    ],
    'author': [
        ('author_id', int),
        ('_id',       str),
        ('avatar',    str),
        ('bio',       str),
        ('email',     str),
        ('name',      str),
        ('orcid',     str),
        ('sid',       str)
    ],
    'org': [
        ('org_id', int),
        ('name',   str),
    ],
    'venue': [
        ('venue_id',    int),
        ('_id',         str),
        ('issn',        str),
        ('online_issn', str),
        ('publisher',   str),
        ('sid',         str),
        ('name',        str),
        ('raw',         str),
        ('t',           str),
        ('type',        str),
    ],
    'fos': [
        ('fos_id', int),
        ('value',  str),
    ],
    'keyword': [
        ('keyword_id', int),
        ('value',      str),
    ],
    'paper_author': [
        ('paper_id',  int),
        ('author_id', int),
    ],
    'author_org': [
        ('author_id', int),
        ('org_id',    int),
    ],
    'paper_venue': [
        ('paper_id', int),
        ('venue_id', int),
    ],
    'paper_fos': [
        ('paper_id', int),
        ('fos_id',   int),
    ],
    'paper_keyword': [
        ('paper_id',   int),
        ('keyword_id', int),
    ],
    'paper_reference': [
        ('referrer_paper_id',  int),
        ('reference_paper_id', int),
    ],
    'paper_url': [
        ('paper_id', int),
        ('url',      str),
    ],
}
