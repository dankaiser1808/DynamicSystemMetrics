from entities.dynamic_metric import DynamicMetric

class Category():
    def __init__(self, name: str, metrics: list[DynamicMetric]):
        self._name = name
        self._metrics = metrics

    @property
    def name(self) -> str:
        return self._name

    @property
    def metrics(self) -> list[DynamicMetric]:
        return self._metrics
