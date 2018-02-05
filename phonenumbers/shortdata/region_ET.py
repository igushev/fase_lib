"""Auto-generated file, do not edit by hand. ET metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_ET = PhoneMetadata(id='ET', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='9\\d{1,2}', possible_number_pattern='\\d{2,3}', possible_length=(2, 3)),
    emergency=PhoneNumberDesc(national_number_pattern='9(?:11?|[23]|9[17])', possible_number_pattern='\\d{2,3}', example_number='991', possible_length=(2, 3)),
    short_code=PhoneNumberDesc(national_number_pattern='9(?:11?|[23]|9[17])', possible_number_pattern='\\d{2,3}', example_number='991', possible_length=(2, 3)),
    short_data=True)
