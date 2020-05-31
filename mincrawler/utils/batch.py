import math
import typing as tp

T = tp.TypeVar("T")


def generate_batch(items: tp.List[T],
                   batch_size: int) -> tp.Iterator[tp.List[T]]:
    num_items = len(items)
    num_batches = math.ceil(num_items / batch_size)

    for i in range(num_batches):
        batch = items[i * batch_size:(i + 1) * batch_size]
        yield batch
