import logging
from decimal import Decimal
from pathlib import Path

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.line_art.line_art_factory import LineArtFactory
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../annotations/test-add-all-line-art-annotation.log", level=logging.DEBUG
)


class TestAddAllLineArtAnnotation(Test):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../annotations/add-all-line-art-annotation")

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0203.pdf"))

    def test_corpus(self):
        super(TestAddAllLineArtAnnotation, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # determine output location
        out_file = self.output_dir / (file.stem + "_out.pdf")

        # attempt to read PDF
        doc = None
        with open(file, "rb") as in_file_handle:
            print("\treading (1) ..")
            doc = PDF.loads(in_file_handle)

        shapes = [
            LineArtFactory.right_sided_triangle(
                Rectangle(Decimal(0), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.isosceles_triangle(
                Rectangle(Decimal(110), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.parallelogram(
                Rectangle(Decimal(220), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.trapezoid(
                Rectangle(Decimal(330), Decimal(0), Decimal(100), Decimal(100))
            ),
            LineArtFactory.diamond(
                Rectangle(Decimal(440), Decimal(0), Decimal(100), Decimal(100))
            ),
            # second row
            LineArtFactory.pentagon(
                Rectangle(Decimal(0), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.hexagon(
                Rectangle(Decimal(110), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.heptagon(
                Rectangle(Decimal(220), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.octagon(
                Rectangle(Decimal(330), Decimal(110), Decimal(100), Decimal(100))
            ),
            LineArtFactory.regular_n_gon(
                Rectangle(Decimal(440), Decimal(110), Decimal(100), Decimal(100)), 17
            ),
            # third row
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(0), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.25),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(110), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.33),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(220), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.5),
            ),
            LineArtFactory.fraction_of_circle(
                Rectangle(Decimal(330), Decimal(220), Decimal(100), Decimal(100)),
                Decimal(0.75),
            ),
            LineArtFactory.droplet(
                Rectangle(Decimal(440), Decimal(220), Decimal(100), Decimal(100))
            ),
            # fourth row
            LineArtFactory.four_pointed_star(
                Rectangle(Decimal(0), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.five_pointed_star(
                Rectangle(Decimal(110), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.six_pointed_star(
                Rectangle(Decimal(220), Decimal(330), Decimal(100), Decimal(100))
            ),
            LineArtFactory.n_pointed_star(
                Rectangle(Decimal(330), Decimal(330), Decimal(100), Decimal(100)), 8
            ),
            LineArtFactory.n_pointed_star(
                Rectangle(Decimal(440), Decimal(330), Decimal(100), Decimal(100)), 10
            ),
            # fifth row
            LineArtFactory.arrow_left(
                Rectangle(Decimal(0), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_right(
                Rectangle(Decimal(110), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_up(
                Rectangle(Decimal(220), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.arrow_down(
                Rectangle(Decimal(330), Decimal(440), Decimal(100), Decimal(100))
            ),
            LineArtFactory.sticky_note(
                Rectangle(Decimal(440), Decimal(440), Decimal(100), Decimal(100))
            ),
        ]

        colors = [
            X11Color("Red"),
            X11Color("Orange"),
            X11Color("Yellow"),
            X11Color("Green"),
            X11Color("Blue"),
            X11Color("Plum"),
        ]

        # add annotation
        for i, s in enumerate(shapes):
            doc.get_page(0).append_polygon_annotation(
                points=s,
                stroke_color=colors[i % len(colors)],
            )

        # attempt to store PDF
        with open(out_file, "wb") as out_file_handle:
            print("\twriting ..")
            PDF.dumps(out_file_handle, doc)

        # attempt to re-open PDF
        with open(out_file, "rb") as in_file_handle:
            print("\treading (2) ..")
            doc = PDF.loads(in_file_handle)

        return True
