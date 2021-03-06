"""Auto-generated file, do not edit by hand. AS metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AS = PhoneMetadata(id='AS', country_code=1, international_prefix='011',
    general_desc=PhoneNumberDesc(national_number_pattern='[5689]\\d{9}', possible_number_pattern='\\d{7}(?:\\d{3})?', possible_length=(10,), possible_length_local_only=(7,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='6846(?:22|33|44|55|77|88|9[19])\\d{4}', example_number='6846221234', possible_length=(10,), possible_length_local_only=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='684(?:2(?:5[2468]|72)|7(?:3[13]|70))\\d{4}', example_number='6847331234', possible_length=(10,), possible_length_local_only=(7,)),
    toll_free=PhoneNumberDesc(national_number_pattern='8(?:00|33|44|55|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='8002123456', possible_length=(10,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='900[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='9002123456', possible_length=(10,)),
    personal_number=PhoneNumberDesc(national_number_pattern='5(?:00|22|33|44|66|77|88)[2-9]\\d{6}', possible_number_pattern='\\d{10}', example_number='5002345678', possible_length=(10,)),
    national_prefix='1',
    national_prefix_for_parsing='1',
    leading_digits='684')
