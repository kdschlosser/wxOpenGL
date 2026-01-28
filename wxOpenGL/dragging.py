from typing import TYPE_CHECKING


from .geometry import point as _point


if TYPE_CHECKING:
    from . import canvas as _canvas
    from .objects import base3d as _base3d


class DragObject:

    def __init__(self, canvas: "_canvas.Canvas", selected: "_base3d.Base3D",
                 anchor_screen: _point.Point, pick_offset: _point.Point,
                 mouse_start: _point.Point, start_obj_pos: _point.Point,
                 last_pos: _point.Point):

        self.canvas = canvas
        self.selected = selected

        # (winx, winy, winz)
        self.anchor_screen = anchor_screen

        # _point.Point
        self.pick_offset = pick_offset

        # (mx,my) in top-left window coords
        self.mouse_start = mouse_start

        # last object world _point.Point used for incremental moves
        self.last_pos = last_pos

        #  _point.Point start position
        self.start_obj_pos = start_obj_pos

    # def move(self, candidate: _point.Point,
    #          start_pos: _point.Point, last_pos: _point.Point):
    #
    #     # if self._x_arrow.is_selected:
    #     #     new_pos = _point.Point(candidate.x, start_pos.y, start_pos.z)
    #     # elif self._y_arrow.is_selected:
    #     #     new_pos = _point.Point(start_pos.x, candidate.y, start_pos.z)
    #     # elif self._z_arrow.is_selected:
    #     #     new_pos = _point.Point(start_pos.x, start_pos.y, candidate.z)
    #     # else:
    #     #     return
    #
    #         # compute incremental delta to move things (arrows and object)
    #     delta = candidate - last_pos
    #
    #     position = self._position
    #     position += delta
    #
    #     return new_pos

    def __call__(self, mouse_point):
        delta = mouse_point - self.mouse_start

        # compute new anchor screen position (top-left coords)
        screen_new = self.anchor_screen + delta

        # Unproject at anchor winZ (note our unproject_point expects top-left coords)
        world_hit = self.canvas.camera.UnprojectPoint(screen_new)

        # candidate world = world_hit + pick_offset
        candidate = world_hit + self.pick_offset

        delta = candidate - self.last_pos

        position = self.selected.position
        position += delta

        # new_pos = self.owner.move(candidate, self.start_obj_pos, self.last_pos)
        self.last_pos = candidate
