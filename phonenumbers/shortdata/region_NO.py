"""Auto-generated file, do not edit by hand. NO metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_NO = PhoneMetadata(id='NO', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,5}', possible_number_pattern='\\d{3,6}', possible_length=(3, 4, 6)),
    toll_free=PhoneNumberDesc(national_number_pattern='1161(?:1[17]|23)', possible_number_pattern='\\d{6}', example_number='116117', possible_length=(6,)),
    emergency=PhoneNumberDesc(national_number_pattern='11[023]', possible_number_pattern='\\d{3}', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:1(?:[0239]|61(?:1[17]|23))|2[048]|4(?:12|[59])|7[57]|90)', possible_number_pattern='\\d{3,6}', example_number='112', possible_length=(3, 4, 6)),
    short_data=True)
