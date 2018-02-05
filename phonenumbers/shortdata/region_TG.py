"""Auto-generated file, do not edit by hand. TG metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_TG = PhoneMetadata(id='TG', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,3}', possible_number_pattern='\\d{3,4}', possible_length=(3, 4)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:1[78]|7[127])', possible_number_pattern='\\d{3,4}', example_number='117', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:011|1[078]|7[127])', possible_number_pattern='\\d{3,4}', example_number='117', possible_length=(3, 4)),
    short_data=True)
