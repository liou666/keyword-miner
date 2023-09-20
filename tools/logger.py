from rich.console import Console
from rich.prompt import Prompt

console = Console()

def info(msg):
    console.print(f"🔸 {msg}")

def success(msg):
    console.print(f"✅ {msg}")

def error(msg):
    console.print(f"[red]😱 {msg}")

def warn(msg):
    console.print(f"[yellow]😅 {msg}")

def status(msg):
    return console.status(f"[bold green]{msg}")

def start(msg):
    console.print(f"[bold green]\n✨ {msg}")

def ask(msg, *args):
    return Prompt.ask(f"[bold cyan]{msg}[/bold cyan]",*args)

def choices(msg,choices,default):
    return Prompt.ask(f"[bold cyan]{msg}[/bold cyan]",choices=choices,default=default)
