# Hotspot Analysis Plugin for QGIS2

A QGIS Plugin to perform Hotspot analysis based on the Python Spatial Analysis Library - [PySAL]. 

**NB: QGIS3 version of the plugin is available at:** https://github.com/danioxoli/HotSpotAnalysis_Plugin/tree/qgis3
**THIS PLUGIN VERSION IS NOT MORE MANTAINED

The Hotspot analysis plugin associates the **Z-scores** and **p-values** (under Complete Spatial Randomness hypothesis) of the Gi* local statistic ([Getis and Ord, 1992]; [Getis and Ord, 1996]), Anselin Local Moran's I ([Anselin, 1995]) and Local Moran Bivariate ([Wartenberg, 1985]; [Anselin et al., 2002]) for each feature of a shapefile, with an assigned **projected coordinate system** and (at least) an associated **numerical attribute**. Output layer allows to indentify hotspots (or coldspots) in the input dataset as well as their statistical significance. 

For what it concerns Gi* local statistic, positive and statistically significant Z-score indicates intense cluster of high values (hotspot). Negative and statistically significant Z-score indicates intense cluster of low values (coldspot). 
With respect to the Local Moran's I (and its bivariate counterpart, the Local Moran Bivariate), Z-scores are translated into quadrant values (q) which depict presence of Clusters or Outliers within the dataset. Significance is computed, based on user's choice, against normality assumption (default) or using conditional permutations approach. 
Please consider the aforementioned litterature for detailed information.

Spatial relation between point features is modeled using a Fixed Distance Band (expressed with the same unit of measure of the projected coordinate system of the input point shapefile) or optionally using the K-nearest neighboor approach. For polygon shapefile analysis, the spatial relation is modeled using queen's case contiguity matrix. For more information, please refer to: [Geospatial Analysis - 5th Edition, 2015 - de Smith, Goodchild, Longley]

Dependency Requirements:

  - **`PySAL`**
  - **`Numpy`**
  - **`Scipy`**
  
These libraries are not included in the QGIS core libraries and must be installed prior to the use of the plugin through the [OSGeo4W Shell] on **Windows**, or through terminal on **Ubuntu** and **macOS** (see the following).

**Note**:_If you are using the [OSGeo-Live] Virtual Machine, you do not need to install any dependency. You can simply install the plugin from the offcial **QGIS Python Plugins Repository**. Depending on the pre-installed Pysal version, some of the functionalities might not be available_
___
### Installation - Windows OS

**1)** Open `OSGeo4W Shell` as `Administrator` and type:
```sh
 $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
 $ python get-pip.py
```
#### Alternatively (1):

Download `get-pip.py` , to enable `PIP` functionalities, which is available at this link: <https://bootstrap.pypa.io/get-pip.py> 

Open `OSGeo4W Shell` as `Administrator` and change the working directory where the `get-pip.py` file is stored and type:
```sh
 $ python get-pip.py
```
Further information regarding `PIP` installation can be found in:
- https://trac.osgeo.org/osgeo4w/wiki/ExternalPythonPackages 
- https://packaging.python.org/en/latest/installing/#install-pip-setuptools-and-wheel

**2)** Download the following packages according to your Python version and your Operating System characteristics:
 
 `Numpy` : https://pypi.anaconda.org/carlkl/simple/numpy/ 

 `Scipy` : https://pypi.anaconda.org/carlkl/simple/scipy/ 
 
**Note**: _Default Python version for `OSGeo4W Shell` is 2.7, select the correct packages accordling to your Operating System, for example: the filename "numpy-1.10.0b1-cp27-none-win_amd64.whl" cp27, amd64 depicts python 2.7 and 64 bit Operating System_

Change the directory to where the downloaded packages are stored and type the following commands:

```sh
 $ pip install numpypackagename
 $ pip install scipypackagename
```
**Note**: extension must be included with the filename
```sh
 $ pip install pysal
```

#### Alternatively (2):

If the pysal installation with **pip** generates errors you can try with manual installation as follows: 

a) Download the compressed **pysal** package at this link

