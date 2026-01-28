from typing import TYPE_CHECKING

from . import base3d as _base3d
from .. import model_loader as _model_loader
from ..geometry import angle as _angle
from ..geometry import point as _point

if TYPE_CHECKING:
    from .. import Canvas as _Canvas
    from .. import gl_materials as _glm



class MeshModel(_base3d.Base3D):

    def __init__(self, canvas: "_Canvas", material: "_glm.GLMaterial",
                 selected_material: "_glm.GLMaterial", smooth: bool,
                 file: str, position: _point.Point | None = None,
                 angle: _angle.Angle | None = None):

        data = _model_loader.load(file)
        _base3d.Base3D.__init__(self, canvas, material, selected_material,
                                smooth, data, position, angle)
