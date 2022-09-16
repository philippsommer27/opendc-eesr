The following documentation is an excerpt from the full EESR documentation site: https://philipp-sommerhalter.gitbook.io/eesr/
# What is EESR?

The Energy Sustainability and Efficiency Reporting (EESR) instrument aims to provide a complete report generation solution for data center (DC) energy efficiency. Featuring a curated library of reporting metrics and visualizations, EESR prioritizes ease of use while maintaining high configurability for all audiences. Additionally, EESR consists of a grid analysis module which provides insight into the sustainability of a data center's energy profile given its energy use over a time period.

### Why?

Why the need for EESR? Data centers energy efficiency research is a crucial part of our fight against climate change. Data center's consume a significant amount of electricity, of which the generation is not always green. To improve the efficiency of our data center, we must first deeply understand their current state. Furthermore, we must also be able to effectively communicate data center efficiency to the multitudes of stakeholders that are directly or indirectly involved with data centers.

### Features

EESR comes equip with a range of features for DC grid analysis and DC energy efficiency and sustainability reporting.&#x20;

#### EESR Reporting Module

The reporting module allows one to generate DC sustainability and energy efficiency reports. Reports feature metric values, source metadata and optionally graphs. Users can choose between different formats, reporting profiles and customize the entirety of the report should they wish to do so. The report is generated as a HTML file which can easily be modified and viewed. For easier distribution the module can also produce a PDF and PNG export.

#### EESR Grid Analysis Module

The grid analysis module derives various metrics and data from a given DC energy trace. By connecting to the [ENTSO-E](https://transparency.entsoe.eu/) API it can infer information about the source of the energy consumption and further deduce global warming impact through CO2 output calculation. The module is particularly suited for experiments as the timeframe, DC country and energy source model can be configured by the user. The results of an analysis can easily be turned into a report.

# Quick Start

In this section we provide a quick overview of how to get started with EESR. A more complete example of its usage can be seen in [this ](https://github.com/philippsommer27/experiments-bsc-thesis-2022)repository.

## Installing

EESR is available as a python package installable through PiP with the following command:

```
pip install opendc-eesr
```

Once installed, the module can be imported into any python project or Jupyter Notebook with:

```python
import eesr
```

With the module imported, you can now make use of the various classes and functions in the grid analysis module and the report generation module. The following two sections cover how to perform a basic analysis and create a report given an OpenDC energy trace.

## Grid Analysis

Within EESR's interface module there helper functions for performing the common tasks of EESR. We can import this interface with:

```python
from eesr import interface
```

The analysis is performed on an energy trace. That is, a tabular data source that has columns `timestamp`, `dc_power_total`, and `it_power_total`. The analysis module accepts a pandas data frame with the timestamp column type being pandas `datetime`.

Using the `opendc_grid_analysis` function from the `interface` module, we can produce the results we need with just one function. The function takes as parameters:

* `dc_path` : the path to the OpenDC trace
* `key_path` : the path to a .txt file containing the ENTSO-E api key code
* `start` : the start time from which the analysis should be performed
* `country` : the country which the analysis should assume the DC exists in
* `out` : path of where to write the results file to
* `tz` :  the time zone to use for the timestamps

Once given all these arguments, the function will preprocess the OpenDC trace into the correct pandas data frame and carry out the grid analysis by calling the `analyze` function of the analysis module. It returns a data frame which is a trace of grid and sustainability related data for every timestamp of the DC's operation. This is useful for further analysis beyond what is provided in the results file.&#x20;

The primary result of the analysis is a .json file containing metrics and metadata conforming to the [sustainability reporting profile](../library/reporting-profiles/sustainability-0.1.md).

## Report Generation

With the results obtained we can now easily produce a report. For the sake of simplicity we will demonstrate reporting in the [compact format](../library/report-templates/compact.md). The `interface` module conveniently provides a `generate_compact_profile` function for doing exactly this. It has as arguments:

* `data_path` : the path of the results matching the input file schema
* `profile_name` : selector for which [reporting profile](../library/reporting-profiles/) to generate the report for
* `generate_domain` : boolean to determine whether domain specific information should be included in report (useful for adding additional information that is not featured in the profile)
* `path` : the path to which to write the report to
