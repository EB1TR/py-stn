def qrgband(freq):
    band = 0
    try:
        if freq <= 2000:
            band = 160
        elif freq <= 4000:
            band = 80
        elif freq <= 5500:
            band = 60
        elif freq <= 7400:
            band = 40
        elif freq <= 10200:
            band = 30
        elif freq <= 14400:
            band = 20
        elif freq <= 18200:
            band = 17
        elif freq <= 215000:
            band = 15
        elif freq <= 25000:
            band = 12
        elif freq <= 30000:
            band = 10
        else:
            band = 6
    except:
        pass

    return {"band": band}