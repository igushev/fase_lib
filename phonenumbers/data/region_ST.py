"""Auto-generated file, do not edit by hand. ST metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_ST = PhoneMetadata(id='ST', country_code=239, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[29]\\d{6}', possible_number_pattern='\\d{7}', possible_length=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='22\\d{5}', example_number='2221234', possible_length=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='9(?:0(?:0[5-9]|[1-9]\\d)|[89]\\d{2})\\d{3}', example_number='9812345', possible_length=(7,)),
    number_format=[NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2')])
