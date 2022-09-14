from pathlib import Path
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
import os
from django.conf import settings
from django.template.loader import render_to_string


class Command(BaseCommand):

    help = 'Create new django app in a modern way'

    def add_arguments(self, parser):
        parser.add_argument(
            "name", help='Name of the application or project.',
            type=str
            )

    def create_package(self, name: str, path: Path) -> None:
        curr_dir = os.getcwd()
        if os.path.isdir(path):
            raise CommandError(f'folder with name: {name} already exists.')
        os.mkdir(path)
        os.chdir(path)
        open(path / "__init__.py", "w").close()
        os.chdir(curr_dir)
    
    def generate_template(self, template_name: str, output_name:str, path: Path, **kwargs) -> None:
        content = render_to_string(template_name, kwargs)
        with open(path / output_name, "w") as f:
            f.write(content)
        
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        app_name = options["name"]
        target_path = settings.BASE_DIR / app_name
        self.create_package(app_name, target_path)
        # generate apps.py
        self.generate_template('apps.txt', 'apps.py', settings.BASE_DIR / app_name, app=app_name)
        # generate managers
        self.create_package("managers", target_path / "managers")
        self.generate_template("softdeletemanager.txt", "softdelete.py", target_path / "managers")
        # generate models
        self.create_package("models", target_path / "models")
        self.generate_template("abstract.txt", 'abstract.py', target_path / "models")
        # generate mixins
        self.create_package("mixins", target_path / "mixins")
        # generate services
        self.create_package("services", target_path / "services")
        # generate tests
        self.create_package("tests", target_path / "tests")
        # generate views
        self.create_package("views", target_path / "views")



