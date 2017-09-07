from CArisTotle import app

app.testing = True
# test_client = app.test_client()
# with app.test_request_context("/"):
#     print(url_for('static', filename="css/custom.css"))

# app.testing = False
app.run()
