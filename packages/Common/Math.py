from decimal import Decimal, ROUND_HALF_UP


def normal_round(number: float | str, precision=0) -> int | float:
    value = Decimal(str(number))

    if precision == 0:
        return int(value.to_integral_value(rounding=ROUND_HALF_UP))
    else:
        quant = Decimal("1").scaleb(-precision)
        return float(value.quantize(quant, rounding=ROUND_HALF_UP))
