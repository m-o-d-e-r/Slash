from flask import Blueprint


class AboutBlueprint(Blueprint):
    def __init__(self, *, name, import_name: str, template_folder, static_folder):
        super().__init__(name, import_name, template_folder=template_folder, static_folder=static_folder)

    def add_route(self, link, target):
        self.add_url_rule(link, view_func=target)

    def add_error_route(self, error_code, handler):
        self.register_error_handler(error_code, handler)