https://pypi.python.org/packages/e7/3b/af87cd60f03734897caa6dc3e840fc10458d0a2c060b3d71803dc56992db/PySAL-1.13.0.tar.gz

The QGIS Python packages are store in this floder:
```sh
 $ C:\PROGRA~1\QGIS2~1.14\apps\Python27\lib\site-packages
``` 
**Note**:  ...\QGIS2~1.14\... has to be changed according to your QGIS version

b) Remove the existing folder containing **pysal**. Then, unzip the package you have downloaded; inside the uncompressed folder you will find a sub-folder called **pysal**. Copy it into the early mentioned path.

**3)** Open QGIS:

Go to `Plugins` -> `Manage and Install plugins` -> `Settings` -> `Show also experimental plugins` 

In `All plugins` tab, look for `Hotspot Analysis` and tick the checkbox.  
A new icon for Hotspot Analysis will appear on the QGIS main panel and in the Vector Menu.

**4)** If you are interested in the **latest unreleased version**:

**Download or clone** the `GitHub` repository given below into QGIS Python Plugins folder:
https://github.com/danioxoli/HotSpotAnalysis_Plugin/archive/master.zip

**Note**: default Plugins folder is:
```sh
 $ cd C:\Users\<your_user_name>\.qgis2\python\plugins
``` 
___
### Installation - Ubuntu

**1)** Open a **Terminal** and type the commands:
```sh
 $ sudo apt-get install python-numpy
 $ sudo apt-get install python-scipy 
```
To install **PySAL**:
```sh
 $ sudo pip install pysal
```

**2)** Open QGIS:

Go to `Plugins` -> `Manage and Install plugins` -> `Settings` -> `Show also experimental plugins` 

In `All plugins` tab, look for `Hotspot Analysis` and tick the Checkbox.  
A new icon for Hotspot Analysis will appear on the QGIS main panel and in the Vector Menu.

**3)** If you are interested in the **latest unreleased version**:

Open a **Terminal** and change directory to QGIS Plugins directory, default is: 
```sh
 $ cd /usr/share/qgis/python/plugins 
``` 
**Clone** the `GitHub` repository into the earlier mentioned path:
```sh
 $  sudo git clone https://github.com/danioxoli/HotSpotAnalysis_Plugin
```

___
### Installation - macOS

**1)** Install dependencies:

If you installed QGIS on your machine using this source : http://www.kyngchaos.com/software/qgis , you would find the required dependencies (**Numpy - Scipy - Pysal**) in the list of the **Optional Python Modules**. You can install them directly from here: http://www.kyngchaos.com/software/python 

Alternatively:

Open a **Terminal** and type the commands:
```sh
 $ sudo pip install numpy
 $ sudo pip install scipy 
 $ sudo easy_install pysal
```

**2)** Open QGIS:

Go to `Plugins` -> `Manage and Install plugins` -> `Settings` -> `Show also experimental plugins` 

In `All plugins` tab, look for `Hotspot Analysis` and tick the Checkbox.  
A new icon for Hotspot Analysis will appear on the QGIS main panel and in the Vector Menu.

**3)** If you are interested in the **latest unreleased version**:

Change directory to QGIS Plugins directory, default is: 
```sh
 $ cd ~/.qgis2/python/plugins
``` 
Open the folder:
```sh
 $ open . 
``` 
**Download and copy** here the unzipped repository folder:
https://github.com/danioxoli/HotSpotAnalysis_Plugin/archive/master.zip

or **Clone** the `GitHub` repository into the earlier mentioned path:
```sh
 $  sudo git clone https://github.com/danioxoli/HotSpotAnalysis_Plugin
```

___

### Additional Material 

An user guide with demo exercises is included here: https://github.com/danioxoli/HotSpotAnalysis_Plugin/blob/master/test_data/Hotspot_Analysis_UserGuide.pdf

Plese cite this as: 

_Oxoli, D., Prestifilippo, G., Bertocchi, D., Zurbaràn, M. (2017). Enabling spatial autocorrelation mapping  in QGIS: The Hotspot Analysis Plugin. GEAM. GEOINGEGNERIA AMBIENTALE E MINERARIA, 151(2), 45-50._

