# -*- coding: latin1 -*-
#---------------------------------------------------------------------
# 
# Numerical Digitize - a Qgis Plugin
#
# Copyright (C) 2010  Cédric Möri
#
# EMAIL: cmoe (at) geoing (dot) ch
# WEB  : www.geoing.ch
#
#---------------------------------------------------------------------
# 
# licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
#---------------------------------------------------------------------
from numericalDigitize import NumericalDigitize     
def name():
  return "NumericalDigitize"
def description():
  return "Digitize with just the keyboard"
def version():
  return "Version 0.3.0"
def classFactory(iface):
  return NumericalDigitize(iface)
def qgisMinimumVersion():
  return "2.0"
def author():
  return "Cédric Möri"
def email():
  return "cmoe@geoing.ch"
def icon():
  return "vector-create-keyboard.png"
