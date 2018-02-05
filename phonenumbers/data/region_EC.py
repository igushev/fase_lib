"""Auto-generated file, do not edit by hand. EC metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_EC = PhoneMetadata(id='EC', country_code=593, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{9,10}|[2-8]\\d{7}|9\\d{8}', possible_number_pattern='\\d{7,11}', possible_length=(8, 9, 10, 11), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='[2-7][2-7]\\d{6}', possible_number_pattern='\\d{7,8}', example_number='22123456', possible_length=(8,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='9(?:(?:39|[45][89]|7[7-9]|[89]\\d)\\d|6(?:[017-9]\\d|2[0-4]))\\d{5}', possible_number_pattern='\\d{9}', example_number='991234567', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='1800\\d{6,7}', possible_number_pattern='\\d{10,11}', example_number='18001234567', possible_length=(10, 11)),
    voip=PhoneNumberDesc(national_number_pattern='[2-7]890\\d{4}', possible_number_pattern='\\d{8}', example_number='28901234', possible_length=(8,)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d)(\\d{3})(\\d{4})', format='\\1 \\2-\\3', leading_digits_pattern=['[247]|[356][2-8]'], national_prefix_formatting_rule='(0\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['9'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(1800)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['1'], national_prefix_formatting_rule='\\1')],
    intl_number_format=[NumberFormat(pattern='(\\d)(\\d{3})(\\d{4})', format='\\1-\\2-\\3', leading_digits_pattern=['[247]|[356][2-8]']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['9']),
        NumberFormat(pattern='(1800)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['1'])],
    mobile_number_portable_region=True)
