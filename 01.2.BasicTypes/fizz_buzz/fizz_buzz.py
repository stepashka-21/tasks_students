import typing as tp


def get_fizz_buzz(n: int) -> list[tp.Union[int, str]]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    st: list[tp.Union[int, str]] = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            st.append("FizzBuzz")
        elif i % 3 == 0:
            st.append("Fizz")
        elif i % 5 == 0:
            st.append("Buzz")
        else:
            st.append(i)
    return st
