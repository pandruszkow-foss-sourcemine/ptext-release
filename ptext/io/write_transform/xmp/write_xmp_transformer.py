import logging
import xml.etree.ElementTree as ET
import zlib
from typing import Optional

from ptext.io.read_transform.types import (
    AnyPDFType,
    Stream,
    Reference,
    Name,
    Decimal,
)
from ptext.io.write_transform.write_base_transformer import (
    WriteBaseTransformer,
    WriteTransformerContext,
)

logger = logging.getLogger(__name__)


class WriteXMPTransformer(WriteBaseTransformer):
    def can_be_transformed(self, any: AnyPDFType):
        return isinstance(any, ET.Element)

    def transform(
        self,
        object_to_transform: AnyPDFType,
        context: Optional[WriteTransformerContext] = None,
    ):
        assert isinstance(object_to_transform, ET.Element)
        assert context is not None
        assert context.destination is not None
        assert context.destination

        # build stream
        out_value = Stream()
        out_value[Name("Type")] = Name("Metadata")
        out_value[Name("Subtype")] = Name("XML")
        out_value[Name("Filter")] = Name("FlateDecode")

        bts = ET.tostring(object_to_transform)
        btsz = zlib.compress(bts, 9)
        out_value[Name("DecodedBytes")] = bts
        out_value[Name("Bytes")] = btsz
        out_value[Name("Length")] = Decimal(len(btsz))

        # copy reference
        out_value.set_reference(object_to_transform.get_reference())  # type: ignore [attr-defined]

        # start object if needed
        started_object = False
        ref = out_value.get_reference()  # type: ignore [attr-defined]
        if ref is not None:
            assert isinstance(ref, Reference)
            if ref.object_number is not None and ref.byte_offset is None:
                started_object = True
                self.start_object(out_value, context)

        # pass stream along to other transformer
        self.get_root_transformer().transform(out_value, context)

        # end object if needed
        if started_object:
            self.end_object(out_value, context)
