"""Auto-generated file, do not edit by hand. ML metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_ML = PhoneMetadata(id='ML', country_code=223, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[246-9]\\d{7}', possible_number_pattern='\\d{8}', possible_length=(8,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2(?:0(?:2\\d|7[0-8])|1(?:2[5-7]|[3-689]\\d))|44[1239]\\d)\\d{4}', example_number='20212345', possible_length=(8,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:2(?:079|17\\d)|[679]\\d{3}|8[239]\\d{2})\\d{4}', example_number='65012345', possible_length=(8,)),
    toll_free=PhoneNumberDesc(national_number_pattern='80\\d{6}', possible_number_pattern='\\d{8}', example_number='80012345', possible_length=(8,)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='80\\d{6}', possible_number_pattern='\\d{8}', example_number='80012345', possible_length=(8,)),
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['[246-9]']),
        NumberFormat(pattern='(\\d{4})', format='\\1', leading_digits_pattern=['67|74'])],
    intl_number_format=[NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['[246-9]']),
        NumberFormat(pattern='(\\d{4})', format='NA', leading_digits_pattern=['67|74'])])
