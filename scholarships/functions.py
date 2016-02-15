
def amount_tot(currency,amount,frequency,period):
    _amount=0
    if currency==0 :
        _amount=amount
    elif currency==1:
        _amount=amount*60
    elif currency==3:
        _amount=amount*102;
    elif currency==2:
        _amount=amount*72
    elif currency==4:
        _amount=amount*0.055;
    elif currency==5:
        _amount=amount*0.60;
    elif currency==6:
        _amount=amount*0.52
    elif currency==7:
        _amount=amount*2.7
    elif currency==8:
        _amount=amount*66.72
    if frequency==0:
        ''' we need nothing to do'''
    elif frequency==1:
        _amount=amount*period*12
    elif frequency==2:
        _amount=amount*period

    return _amount

def indianformat(paisa):
    if paisa < 1000:
        return str(paisa)
    paisa=str(paisa)
    paisalast = paisa[-3:]
    paisafirst = paisa[0:-3]
    paisafirst = paisafirst[::-1]
    n=2
    listw=[paisafirst[i:i+n] for i in range(0, len(paisafirst), n)]
    paisafirst=','.join(listw)
    paisafirst=paisafirst[::-1]
    paisa=paisafirst+','+paisalast
    return paisa

def sctype(index,amount):
    if amount==0:
        return 'varies'
    if index==0:
        return ''
    elif index==1:
        return 'monthly'
    elif index==2:
        return 'yearly'