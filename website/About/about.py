from .settings import AboutBlueprint
from .route import AboutRoute
import os

about_blueprint = AboutBlueprint(
    name="about", import_name=__name__,
    template_folder=os.environ.get("TEMPLATES_DIR"),
    static_folder=os.environ.get("STATIC_DIR")
)

about_blueprint.add_route("/", AboutRoute.main)
