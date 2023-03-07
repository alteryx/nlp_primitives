import asyncio


class CurrentEventLoop(object):
    """Represents the current event loop for a thread.

    Description:
        Gets the running event loop for a thread, or creates a new one.
        If a new event loop is created, the close method will close it, otherwise close is a noop.
    """

    def __init__(self):
        try:
            self.loop = asyncio.get_running_loop()
            self.should_close = False
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            self.should_close = True

    def close(self):
        if self.should_close:
            self.loop.close()