Latest presentation available here: http://www.slideshare.net/danieleoxoli/hotspot-analysis-with-qgis-foss4git-2017

**Note**: part of this material might be based on the **old version of the plugin**! 

___

### Changeset

##### Changeset 06/2017
- Enabled the use of k-nearest neighbor spatial weights matrix for point shapefiles
- Minor bugs fixed

##### Changeset 03/2017
- Enabled Anselin Local Moran's I and Bivariate Local Moran computation
- Minor bugs fixed

##### Changeset 02/2017
- The plugin has been **officially published** on the QGIS plugin repository
- Minor bugs fixed

##### Changeset 01/2017
- Enabled the use of negative numerical attributes [Getis and Ord, 1996] 
- Enabled polygon shapefiles as input using queen's case contiguity spatial weight matrix. 
- Enabled the possibility of selecting between normality assumption (default) and standard normal approximation from permutations to compute Gi* Z-scores and associated p-values. 

##### Changeset 12/2016
New check botton to eneable the usage of **row standardized** spatial weights

##### Changeset 11/2016
With this new version, the output layer is displayed with an **automatic style** which enables hotspot and coldspot visualization. Moreover, a **default Fixed Distance Band** is dispalyed. This latter represents the minimum distance to ensure 
at least 1 neighbor to any element of the dataset in order to compute spatial weights for Gi* 

##### Changeset 10/2016
The current version does not require Pyshp as well as to specify the feature coordinates as two separate fields in the attribute table of the input shapefile. Only the numerical attribute must be included and selected using the graphical interface on QGIS. Nevertheless, be sure that your input shapefile is projected. The unit of measure in which you express the analysis distance must agree with the one of the projected coordinate system of your input layer. 

___
### Future work

 - Test on the new functionalities addedd
 - improve GUI appereance
 - Update User guide and documentation for Anselin Local Moran's I and Bivariate Local Moran computation
 - Create a new branch of the sotware without external Python dependnecies
 
___

Bug tracker and Wiki

##### License

_The Hotspot Analysis plugin is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation_

Copyright © 2017 Daniele Oxoli/ Mayra Zurbaràn/ Gabriele Prestifilippo/ Stanly Shaji - Politecnico Di Milano.

E-mail: daniele.oxoli@polimi.it

 [PySAL]: <http://pysal.readthedocs.io/en/v1.11.0/#>
 [Getis and Ord, 1992]: <http://onlinelibrary.wiley.com/doi/10.1111/j.1538-4632.1992.tb00261.x/full>
 [Geospatial Analysis - 5th Edition, 2015 - de Smith, Goodchild, Longley]: <http://www.spatialanalysisonline.com/HTML/index.html?local_indicators_of_spatial_as.htm>
 [OSGeo4W Shell]:<http://trac.osgeo.org/osgeo4w/>
 [OSGeo-Live]:<https://live.osgeo.org>
 [Getis and Ord, 1996]: <http://onlinelibrary.wiley.com/doi/10.1111/j.1538-4632.1995.tb00912.x/pdf>
 [Anselin, 1995]: <http://onlinelibrary.wiley.com/store/10.1111/j.1538-4632.1995.tb00338.x/asset/j.1538-4632.1995.tb00338.x.pdf;jsessionid=A8B95BCA3E3DAFED243732CC66B31B63.f02t01?v=1&t=j0hvb8t7&s=c3f30861dca953c035e5b1dbbc24ea6b659a82c5>
 [Wartenberg, 1985]:<http://onlinelibrary.wiley.com/store/10.1111/j.1538-4632.1985.tb00849.x/asset/j.1538-4632.1985.tb00849.x.pdf?v=1&t=j0uyit1b&s=7ad70b665f08164ec74068d58eedf6f65e072dfa>
 [Anselin et al., 2002]:<https://pdfs.semanticscholar.org/4e34/bd70317377971ba8df7259288b972ad6a239.pdf>
