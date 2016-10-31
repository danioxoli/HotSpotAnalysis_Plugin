# Hotspot Analysis Plugin for QGIS

A QGIS Plugin to perform Hotspot analysis based on the Python Spatial Analysis Library - [PySAL]. 

The Hotspot analysis plugin associate the **Z-scores** and **p-values** (under Complete Spatial Randomness) of the Gi* local statistic ([Getis and Ord, 1992]) for each feature of a points shapefile, characterized by **X,Y projected coordinates** and an associated **numerical attribute**. Output layer enables to indentify hotspots (or coldspots) in the input dataset as well as their statistical significance. 

Positive and statistically significant Z-score indicates intense cluster of high values (hotspot). Negative and statistically significant Z-score indicates intense cluster of low values (coldspot).

Spatial relation between features is modeled using a Fixed Distance Band (expressed with the same unit of measure of the projected coordinate system of the input shapefile), which allows to compute Gi* for any point by considering its neighborhoods within this fixed distance. For more information, please refer to: [Geospatial Analysis - 5th Edition, 2015 - de Smith, Goodchild, Longley]

Dependency Requirements:

  - **`PySAL`**
  - **`Numpy`**
  - **`Scipy`**

These libraries are not included in the QGIS core libraries and must be installed prior to the use of the plugin through the [OSGeo4W Shell] on **Windows**, or through terminal on **Ubuntu**. 
___
### Installation - Windows OS

Download `get-pip.py` ,to enable `PIP` functionalities, which is available at this link: <https://bootstrap.pypa.io/get-pip.py> 

Open `OSGeo4W Shell` as `Administrator` and change the working directory where the `get-pip.py` file is stored and type :
```sh
 $ python get-pip.py
```
(Further information regarding `PIP` installation can be found in:
https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel)

Download the following packages according to your Python version and your Operating System characteristics:
 
 `Numpy` : https://pypi.anaconda.org/carlkl/simple/numpy/ 

 `Scipy` : https://pypi.anaconda.org/carlkl/simple/scipy/ 
 
**Note**: for example, in the filename "numpy-1.10.0b1-cp34-none-win_amd64.whl " cp34, amd64 depicts python 3.4 and 64 bit Operating System

Change the directory to where the downloaded packages are stored and type the following commands:

```sh
 $ pip install numpypackagename
 $ pip install scipypackagename
```
**Note**: extension must be included with the filename
```sh
 $ pip install pysal
```

Download or clone the `Github` repository given below into QGIS Python Plugins folder.
https://github.com/stanly3690/HotSpotAnalysis_Plugin 

**Note**: default Plugins folder is:
```sh
 $ cd C:\Users\<your_user_name>\.qgis2\python\plugins
``` 
Open QGIS:

Go to `Plugins` -> `Manage and Install plugins` -> `Settings` -> `Show also experimental plugins` 

In `All plugins` tab, look for `HotSpotAnalysis` and tick the checkbox.  
A new icon for Hotspot analyis will appear on the QGIS main panel.
___
### Installation - Ubuntu

Open a **Terminal** and type the commands:
```sh
 $ sudo apt-get install python-numpy
 $ sudo apt-get install python-scipy 
```
To install **PySAL**:
```sh
 $ sudo pip install pysal
```
Change directory to QGIS Plugins directory, default is : 
```sh
 $ cd /usr/share/qgis/python/plugins 
``` 
Clone the `GitHub` repository into the earlier mentioned path:
```sh
 $  sudo git clone https://github.com/stanly3690/HotSpotAnalysis_Plugin 
```
Then Open QGIS:

Go to `Plugins` -> `Manage and Install plugins` -> `Settings` -> `Show also experimental plugins` 

In `All plugins` tab, look for `HotSpotAnalysis` and tick the Checkbox.  
A new icon for Hotspot analyis will appear on the QGIS main panel.
___

An example of plugin application is available here: https://peerj.com/preprints/2204/

**Note**: this paper is based on the **old version of the plugin**! 

The current version **does not require Pyshp as well as to specify the feature coordinates as two separate fields in the attribute table** of the input shapefile. Only the numerical attribute must be included and selected using the graphical interface on QGIS. Nevertheless, be sure that your input shapefile is projected. The unit of measure in which you express the analysis distance must agree with the one of the projected coordinate system of your input layer. 
With this new version, the output layer is displayed with an **automatic style** which enable Hotspot and Coldspot visualization.

A demo exercise with the new plugin version here: (_file under construction, contact the author for any issue_)
___
Bug tracker and Wiki

##### License

_HotSpotAnalysis-plugin is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version_

Copyright © 2016 Stanly Shaji/ ArunKumar Muthusamy/ Daniele Oxoli/ Mayra Zurbaràn - Politecnico Di Milano.

E-mail: daniele.oxoli@polimi.it

 [PySAL]: <http://pysal.readthedocs.io/en/v1.11.0/#>
 [Getis and Ord, 1992]: <http://onlinelibrary.wiley.com/doi/10.1111/j.1538-4632.1992.tb00261.x/full>
 [Geospatial Analysis - 5th Edition, 2015 - de Smith, Goodchild, Longley]: <http://www.spatialanalysisonline.com/HTML/index.html?local_indicators_of_spatial_as.htm>
 [OSGeo4W Shell]:<http://trac.osgeo.org/osgeo4w/>
