
from entities.column_config import ColumnConfig

class TableConfig():
    def __init__(self, title: str, style: str, wait_before_refresh: float, refresh_per_second: int, column_config: ColumnConfig):
        self._title = title
        self._style = style
        self._wait_before_refresh = wait_before_refresh
        self._refresh_per_second =  refresh_per_second
        self.column_config = column_config

    @property
    def title(self) -> str:
        return self._title

    @property
    def style(self) -> str:
        return self._style

    @property
    def wait_before_refresh(self) -> float:
        return self._wait_before_refresh

    @property
    def refresh_per_second(self) -> int:
        return self._refresh_per_second
