"""Auto-generated file, do not edit by hand. LA metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_LA = PhoneMetadata(id='LA', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='19[015]', possible_number_pattern='\\d{3}', example_number='190', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='19[015]', possible_number_pattern='\\d{3}', example_number='190', possible_length=(3,)),
    short_data=True)
