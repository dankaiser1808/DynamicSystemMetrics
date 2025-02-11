import psutil

class DynamicMetric():
    def __init__(self, name: str, description: str, function: str,  attribute = None, parameters: tuple = None, unit: str = "MB", show_percentage: bool = False):
        self._name = name
        self._function = function
        self._attribute = attribute
        self._parameters = parameters
        self._description = description
        self._unit = unit
        self._show_percentage = show_percentage

    @property
    def name(self) -> str:
        return self._name

    @property
    def function(self) -> str:
        return self._function

    @property
    def attribute(self) -> str:
        return self._attribute

    @property
    def parameters(self) -> tuple:
        return self._parameters

    @property
    def description(self) -> str:
        return self._description

    @property
    def show_percentage(self) -> bool:
        return self._show_percentage

    @property
    def unit(self) -> str:
        return self._unit

    def convert_to_unit(self, bytes: int) -> float:
        if self._unit == "GB":
            return bytes / (1024 ** 3)
        if self._unit == "MB":
            return bytes / (1024 ** 2)

    def calc_to_percentage(self, value: int, total: int) -> float:
        return value / total * 100

    def psutil_function_call(self) -> str:
        percentage_value: float = 0
        psutil_function = self.get_psutil_function()
        if psutil_function:
            parameters = self.get_psutil_function_parameters()
            attribute = self.get_psutil_function_attribute()
            value = self.psutil_execute_function(psutil_function, parameters, attribute)

            if self._show_percentage:
                total = self.psutil_execute_function(psutil_function, parameters, "total")
                percentage_value = self.calc_to_percentage(value, total)

            if self._unit != None and self._unit != "":
                value = self.convert_to_unit(value)

            return self.format_output(value, percentage_value)
        else:
            return None

    def psutil_execute_function(self, function: str, parameters: tuple, attribute: str) -> any:
        psutil_function = getattr(psutil, function)
        if parameters != None and attribute != None:
            return getattr(psutil_function(*parameters), attribute)
        elif parameters == None and attribute != None:
            return getattr(psutil_function(), attribute)
        elif parameters != None and attribute == None:
            return psutil_function(*parameters)
        else:
            return psutil_function()

    def get_psutil_function(self) -> str:
        if self._function != None and self._function != "":
            if callable(getattr(psutil,self._function)):
                return self._function
        return None

    def get_psutil_function_attribute(self) -> str:
        if self._attribute != None and self._attribute != "":
            return self._attribute
        return None

    def get_psutil_function_parameters(self) -> tuple:
        if self._parameters != None and self._parameters != "":
            return self._parameters
        return None

    def format_output(self, value: float, percentage: float) -> str:
        if self._show_percentage:
            return f"{value:.2f}{self._unit} {percentage:.0f}%"
        elif self._unit:
            return f"{value:.2f}{self._unit}"
        else:
            return f"{value:.2f}"
