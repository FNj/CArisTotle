from CArisTotle import app
from CArisTotle.datamodel.procedures import init_db, drop_all
from CArisTotle.dev.test_data import test_data

app.testing = True
# test_client = app.test_client()
# with app.test_request_context("/"):
#     print(url_for('static', filename="css/custom.css"))

# app.testing = False

drop_all()
init_db()
test_data()

app.run()
