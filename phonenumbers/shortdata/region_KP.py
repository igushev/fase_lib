"""Auto-generated file, do not edit by hand. KP metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_KP = PhoneMetadata(id='KP', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[18]\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:12|19)|819', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:12|19)|819', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_data=True)
