from application import create_app

app, db = create_app("dev")
app.run()
