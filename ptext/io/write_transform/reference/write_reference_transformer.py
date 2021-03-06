from typing import Optional

from ptext.io.read_transform.types import AnyPDFType, Reference
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)


class WriteReferenceTransform(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, Reference)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert context is not None
        assert context.destination is not None
        assert isinstance(object_to_transform, Reference)

        assert object_to_transform.object_number is not None
        context.destination.write(
            bytes(
                "%d %d R"
                % (
                    object_to_transform.object_number,
                    object_to_transform.generation_number or 0,
                ),
                "latin1",
            )
        )
