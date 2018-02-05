"""Auto-generated file, do not edit by hand. ME metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_ME = PhoneMetadata(id='ME', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 4, 5, 6)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:12|2[234])', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:[035]\\d{2}|1(?:[013-57-9]\\d|2|6\\d{3})|2\\d{1,2}|4\\d{2,3}|9\\d{3})', possible_number_pattern='\\d{3,6}', example_number='1011', possible_length=(3, 4, 5, 6)),
    short_data=True)
