"""Auto-generated file, do not edit by hand. NU metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_NU = PhoneMetadata(id='NU', country_code=683, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-5]\\d{3}', possible_number_pattern='\\d{4}', possible_length=(4,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='[34]\\d{3}', example_number='4002', possible_length=(4,)),
    mobile=PhoneNumberDesc(national_number_pattern='[125]\\d{3}', example_number='1234', possible_length=(4,)))
