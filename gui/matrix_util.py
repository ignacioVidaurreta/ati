import numpy as np

SUM = "addition"
SUB = "substraction"
MUL = "multiplication"

# We want to make sure we are using ndarrays
def use_ndarray(operation_fn):
    def _call_function_with_ndarray_args(A, B):
        return operation_fn(np.array(A), np.array(B))

    return _call_function_with_ndarray_args


def valid_shape(A, B, operation):
    if operation in [SUM, SUB]:
        are_similar = A.shape == B.shape
    elif operation == MUL:
        are_similar = A.shape[1] == B.shape[0]

    if not are_similar:
        print(f"Error: cannot perform {operation}. Incompatible shapes A: {A.shape} B: {B.shape}")

    return are_similar

@use_ndarray
def matrix_sum(A, B):
    if not valid_shape(A, B, SUM):
        return None

    return np.add(A, B)

@use_ndarray
def matrix_mult(A, B):
    if not valid_shape(A, B, MUL):
        return None

    return np.matmul(A, B)

@use_ndarray
def matrix_subst(A, B):
    if not valid_shape(A, B, SUB):
        return None

    return np.subtract(A, B)
