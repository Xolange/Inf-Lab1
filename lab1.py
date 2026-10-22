import re
import math


def cnt(s):
    s = s.strip()

    if not s:
        raise ValueError("Выражение не введено")

    try:
        n = float(s)
        if int(n) == n:
            return int(n)
        else:
            return n
    except ValueError:
        pass

    if s.count('(') != s.count(')'):
        raise ValueError("Неправильное количество скобок")

    if s.count(">=") > 0:
        p = s.split(">=")

        l = cnt(p[0])

        for i in p[1:]:
            r = cnt(i)

            if l >= r:
                l = r
            else:
                return "Ложь"

        return "Правда"

    m = re.search(r'log10\s*\(([^()]*)\)', s)

    if m:
        x = cnt(m.group(1))

        if x <= 0:
            raise ValueError(
                "Аргумент логарифма должен быть больше нуля"
            )

        res = math.log10(x)
        return cnt(s[:m.start()] + str(res) + s[m.end():])

    if "(" in s:
        io = s.rfind('(')
        ic = s.find(')', io)

        if ic == -1:
            raise ValueError("Не найдена закрывающая скобка")

        inner = s[io + 1:ic]
        val = cnt(inner)
        return cnt(s[:io] + str(val) + s[ic + 1:])

    m = re.search(r"(-?\d+\.?\d*)\s*([*/])\s*(-?\d+\.?\d*)", s)

    if m:
        l = float(m.group(1))
        op = m.group(2)
        r = float(m.group(3))

        if op == "*":
            res = l * r
        else:
            if r == 0:
                raise ZeroDivisionError("Деление на ноль запрещено")
            res = l / r

        return cnt(s[:m.start()] + str(res) + s[m.end():])

    m = re.search(r"(-?\d+\.?\d*)\s*([+\-])\s*(-?\d+\.?\d*)", s)

    if m:
        l = float(m.group(1))
        op = m.group(2)
        r = float(m.group(3))
        res = l - r if op == '-' else l + r

        return cnt(s[:m.start()] + str(res) + s[m.end():])

    raise ValueError("Некорректное арифметическое выражение")


def check_input(s):
    if not s.strip():
        raise ValueError("Выражение не введено")

    cl = re.sub(r'log10', '', s)

    if re.search(r'[^0-9+\-*/().>=\s]', cl):
        raise ValueError("Введены некорректные символы")


s = input("Введите выражение: ")

try:
    check_input(s)
    print("Результат:", cnt(s))
except (ValueError, ZeroDivisionError) as e:
    print("Ошибка:", e)
