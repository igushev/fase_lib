"""Auto-generated file, do not edit by hand. BS metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BS = PhoneMetadata(id='BS', country_code=1, international_prefix='011',
    general_desc=PhoneNumberDesc(national_number_pattern='[2589]\\d{9}', possible_number_pattern='\\d{7}(?:\\d{3})?', possible_length=(10,), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='242(?:3(?:02|[236][1-9]|4[0-24-9]|5[0-68]|7[3467]|8[0-4]|9[2-467])|461|502|6(?:0[1-3]|12|7[67]|8[78]|9[89])|7(?:02|88))\\d{4}', example_number='2423456789', possible_length=(10,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='242(?:3(?:5[79]|[79]5)|4(?:[2-4][1-9]|5[1-8]|6[2-8]|7\\d|81)|5(?:2[45]|3[35]|44|5[1-9]|65|77)|6[34]6|7(?:27|38)|8(?:0[1-9]|1[02-9]|2\\d|99))\\d{4}', example_number='2423591234', possible_length=(10,), possible_length_local_only=(7,)),
    toll_free=PhoneNumberDesc(national_number_pattern='242300\\d{4}|8(?:00|33|44|55|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{7}(?:\\d{3})?', example_number='8002123456', possible_length=(10,), possible_length_local_only=(7,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='900[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='9002123456', possible_length=(10,)),
    personal_number=PhoneNumberDesc(national_number_pattern='5(?:00|22|33|44|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='5002345678', possible_length=(10,)),
    national_prefix='1',
    national_prefix_for_parsing='1',
    leading_digits='242')
