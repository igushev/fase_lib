"""Auto-generated file, do not edit by hand. IL metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_IL = PhoneMetadata(id='IL', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,4}', possible_number_pattern='\\d{3,5}', possible_length=(3, 4, 5)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:0[012]|12)', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:0(?:[012]|400)|1(?:[013-9]\\d|2)|[2-9]\\d{2})', possible_number_pattern='\\d{3,5}', example_number='1455', possible_length=(3, 4, 5)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='10400', possible_number_pattern='\\d{5}', example_number='10400', possible_length=(5,)),
    short_data=True)
