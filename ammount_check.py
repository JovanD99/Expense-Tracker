import re

def amount_check(number):
    """checks if the provided argument is an amount of some 
    sort e.g money, measurement etc.""" 
        
    # one digit numbers, positive, negative or zero
    match1 = re.match("-?[0-9]$", str(number))
    # positive or negative integer with more than one digit
    match2 = re.match("-?[1-9]+[0-9]+$", str(number))
    # numbers with only one digits before the decimal point
    match3 = re.match("-?[0-9]\.[0-9]+$", str(number))
    # numbers with more than one digit before the decimal point
    match4 = re.match("-?[1-9][0-9]+\.[0-9]+$", str(number))
    # positive decimal numbers starting with a dot
    match5 = re.match("\.[0-9]+$", str(number))

    if any([match1, match2, match3, match4, match5]):
        return True
    else:
        return False


