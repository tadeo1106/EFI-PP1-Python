from datetime import datetime


def determinar_mes(m=0):
    fecha_actual = datetime.now()
    mes = fecha_actual.month + m
    year = fecha_actual.year

    if mes > 12:
        mes -= 12
        year += 1

    inicio_mes = datetime(year, mes, 1)
    if mes == 12:
        fin_mes = datetime(year + 1, 1, 1)
    else:
        fin_mes = datetime(year, mes + 1, 1)

    return inicio_mes, fin_mes


inicio_mes, fin_mes = determinar_mes(2)
print("Inicio del mes:", inicio_mes)
print("Fin del mes:", fin_mes)
