def calcula_total(obj, campo):
    total = 0
    for i in obj:
        # getattr: retorna o valor de um atributo de determinado objeto
        total += getattr(i, campo)
    return total