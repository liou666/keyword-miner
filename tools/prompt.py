import questionary
from rich.prompt import Prompt

# promopt
def ask(msg, *args):
    return Prompt.ask(f"[bold cyan]{msg}[/bold cyan]",*args)

def choices(msg,choices,default):
    return Prompt.ask(f"[bold cyan]{msg}[/bold cyan]",choices=choices,default=default)

def select(msg,choices):
    return questionary.select(
        msg,
        choices=choices,
        style= questionary.Style([('highlighted', 'fg:#622ab7 bold')]
    )).ask()

def input(msg,validate=None):
    return questionary.text(msg,validate=validate).ask()
