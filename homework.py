def late(now, classes, bus):
    hn = ''
    mn = ''
    hc = ''
    mc = ''
    if len(now) == 4:
        hn = now[0]
        mn = now[2:]
    elif len(now) == 5:
        hn = now[:1]
        mn = now[3:]
    if len(classes) == 4:
        hc = classes[0]
        mc = classes[2:]
    elif len(classes) == 5:
        hc = classes[:1]
        mc = classes[3:]
    if hn < hc:
        m = (60 - int(mn)) + (60 - int(mc))
        for i in bus:
            if i < 5:
                continue
            elif i >= 5:
                mb = i
                break
        if m < (20 + mb):
            return('Опоздание')
        else:
             return('Выйти через', m - (20 + mb), 'минут')


print(late('9:20', '9:35', [4, 25, 30]))
