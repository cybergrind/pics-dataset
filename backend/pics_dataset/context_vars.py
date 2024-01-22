from contextvars import ContextVar

CONTROLLER: ContextVar[None] = ContextVar("main_controller", default=None)
