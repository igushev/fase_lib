"""Auto-generated file, do not edit by hand. BL metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BL = PhoneMetadata(id='BL', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d', possible_number_pattern='\\d{2}', possible_length=(2,)),
    emergency=PhoneNumberDesc(national_number_pattern='18', possible_number_pattern='\\d{2}', example_number='18', possible_length=(2,)),
    short_code=PhoneNumberDesc(national_number_pattern='18', possible_number_pattern='\\d{2}', example_number='18', possible_length=(2,)),
    short_data=True)
