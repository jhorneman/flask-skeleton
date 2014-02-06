flask-skeleton
==============

A skeleton for Flask applications.

Goals:
* Convenient and safe selection of configurations for multiple run modes:
    * dev        - local, personal development server.
    * test       - used for automated testing.
    * production - deployed on Heroku.
* Database support using SQLAlchemy
	* SQLite for dev / team configurations
	* PostgreSQL for production
* Support for automated tests
* Support for logging and debugging
* Easy to use in actual projects
* Easy to generate documentation

Future goals:
* Support for asset management (javascript, CSS)
* Integration of basic CSS (reset, Bootstrap)
