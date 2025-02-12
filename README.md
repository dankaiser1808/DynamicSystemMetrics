# DynamicSystemMetrics

A flexible script that renders a system metrics table using `psutil`. Function calls are dynamically defined and executed at runtime via a YAML configuration, allowing high customization and adaptability.

## Why?

Since I wanted to play around with Python, I built this small project focused on OS-level metrics. The idea was to showcase how injecting values via a config file can make code more flexible and adaptable.

Since `psutil` metric-gathering functions are generated at runtime, we can dynamically add new ones to be rendered in the table. Of course, this comes with a trade-off: higher complexity and trickier debugging. In a real production setup, you'd typically send these metrics to a collector like Prometheus instead-but hey, this is just for fun and learning!

## Example

Here’s an example of the generated table using `config.yaml`:

![Table](docs/config_table.png)

And another example using `config_system_info.yaml`, which also includes static system metrics:

![Table2](docs/config_system_info_table.png)

Based on the provided config file, we can define the actual values shown, the table’s style, and which metrics should be visualized! :rocket:

## Possible Enhancements

While this project serves as a proof of concept, here are some potential improvements:

- **More complex calculations**: Calculations of provided metrics. This could be implemented via a dynamic calculator that determines operations defined in the YAML file and executes them.

- **Structured logging**: In a production setup, structured logging (JSON format) would improve filtering and flexibility in distributed setups.

- **Unit tests**: Currently no tests are defined for the DynamicMetric functions.
