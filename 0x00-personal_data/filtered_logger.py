from typing import List
import re


obj = {
    'find': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'restore': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters line.
    """
    find, restore = (obj["find"], obj["restore"])
    return re.sub(find(fields, separator), restore(redaction), message)