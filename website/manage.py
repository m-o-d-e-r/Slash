import sys
import os

print(sys.argv)

if len(sys.argv) != 1 and sys.argv[1] == "run":
    BASE_APP = os.path.dirname(__file__) + "/Main/main.py"
    BASE_FILE = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_DIR = BASE_DIR + "\\templates"
    STATIC_DIR = BASE_DIR + "\\static"
    MEDIA_DIR = BASE_DIR + "\\media"

    APPS_LIST = ["Main", "About"]
    APPS: dict = {}

    for app in APPS_LIST:
        APPS.update(
            {
                app: "{}\\{}\\{}.py".format(
                    BASE_DIR,
                    app,
                    app.lower()
                )
            }
        )

    os.environ.setdefault('BASE_APP', BASE_APP)
    os.environ.setdefault('BASE_FILE', BASE_FILE)
    os.environ.setdefault('BASE_DIR', BASE_DIR)
    os.environ.setdefault('TEMPLATES_DIR', TEMPLATES_DIR)
    os.environ.setdefault('STATIC_DIR', STATIC_DIR)
    os.environ.setdefault('MEDIA_DIR', MEDIA_DIR)

    print("Server started...")
    os.system(BASE_APP)

