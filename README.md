# Address (Data from CSDI)

The address data from the government was stored with nested and complex geojson format. Therefore, this project is to decompose the address into a "ready to use" format.

The address will be update monthly from the DPO (Digital Policy Office), therefore this database will be updated every month. 

### Concept

To decompose the address, first is to extract the geojson files by the attributes and remap the attributes into csv table format. 


### Methods

* Data collection from CSDI (https://portal.csdi.gov.hk/geoportal/?lang=en&datasetId=dpo_rcd_1629267205232_33603)
* Extract the geojson by attribute 
* Remap the attributes into a table format 
* Merge all the per district tables into a single file (zipped, due to it is quite large)
* Data release with table format 
