"""Auto-generated file, do not edit by hand. TW metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_TW = PhoneMetadata(id='TW', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='11[029]', possible_number_pattern='\\d{3}', example_number='110', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='11[029]', possible_number_pattern='\\d{3}', example_number='110', possible_length=(3,)),
    short_data=True)
