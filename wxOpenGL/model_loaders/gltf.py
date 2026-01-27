from OCP.RWGltf import RWGltf_CafReader

from . import ocp_read_shape as _ocp_read_shape


def load(file):
    reader = RWGltf_CafReader()
    reader.ReadFile(file)
    reader.TransferRoots()
    shape = reader.Shape()

    vertices, faces = _ocp_read_shape(shape)

    return [[vertices, faces]]
