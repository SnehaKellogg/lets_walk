1. We now have a Year column being served up at the following Route: /InspectionDate/<year>. replace <year> with the year you need and it will load.
2. Route 2: /data -- serves up everything (3k records - feel free to up this)
3. Route 3: /refreshdb -- accessing this will delete your current database, gather updated data and create a new one with the same name (not exactly secure, but what the heck)

Steps.
1. Run refreshdb.py in console first
2. Run app.py
(app.py will not work without a db connection so running refresh.py takes care of that)