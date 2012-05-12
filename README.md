flask-skeleton
==============

A skeleton for Flask applications.

Goals:
* Convenient and safe selection of multiple configurations
** dev - local, personal development server
** team - still local server, for development by team (specifically non-coder team members)
** production - deployed on Heroku
* Database support using SQLAlchemy
** SQLite for dev / team configurations
** PostgreSQL for production
* Support for automated tests
* Convenient and extendable admin tasks
** Running the server
** Creating the database
** Deployment to Heroku
* Easy use in actual projects

Future goals:
* Support for asset management (javascript, CSS)
* Integration of basic CSS (reset, Bootstrap)
