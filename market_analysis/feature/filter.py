import statistics
from typing import Any
from market_analysis.db.models import Order


async def filter_orders(orders: list[Order]) -> list[dict[str, Any]]:
    order_lists: dict[str, list[Order]] = {}
    result: list[dict[str, Any]] = []

    for order in orders:
        url_name = order.url_name
        if order.order_type == 'sell':
            if url_name in order_lists:
                order_lists[url_name].append(order)
            else:
                order_lists[url_name] = [order]

    for key in order_lists.keys():
        item = order_lists[key]

        low_rank: list[int] = []
        high_rank: list[int] = []

        max_rank = 0

        for order in item:
            if order.rank > max_rank:
                max_rank = order.rank

        for order in item:
            if order.rank == 0:
                low_rank.append(order.platinum)
            elif order.rank == max_rank:
                high_rank.append(order.platinum)

        filtered_low_rank = filter(low_rank, 0)
        filtered_high_rank = filter(high_rank, max_rank)

        result.append({
            'url_name': key,
            'max_rank': max_rank,
            'low': filtered_low_rank,
            'high': filtered_high_rank
        })

    return result


def filter(array: list[int], rank: int) -> dict[str, int]:
    array.sort()
    med = statistics.median(array)
    array_second, array_third, array_final = [], [], []

    for index, value in enumerate(array):
        if value < (med * 2):
            array_second.append(value)
        else:
            break

    array_second.sort()

    for index, value in enumerate(array_second):
        if index == 0:
            array_third.append(value)
            continue
        if (value * 2) > array_second[index - 1]:
            array_third.append(value)
        else:
            break

    array_third.sort()

    for index in range(int(len(array_second) / 2)):
        array_final.append(array_third[index])

    result = statistics.median(array_final)

    if rank == 0:
        return {
            'result': result,
            'inaccuracy': round(result / 10)
        }
    else:
        return {
            'result': result,
            'inaccuracy': round(result / 20)
        }
