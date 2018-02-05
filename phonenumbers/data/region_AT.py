"""Auto-generated file, do not edit by hand. AT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AT = PhoneMetadata(id='AT', country_code=43, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-9]\\d{3,12}', possible_number_pattern='\\d{3,13}', possible_length=(4, 5, 6, 7, 8, 9, 10, 11, 12, 13), possible_length_local_only=(3,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='1\\d{3,12}|(?:2(?:1[467]|2[13-8]|5[2357]|6[1-46-8]|7[1-8]|8[124-7]|9[1458])|3(?:1[1-8]|3[23568]|4[5-7]|5[1378]|6[1-38]|8[3-68])|4(?:2[1-8]|35|63|7[1368]|8[2457])|5(?:12|2[1-8]|3[357]|4[147]|5[12578]|6[37])|6(?:13|2[1-47]|4[1-35-8]|5[468]|62)|7(?:2[1-8]|3[25]|4[13478]|5[68]|6[16-8]|7[1-6]|9[45]))\\d{3,10}', example_number='1234567890', possible_length=(4, 5, 6, 7, 8, 9, 10, 11, 12, 13), possible_length_local_only=(3,)),
    mobile=PhoneNumberDesc(national_number_pattern='6(?:5[0-3579]|6[013-9]|[7-9]\\d)\\d{4,10}', possible_number_pattern='\\d{7,13}', example_number='664123456', possible_length=(7, 8, 9, 10, 11, 12, 13)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{6,10}', possible_number_pattern='\\d{9,13}', example_number='800123456', possible_length=(9, 10, 11, 12, 13)),
    premium_rate=PhoneNumberDesc(national_number_pattern='9(?:0[01]|3[019])\\d{6,10}', possible_number_pattern='\\d{9,13}', example_number='900123456', possible_length=(9, 10, 11, 12, 13)),
    shared_cost=PhoneNumberDesc(national_number_pattern='8(?:10\\d|2(?:[01]\\d|8\\d?))\\d{5,9}', possible_number_pattern='\\d{8,13}', example_number='810123456', possible_length=(8, 9, 10, 11, 12, 13)),
    voip=PhoneNumberDesc(national_number_pattern='780\\d{6,10}', possible_number_pattern='\\d{9,13}', example_number='780123456', possible_length=(9, 10, 11, 12, 13)),
    uan=PhoneNumberDesc(national_number_pattern='5(?:(?:0[1-9]|17)\\d{2,10}|[79]\\d{3,11})|720\\d{6,10}', possible_number_pattern='\\d{5,13}', example_number='50123', possible_length=(5, 6, 7, 8, 9, 10, 11, 12, 13)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(116\\d{3})', format='\\1', leading_digits_pattern=['116'], national_prefix_formatting_rule='\\1'),
        NumberFormat(pattern='(1)(\\d{3,12})', format='\\1 \\2', leading_digits_pattern=['1'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(5\\d)(\\d{3,5})', format='\\1 \\2', leading_digits_pattern=['5[079]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(5\\d)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['5[079]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(5\\d)(\\d{4})(\\d{4,7})', format='\\1 \\2 \\3', leading_digits_pattern=['5[079]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3,10})', format='\\1 \\2', leading_digits_pattern=['316|46|51|732|6(?:5[0-3579]|[6-9])|7(?:[28]0)|[89]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{3,9})', format='\\1 \\2', leading_digits_pattern=['2|3(?:1[1-578]|[3-8])|4[2378]|5[2-6]|6(?:[12]|4[1-9]|5[468])|7(?:2[1-8]|35|4[1-8]|[5-79])'], national_prefix_formatting_rule='0\\1')],
    mobile_number_portable_region=True)
