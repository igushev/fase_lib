"""Auto-generated file, do not edit by hand. MD metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_MD = PhoneMetadata(id='MD', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[19]\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 4, 5, 6)),
    toll_free=PhoneNumberDesc(national_number_pattern='116\\d{3}', possible_number_pattern='\\d{6}', example_number='116000', possible_length=(6,)),
    emergency=PhoneNumberDesc(national_number_pattern='112|90[1-3]', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:1(?:2|6(?:000|1(?:11|23))|8\\d{1,2}|99)|4\\d{3}|6[0-389]\\d|9(?:0[04-9]|[1-4]\\d))|90[1-3]', possible_number_pattern='\\d{3,6}', example_number='116000', possible_length=(3, 4, 5, 6)),
    short_data=True)
