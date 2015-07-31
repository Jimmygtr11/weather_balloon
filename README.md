# weather_balloon.py
Predicts where you need to launch your weather balloon in order for it to land on your desired coordinates.

# Setup
Change the values (aside from `'launchsite'`, `'lat'`, `'lon'`, and `'submit'`) in the `payload` dictionary to what you want:
```python
self.payload = {'launchsite' : 'Other',
                'lat'        : str(lat),
                'lon'        : str(lon),
                # Edit values within lines
                # --------------------------------
                'initial_alt': '0',  # (m)
                'hour'       : '15',  # (UTC)
                'min'        : '0',
                'second'     : '0',
                'day'        : '5',
                'month'      : '8',
                'year'       : '2015',
                'ascent'     : '5',  # (m/s)
                'burst'      : '30000',  # (m)
                'drag'       : '5',  # (m/s)
                # --------------------------------
                'submit'     : 'Run Prediction'}
```
# Usage
```
python weather_balloon.py
```
Enter latitude and longitude:
```
Latitude?
> 44.2708
Longitude?
> -71.2978
```
Allow the program to run for 3-5 minutes.

# Results
```
----------------------------------------------------------------------------------------------------
The best launching coordinates are (43.9008, -72.7478), which lands on (44.2761, -71.296)
HabHub Predictor URL: http://predict.habhub.org/#!/uuid=ec06ebefb2322b21955433f83a356e8e2eb395c3
Google Maps launch site URL: https://www.google.com/maps/place/43.9008+-72.7478
----------------------------------------------------------------------------------------------------
```

# Dependencies
`weather_balloon.py` requires the Python [Requests](http://docs.python-requests.org/en/latest/) module.
You can install this by using `pip`:
```
pip install requests
```

#### Reference
This program uses a [predictor tool](http://predict.habhub.org/) from [habhub](http://habhub.org/).

