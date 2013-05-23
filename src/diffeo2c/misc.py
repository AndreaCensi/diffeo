from contracts import new_contract, contract
import numpy as np

@new_contract
@contract(x='array[MxNx2](float32)')
def valid_diffeomorphism_cont(x):
    assert x.dtype == np.dtype('float32')
    M, N = x.shape[0], x.shape[1]
    assert (0 <= x[:, :, 0]).all()
    assert (x[:, :, 0] < M).all()
    assert (0 <= x[:, :, 1]).all()
    assert (x[:, :, 1] < N).all()
