# Alpaca: An Economic Evaluation Plug-In for Scenario Planning Tools
The "Alpaca" project, funded by the Lincoln Institute of Land Policy (http://www.lincolninst.edu/), developed software designed to facilitate the integration of bid-rent land use models with scenario planning tools.  Such models can enhance scenario planning efforts by simulating how real estate markets work, adding a variety of metrics relating to topics such as:
* Property value and rent
* Socio-economic characteristics of tenants
* Housing affordability and cost burden

The code developed in the course of the project included:
* mu-land: the "core" bid-rent model evaluation software
* muLandWeb: a Python wrapper for mu-land allowing models to be offered as web services callable by third-party tools
* example: client-side Python scripts developed in case studies, showcasing various methods of using mu-land

The core mu-land program is used in the Demand sub-model of the SRF System.  The only modifications from the original software are those necessary for the executable to run on Windows.  The "muLand" folder contains the code for the version of this program used in the SRF System.

# Requirements
The mu-land core uses Boost 1.54 libraries.

# Installation
If you do not have a pre-compiled binary of mu-land available for your system, then it must be compiled and installed first.  Follow the instructions in the "readme" file within the mu-land folder.

# Credits
* Software design/testing:
 * Colby Brown (colby@manhangroup.com)
 * Pedro Donoso (pedrodonosos@gmail.com)
* Programming:
 * Felipe Saavedra (fsaavedr@dcc.uchile.cl)
 * Leandro Lima (leandro.lima@toptal.com)
 * Kaden Weber (kweber142@gmail.com)
