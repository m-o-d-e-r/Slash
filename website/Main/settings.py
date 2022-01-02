from flask import Flask, Blueprint
import os



class Main(Flask):
    def __init__(self, *, import_name: str, template_folder, static_folder):
        super().__init__(import_name, template_folder=template_folder, static_folder=static_folder)
    
    def reg_app(self, blueprint: Blueprint, link: str):
        self.register_blueprint(blueprint, url_prefix=link)

    def add_route(self, link, target):
        self.add_url_rule(link, view_func=target)

    def add_error_route(self, error_code, handler):
        self.register_error_handler(error_code, handler)
