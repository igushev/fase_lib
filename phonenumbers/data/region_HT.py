"""Auto-generated file, do not edit by hand. HT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_HT = PhoneMetadata(id='HT', country_code=509, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[2-489]\\d{7}', possible_number_pattern='\\d{8}', possible_length=(8,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='2(?:2\\d|5[1-5]|81|9[149])\\d{5}', example_number='22453300', possible_length=(8,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:[34]\\d{2}|9(?:8[0-35]|9[5-9]))\\d{5}', example_number='34101234', possible_length=(8,)),
    toll_free=PhoneNumberDesc(national_number_pattern='8\\d{7}', possible_number_pattern='\\d{8}', example_number='80012345', possible_length=(8,)),
    voip=PhoneNumberDesc(national_number_pattern='98[89]\\d{5}', possible_number_pattern='\\d{8}', example_number='98901234', possible_length=(8,)),
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{2})(\\d{4})', format='\\1 \\2 \\3')])
