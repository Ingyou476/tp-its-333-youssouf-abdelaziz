from app import app
from flasgger import Swagger

Swagger(app)

app.run(host="0.0.0.0", port=5000, debug=True)
