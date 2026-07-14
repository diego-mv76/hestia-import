import typer

from hestia_import import __version__
from hestia_import.commands.analyze import analyze
from hestia_import.commands.plan import plan
from hestia_import.commands.execute import execute
from hestia_import.commands.doctor import doctor

app = typer.Typer(
    help="Migrador de backups cPanel hacia HestiaCP",
    no_args_is_help=True,
)


@app.command()
def version():
    """Mostrar versión."""
    print(f"Hestia Import {__version__}")


app.command()(analyze)
app.command()(plan)
app.command()(execute)
app.command()(doctor)

if __name__ == "__main__":
    app()
