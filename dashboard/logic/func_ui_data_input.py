from components.comp_data_input import check_icon


def check_accurate_numeric_range(input_value:int):
    """ """

    if isinstance(input_value, int):
        check = input_value > 0 and input_value <= 1000
        return check_icon(check)
    else:
        return check_icon(False)
    

def check_accurate_new_data(re_value:bool, ):
    """ """

    if re_value:
        return check_icon(True)
    else:
        return check_icon(True)
    