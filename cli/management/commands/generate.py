from pathlib import Path
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
import os
from django.conf import settings
from django.template.loader import render_to_string


class Command(BaseCommand):

    help = 'Generate new classes service|model|mixins'

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '-s', '--service', 
            help='service class name', type=str
            )
        parser.add_argument(
            '-a', '--app',
            help='specify the target application', type=str
            )
    
    def generate_template(self, template_name: str, output_name:str, path: Path, **kwargs) -> None:
        content = render_to_string(template_name, kwargs)
        with open(path / output_name, "w") as f:
            f.write(content)
    
    def handle(self, *args: Any, **options: Any) -> None:
        service_name : str = options["service"]
        app_name = options["app"]
        target_path = settings.BASE_DIR / app_name / "services"
        self.generate_template('service.txt', service_name.lower() + '.py', target_path, model=service_name)