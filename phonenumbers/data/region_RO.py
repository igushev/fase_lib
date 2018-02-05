"""Auto-generated file, do not edit by hand. RO metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_RO = PhoneMetadata(id='RO', country_code=40, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[23]\\d{5,8}|[7-9]\\d{8}', possible_number_pattern='\\d{6,9}', possible_length=(6, 9)),
    fixed_line=PhoneNumberDesc(national_number_pattern='2(?:1(?:\\d{7}|9\\d{3})|[3-6](?:\\d{7}|\\d9\\d{2}))|3(?:1\\d{4}(?:\\d{3})?|[3-6]\\d{7})', example_number='211234567', possible_length=(6, 9)),
    mobile=PhoneNumberDesc(national_number_pattern='7(?:[0-8]\\d{2}|99\\d)\\d{5}', possible_number_pattern='\\d{9}', example_number='712345678', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{6}', possible_number_pattern='\\d{9}', example_number='800123456', possible_length=(9,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='90[036]\\d{6}', possible_number_pattern='\\d{9}', example_number='900123456', possible_length=(9,)),
    shared_cost=PhoneNumberDesc(national_number_pattern='801\\d{6}', possible_number_pattern='\\d{9}', example_number='801123456', possible_length=(9,)),
    uan=PhoneNumberDesc(national_number_pattern='37\\d{7}', possible_number_pattern='\\d{9}', example_number='372123456', possible_length=(9,)),
    national_prefix='0',
    preferred_extn_prefix=' int ',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['[23]1'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['[23]1'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[23][3-7]|[7-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(2\\d{2})(\\d{3})', format='\\1 \\2', leading_digits_pattern=['2[3-6]'], national_prefix_formatting_rule='0\\1')],
    mobile_number_portable_region=True)
