"""
Simplified VM code which works for some cases.
You need extend/rewrite code to pass all cases.
"""

import builtins
import dis
import operator
import types
import typing as tp


class Frame:
    """
    Frame header in cpython with description
        https://github.com/python/cpython/blob/3.9/Include/frameobject.h#L17

    Text description of frame parameters
        https://docs.python.org/3/library/inspect.html?highlight=frame#types-and-members
    """

    def __init__(self,
                 frame_code: types.CodeType,
                 frame_builtins: dict[str, tp.Any],
                 frame_globals: dict[str, tp.Any],
                 frame_locals: dict[str, tp.Any]) -> None:
        self.code = frame_code
        self.builtins = frame_builtins
        self.globals = frame_globals
        self.locals = frame_locals
        self.data_stack: tp.Any = []
        self.return_value = None
        self.position = 0

    def get_iter_op(self):
        self.push(iter(self.pop()))

    def load_assertion_error_op(self, op):
        pass

    def raise_varargs_op(self, val: int) -> None:
        pass

    def extended_arg_op(self, val: int) -> None:
        pass

    def top(self) -> tp.Any:
        return self.data_stack[-1]

    def pop(self) -> tp.Any:
        return self.data_stack.pop()

    def push(self, *values: tp.Any) -> None:
        self.data_stack.extend(values)

    def popn(self, n: int) -> tp.Any:
        """
        Pop a number of values from the value stack.
        A list of n values is returned, the deepest value first.
        """
        if n > 0:
            returned = self.data_stack[-n:]
            self.data_stack[-n:] = []
            return returned
        else:
            return []

    def run(self) -> tp.Any:
        for instruction in dis.get_instructions(self.code):
            getattr(self, instruction.opname.lower() + "_op")(instruction.argval)
        return self.return_value

    def call_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-CALL_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3496
        """
        arguments = self.popn(arg)
        f = self.pop()
        self.push(f(*arguments))

    def call_function_kw_op(self, arg: tp.Any) -> None:
        x = self.pop()
        s = len(x)
        y = self.popn(x)
        pos = self.popn(x)
        kw = dict()
        for i in range(s):
            kw[x[i]] = y[i]
        f = self.pop()
        self.push(f(*pos, **kw))

    def load_name_op(self, arg: tp.Any) -> None:
        """
        Partial realization

        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2416
        """
        if arg in self.builtins:
            self.push(self.builtins[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        elif arg in self.locals:
            self.push(self.locals[arg])
        else:
            raise NameError

    def load_global_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_GLOBAL

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2480
        """
        if arg in self.builtins:
            self.push(self.builtins[arg])
        elif arg in self.globals:
            self.push(self.globals[arg])
        else:
            raise NameError

    def load_const_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-LOAD_CONST

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1346
        """
        self.push(arg)

    def load_fast_op(self, arg: tp.Any) -> None:
        if arg in self.locals:
            self.push(self.locals[arg])
        else:
            raise NameError

    def load_attr_op(self, arg: tp.Any) -> None:
        self.push(getattr(self.pop(), arg))

    def load_method_op(self, arg: tp.Any) -> None:
        x = self.pop()
        if hasattr(x, arg):
            self.push(getattr(x, arg))
        else:
            raise AttributeError

    def call_method_op(self, arg: tp.Any) -> None:
        s = int(arg)
        args = self.popn(s)
        x = self.pop()
        self.push(x(*args))

    def return_value_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-RETURN_VALUE

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1911
        """
        self.return_value = self.pop()

    def pop_top_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-POP_TOP

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L1361
        """
        self.pop()

    def make_function_op(self, arg: int) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-MAKE_FUNCTION

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L3571

        Parse stack:
            https://github.com/python/cpython/blob/3.9/Objects/call.c#L671

        Call function in cpython:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L4950
        """
        name = self.pop()  # the qualified name of the function (at TOS)  # noqa
        code = self.pop()  # the code associated with the function (at TOS1)

        # TODO: use arg to parse function defaults

        def f(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
            # TODO: parse input arguments using code attributes such as co_argcount

            parsed_args: tp.Dict[str, tp.Any] = {}
            f_locals = dict(self.locals)
            f_locals.update(parsed_args)

            frame = Frame(code, self.builtins, self.globals, f_locals)  # Run code in prepared environment
            return frame.run()

        self.push(f)

    def store_name_op(self, arg: tp.Any) -> None:
        """
        Operation description:
            https://docs.python.org/release/3.9.7/library/dis.html#opcode-STORE_NAME

        Operation realization:
            https://github.com/python/cpython/blob/3.9/Python/ceval.c#L2280
        """
        const = self.pop()
        self.locals[arg] = const

    def store_global_op(self, arg: tp.Any) -> None:
        self.globals[arg] = self.pop()

    def store_fast_op(self, arg: tp.Any) -> None:
        self.locals[arg] = self.pop()

    def store_subscr_op(self, *args: tp.Any) -> None:
        x, y = self.popn(2)
        x[y] = self.pop()
        self.push(x)
        self.push(y)

    def store_attr_op(self, arg: tp.Any) -> None:
        x, y = self.popn(2)
        setattr(y, arg, x)

    def store_deref_op(self, arg: tp.Any) -> None:
        self.push(cells[arg].set(self.pop()))

    def store_map_op(self) -> None:
        a, b, c = self.popn(3)
        a[c] = b
        self.push(a)

    def delete_global_op(self, arg: tp.Any) -> None:
        del self.globals[arg]

    def delete_fast_op(self, arg: tp.Any) -> None:
        del self.locals[arg]

    def delete_name_op(self, arg: tp.Any) -> None:
        del self.locals[arg]

    def delete_subscr_op(self, *args: tp.Any):
        x, y = self.popn(2)
        del x[y]

    def delete_attr_op(self, arg: tp.Any) -> None:
        delattr(self.pop(), arg)

    def jump_forward_op(self, arg: tp.Any) -> None:
        self.position = arg

    def jump_absolute_op(self, arg: tp.Any) -> None:
        self.position = arg

    def pop_jump_if_true_op(self, arg: tp.Any) -> None:
        if self.pop():
            self.position = arg

    def jump_if_true_or_pop_op(self, arg: tp.Any) -> None:
        if self.top():
            self.position = arg
        else:
            self.pop()

    def pop_jump_if_false_op(self, arg: tp.Any) -> None:
        if not self.pop():
            self.position = arg

    def jump_if_false_or_pop(self, arg: tp.Any) -> None:
        if not self.top():
            self.position = arg
        else:
            self.pop()

    def dict_update_op(self, i: tp.Any) -> None:
        x, y = self.popn(2)
        dict.update(x[-i], y)

    def build_set_op(self, arg: tp.Any) -> None:
        self.push(set(self.popn(arg)))

    def build_tuple_op(self, arg: tp.Any) -> None:
        self.push(tuple(self.popn(arg)))

    def build_slice_op(self, arg: tp.Any) -> None:
        self.push(slice(*self.popn(arg)))

    def build_list_op(self, arg: tp.Any) -> None:
        self.push(list(self.popn(arg)))

    def build_string_op(self, arg: tp.Any) -> None:
        self.push(str((self.popn(arg)).join()))

    def build_map_op(self, arg: tp.Any) -> None:
        self.push({})

    def build_const_key_map_op(self, size: int) -> None:
        x = self.pop()
        y = self.popn(size)
        self.push({key: value for key, value in zip(x, y)})

    def binary_add_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a += b
        self.push(a)

    def binary_and_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a *= b
        self.push(a)

    def binary_lshift_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a <<= b
        self.push(a)

    def binary_rshift_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a >>= b
        self.push(a)

    def binary_power_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a **= b
        self.push(a)

    def binary_floor_divide_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a //= b
        self.push(a)

    def binary_true_divide_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a /= b
        self.push(a)

    def binary_modulo_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a %= b
        self.push(a)

    def binary_multiply_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a *= b
        self.push(a)

    def binary_matrix_multiply_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a @= b
        self.push(a)

    def binary_subtract_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a -= b
        self.push(a)

    def binary_subscr_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        self.push(operator.getitem(a, b))

    def binary_xor_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a ^= b
        self.push(a)

    def binary_or_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a |= b
        self.push(a)

    def dup_top_op(self, *args: tp.Any) -> None:
        self.push(self.top())

    def dup_top_two_op(self, *args: tp.Any) -> None:
        x, y = self.popn(2)
        self.push(x)
        self.push(y)
        self.push(x)
        self.push(y)

    def get_aiter_op(self, arg: tp.Any) -> None:
        self.push(self.pop().__aiter__())

    def inplace_add_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a += b
        self.push(a)

    def inplace_and_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a *= b
        self.push(a)

    def inplace_lshift_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a <<= b
        self.push(a)

    def inplace_rshift_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a >>= b
        self.push(a)

    def inplace_power_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a **= b
        self.push(a)

    def inplace_floor_divide_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a //= b
        self.push(a)

    def inplace_true_divide_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a /= b
        self.push(a)

    def inplace_modulo_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a %= b
        self.push(a)

    def inplace_multiply_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a *= b
        self.push(a)

    def inplace_matrix_multiply_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a @= b
        self.push(a)

    def inplace_subtract_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a -= b
        self.push(a)

    def inplace_subscr_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        self.push(operator.getitem(a, b))

    def inplace_xor_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a ^= b
        self.push(a)

    def inplace_or_op(self, op: tp.Any) -> None:
        a, b = self.popn(2)
        a |= b
        self.push(a)

    def list_append_op(self, arg: tp.Any):
        x = self.pop()
        l = self.peek(arg)
        l.append(x)

    def list_extend_op(self, *args: tp.Any):
        x, y = self.popn(2)
        x.extend(y)
        self.push(x)

    def list_to_tuple_op(self, arg: tp.Any) -> None:
        self.push(tuple(self.popn(arg)))

    def map_add_op(self, arg: tp.Any) -> None:
        x, y = self.popn(2)
        dict.__setitem__(self.data_stack[-arg], x, y)

    def rot_two_op(self, op: tp.Any) -> None:
        x, y = self.popn(2)
        self.push(y)
        self.push(x)

    def rot_three_op(self, op: tp.Any) -> None:
        x, y, z = self.popn(3)
        self.push(z)
        self.push(y)
        self.push(x)

    def rot_four_op(self, op: tp.Any) -> None:
        x, y, z, t = self.popn(4)
        self.push(t)
        self.push(z)
        self.push(y)
        self.push(x)

    def byte_LOAD_BUILD_CLASS(self):
        self.push(__build_class__)

    def set_update_op(self, *args: tp.Any) -> None:
        pass

    def set_add_op(self, arg: tp.Any) -> None:
        x = self.pop()
        s = self.peek(arg)
        s += x

    def unary_positive_op(self, op: tp.Any) -> None:
        self.push(+self.pop())

    def unary_negative_op(self, op: tp.Any) -> None:
        self.push(-self.pop())

    def unary_not_op(self, op: tp.Any) -> None:
        self.push(not self.pop())

    def unary_invert_op(self, op: tp.Any) -> None:
        self.push(~self.pop())

    def unpack_sequence_op(self, arg: tp.Any) -> None:
        x = self.pop()
        for i in reversed(x):
            self.push(i)

    operators = {
        '<': lambda x, y: x < y, '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y, '>': lambda x, y: x > y,
        '==': lambda x, y: x == y, '!=': lambda x, y: x != y,
        'is not': lambda x, y: x is not y, 'is': lambda x, y: x is y,
        'in': lambda x, y: x in y, 'not in': lambda x, y: x not in y,
    }

    def compare_op_op(self, comparator: tp.Any) -> None:
        x, y = self.popn(2)
        if comparator in self.operators:
            op = self.operators[comparator]
            self.push(op(x, y))
        else:
            raise NameError

    def is_op_op(self, op: tp.Any) -> None:
        x, y = self.popn(2)
        if op == 1:
            self.push(x is not y)
        else:
            self.push(x is y)

    def contains_op_op(self, op: tp.Any) -> None:
        x, y = self.popn(2)
        if op == 1:
            self.push(x not in y)
        else:
            self.push(x in y)


class VirtualMachine:
    def run(self, code_obj: types.CodeType) -> None:
        """
        :param code_obj: code for interpreting
        """
        globals_context: tp.Dict[str, tp.Any] = {}
        frame = Frame(code_obj, builtins.globals()['__builtins__'], globals_context, globals_context)
        return frame.run()
