"""Auto-generated file, do not edit by hand. LY metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_LY = PhoneMetadata(id='LY', country_code=218, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[25679]\\d{8}', possible_number_pattern='\\d{7,9}', possible_length=(9,), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2[1345]|5[1347]|6[123479]|71)\\d{7}', example_number='212345678', possible_length=(9,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='9[1-6]\\d{7}', possible_number_pattern='\\d{9}', example_number='912345678', possible_length=(9,)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='([25679]\\d)(\\d{7})', format='\\1-\\2', national_prefix_formatting_rule='0\\1')])
