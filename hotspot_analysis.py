# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HotspotAnalysis
                                 A QGIS plugin
 This plugin implements the statistics needed for the Hotspot Analysis
                             -------------------
        begin                : 2017-02-22
        copyright            : (C) 2017 by Daniele Oxoli, Gabriele Prestifilippo, Mayra Zurbaràn, Stanly Shaji / Politecnico Di Milano
        email                : daniele.oxoli@polimi.it
        git sha              : $Format:%H$
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from __future__ import absolute_import
from builtins import str
from builtins import range
from builtins import object
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QComboBox, QFrame, QLineEdit, QMessageBox
from qgis.PyQt.QtGui import QIcon
#from qgis.core import QgsMapLayerRegistry, QgsVectorLayer (not working)
from qgis.core import *

# Initialize Qt resources from file resources.py
from . import resources
# Import the code for the dialog
from .hotspot_analysis_dialog import HotspotAnalysisDialog
import os.path

import pysal
from pysal.esda.getisord import *
from pysal.esda.moran import *
from pysal.weights.Distance import DistanceBand
# from pysal.weights.util import get_points_array_from_shapefile
import numpy
import sys

from osgeo import ogr, gdal

type = 0  # geometry type: 1 point, 3 polygon


class NullWriter(object):
    def write(self, value): pass


sys.stdout = sys.stderr = NullWriter()


def pr(self, msg):
    QMessageBox.information(self.iface.mainWindow(), "Debug", msg)


