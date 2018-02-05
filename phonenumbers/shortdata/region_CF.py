"""Auto-generated file, do not edit by hand. CF metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_CF = PhoneMetadata(id='CF', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,3}', possible_number_pattern='\\d{3,4}', possible_length=(3, 4)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:1[78]|220)', possible_number_pattern='\\d{3,4}', example_number='1220', possible_length=(3, 4)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:1[478]|220)', possible_number_pattern='\\d{3,4}', example_number='117', possible_length=(3, 4)),
    short_data=True)
