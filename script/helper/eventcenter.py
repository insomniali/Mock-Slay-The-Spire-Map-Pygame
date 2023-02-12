import logging


_LOGGER = logging.getLogger("eventcenter")


class EventCenter:
    subscriber = {}

    @classmethod
    def subscribe(cls, event_type, func, reason, once=False):
        handles = {} if event_type not in cls.subscriber else cls.subscriber[event_type]
        if reason in handles:
            _LOGGER.debug("msg duplicate %s %s %s %s", event_type, once, reason)
            handle = handles[reason]
            handle.destroy()

        handle = EventHandle(event_type, func, once, reason)
        handles[reason] = handle
        cls.subscriber[event_type] = handles

    @classmethod
    def cancel(cls, event_type, reason):
        if event_type not in cls.subscriber:
            return
        if reason not in cls.subscriber[event_type]:
            return
        handle = cls.subscriber[event_type][reason]
        del cls.subscriber[event_type][reason]
        handle.destroy()

    @classmethod
    def process_event(cls, event):
        if event.type not in cls.subscriber:
            return
        to_destroy = []
        for reason in list(cls.subscriber[event.type]):
            handle = cls.subscriber[event.type][reason]
            handle(event)
            if not handle.once:
                continue
            to_destroy.append(handle)

        for handle in to_destroy:
            handle.destroy()


class EventHandle:

    def __init__(self, event_type, func, once, reason):
        self.event_type = event_type
        self.once = once
        self.reason = reason
        self._handle = func

    def __repr__(self):
        classname = self.__class__.__name__
        return "%s_%s_%s_%s" % (classname, self.event_type, self.once, self.reason)

    def __call__(self, event):
        self._handle(event)

    def destroy(self):
        self._handle = None
