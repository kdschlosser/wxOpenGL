
from typing import Self, Callable, Iterable, Union
import weakref
import math
import numpy as np
from scipy.spatial.transform import Rotation as _Rotation

from . import point as _point


class Angle:

    def __array_ufunc__(self, func, method, inputs, instance, **kwargs):
        if func == np.matmul:
            if isinstance(instance, np.ndarray):
                arr = np.array(self.as_float, dtype=np.float64)
                arr @= instance
                x, y, z = arr

                self._x = x
                self._y = y
                self._z = z

                self._process_update()
                return self
            else:
                return inputs @ self._R.as_matrix().T

        if func == np.add:
            arr = np.array(self.as_float, dtype=np.float64)

            if isinstance(instance, np.ndarray):
                arr = np.array(self.as_float, dtype=np.float64)
                arr += instance
                x, y, z = arr
                self._x = x
                self._y = y
                self._z = z

                self._process_update()
                return self
            else:
                return inputs + arr

        if func == np.subtract:
            arr = np.array(self.as_float, dtype=np.float64)

            if isinstance(instance, np.ndarray):
                arr -= instance
                x, y, z = arr
                self._x = x
                self._y = y
                self._z = z

                self._process_update()
                return self
            else:
                return inputs + arr

        raise RuntimeError

    def __init__(self, R=None):

        if R is None:
            R = _Rotation.from_quat([0.0, 0.0, 0.0, 1.0])  # NOQA

        self._R = R

        self.__callbacks = []
        self._ref_count = 0

    def __enter__(self):
        self._ref_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ref_count -= 1

    def __remove_callback(self, ref):
        try:
            self.__callbacks.remove(ref)
        except:  # NOQA
            pass

    def bind(self, cb: Callable[["Angle"], None]) -> bool:
        # We don't explicitly check to see if a callback is already registered.
        # What we care about is if a callback is called only one time and that
        # check is done when the callbacks are being executed. If there happens
        # to be a duplicate, the duplicate is then removed at that point in time.
        ref = weakref.WeakMethod(cb, self.__remove_callback)
        self.__callbacks.append(ref)
        return True

    def unbind(self, cb: Callable[["Angle"], None]) -> None:
        for ref in self.__callbacks[:]:
            callback = ref()
            if callback is None:
                self.__callbacks.remove(ref)
            elif callback == cb:
                # We don't return after locating a matching callback in the
                # event a callback was registered more than one time. Duplicates
                # are also removed at the time callbacks get called but if an update
                # to an angle never occurs we want to make sure that we explicitly
                # unbind all callbacks including duplicates.
                self.__callbacks.remove(ref)

    def _process_update(self):
        if self._ref_count:
            return

        for ref in self.__callbacks[:]:
            cb = ref()
            if cb is None:
                self.__callbacks.remove(ref)
            else:
                cb(self)

    @property
    def inverse(self) -> "Angle":
        R = self._R.inv()
        return Angle(R)

    @classmethod
    def _quat_to_euler(cls, quat: np.ndarray) -> tuple[float, float, float]:
        c = quat[0]
        d = quat[1]
        e = quat[2]
        f = quat[3]
        g = c + c
        h = d + d
        k = e + e
        a = c * g
        l = c * h  # NOQA
        c = c * k
        m = d * h
        d = d * k
        e = e * k
        g = f * g
        h = f * h
        f = f * k

        matrix = np.array([1 - (m + e), l + f, c - h, 0,
                           l - f, 1 - (a + e), d + g, 0,
                           c + h, d - g, 1 - (a + m), 0], dtype=np.float64)

        return cls._matrix_to_euler(matrix)

    @staticmethod
    def _matrix_to_euler(matrix: np.ndarray) -> tuple[float, float, float]:

        def clamp(a_, b_, c_):
            return max(b_, min(c_, a_))

        a = matrix[0]
        f = matrix[4]
        g = matrix[8]
        h = matrix[1]
        k = matrix[5]
        l = matrix[9]  # NOQA
        m = matrix[2]
        n = matrix[6]
        e = matrix[10]

        y = math.asin(clamp(g, -1, 1))
        if 0.99999 > abs(g):
            x = math.atan2(-l, e)
            z = math.atan2(-f, a)
        else:
            x = math.atan2(n, k)
            z = 0

        return math.degrees(x), math.degrees(y), math.degrees(z)

    @staticmethod
    def _euler_to_quat(x: float, y: float, z: float) -> np.ndarray:

        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        d2 = 2.0
        x_half = x / d2
        y_half = y / d2
        z_half = z / d2

        c = math.cos(x_half)
        d = math.cos(y_half)
        e = math.cos(z_half)
        f = math.sin(x_half)
        g = math.sin(y_half)
        h = math.sin(z_half)

        x = f * d * e + c * g * h
        y = c * g * e - f * d * h
        z = c * d * h + f * g * e
        w = c * d * e - f * g * h

        quat = np.array([x, y, z, w], dtype=np.float32)
        return quat

    @property
    def x(self) -> float:
        quat = self._R.as_quat()
        angles = self._quat_to_euler(quat)
        return angles[0]

    @x.setter
    def x(self, value: float):
        quat = self._R.as_quat()
        angles = list(self._quat_to_euler(quat))
        angles[0] = value

        quat = self._euler_to_quat(*angles)

        self._R = _Rotation.from_quat(quat)  # NOQA
        self._process_update()

    @property
    def y(self) -> float:
        quat = self._R.as_quat()
        angles = self._quat_to_euler(quat)
        return angles[1]

    @y.setter
    def y(self, value: float):
        quat = self._R.as_quat()
        angles = list(self._quat_to_euler(quat))
        angles[1] = value

        quat = self._euler_to_quat(*angles)

        self._R = _Rotation.from_quat(quat)  # NOQA
        self._process_update()

    @property
    def z(self) -> float:
        quat = self._R.as_quat()
        angles = self._quat_to_euler(quat)
        return angles[2]

    @z.setter
    def z(self, value: float):
        quat = self._R.as_quat()
        angles = list(self._quat_to_euler(quat))
        angles[2] = value

        quat = self._euler_to_quat(*angles)

        self._R = _Rotation.from_quat(quat)  # NOQA
        self._process_update()

    def copy(self) -> "Angle":
        return Angle.from_quat(self._R.as_quat())

    def __iadd__(self, other: Union["Angle", np.ndarray]) -> Self:
        if isinstance(other, Angle):
            x, y, z = other
        else:
            x, y, z = (float(item) for item in other)

        tx, ty, tz = self

        tx += x
        ty += y
        tz += z

        quat = self._euler_to_quat(tx, ty, tz)
        self._R = _Rotation.from_quat(quat)  # NOQA
        self._process_update()
        return self

    def __add__(self, other: Union["Angle", np.ndarray]) -> "Angle":
        if isinstance(other, Angle):
            x, y, z = other
        else:
            x, y, z = (float(item) for item in other)

        tx, ty, tz = self

        tx += x
        ty += y
        tz += z
        quat = self._euler_to_quat(tx, ty, tz)
        return self.from_quat(quat)

    def __isub__(self, other: Union["Angle", np.ndarray]) -> Self:
        if isinstance(other, Angle):
            x, y, z = other
        else:
            x, y, z = (float(item) for item in other)

        tx, ty, tz = self

        tx -= x
        ty -= y
        tz -= z
        quat = self._euler_to_quat(tx, ty, tz)
        self._R = _Rotation.from_quat(quat)  # NOQA
        self._process_update()
        return self

    def __sub__(self, other: Union["Angle", np.ndarray]) -> "Angle":
        if isinstance(other, Angle):
            x, y, z = other
        else:
            x, y, z = (float(item) for item in other)

        tx, ty, tz = self

        tx -= x
        ty -= y
        tz -= z
        quat = self._euler_to_quat(tx, ty, tz)
        return self.from_quat(quat)

    def __rmatmul__(self, other: Union[np.ndarray, _point.Point]) -> np.ndarray:
        if isinstance(other, np.ndarray):
            other @= self._R.as_matrix().T
        elif isinstance(other, _point.Point):
            values = other.as_numpy @ self._R.as_matrix().T

            x = float(values[0])
            y = float(values[1])
            z = float(values[2])
            quat = self._euler_to_quat(x, y, z)
            other._R = _Rotation.from_quat(quat)  # NOQA
            other._process_update()  # NOQA

        elif isinstance(other, Angle):
            matrix = other._R.as_matrix() @ self._R.as_matrix()  # NOQA
            other._R = _Rotation.from_matrix(matrix)  # NOQA
            other._process_update()
        else:
            raise RuntimeError('sanity check')

        return other

    def __imatmul__(self, other: Union[np.ndarray, _point.Point]) -> np.ndarray:
        if isinstance(other, np.ndarray):
            other @= self._R.as_matrix().T
        elif isinstance(other, _point.Point):
            values = other.as_numpy @ self._R.as_matrix().T

            x = float(values[0])
            y = float(values[1])
            z = float(values[2])

            with other:
                other.x = x
                other.y = y
                other.z = z

            other._process_update()  # NOQA

        elif isinstance(other, Angle):
            matrix = self._R.as_matrix() @ other._R.as_matrix()  # NOQA
            self._R = _Rotation.from_matrix(matrix)  # NOQA
            self._process_update()
            return self
        else:
            raise RuntimeError('sanity check')

        return other

    def __matmul__(self, other: Union[np.ndarray, _point.Point]) -> np.ndarray:
        if isinstance(other, np.ndarray):
            other = other @ self._R.as_matrix().T
        elif isinstance(other, _point.Point):
            values = other.as_numpy @ self._R.as_matrix().T
            x = float(values[0])
            y = float(values[1])
            z = float(values[2])

            other = _point.Point(x, y, z)
        elif isinstance(other, Angle):
            matrix = self._R.as_matrix() @ other._R.as_matrix()  # NOQA
            R = _Rotation.from_matrix(matrix)  # NOQA
            other = Angle(R)
        else:
            raise RuntimeError('sanity check')

        return other

    def __bool__(self):
        return self.as_float == (0, 0, 0)

    def __eq__(self, other: "Angle") -> bool:
        x1, y1, z1 = self
        x2, y2, z2 = other

        return x1 == x2 and y1 == y2 and z1 == z2

    def __ne__(self, other: "Angle") -> bool:
        return not self.__eq__(other)

    @property
    def as_float(self) -> tuple[float, float, float]:
        quat = self._R.as_quat()
        x, y, z = self._quat_to_euler(quat)

        return x, y, z

    @property
    def as_int(self) -> tuple[int, int, int]:
        x, y, z = self.as_float
        return int(x), int(y), int(z)

    @property
    def as_quat(self) -> np.ndarray:
        return self._R.as_quat()

    @property
    def as_matrix(self) -> np.ndarray:
        return self._R.as_matrix().T

    def __iter__(self) -> Iterable[float]:
        quat = self._R.as_quat()
        x, y, z = self._quat_to_euler(quat)

        return iter([x, y, z])

    def __str__(self) -> str:
        quat = self._R.as_quat()
        x, y, z = self._quat_to_euler(quat)
        return f'X: {x}, Y: {y}, Z: {z}'

    @classmethod
    def from_matrix(cls, matrix: np.ndarray):
        R = _Rotation.from_matrix(matrix)  # NOQA
        return cls(R)

    @classmethod
    def from_euler(cls, x: float, y: float, z: float) -> "Angle":
        quat = cls._euler_to_quat(x, y, z)
        R = _Rotation.from_quat(quat)  # NOQA
        ret = cls(R)
        return ret

    @classmethod
    def from_quat(cls, q: list[float, float, float, float] | np.ndarray) -> "Angle":
        R = _Rotation.from_quat(q)  # NOQA
        return cls(R)

    @classmethod
    def from_points(cls, p1: _point.Point, p2: _point.Point) -> "Angle":
        # the sign for all of the verticies in the array needs to be flipped in
        # order to handle the -Z axis being near
        p1 = -p1.as_numpy
        p2 = -p2.as_numpy

        f = p2 - p1

        fn = np.linalg.norm(f)
        if fn < 1e-6:
            return cls.from_euler(0.0, 0.0, 0.0)

        f = f / fn  # world-space direction of the line

        local_forward = np.array([0.0, 0.0, -1.0],
                                 dtype=np.dtypes.Float64DType)

        nz = np.nonzero(local_forward)[0][0]
        sign = np.sign(local_forward[nz])
        forward_world = f * sign

        up = np.asarray((0.0, 1.0, 0.0),
                        dtype=np.dtypes.Float64DType)

        if np.allclose(np.abs(np.dot(forward_world, up)), 1.0, atol=1e-8):
            up = np.array([0.0, 0.0, 1.0],
                          dtype=np.dtypes.Float64DType)

            if np.allclose(np.abs(np.dot(forward_world, up)), 1.0, atol=1e-8):
                up = np.array([1.0, 0.0, 0.0],
                              dtype=np.dtypes.Float64DType)

        right = np.cross(up, forward_world)  # NOQA

        rn = np.linalg.norm(right)
        if rn < 1e-6:
            raise RuntimeError("degenerate right vector")

        right = right / rn

        true_up = np.cross(forward_world, right)  # NOQA

        rot = np.column_stack((right, true_up, forward_world))

        R = _Rotation.from_matrix(rot)  # NOQA
        return cls(R)
