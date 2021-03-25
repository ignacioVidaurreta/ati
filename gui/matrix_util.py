import numpy as np
from PIL import Image

SUM = "addition"
SUB = "substraction"
MUL = "multiplication"

# We want to make sure we are using ndarrays
def use_ndarray(operation_fn):
    def _call_function_with_ndarray_args(A, B):
        return operation_fn(np.array(A), np.array(B))

    return _call_function_with_ndarray_args


def valid_shape(A, B, operation):
    are_similar = A.shape == B.shape

    if not are_similar:
        print(f"Error: cannot perform {operation}. Incompatible shapes A: {A.shape} B: {B.shape}")

    return are_similar

def valid_bands(A, B, op):
    A_RGB = type(A[0][0]) is np.ndarray or tuple
    B_RGB = type(B[0][0]) is np.ndarray or tuple

    if (A_RGB and B_RGB):
        return True
    if (not A_RGB and not B_RGB):
        return True
    else:
        print(f"Error: cannot perform {operation}. Incompatible image types")
        return False

@use_ndarray
def matrix_sum(A, B):
    if not valid_shape(A, B, SUM):
        return None

    if not valid_bands(A, B, SUM):
        return None

    RGB = type(A[0][0]) is np.ndarray

    if RGB:
        return normalizeOperation(A, B, lambda x, y: x+y)

    else:
        return normalizeOperationOneChannel(A, B, lambda x, y: x+y)

@use_ndarray
def matrix_mult(A, B):
    if not valid_shape(A, B, MUL):
        return None

    if not valid_bands(A, B, MUL):
        return None

    RGB = type(A[0][0]) is np.ndarray

    tmp = np.multiply(A,B)
    # If every element is valid we shouldnt normalize
    if (tmp > 0).all() & (tmp < 255).all():
        return tmp
    if RGB:
        return normalizeOperation(A, B, lambda x, y: x * y)

    else:
        return normalizeOperationOneChannel(A, B, lambda x, y: x * y)

@use_ndarray
def matrix_subst(A, B):
    if not valid_shape(A, B, SUB):
        return None

    if not valid_bands(A, B, matrix_subst):
        return None

    RGB = type(A[0][0]) is np.ndarray

    tmp = A + B
    # If every element is valid we shouldnt normalize
    if (tmp > 0).all() & (tmp < 255).all():
        return tmp

    if RGB:
        return normalizeOperation(A, B, lambda x, y: x-y)

    else:
        return normalizeOperationOneChannel(A, B, lambda x, y: x-y )



def normalizeOperationOneChannel(A, B, op):
    C = A.copy()
    minval = 255
    maxval = 0
    for x in range(A.shape[0]):
        for y in range(A.shape[1]):
            aux = op(A[x][y], B[x][y])
            if aux < minval:
                minval = aux
            if aux > maxval:
                maxval = aux
    print(minval)
    print(maxval)
    for x in range(A.shape[0]):
        for y in range(A.shape[1]):
            aux = op(A[x][y], B[x][y])
            if(minval == 0 and maxval == 0):
                C[x][y] = 0
            else:
                C[x][y] = round((aux - minval)*255 / (maxval-minval))
    return C

def normalizeOperation(A, B, op):
    rA, gA, bA = A[:,:,0], A[:,:,1], A[:,:,2]
    rB, gB, bB = B[:,:,0], B[:,:,1], B[:,:,2]
    rC = normalizeOperationOneChannel(rA, rB, op)
    gC = normalizeOperationOneChannel(gA, gB, op)
    bC = normalizeOperationOneChannel(bA, bB, op)
    C = np.dstack((rC,gC,bC))
    return C
