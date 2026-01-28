from typing import TYPE_CHECKING


from .geometry import point as _point


if TYPE_CHECKING:
    from . import canvas as _canvas
    from .objects import base3d as _base3d


class DragObject:

    def __init__(self, canvas: "_canvas.Canvas", selected: "_base3d.Base3D"):

        self.canvas = canvas
        self.selected = selected

        # last object world _point.Point used for incremental moves
        self.last_pos = selected.position.copy()
        self.axis_lock = _point.Point(0, 0, 0)

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

    def __call__(self, delta):
        # project center to screen
        anchor_screen = self.canvas.camera.ProjectPoint(self.selected.position)

        # compute pick-world and offsets
        pick_world = self.canvas.camera.UnprojectPoint(anchor_screen)
        pick_offset = self.selected.position - pick_world

        # compute new anchor screen position (top-left coords)
        screen_new = anchor_screen + delta

        # Unproject at anchor winZ (note our unproject_point expects top-left coords)
        world_hit = self.canvas.camera.UnprojectPoint(screen_new)

        world_hit += pick_offset
        delta = world_hit - self.last_pos

        print('world_hit:', world_hit)
        print('delta:', delta)

        if tuple(self.axis_lock) == (0.0, 0.0, 0.0):
            if delta.z <= delta.x >= delta.y:
                self.axis_lock.x = 1.0
            elif delta.x <= delta.y >= delta.z:
                self.axis_lock.y = 1.0
            elif delta.x <= delta.z >= delta.y:
                self.axis_lock.z = 1.0
            else:
                print(world_hit)
                print(delta)
                raise RuntimeError

        delta.x *= self.axis_lock.x
        delta.y *= self.axis_lock.y
        delta.z *= self.axis_lock.z

        print('delta:', delta)

        position = self.selected.position
        print('position:', position)
        position += delta
        print('position:', position)
        print()

        # new_pos = self.owner.move(candidate, self.start_obj_pos, self.last_pos)
        self.last_pos = world_hit
