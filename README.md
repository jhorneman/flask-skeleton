flask-skeleton
==============

A skeleton for Flask applications.

Goals:
* Convenient and safe selection of configurations for multiple run modes:
    * dev        - local, personal development server.
    * test       - used for automated testing.
    * team       - still local server, for development by team (specifically non-coder team members).
    * production - deployed on Heroku.
* Database support using SQLAlchemy
	* SQLite for dev / team configurations
	* PostgreSQL for production
* Support for automated tests
* Support for logging and debugging
* Convenient and extendable admin tasks
	* Running the server
	* Creating the database
	* Deployment to Heroku
* Easy to use in actual projects
* Easy to generate documentation

Future goals:
* Support for asset management (javascript, CSS)
* Integration of basic CSS (reset, Bootstrap)
