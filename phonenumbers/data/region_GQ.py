"""Auto-generated file, do not edit by hand. GQ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_GQ = PhoneMetadata(id='GQ', country_code=240, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[23589]\\d{8}', possible_number_pattern='\\d{9}', possible_length=(9,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='3(?:3(?:3\\d[7-9]|[0-24-9]\\d[46])|5\\d{2}[7-9])\\d{4}', example_number='333091234', possible_length=(9,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:222|55[15])\\d{6}', example_number='222123456', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='80\\d[1-9]\\d{5}', possible_number_pattern='\\d{9}', example_number='800123456', possible_length=(9,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90\\d[1-9]\\d{5}', possible_number_pattern='\\d{9}', example_number='900123456', possible_length=(9,)),
    number_format=[NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[235]']),
        NumberFormat(pattern='(\\d{3})(\\d{6})', format='\\1 \\2', leading_digits_pattern=['[89]'])])
