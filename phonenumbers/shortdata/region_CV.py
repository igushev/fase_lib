"""Auto-generated file, do not edit by hand. CV metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_CV = PhoneMetadata(id='CV', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    emergency=PhoneNumberDesc(national_number_pattern='13[012]', possible_number_pattern='\\d{3}', example_number='132', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='13[012]', possible_number_pattern='\\d{3}', example_number='132', possible_length=(3,)),
    short_data=True)
