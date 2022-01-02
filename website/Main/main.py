import sys
import os

BASE_DIR = os.environ.get("BASE_DIR")
sys.path.append(BASE_DIR) if BASE_DIR is not None else ""

from About.about import about_blueprint
from route import MainRoute
from settings import Main


app = Main(
    import_name=__name__,
    template_folder=os.environ.get("TEMPLATES_DIR"),
    static_folder=os.environ.get("STATIC_DIR")
)

app.reg_app(about_blueprint, "/about")
app.add_route("/", MainRoute.main)
app.add_error_route(404, MainRoute.error_404)
app.add_error_route(500, MainRoute.error_500)

app.run("127.0.0.1", 8888, debug=True)
