"""Auto-generated file, do not edit by hand. BH metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BH = PhoneMetadata(id='BH', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[0189]\\d{2,4}', possible_number_pattern='\\d{3,5}', possible_length=(3, 5)),
    toll_free=PhoneNumberDesc(national_number_pattern='(?:0[167]|81)\\d{3}', possible_number_pattern='\\d{5}', example_number='07123', possible_length=(5,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='9[148]\\d{3}', possible_number_pattern='\\d{5}', example_number='94123', possible_length=(5,)),
    emergency=PhoneNumberDesc(national_number_pattern='[19]99', possible_number_pattern='\\d{3}', example_number='999', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='0[167]\\d{3}|1(?:[02]\\d|12|4[01]|51|8[18]|9[169])|8[158]\\d{3}|9(?:[148]\\d{3}|9[02489])', possible_number_pattern='\\d{3,5}', example_number='999', possible_length=(3, 5)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='0[67]\\d{3}|88000|98555', possible_number_pattern='\\d{5}', example_number='88000', possible_length=(5,)),
    short_data=True)
