from ptext.pdf.canvas.event.event_listener import Event
from ptext.pdf.page.page import Page


class BeginPageEvent(Event):
    """
    This implementation of Event is triggered right before the Canvas is being processed.
    """

    def __init__(self, page: Page):
        self.page = page

    def get_page(self) -> Page:
        return self.page
