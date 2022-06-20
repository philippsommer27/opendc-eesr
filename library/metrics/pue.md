# ⚡ PUE

Power Usage Effectiveness (PUE) was proposed by [The Green Grid](https://www.thegreengrid.org/) in 2007 in an effort promote a better understanding of energy use in data centers. PUE provides high level insight into how much of the total energy provisioned to the facility is used in the IT equipment for productivity. &#x20;

{% hint style="info" %}
In contrary to its name, PUE is actually a measure of [energy rather than power](https://ctlsys.com/support/energy\_kwh\_vs-\_power\_kw/).
{% endhint %}

<details>

<summary>Details</summary>

Unit: **NA**

Minimum: **1.0**

Maximum: **∞**

Ideal: **1.0**

Industry Average ([2020](https://www.statista.com/statistics/1229367/data-center-average-annual-pue-worldwide/)): 1.59

****

</details>

## Formula

$$
PUE = \frac{TOTAL \ FACILITY \ ENERGY}{IT \  EQUIPMENT \ ENERGY }
$$

Where&#x20;

$$TOTAL \ FACILITY \ ENERGY$$ is the entire energy consumption of the data center including infrastructure and staff facilities and,&#x20;

$$IT \ EQUIPMENT \ ENERGY$$ represents the energy use of the just the IT equipment such as servers, networking and storage.

## Evaluation

PUE is by far the most popular data center energy efficiency metric adopted across the industry. It is standardized in both [ISO/IEC 30134-2:2016](https://www.iso.org/standard/63451.html) and [EN 50600-4-2:2016](https://www.en-standard.eu/csn-en-50600-4-2-information-technology-data-centre-facilities-and-infrastructures-part-4-2-power-usage-effectiveness/). This allows institutions and organizations to set targets for data centers to reach in terms of PUE.&#x20;

Despite its heavy use, PUE is limited as a metric and suffers from misuse.

Generally, a large value **can** be indicative of inefficiencies in a data center's infrastructure, **but** this must be taken as a signal for further investigation; not a final fact. No conclusions can be drawn about the efficiency of IT equipment, scheduling techniques, and resource allocation from PUE.&#x20;

**Unsuitable for Comparison**

One of the major disadvantages of PUE is that is not suitable for comparing different data centers. This is due to multiple reasons.&#x20;

1. Differences in the climate of two data centers can result in vastly different PUE values but does not oblige that one data center has a more energy efficient system than the other.
2. Unless specifically detailed, two PUE values from different sources could be measured in different ways. Variations such as measuring points and measurement interval renders a blind comparison useless.&#x20;

**Difficult to Measure**

Although not an inherent flaw with the metric, PUE poses the challenge of needing measuring points at various locations for best insight. Energy measurements should take place as near to the IT equipment as possible, however this is not always possible and as such losses from intermediate power delivery systems are not taken into account.&#x20;

Measuring can also be difficult in data center located in an office room with no obvious metering opportunity.&#x20;

**Solo Metric**

Data centers reporting their energy efficiency will commonly solely report PUE. This is misleading to the public as it only reports facility efficiency, one of the many areas where efficiency can and should be measured.

{% hint style="danger" %}
Despite its criticism and flaws, PUE was included in EESR due to its prevalence in the field. However, we recommend the community shift from using PUE as a single energy efficiency metric to reporting multiple metrics. TUE provides a better alternative to PUE.&#x20;
{% endhint %}

## Interpretation

The PUE metric can provide the following insight into the data center configuration and operations.

### <mark style="color:red;">High</mark> PUE Value

A <mark style="color:red;">high</mark> PUE value **DOES** indicate that:

* the facility's supporting infrastructure uses a significant amount of energy to support the IT equipment.

A <mark style="color:red;">high</mark> PUE value **DOES NOT** indicate that:

* the IT equipment is inefficient
* the cooling infrastructure is inefficient

### <mark style="color:green;">Low</mark> PUE Value

A <mark style="color:green;">low</mark> PUE value **DOES** indicate that:

* the facility requires significantly little infrastructure energy to support its main IT equipment

A <mark style="color:green;">low</mark> PUE value **DOES NOT** indicate that:

* the data center is _sustainable_
* uses energy efficient equipment and no energy is wasted

## Sources

\[1] [PUE: A COMPREHENSIVE EXAMINATION OF THE METRIC](https://www.thegreengrid.org/en/resources/library-and-tools/20-PUE%3A-A-Comprehensive-Examination-of-the-Metric) [\[pdf\]](https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric\_v6.pdf)

\[2] [A case study and critical assessment in calculating power usage effectiveness for a data centre](https://www.sciencedirect.com/science/article/pii/S0196890413004068?casa\_token=f-EiVfn8zvsAAAAA:mN75A6avLCa-EG781qqHv-OFZEway70cLnm3C2ALu16mLeDe50j5pYeE9gPe7AdF4VktyLyK0ug) [\[pdf\]](https://pdf.sciencedirectassets.com/271098/1-s2.0-S0196890413X0010X/1-s2.0-S0196890413004068/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBcaCXVzLWVhc3QtMSJGMEQCICjqbsd4Y2jSA6ntr3hnla00uqdiz%2BdBybE7MYqiR6yiAiBuXite6bC2Gq9QGsdFeYKwD4GO4TvETBw8J5CqVzBM3irSBAgwEAQaDDA1OTAwMzU0Njg2NSIMZcpCPKukGgwgJKooKq8EJwqoRvOjXjr7gpxdtah47xe48KYEKFohXo5PpSRT3MtsoPwkWzYNxPXV%2Fup77qUpdH0uf8fxvPKh2AiKMxFGy6v%2BneSlJ8jjyWlrz4lnjkQjQFGEvLKkGExsOr99z%2FevkatqZU37ieHLzXVFmeQjfk4FfbHK50lbpUy88tnbQUQbo3yz27r5x4DwoZEGBQYnNInLCDGqGPh4keHKPnMNppBgq5oi8ANqX1aKn0U9wFF4vRNYs7CjfVJAdr9B%2BOvJfbhEA6uZWIT2hTlE704mqyOL%2FAEswdETIYydH5Jo8lUj2pOTEMEzaf%2F46nixkzTXFQMDUR6JETPhVW0ASlIP2%2FRtOUfc5nunEYjrg5D985zxyZfUsQWDYYdILl9fqBKTFgQUcJBopbz1zB57YyVf3Kb1TniZhptgQbMRFkLjLafg43M3J%2BA4mVOKppNFNxFf2VB89rVlgR6OLUREpn%2Fo6bBfGK8HK2PgM1snnc3D07ICe8p3VQBmcWKNexof4KSq4t05swJv1EO8k%2F6ugQ1xEjhrYCiP%2FTgnKVXv48VtFi12SMEDgo8Mv%2B9vwXnm%2FcPA7F1qKTPVrMZwyvtZvXs0AFHrPRs0WfdC5EtWd2CEHfMnAV%2Fy8qxht8mR%2B8IwGpy5TEGyLnQTFvPMlgLc%2BUNJYMfOTpwRYnralKvgasOjJm2deIR7750sQZGvM3c%2FJlPKAt7h9Axu9JrcZKfFc9vH%2FeJo4L49TZ6bG449sprfqDCljsKVBjqqAWKQqow%2BCqjolk7%2FZ7tqd4dxWGe5PsCJEVBiog9Ka%2BPOXEGTX1BkEheDzJYiPnZpTmkzQWGkxt4FmgufC8oFI2%2F1h6Uba3fXa8bQ4h3MRb502yBLNNLj6cEXMr5qQJi8kdGM6ehQBx96LH5nLGmJSOuMBvNYIIhXGGuNjvBNBir1azeniigREPdSWgTnAzZYGLC3YKSfgdRMntF1vYiCyJsNiWaTUXgiXrjb\&X-Amz-Algorithm=AWS4-HMAC-SHA256\&X-Amz-Date=20220620T162349Z\&X-Amz-SignedHeaders=host\&X-Amz-Expires=300\&X-Amz-Credential=ASIAQ3PHCVTYZ2Y5ZLA5%2F20220620%2Fus-east-1%2Fs3%2Faws4\_request\&X-Amz-Signature=2986bdeaffb5712a51972ec0e048b9ee1ef716db61020ed4fea6937c6969e141\&hash=c575c99ac4f613c2dfc1a9975f24f51ed52b2d2012657dc149a0329a747056a4\&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61\&pii=S0196890413004068\&tid=spdf-fa2e1cab-682c-4b10-8398-90516161983b\&sid=2a69fd093762f54f186acfa985e950431ccbgxrqb\&type=client\&ua=4d530753015b0456550b\&rr=71e5d9e44d23b734)

\[3] [Power usage effectiveness in data centers: overloaded and underachieving](https://www.sciencedirect.com/science/article/pii/S1040619016300446?casa\_token=HzCV\_L\_vvtYAAAAA:eHvUvdGIcb3xRSRN7P9ZUzwTJiaJcGQHQMeAm-IrizzQb2M\_xwZDN6HULowT9K6jdfUdGMMKNaE) [\[pdf\]](https://pdf.sciencedirectassets.com/272016/1-s2.0-S1040619016X0005X/1-s2.0-S1040619016300446/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBcaCXVzLWVhc3QtMSJGMEQCICjqbsd4Y2jSA6ntr3hnla00uqdiz%2BdBybE7MYqiR6yiAiBuXite6bC2Gq9QGsdFeYKwD4GO4TvETBw8J5CqVzBM3irSBAgwEAQaDDA1OTAwMzU0Njg2NSIMZcpCPKukGgwgJKooKq8EJwqoRvOjXjr7gpxdtah47xe48KYEKFohXo5PpSRT3MtsoPwkWzYNxPXV%2Fup77qUpdH0uf8fxvPKh2AiKMxFGy6v%2BneSlJ8jjyWlrz4lnjkQjQFGEvLKkGExsOr99z%2FevkatqZU37ieHLzXVFmeQjfk4FfbHK50lbpUy88tnbQUQbo3yz27r5x4DwoZEGBQYnNInLCDGqGPh4keHKPnMNppBgq5oi8ANqX1aKn0U9wFF4vRNYs7CjfVJAdr9B%2BOvJfbhEA6uZWIT2hTlE704mqyOL%2FAEswdETIYydH5Jo8lUj2pOTEMEzaf%2F46nixkzTXFQMDUR6JETPhVW0ASlIP2%2FRtOUfc5nunEYjrg5D985zxyZfUsQWDYYdILl9fqBKTFgQUcJBopbz1zB57YyVf3Kb1TniZhptgQbMRFkLjLafg43M3J%2BA4mVOKppNFNxFf2VB89rVlgR6OLUREpn%2Fo6bBfGK8HK2PgM1snnc3D07ICe8p3VQBmcWKNexof4KSq4t05swJv1EO8k%2F6ugQ1xEjhrYCiP%2FTgnKVXv48VtFi12SMEDgo8Mv%2B9vwXnm%2FcPA7F1qKTPVrMZwyvtZvXs0AFHrPRs0WfdC5EtWd2CEHfMnAV%2Fy8qxht8mR%2B8IwGpy5TEGyLnQTFvPMlgLc%2BUNJYMfOTpwRYnralKvgasOjJm2deIR7750sQZGvM3c%2FJlPKAt7h9Axu9JrcZKfFc9vH%2FeJo4L49TZ6bG449sprfqDCljsKVBjqqAWKQqow%2BCqjolk7%2FZ7tqd4dxWGe5PsCJEVBiog9Ka%2BPOXEGTX1BkEheDzJYiPnZpTmkzQWGkxt4FmgufC8oFI2%2F1h6Uba3fXa8bQ4h3MRb502yBLNNLj6cEXMr5qQJi8kdGM6ehQBx96LH5nLGmJSOuMBvNYIIhXGGuNjvBNBir1azeniigREPdSWgTnAzZYGLC3YKSfgdRMntF1vYiCyJsNiWaTUXgiXrjb\&X-Amz-Algorithm=AWS4-HMAC-SHA256\&X-Amz-Date=20220620T162324Z\&X-Amz-SignedHeaders=host\&X-Amz-Expires=300\&X-Amz-Credential=ASIAQ3PHCVTYZ2Y5ZLA5%2F20220620%2Fus-east-1%2Fs3%2Faws4\_request\&X-Amz-Signature=b5ca352cecd7906f4f30d4c8fd1835fc7042e66b53f4e1c271453f9f60ec99b4\&hash=cb4559383cfd2bbdf12b449893d118c313263796055a9af4e5895ccd98245750\&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61\&pii=S1040619016300446\&tid=spdf-1a08aa59-be6a-4efa-b610-4511ea1f75e9\&sid=2a69fd093762f54f186acfa985e950431ccbgxrqb\&type=client\&ua=4d530753015b555a540d\&rr=71e5d9485bb4b96e)
