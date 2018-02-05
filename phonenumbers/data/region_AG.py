"""Auto-generated file, do not edit by hand. AG metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AG = PhoneMetadata(id='AG', country_code=1, international_prefix='011',
    general_desc=PhoneNumberDesc(national_number_pattern='[2589]\\d{9}', possible_number_pattern='\\d{7}(?:\\d{3})?', possible_length=(10,), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='268(?:4(?:6[0-38]|84)|56[0-2])\\d{4}', example_number='2684601234', possible_length=(10,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='268(?:464|7(?:2\\d|3[246]|64|7[0-689]|8[02-68]))\\d{4}', example_number='2684641234', possible_length=(10,), possible_length_local_only=(7,)),
    toll_free=PhoneNumberDesc(national_number_pattern='8(?:00|33|44|55|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='8002123456', possible_length=(10,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='900[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='9002123456', possible_length=(10,)),
    personal_number=PhoneNumberDesc(national_number_pattern='5(?:00|22|33|44|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='5002345678', possible_length=(10,)),
    voip=PhoneNumberDesc(national_number_pattern='26848[01]\\d{4}', possible_number_pattern='\\d{7}(?:\\d{3})?', example_number='2684801234', possible_length=(10,), possible_length_local_only=(7,)),
    pager=PhoneNumberDesc(national_number_pattern='26840[69]\\d{4}', possible_number_pattern='\\d{7}(?:\\d{3})?', example_number='2684061234', possible_length=(10,), possible_length_local_only=(7,)),
    national_prefix='1',
    national_prefix_for_parsing='1',
    leading_digits='268')
