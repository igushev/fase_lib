"""Auto-generated file, do not edit by hand. SR metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_SR = PhoneMetadata(id='SR', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,3}', possible_number_pattern='\\d{3,4}', possible_length=(3, 4)),
    emergency=PhoneNumberDesc(national_number_pattern='115', possible_number_pattern='\\d{3}', example_number='115', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1\\d{2,3}', possible_number_pattern='\\d{3,4}', example_number='1234', possible_length=(3, 4)),
    short_data=True)
