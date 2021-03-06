from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Decimal
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteNumberTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Decimal)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Decimal)

        is_integer = object_to_transform == int(object_to_transform)

        if is_integer:
            context.destination.write(bytes(str(int(object_to_transform)), "latin1"))
        else:
            context.destination.write(
                bytes("{:.2f}".format(float(object_to_transform)), "latin1")
            )
