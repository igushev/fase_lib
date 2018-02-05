"""Auto-generated file, do not edit by hand. NL metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_NL = PhoneMetadata(id='NL', country_code=31, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{4,8}|[2-7]\\d{8}|[89]\\d{6,9}', possible_number_pattern='\\d{5,10}', possible_length=(5, 6, 7, 8, 9, 10)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:1[0135-8]|2[02-69]|3[0-68]|4[0135-9]|[57]\\d|8[478])\\d{7}', possible_number_pattern='\\d{9}', example_number='101234567', possible_length=(9,)),
    mobile=PhoneNumberDesc(national_number_pattern='6[1-58]\\d{7}', possible_number_pattern='\\d{9}', example_number='612345678', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{4,7}', possible_number_pattern='\\d{7,10}', example_number='8001234', possible_length=(7, 8, 9, 10)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90[069]\\d{4,7}', possible_number_pattern='\\d{7,10}', example_number='9061234', possible_length=(7, 8, 9, 10)),
    voip=PhoneNumberDesc(national_number_pattern='(?:6760|85\\d{2})\\d{5}', possible_number_pattern='\\d{9}', example_number='851234567', possible_length=(9,)),
    pager=PhoneNumberDesc(national_number_pattern='66\\d{7}', possible_number_pattern='\\d{9}', example_number='662345678', possible_length=(9,)),
    uan=PhoneNumberDesc(national_number_pattern='140(?:1(?:[035]|[16-8]\\d)|2(?:[0346]|[259]\\d)|3(?:[03568]|[124]\\d)|4(?:[0356]|[17-9]\\d)|5(?:[0358]|[124679]\\d)|7\\d|8[458])', possible_number_pattern='\\d{5,6}', example_number='14020', possible_length=(5, 6)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='14\\d{3,4}', possible_number_pattern='\\d{5,6}', example_number='14123', possible_length=(5, 6)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='([1-578]\\d)(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['1[035]|2[0346]|3[03568]|4[0356]|5[0358]|7|8[4578]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='([1-5]\\d{2})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['1[16-8]|2[259]|3[124]|4[17-9]|5[124679]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(6)(\\d{8})', format='\\1 \\2', leading_digits_pattern=['6[0-57-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(66)(\\d{7})', format='\\1 \\2', leading_digits_pattern=['66'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(14)(\\d{3,4})', format='\\1 \\2', leading_digits_pattern=['14'], national_prefix_formatting_rule='\\1'),
        NumberFormat(pattern='([89]0\\d)(\\d{4,7})', format='\\1 \\2', leading_digits_pattern=['80|9'], national_prefix_formatting_rule='0\\1')],
    mobile_number_portable_region=True)
