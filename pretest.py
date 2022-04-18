def sum_of_items(lst: list) -> int:
    """
    Given a list of integers, return the sum of these integers.
    If the list is empty, return 0.
    ex. [5, 6, 2, 1] --> 5+6+2+1=14
    ex. [0, 0] --> 0+0=0
    """
    sum = 0
    for i in lst:
        sum += i
    return sum

def dict_of_num_type_lsts(lst: list) -> dict:
    """
    Given a list of integers, create a dictionary with three keys: "pos_lst", "zero_lst", and "neg_lst".
    The value of key "pos_lst" should be the list of all positive integers in the argument.
    The value of key "zero_lst" should be the list of all zeroes in the argument.
    The value of key "neg_lst" should be the list of all negative integers in the argument.
    ex. [4, 2, 5, 0, 2, 1, 0, -1] -->
        {"pos_lst": [4, 2, 5, 2, 1], "zero_lst": [0, 0], "neg_lst": [-1]}
    """
    dic = {
        "pos_lst": [],
        "zero_lst": [],
        "neg_lst": []
    }
    for i in lst:
        if i == 0:
            dic["zero_lst"].append(i)
        elif i > 0:
            dic["pos_lst"].append(i)
        else:
            dic["neg_lst"].append(i)
    return dic

def ratings_adjustment(ratings):
    """
    Given a dictionary containing the overall student ratings of the AppDev courses,
    with course names as keys and ratings as values, ensure that the results are correct.

    Naturally, any courses with a higher rating than 'backend' must have cheated,
    so they should be removed from the dictionary entirely.

    Return the corrected dictionary.
    """
    top_score = ratings['backend']
    keys_to_remove = []
    for key in ratings:
        if ratings[key] > top_score:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        ratings.pop(key)
    return ratings
    

class Counter:
    """
    Implement a function 'getVal' that gets the value of an object. 
    On creation, this value should be 0.
    Implement a function called "inc" that increases the value of the object
    by 1.
    Implement a function called "dec" that decreases the value of the obejct
    by 1.
    """
    def __init__(self):
        self.val = 0

    def getVal(self):
        return self.val

    def inc(self):
        self.val += 1

    def dec(self):
        self.val -= 1

if __name__ == "__main__":
    empty_lst = []
    big_lst = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    small_lst = [-1, 0, 1]
    lst_with_only_zeroes = [0, 0, 0]

    print("sum_of_items results:")
    print(f"sum_of_items({empty_lst}): {sum_of_items(empty_lst)}")
    print(f"sum_of_items({big_lst}): {sum_of_items(big_lst)}")
    print(f"sum_of_items({small_lst}): {sum_of_items(small_lst)}")
    print(
        f"sum_of_items({lst_with_only_zeroes}): {sum_of_items(lst_with_only_zeroes)}"
    )
    print()

    print("dict_of_num_type_lsts results:")
    print(
        f"dict_of_num_type_lsts({empty_lst}): {dict_of_num_type_lsts(empty_lst)}"
    )
    print(f"dict_of_num_type_lsts({big_lst}): {dict_of_num_type_lsts(big_lst)}")
    print(
        f"dict_of_num_type_lsts({small_lst}): {dict_of_num_type_lsts(small_lst)}"
    )
    print(
        f"dict_of_num_type_lsts({lst_with_only_zeroes}): {dict_of_num_type_lsts(lst_with_only_zeroes)}"
    )
    print()

    test_ratings = {'backend': 5, 'ios': 3, 'android': 7}
    print("ratings_adjustment results:")
    print(f"ratings_adjustment({test_ratings}): {ratings_adjustment(test_ratings)}")
    print()

    print("Counter results:")
    counter = Counter()
    print(f"counter.getVal(): {counter.getVal()}")
    counter.inc()
    counter.inc()
    print(f"counter.inc(), counter.inc(): {counter.getVal()}")
    counter.dec()
    print(f"counter.dec(): {counter.getVal()}")
    print()


