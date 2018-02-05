"""Auto-generated file, do not edit by hand. SK metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_SK = PhoneMetadata(id='SK', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 4, 5, 6)),
    toll_free=PhoneNumberDesc(national_number_pattern='116\\d{3}', possible_number_pattern='\\d{6}', example_number='116000', possible_length=(6,)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:12|5[058])', possible_number_pattern='\\d{3,6}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:1(?:2|6(?:000|111)|8[0-8])|[24]\\d{3}|5[0589]|8\\d{3})', possible_number_pattern='\\d{3,6}', example_number='112', possible_length=(3, 4, 5, 6)),
    short_data=True)
