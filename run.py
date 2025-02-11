import time, yaml, logging, sys
from rich.table import Table
from rich.live import Live

from entities.column_config import ColumnConfig
from entities.table_config import TableConfig
from entities.dynamic_metric import DynamicMetric
from entities.category import Category

categories: list[Category] = []
table_config: TableConfig = {}
column_config: ColumnConfig = []

#TODO: Logging should be in JSON format for structured logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if len(sys.argv) != 2:
    logging.info("Usage: py run.py <config_name>.yaml")
    sys.exit(1)

#TODO: config.yaml file could be passed as arg.
with open(sys.argv[1]) as stream:
    try:
        config = yaml.safe_load(stream)
        table = config.get("table", None)

        if not table:
            raise TypeError("Table not set in config.yaml")
        if not config["categories"]:
            raise TypeError("Categories not set in config.yaml")

        for column in table["columns"]:
            column_config.append(ColumnConfig(
                name=column.get("name", None),
                justify=column.get("justify", "left"),
                no_wrap=column.get("no_wrap", True),
                style=column.get("style", "green")
            ))

        table_config = TableConfig(
            title = table.get("title", "System Metrics"),
            style = table.get("style", "magenta"),
            wait_before_refresh = config.get("wait_before_refresh", 0.5),
            refresh_per_second = config.get("refresh_per_second", 10),
            column_config=column_config
        )

        for category in config["categories"]:
            metrics: list[DynamicMetric] = []
            for metric in category["metrics"]:
                metrics.append(
                DynamicMetric(
                    name=metric.get("name", None),
                    description=metric.get("description", ""),
                    function=metric.get("function", None),
                    attribute=metric.get("attribute", None),
                    parameters=metric.get("parameters", None),
                    unit= metric.get("unit", None),
                    show_percentage=metric.get("show_percentage", False)
                )
            )

            new_category = Category(category.get("name", None), metrics)
            categories.append(new_category)

    except FileNotFoundError as file_not_found_error:
        logging.exception(file_not_found_error)
    except AttributeError as attribute_error:
        logging.exception(attribute_error)
    except TypeError as type_error:
        logging.exception(type_error)
    except ValueError as value_error:
        logging.exception(value_error)
    except Exception as error:
        logging.exception(error)

def create_table_rows(table: Table, metrics: list[DynamicMetric], category_emoji: str):
    table.add_row(category_emoji)

    for metric in metrics:
        metric_value = metric.psutil_function_call()
        table.add_row("",metric.name, metric_value, metric.description)

def generate_table() -> Table:
    table = Table(title=table_config.title, style=table_config.style)

    for column in table_config.column_config:
        table.add_column(column.name, justify=column.justify, no_wrap=column.no_wrap, style=column.style)

    for category in categories:
        create_table_rows(table, category.metrics, category.name)
        table.rows[-1].end_section = True

    return table

with Live(generate_table(), refresh_per_second=table_config.refresh_per_second) as live:
    while True:
        time.sleep(table_config.wait_before_refresh)
        live.update(generate_table())
