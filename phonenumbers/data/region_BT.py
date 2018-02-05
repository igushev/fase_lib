"""Auto-generated file, do not edit by hand. BT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BT = PhoneMetadata(id='BT', country_code=975, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-8]\\d{6,7}', possible_number_pattern='\\d{6,8}', possible_length=(7, 8), possible_length_local_only=(6,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:2[3-6]|[34][5-7]|5[236]|6[2-46]|7[246]|8[2-4])\\d{5}', possible_number_pattern='\\d{6,7}', example_number='2345678', possible_length=(7,), possible_length_local_only=(6,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:1[67]|77)\\d{6}', possible_number_pattern='\\d{8}', example_number='17123456', possible_length=(8,)),
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['1|77']),
        NumberFormat(pattern='([2-8])(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[2-68]|7[246]'])])
