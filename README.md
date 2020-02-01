# Numerical Digitize 3

Plugin for QGIS for creating or editing features by adding or changing
coordinates of node points.
**Warning - It's first release of plugin with bugs. Use it on you own risk.**

![Common image](images/readme.png)

## Installation

### Prerequisite

* QGIS version 3.4 or later

### Install via plugin repository in QGIS

1. In QGIS, navigate to menu **Plugins** > **Manage and Install Plugins...** >
**All**
2. Search for `Numerical Digitize 3` > **Install plugin**
3. Switch to tab **Installed**, make sure the plugin `Numerical Digitize 3` is
enabled.

### Install manually from zip file in QGIS

1. Download the [latest release](https://github.com/desertwolf7/numericalDigitize3/releases) zip file
2. In QGIS, navigate to menu **Plugins** > **Manage and Install Plugins...** >
**Install from ZIP**, then select the downloaded zip file.
3. Switch to tab **Installed**, make sure the plugin `Numerical Digitize 3` is
enabled.

## Usage

The extension for QGIS Numeric Digitize 3 is for adding or
edit objects such as a point, line, or polygon by entering or
change the coordinate values of their node points.

This version of the extension is used for create or edit objects with one type
and consisting of points and lines. Working correctly with objects containing
curves, surfaces, or a collection of graphics primitives of various types are
not guaranteed.

The extension supports multi-part objects or contours and supports Z and M
coordinate values.

When you finish adding or editing an object, will done automatic translation of
coordinates into the coordinate system of the layer being edited.

In addition to editing the coordinates of the node points, the extension
allows you to following:

1. Paste a table of coordinate values from the clipboard or copy to the 
coordinates to clipboard for entered or existing coordinates.
2. Convert coordinate values from one projection to another.
3. Exchange coordinate values for X and Y.
4. Add or remove parts of objects and/or rings for polygons.
5. Add, edit, or delete anchor points.

In the main menu QGIS *Vector* will be added a new menu item *Numerical
digitize* coordinates with three submenu items *Numerical digitizing*,
*Numerical edit* and *Help*.

Read documentation for details of use.

