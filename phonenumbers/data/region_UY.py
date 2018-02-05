"""Auto-generated file, do not edit by hand. UY metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_UY = PhoneMetadata(id='UY', country_code=598, international_prefix='0(?:1[3-9]\\d|0)',
    general_desc=PhoneNumberDesc(national_number_pattern='[2489]\\d{6,7}', possible_number_pattern='\\d{7,8}', possible_length=(7, 8), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='2\\d{7}|4[2-7]\\d{6}', example_number='21231234', possible_length=(8,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='9[1-9]\\d{6}', possible_number_pattern='\\d{8}', example_number='94231234', possible_length=(8,)),
    toll_free=PhoneNumberDesc(national_number_pattern='80[05]\\d{4}', possible_number_pattern='\\d{7}', example_number='8001234', possible_length=(7,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90[0-8]\\d{4}', possible_number_pattern='\\d{7}', example_number='9001234', possible_length=(7,)),
    preferred_international_prefix='00',
    national_prefix='0',
    preferred_extn_prefix=' int. ',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{4})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['[24]']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['9[1-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['[89]0'], national_prefix_formatting_rule='0\\1')])