class HotspotAnalysis(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'HotspotAnalysis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = HotspotAnalysisDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Hotspot Analysis')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'HotspotAnalysis')
        self.toolbar.setObjectName(u'HotspotAnalysis')
        # Load output directory path
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)
        self.clear_ui()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('HotspotAnalysis', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/HotspotAnalysis/hotspot.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Hotspot Analysis'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Hotspot Analysis'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_output_file(self):
        """Selects the output file directory"""
        filename, __ = QFileDialog.getSaveFileName(self.dlg, "Select output path directory ")
        self.dlg.lineEdit.setText(filename)

    def optimizedThreshold(self, checked):
        """Settings for Optimized threshold"""
        if checked == True:
            self.dlg.lineEdit_minT.setEnabled(True)
            self.dlg.lineEdit_maxT.setEnabled(True)
            self.dlg.lineEdit_dist.setEnabled(True)
            self.dlg.lineEditThreshold.setEnabled(False)
            self.dlg.lineEditThreshold.clear()
            self.dlg.label_threshold.setEnabled(False)
            self.dlg.label_7.setEnabled(True)
            self.dlg.label_8.setEnabled(True)
            self.dlg.label_9.setEnabled(True)

        else:
            self.dlg.lineEdit_minT.setEnabled(False)
            self.dlg.lineEdit_minT.clear()
            self.dlg.lineEdit_maxT.clear()
            self.dlg.lineEdit_dist.clear()
            self.dlg.lineEdit_maxT.setEnabled(False)
            self.dlg.lineEdit_dist.setEnabled(False)
            self.dlg.lineEditThreshold.setEnabled(True)
            self.dlg.label_threshold.setEnabled(True)
            self.dlg.label_7.setEnabled(False)
            self.dlg.label_8.setEnabled(False)
            self.dlg.label_9.setEnabled(False)

    def randomPermChecked(self, checked):
        """Settings for Random permutations"""
        if checked == True:
            self.dlg.lineEdit_random.setEnabled(True)
        else:
            self.dlg.lineEdit_random.setEnabled(False)

    def moranBiChecked(self, checked):
        if checked == True:
            self.dlg.comboBox_C_2.setEnabled(True)
        else:
            self.dlg.comboBox_C_2.setEnabled(False)

    def knnChecked(self, checked):
        if checked == True:
            self.dlg.lineEditThreshold.clear()
            self.dlg.lineEditThreshold.setEnabled(False)
            self.dlg.knn_number.setEnabled(True)
        else:
            self.dlg.lineEditThreshold.setEnabled(True)

    def clear_ui(self):
        """Clearing the UI for new operations"""
        self.dlg.comboBox.clear()
        self.dlg.lineEdit.clear()
        self.dlg.lineEditThreshold.clear()
        self.dlg.comboBox_C.clear()
        self.dlg.comboBox_C_2.clear()
        self.dlg.comboBox_C_2.setEnabled(False)
        self.dlg.lineEditThreshold.setEnabled(True)
        self.dlg.checkBox_optimizeDistance.setChecked(False)
        self.dlg.checkBox_rowStandard.setChecked(False)
        self.dlg.checkBox_randomPerm.setChecked(False)
        self.dlg.checkBox_queen.setChecked(False)
        self.dlg.checkBox_queen.setEnabled(False)
        self.dlg.lineEdit_minT.setEnabled(False)
        self.dlg.lineEdit_maxT.setEnabled(False)
        self.dlg.lineEdit_dist.setEnabled(False)
        self.dlg.lineEdit_minT.clear()
        self.dlg.lineEdit_maxT.clear()
        self.dlg.lineEdit_dist.clear()
        self.dlg.lineEditThreshold.clear()
        self.dlg.label_7.setEnabled(False)
        self.dlg.label_8.setEnabled(False)
        self.dlg.label_9.setEnabled(False)
        self.dlg.knn_number.setEnabled(False)
        self.dlg.checkBox_knn.setChecked(False)
        self.dlg.checkBox_knn.setEnabled(True)
        self.load_comboBox()

    def clear_fields(self):
        """Clearing the fields when layers are changed"""
        self.dlg.comboBox_C.clear()
        self.dlg.comboBox_C_2.clear()

    def write_file(self, filename, statistics, layerName, inLayer, inDataSource, y, threshold1):
        """Writing the output shapefile into the mentioned directory"""
        outDriver = ogr.GetDriverByName("ESRI Shapefile")

        layerName = layerName.split('.')
        layerName.pop()
        # layerName = '.'.join(layerName)

        outShapefile = filename + ".shp"

        # Remove eventually alrady exisiting output
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)

        # Create the output shapefile
        outDataSource = outDriver.CreateDataSource(outShapefile)
        outLayer = outDataSource.CreateLayer("output", inLayer.GetSpatialRef(), inLayer.GetLayerDefn().GetGeomType())

        # Add input Layer Fields to the output Layer
        inLayerDefn = inLayer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)

        ##
        # Add additional fields - for more types other than Strings take a look at http://pcjericks.github.io/py-gdalogr-cookbook/layers.html#create-a-new-shapefile-and-add-data
        ##

        # Add empty field to store Pysal results
        Z_field = ogr.FieldDefn("Z-score", ogr.OFTReal)
        Z_field.SetWidth(15)
        Z_field.SetPrecision(10)
        outLayer.CreateField(Z_field)

        p_field = ogr.FieldDefn("p-value", ogr.OFTReal)
        p_field.SetWidth(15)
        p_field.SetPrecision(10)
        outLayer.CreateField(p_field)

        # if not Gi*
        if (self.dlg.checkBox_moran.isChecked() == 1 or self.dlg.checkBox_moranBi.isChecked() == 1):
            intValue = int(ogr.OFTReal)
            q_field = ogr.FieldDefn("q-value", intValue)
            q_field.SetWidth(15)
            q_field.SetPrecision(10)
            outLayer.CreateField(q_field)

        # Get the output Layer's Feature Definition
        outLayerDefn = outLayer.GetLayerDefn()
        # Get the input Layer's Feature Definition
        inLayerDefn = inLayer.GetLayerDefn()

        # Add features to the ouput Layer
        for i in range(0, inLayer.GetFeatureCount()):
            # Get the input Feature
            inFeature = inLayer.GetFeature(i)
            # Create output Feature
            outFeature = ogr.Feature(outLayerDefn)
            # Add field values from input Layer
            for j in range(0, inLayerDefn.GetFieldCount()):
                outFeature.SetField(outLayerDefn.GetFieldDefn(j).GetNameRef(), inFeature.GetField(j))
            # Set geometry
            geom = inFeature.GetGeometryRef()
            outFeature.SetGeometry(geom)

            if self.dlg.checkBox_gi.isChecked() == 1:
                # Add Z-scores and p-values to their field column
                if self.dlg.checkBox_randomPerm.isChecked() == 1:  # to use permutation approach
                    if min(y) >= 0:
                        outFeature.SetField("Z-score", statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_z_sim[i] * 2)
                    else:
                        outFeature.SetField("Z-score", -statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_z_sim[i] * 2)

                else:  # to use normality hypothesis

                    if min(y) >= 0:
                        outFeature.SetField("Z-score", statistics.Zs[i])
                        outFeature.SetField("p-value", statistics.p_norm[i] * 2)
                    else:
                        outFeature.SetField("Z-score", -statistics.Zs[i])
                        outFeature.SetField("p-value", statistics.p_norm[i] * 2)

            else:

                if self.dlg.checkBox_randomPerm.isChecked() == 1:  # to use permutation approach
                    if min(y) >= 0:
                        outFeature.SetField("Z-score", statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_sim[i] * 2)
                    else:
                        outFeature.SetField("Z-score", -statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_sim[i] * 2)

                else:  # to use normality hypothesis

                    if min(y) >= 0:
                        outFeature.SetField("Z-score", statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_z_sim[i] * 2)
                    else:
                        outFeature.SetField("Z-score", -statistics.z_sim[i])
                        outFeature.SetField("p-value", statistics.p_z_sim[i] * 2)
                outFeature.SetField("q-value", statistics.q[i])

            # Add new feature to output Layer
            outLayer.CreateFeature(outFeature)

        # Close DataSources
        inDataSource.Destroy()
        outDataSource.Destroy()
        if threshold1:
            self.success_msg(threshold1)
        new_layer = self.iface.addVectorLayer(filename + ".shp", str(os.path.basename(os.path.normpath(filename))),
                                              "ogr")
        if not new_layer:
            QMessageBox.information(self.dlg, self.tr("New Layer"), self.tr("Layer Cannot be Loaded"), QMessageBox.Ok)
        self.clear_ui()

    def load_comboBox(self):
        """Load the fields into combobox when layers are changed"""

        layer_shp = []
        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        if len(layers) != 0:  # checklayers exist in the project
            for layer in layers:
                if hasattr(layer, "dataProvider"):  # to not consider Openlayers basemaps in the layer list
                    myfilepath = layer.dataProvider().dataSourceUri()  # directory including filename
                    (myDirectory, nameFile) = os.path.split(myfilepath)  # splitting into directory and filename
                    if (".shp" in nameFile):
                        layer_shp.append(layer)

        selectedLayerIndex = self.dlg.comboBox.currentIndex()

        if selectedLayerIndex < 0 or selectedLayerIndex > len(layer_shp):
            return
        try:
            selectedLayer = layer_shp[selectedLayerIndex]
        except:
            return

        fieldnames = [field.name() for field in selectedLayer.fields()]

        self.clear_fields()
        self.dlg.comboBox_C.addItems(fieldnames)
        self.dlg.comboBox_C_2.addItems(fieldnames)
        (path, layer_id) = selectedLayer.dataProvider().dataSourceUri().split('|')

        inDriver = ogr.GetDriverByName("ESRI Shapefile")
        inDataSource = inDriver.Open(path, 0)
        inLayer = inDataSource.GetLayer()
        global type
        type = inLayer.GetLayerDefn().GetGeomType()

        if type == 3:  # is a polygon
            self.dlg.checkBox_queen.setChecked(True)
            self.dlg.lineEditThreshold.setEnabled(False)
            self.dlg.checkBox_knn.setEnabled(False)
            self.dlg.knn_number.setEnabled(False)
            self.dlg.checkBox_optimizeDistance.setChecked(False)
            self.dlg.checkBox_optimizeDistance.setEnabled(False)
            self.dlg.lineEdit_minT.setEnabled(False)
            self.dlg.lineEdit_maxT.setEnabled(False)
            self.dlg.lineEdit_dist.setEnabled(False)

        else:
            self.dlg.checkBox_queen.setChecked(False)
            self.dlg.checkBox_knn.setEnabled(True)
            self.dlg.knn_number.setEnabled(True)
            self.dlg.lineEditThreshold.setEnabled(True)
            self.dlg.checkBox_optimizeDistance.setEnabled(True)
            self.dlg.lineEdit_minT.setEnabled(True)
            self.dlg.lineEdit_dist.setEnabled(True)
            self.dlg.lineEdit_maxT.setEnabled(True)
            thresh = pysal.min_threshold_dist_from_shapefile(path)
            self.dlg.lineEditThreshold.setText(str(int(thresh)))

    def error_msg(self):
        """Message to report missing fields"""
        self.clear_ui()
        self.loadLayerList()
        QMessageBox.warning(self.dlg.show(), self.tr("HotspotAnalysis:Warning"),
                            self.tr("Please specify input fields properly"), QMessageBox.Ok)

    def success_msg(self, distance):
        """Message to report succesful file creation"""
        QMessageBox.information(self.dlg, self.tr("HotspotAnalysis:Success"),
                                self.tr("File is generated Succesfully (Distance used = " + str(distance) + ")"),
                                QMessageBox.Ok)

    def validator(self):
        """Validator to Check whether the inputs are given properly"""

        # Polygon case
        if self.dlg.checkBox_queen.isChecked() == 1:
            return 1

        if ((self.dlg.checkBox_optimizeDistance.isChecked() == 0
             and self.dlg.lineEditThreshold.text() != "")
            or (self.dlg.checkBox_optimizeDistance.isChecked() == 1
                and (self.dlg.lineEdit_dist.text() != ""
                     and self.dlg.lineEdit_maxT.text() != ""
                     and self.dlg.lineEdit_minT.text() != "")) or
                (self.dlg.checkBox_knn.isChecked() == 1)) \
                and self.dlg.lineEdit.text() != "":
            return 1
        else:
            return 0

    def loadLayerList(self):
        layers_list = []
        layers_shp = []
        # Show the shapefiles in the ComboBox
        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        if len(layers) != 0:  # checklayers exist in the project
            for layer in layers:
                if hasattr(layer, "dataProvider"):  # to not consider Openlayers basemaps in the layer list
                    myfilepath = layer.dataProvider().dataSourceUri()  # directory including filename
                    (myDirectory, nameFile) = os.path.split(myfilepath)  # splitting into directory and filename
                    if (".shp" in nameFile):
                        layers_list.append(layer.name())
                        layers_shp.append(layer)
            self.dlg.comboBox.addItems(layers_list)  # adding layers to comboBox
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            if selectedLayerIndex < 0 or selectedLayerIndex > len(layers_shp):
                return
            selectedLayer = layers_shp[selectedLayerIndex]
            fieldnames = [field.name() for field in selectedLayer.fields()]  # fetching fieldnames of layer
            self.clear_fields()
            self.dlg.comboBox_C.addItems(fieldnames)
            self.dlg.comboBox_C_2.addItems(fieldnames)
            try:
                self.dlg.comboBox.activated.connect(lambda: self.load_comboBox())
                self.dlg.comboBox.currentIndexChanged.connect(lambda: self.load_comboBox())
                self.dlg.checkBox_optimizeDistance.toggled.connect(self.optimizedThreshold)  # checkbox toggle event
                self.dlg.checkBox_randomPerm.toggled.connect(self.randomPermChecked)  # checkbox toggle event
                self.dlg.checkBox_moranBi.toggled.connect(self.moranBiChecked)  # checkbox toggle event
                self.dlg.checkBox_knn.toggled.connect(self.knnChecked)  # checkbox toggle event
            except:
                return False
            return [layers, layers_shp]
        else:
            return [layers, False]

    def run(self):
        """Run method that performs all the real work"""  # show the dialog

        self.clear_ui()
        layers, layers_shp = self.loadLayerList()
        if len(layers) == 0:
            return

        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed and fields are not empty
        if result and (self.validator() == 1):
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            if selectedLayerIndex < 0 or selectedLayerIndex > len(layers):
                return
            selectedLayer = layers_shp[selectedLayerIndex]
            layerName = selectedLayer.dataProvider().dataSourceUri()
            C = selectedLayer.fieldNameIndex(self.dlg.comboBox_C.currentText())
            C2 = selectedLayer.fieldNameIndex(self.dlg.comboBox_C_2.currentText())
            filename = self.dlg.lineEdit.text()
            (path, layer_id) = layerName.split('|')
            inDriver = ogr.GetDriverByName("ESRI Shapefile")
            inDataSource = inDriver.Open(path, 0)
            inLayer = inDataSource.GetLayer()
            type = inLayer.GetLayerDefn().GetGeomType()
            u = []
            for i in range(0, inLayer.GetFeatureCount()):
                geometry = inLayer.GetFeature(i)
                u.append(geometry.GetField(C))

            y = numpy.array(u)  # attributes vector

            if self.dlg.checkBox_moranBi.isChecked() == 1:
                v = []
                for i in range(0, inLayer.GetFeatureCount()):
                    geometry = inLayer.GetFeature(i)
                    v.append(geometry.GetField(C2))
                x = numpy.array(v)

            if type == 1:  # point
                t = ()
                for feature in inLayer:
                    geometry = feature.GetGeometryRef()
                    xy = (geometry.GetX(), geometry.GetY())
                    t = t + (xy,)
                    # t = get_points_array_from_shapefile(layerName.split("|")[0])
                if self.dlg.lineEditThreshold.text() and self.dlg.lineEditThreshold.text() != "":  # if threshold is given
                    threshold1 = int(self.dlg.lineEditThreshold.text())
                elif self.dlg.checkBox_knn.isChecked() == 0:  # if user needs to optimize threshold (no knn)
                    mx_moran = -1000.0
                    mx_i = -1000.0
                    minT = int(self.dlg.lineEdit_minT.text())
                    maxT = int(self.dlg.lineEdit_maxT.text())
                    dist = int(self.dlg.lineEdit_dist.text())
                    for i in range(minT, maxT + dist, dist):
                        w = DistanceBand(t, threshold=i, p=2, binary=False)
                        moran = pysal.Moran(y, w)
                        # print moran.z_norm
                        if moran.z_norm > mx_moran:
                            mx_i = i
                            mx_moran = moran.z_norm
                    threshold1 = int(mx_i)
                if self.dlg.checkBox_knn.isChecked() == 1:
                    weightValue = int(self.dlg.knn_number.text())
                    w = pysal.knnW_from_shapefile(layerName.split("|")[0], k=weightValue, p=1)
                    threshold1 = "None / KNN used - K = " + self.dlg.knn_number.text()
                else:
                    w = DistanceBand(t, threshold1, p=2, binary=False)
            else:  # polygon
                w = pysal.queen_from_shapefile(layerName.split("|")[0])
                threshold1 = "None / Queen's Case used"
            if self.dlg.checkBox_rowStandard.isChecked() == 1:
                type_w = "R"
            else:
                type_w = "B"

            if self.dlg.checkBox_randomPerm.isChecked() == 1:
                permutationsValue = int(self.dlg.lineEdit_random.text())
            else:
                permutationsValue = 999

            numpy.random.seed(12345)
            if self.dlg.checkBox_gi.isChecked() == 1:
                statistics = G_Local(y, w, star=True, transform=type_w, permutations=permutationsValue)
            elif self.dlg.checkBox_moran.isChecked() == 1:
                statistics = Moran_Local(y, w, transformation=type_w, permutations=permutationsValue)
            else:
                statistics = Moran_Local_BV(y, x, w, transformation=type_w, permutations=permutationsValue)

            self.write_file(filename, statistics, layerName, inLayer,
                            inDataSource,
                            y, threshold1)
            # assign the style to the output layer on QGIS
            if self.dlg.checkBox_gi.isChecked() == 1:
                if type == 1:  # point
                    stylePath = "/layer_style/hotspots_class.qml"
                else:
                    stylePath = "/layer_style/hotspots_class_poly.qml"
                self.iface.activeLayer().loadNamedStyle(os.path.dirname(__file__) + stylePath)
            else:
                if type == 1:  # point
                    stylePath = "/layer_style/moran_class.qml"
                else:
                    stylePath = "/layer_style/moran_class_poly.qml"
                self.iface.activeLayer().loadNamedStyle(os.path.dirname(__file__) + stylePath)

        elif result and (self.validator() == 0):
            self.error_msg()
        else:
            self.clear_ui()
        pass
