import meshio
from . import meshio_read_mesh as _meshio_read_mesh


def load(file):
    m = meshio.read(file)
    vertices, faces = _meshio_read_mesh(m)
    return [[vertices, faces]]
