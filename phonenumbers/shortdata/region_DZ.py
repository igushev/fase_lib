"""Auto-generated file, do not edit by hand. DZ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_DZ = PhoneMetadata(id='DZ', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[17]\\d{1,2}', possible_number_pattern='\\d{2,3}', possible_length=(2, 3)),
    emergency=PhoneNumberDesc(national_number_pattern='1[47]', possible_number_pattern='\\d{2}', example_number='17', possible_length=(2,)),
    short_code=PhoneNumberDesc(national_number_pattern='1[47]|730', possible_number_pattern='\\d{2,3}', example_number='17', possible_length=(2, 3)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='730', possible_number_pattern='\\d{3}', example_number='730', possible_length=(3,)),
    short_data=True)
