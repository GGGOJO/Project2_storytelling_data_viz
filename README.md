# U.S. Scientists
Numbers, Locations, and Economic Impact: A Data Story

This repository holds the frontend and backend code to five data visualizations. 

The story is to understand scientists that live in the United States. Through these data visulizations, we learn the following:

* The US has the majority of Nobel prize laureates.
* The state of CA has the most (194) laureates, followed by MA (146) and NY (118).
* The University of California System had the most laureates (42), followed by Harvard (37) and Stanford (23).
* Relatively speaking, science and engineering (S&E) jobs and research and development (R&D) activities are below 10% of all jobs per state. Furthermore S&E and R&D are concentrated in a few states (CA, CO, MA, MD, NM, VA, and WA).

Recommendation: In this technological age, more investment and training are likely to be needed for the U.S. to continue to be innovative in advancing society’s needs.


## BACKEND
Using two datasets (nobel prize laureates, which was webscraped) and the national center for science and engineering statistics from the National Science Foundation, data were cleaned in jupyter notebook with pandas and numpy. 

The data were then transferred to Postgresql to create a new database.  

From the database, I used the python Flask API library to return the data into json data.

## FRONTEND
Using javascript, css, and bootstrap, the json data were used in plotly or leaflet charts to visualizing the data.
