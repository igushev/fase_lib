"""Auto-generated file, do not edit by hand. EG metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_EG = PhoneMetadata(id='EG', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[13]\\d{2,4}', possible_number_pattern='\\d{3,5}', possible_length=(3, 5)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:2[23]|80)', possible_number_pattern='\\d{3}', example_number='122', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:2[23]|80)|34400', possible_number_pattern='\\d{3,5}', example_number='122', possible_length=(3, 5)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='34400', possible_number_pattern='\\d{5}', example_number='34400', possible_length=(5,)),
    short_data=True)
