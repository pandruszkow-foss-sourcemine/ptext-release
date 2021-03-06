import typing
from decimal import Decimal
from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.geometry.line_segment import LineSegment
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


def _bezier(p0, p1, p2, p3) -> typing.List[LineSegment]:
    pts = []
    ONE = Decimal(1)
    for t in [
        Decimal(x) for x in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ]:
        x = (
            (ONE - t) ** 3 * p0[0]
            + 3 * t * (ONE - t) ** 2 * p1[0]
            + 3 * t ** 2 * (ONE - t) * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            (ONE - t) ** 3 * p0[1]
            + 3 * t * (ONE - t) ** 2 * p1[1]
            + 3 * t ** 2 * (ONE - t) * p2[1]
            + t ** 3 * p3[1]
        )
        pts.append((x, y))

    # build List of LineSegments
    out: typing.List[LineSegment] = []
    for i in range(1, len(pts)):
        out.append(LineSegment(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]))

    # return
    return out


class AppendCubicBezierCurve1(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    (x1 , y1 ) and (x2 , y2 ) as the Bézier control points (see 8.5.2.2,
    "Cubic Bézier Curves"). The new current point shall be
    (x3 , y3 ).
    """

    def __init__(self):
        super().__init__("c", 6)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)
        assert isinstance(operands[4], Decimal)
        assert isinstance(operands[5], Decimal)

        # get graphic state
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = (operands[0], operands[1])
        p2 = (operands[2], operands[3])
        p3 = (operands[4], operands[5])

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)


class AppendCubicBezierCurve2(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    the current point and (x2 , y2 ) as the Bézier control points (see
    8.5.2.2, "Cubic Bézier Curves"). The new current point shall
    be (x3 , y3 ).
    """

    def __init__(self):
        super().__init__("v", 4)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)

        # get graphic state
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = p0
        p2 = (operands[0], operands[1])
        p3 = (operands[2], operands[3])

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)


class AppendCubicBezierCurve3(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    (x1 , y1 ) and (x3 , y3 ) as the Bézier control points (see 8.5.2.2,
    "Cubic Bézier Curves"). The new current point shall be (x3 , y3 ).
    """

    def __init__(self):
        super().__init__("y", 4)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)

        # get graphic state
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = (operands[0], operands[1])
        p2 = (operands[2], operands[3])
        p3 = p2

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)
