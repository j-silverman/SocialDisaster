# SocialDisaster
This is an application made in the django web framework for bu cs492 SPARK Product Development Lab that takes twitter info from Hurricane Harvey and categorizes it into useful categories which are then displayed on a map.

To run this you must create a config.py file in the SocialDisaster/socialdisaster dir the files contents should be in the form
MAPS_API_KEY = <'your google maps geocode API key'>

To populate SQLite DB you must run inserTestData.py -> Analysis.py -> getCoordinates.py
