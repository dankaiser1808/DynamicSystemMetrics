
class ColumnConfig():
    def __init__(self, name: str, justify: str, no_wrap: True, style: str):
        super().__init__()
        self._name = name
        self._justify = justify
        self._no_wrap = no_wrap
        self._style = style

    @property
    def name(self) -> str:
        return self._name

    @property
    def justify(self) -> str:
        return self._justify

    @property
    def no_wrap(self) -> bool:
        return self._no_wrap

    @property
    def style(self) -> str:
        return self._style
