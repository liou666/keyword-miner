from rich.console import Console

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


