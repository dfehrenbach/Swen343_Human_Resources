""" This aids with address validation by means of using REGEX
"""
import re


def validate_address(address):
    """
    :param address:
    :return: dictionary containing components of the address
            that is with the keys: street_address, city, state, and zip
    """
    regex = r'^([\d]+[\s[a-zA-Z/.\u00C0-\u017F]+),' \
            r'([\s[a-zA-Z\u00C0-\u017F]+),' \
            r'([\s[a-zA-Z\u00C0-\u017F]+)\s([\d]+)$'
    regex_object = re.compile(regex)
    if not regex_object.match(address):
        return {'error_message': 'Address is formatted incorrectly. Instead, it needs to be formatted like so: '
                                 '(replace everything in <> with the appropriate value)',
                'address': {'format': '<Street Number> <Street Name> <Street Modifier if necessary>, '
                                      '<City>, <State> <Zipcode>',
                            'example': '12345 Example St., Example City, State 12345',
                            'provided': address}}, 500

    return {'street_address': re.search(regex, address).group(1),
            'city': re.search(regex, address).group(2),
            'state': re.search(regex, address).group(3),
            'zip': re.search(regex, address).group(4)}
