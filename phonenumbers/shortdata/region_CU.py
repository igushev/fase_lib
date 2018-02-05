"""Auto-generated file, do not edit by hand. CU metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_CU = PhoneMetadata(id='CU', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 6)),
    emergency=PhoneNumberDesc(national_number_pattern='10[456]', possible_number_pattern='\\d{3}', example_number='106', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:0[456]|1(?:6111|8)|40)', possible_number_pattern='\\d{3,6}', example_number='140', possible_length=(3, 6)),
    short_data=True)
