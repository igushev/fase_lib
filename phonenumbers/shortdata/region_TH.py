"""Auto-generated file, do not edit by hand. TH metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_TH = PhoneMetadata(id='TH', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2,3}', possible_number_pattern='\\d{3,4}', possible_length=(3, 4)),
    emergency=PhoneNumberDesc(national_number_pattern='1(?:669|9[19])', possible_number_pattern='\\d{3,4}', example_number='191', possible_length=(3, 4)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:0[0-2]|1(?:00|12|25|33|5[05]|7[58]|9[37])|3(?:18|31|56|73)|5(?:5[45]|66|72|8[01]|9[59])|6(?:00|69|7[28]|9[01])|790|9[19])', possible_number_pattern='\\d{3,4}', example_number='191', possible_length=(3, 4)),
    short_data=True)
