"""Auto-generated file, do not edit by hand. SL metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_SL = PhoneMetadata(id='SL', country_code=232, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[2-9]\\d{7}', possible_number_pattern='\\d{6,8}', possible_length=(8,), possible_length_local_only=(6,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='[235]2[2-4][2-9]\\d{4}', example_number='22221234', possible_length=(8,), possible_length_local_only=(6,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:2[15]|3[03-5]|4[04]|5[05]|66|7[6-9]|88|99)\\d{6}', example_number='25123456', possible_length=(8,)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{6})', format='\\1 \\2', national_prefix_formatting_rule='(0\\1)')])
