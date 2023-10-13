from typing import List

from .models import MenuLink


def wrapp_data(data: List[MenuLink], split_address: List[str]):
    """
    Преобазовывает данные в словать содержащие имеющий древовидную структуру
    в которой если узел находиться в адрессе создаеться дополнительный уровень вложенности, с
    помощью рекурсии, а если узел не находится в адрессе запоминаеться с помощью ключа и значения
    :param data: данные для образования отсортированные по левому ключу
    :param split_address: массив из slug-ов
    :return: переобразованный словарь
    """
    res = {}

    def backtracking(index: int, depth: int, curr: dict):
        while index < len(data) and abs(data[index].level - depth + 1) > 1:
            if (depth < len(split_address) and data[index].slug != split_address[depth]) or depth == len(split_address):
                curr[data[index].slug] = data[index]
                index += ((data[index].right_key - data[index].left_key - 1) // 2) + 1
            else:
                curr[data[index].slug] = {
                    'value': data[index],
                    'children': {},
                }
                index = backtracking(index + 1, depth + 1, curr.get(data[index].slug).get('children'))
        return index

    backtracking(0, 0, res)
    return res
