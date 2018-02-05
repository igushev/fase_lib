"""Auto-generated file, do not edit by hand. KZ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_KZ = PhoneMetadata(id='KZ', country_code=7, international_prefix='810',
    general_desc=PhoneNumberDesc(national_number_pattern='(?:33\\d|7\\d{2}|80[09])\\d{7}', possible_number_pattern='\\d{10}', possible_length=(10,)),
    fixed_line=PhoneNumberDesc(national_number_pattern='33622\\d{5}|7(?:1(?:0(?:[23]\\d|4[0-3]|59|63)|1(?:[23]\\d|4[0-79]|59)|2(?:[23]\\d|59)|3(?:2\\d|3[0-79]|4[0-35-9]|59)|4(?:[24]\\d|3[013-9]|5[1-9])|5(?:2\\d|3[1-9]|4[0-7]|59)|6(?:[234]\\d|5[19]|61)|72\\d|8(?:[27]\\d|3[1-46-9]|4[0-5]))|2(?:1(?:[23]\\d|4[46-9]|5[3469])|2(?:2\\d|3[0679]|46|5[12679])|3(?:[234]\\d|5[139])|4(?:2\\d|3[1235-9]|59)|5(?:[23]\\d|4[01246-8]|59|61)|6(?:2\\d|3[1-9]|4[0-4]|59)|7(?:[2379]\\d|40|5[279])|8(?:[23]\\d|4[0-3]|59)|9(?:2\\d|3[124578]|59)))\\d{5}', example_number='7123456789', possible_length=(10,)),
    mobile=PhoneNumberDesc(national_number_pattern='7(?:0[012578]|47|6[02-4]|7[15-8]|85)\\d{7}', example_number='7710009998', possible_length=(10,)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{7}', possible_number_pattern='\\d{10}', example_number='8001234567', possible_length=(10,)),
    premium_rate=PhoneNumberDesc(national_number_pattern='809\\d{7}', possible_number_pattern='\\d{10}', example_number='8091234567', possible_length=(10,)),
    voip=PhoneNumberDesc(national_number_pattern='751\\d{7}', possible_number_pattern='\\d{10}', example_number='7511234567', possible_length=(10,)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='751\\d{7}', possible_number_pattern='\\d{10}', example_number='7511234567', possible_length=(10,)),
    preferred_international_prefix='8~10',
    national_prefix='8',
    national_prefix_for_parsing='8')
