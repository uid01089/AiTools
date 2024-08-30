from Ai.AiContext import AiContext
from ContextIf import ContextIf


class Context(AiContext, ContextIf):
    def __init__(self, model: str) -> None:
        AiContext.__init__(self, model)
