# Dependencies

EESR leverages multiple open source technologies for its implementation.&#x20;

* [Domonic](https://domonic.readthedocs.io/) [\[GitHub\]](https://github.com/byteface/domonic) is used to parse, modify ,and generate the HTML reports based on templates.
* [Plotly](https://plotly.com/python/) [\[GitHub\]](https://github.com/plotly/plotly.py) is the graphing library of choice. It is well known and features an extensive customizable library of graphs suiting our reporting needs.&#x20;
* [JSON Schema](https://json-schema.org/) allows the instrument to validate data inputs, custom profiles/templates/ratings, and metadata against a well defined schema.&#x20;

The table below shows the version of the dependencies for each release.

| EESR Version | Domonic                                            | Plotly                                          | JSON Schema (draft version)                                         |
| ------------ | -------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| 0.0.1        | [0.9.10](https://pypi.org/project/domonic/0.9.10/) | [5.8.2](https://pypi.org/project/plotly/5.8.2/) | [2020-12](https://json-schema.org/draft/2020-12/release-notes.html) |
