# PMEL - Serial Visualizer Requirements

> National Oceanic and Atmospheric Administration <br>
> Pacific Marine Environmental Laboratory <br>
> 7600 Sand Point Way NE <br>
> Bldg 3/EDD <br>
> Seattle, WA 98115 <br>

## Overview
The Serial Visualizer is being developed to meet a common need across the
engineering development division (EDD) and the other divisions within the Pacific
Marine Environmental Laboratory (PMEL).  With the number of serial sensors and devices used on a daily basis within the lab, there is often a need to monitor
the output of these sensor over a serial port.  Often, these serial data streams
are saved as a .csv or .txt fil before being imported into Excel, Matlab or Python.

This project is an attempt to minimize the number of steps to visualize the data
stream by providing a serial connection capable of generating the same visualizations in real-time.  In addition, the program will have the ability to
"playback" the data, as well as zoom in on specific events.


## Requirements
The PMEL Serial Visualizer program:

-----

* **MUST** be capable of two-way serial communication at baud rates up to 115,200
baud.

* **MUST** be capable of parsing up to eight (8) values in a single transmission.

* **MUST** be capable of parsing user selectable character delimiters.

* **MUST** be capable of parsing user selectable line termination character
strings.

* **MUST** be capable of displaying up to eight (8) data streams on plot
concurrently.

* **MUST** have the ability to poll a sensor with a common string.

* **MUST** be capable of saving received data in .txt, .csv, or other common data formats.

* **MUST** be capable of "playback" function for captured data.

* **MUST** be capable of zoom on data function.

* **MUST** have console ability (both tx and rx)

-----

* **SHOULD** be capable of generating up to eight (8) individual plots.

* **SHOULD** be capable of parsing complex messages.

* **SHOULD** be capable of "triggering" off of selected events.


-----
