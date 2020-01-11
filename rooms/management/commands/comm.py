from django.core.management.base import BaseCommand

help = "what??"


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--times", help="what is it?")

    def handle(self, *args, **options):
        times = options.get("times")
        for t in range(0, int(times)):
            self.stdout.write(self.style.NOTICE("heyhey!\n"))
