ACCN_LENGTH = 9
sunquest_days = {
    'X': '01',
    'M': '02',
    'T': '03',
    'W': '04',
    'H': '05',
    'F': '06',
    'S': '07'
}


def sunquest_fix(accn):
    if accn[0].isalpha():
        try:
            new_accn = sunquest_days[accn[0]]
        except:
            return None
        old_acn = accn[1:]
        if not old_acn.isdigit():
            print "sorry invalid accn"
            return None
        while len(new_accn)+len(old_acn) < ACCN_LENGTH:
            new_accn += '0'
        return new_accn + old_acn
    else:
        if len(accn) == ACCN_LENGTH:
            print "I did nothing"
            return accn
        else:
            print "too short"
            return None

if __name__ == "__main__":

    test = 'X32a'
    print sunquest_fix(test)
    test = 'M21'
    print sunquest_fix(test)
    test = '010000021'
    print sunquest_fix(test)
    test = '000321'
    print sunquest_fix(test)

    0o10002345
