"""Auto-generated file, do not edit by hand. TN metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_TN = PhoneMetadata(id='TN', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='19[078]', possible_number_pattern='\\d{3}', example_number='197', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='19[078]', possible_number_pattern='\\d{3}', example_number='197', possible_length=(3,)),
    short_data=True)
