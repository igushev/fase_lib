"""Auto-generated file, do not edit by hand. NF metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_NF = PhoneMetadata(id='NF', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='9\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='9(?:11|55|77)', possible_number_pattern='\\d{3}', example_number='911', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='9(?:11|55|77)', possible_number_pattern='\\d{3}', example_number='911', possible_length=(3,)),
    short_data=True)
