from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class PopGraphicsState(CanvasOperator):
    """
    Restore the graphics state by removing the most recently saved
    state from the stack and making it the current state (see 8.4.2,
    "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("Q", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert len(canvas.graphics_state_stack) > 0
        canvas.graphics_state = canvas.graphics_state_stack.pop(-1)
