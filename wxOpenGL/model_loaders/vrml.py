
from OCP.Vrml import Vrml_Provider
from . import ocp_read_shape as _ocp_read_shape


def load(file):
    reader = Vrml_Provider()
    reader.ReadFile(file)
    reader.TransferRoots()
    shape = reader.Shape()

    vertices, faces = _ocp_read_shape(shape)

    return [[vertices, faces]]
