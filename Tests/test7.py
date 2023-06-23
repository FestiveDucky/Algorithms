import itertools
import multiprocessing
from multiprocessing import Value


# error_value = Value('i', 0)  # assign as integer type


def get_data(args):
    url, error_value = args
    try:
        # all even numbers -> ZeroDivisionError
        if url % 2 == 0:
            1 / 0
    except ZeroDivisionError as e:
        #   with error_value.get_lock():
        # read/write is not an atomic operatoion
        # lock is required to do it right
        # the context manager makes the use of it easier
        error_value.value += str(1)
        print("ZeroDivisionError -->", url, "/ 0")


if __name__ == '__main__':
    with multiprocessing.Pool(6) as p:
        with multiprocessing.Manager() as manager:
            error_value = manager.Value(1, "")
            args = itertools.product([0, 1, 2, 3, 4], [error_value])
            results = p.map(get_data, args)
            # usually you should consume the results
            # actually get_data does not return explicit something
            # so it returns implicit for each call None
            for result in results:
                ...
            # pro tip: 3 dots is Ellipsis, a placeholder used for numpy
            #          I use it often to have a placeholder for missing code
            print("Total errors:", error_value.value)