"""Auto-generated file, do not edit by hand. PT metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_PT = PhoneMetadata(id='PT', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 6)),
    toll_free=PhoneNumberDesc(national_number_pattern='116(?:000|111)', possible_number_pattern='\\d{6}', example_number='116000', possible_length=(6,)),
    emergency=PhoneNumberDesc(national_number_pattern='11[25]', possible_number_pattern='\\d{3,6}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='11(?:[2578]|6(?:000|111))', possible_number_pattern='\\d{3,6}', example_number='112', possible_length=(3, 6)),
    short_data=True)
