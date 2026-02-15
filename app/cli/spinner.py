from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live

console = Console()


async def run_with_spinner(coro):
    spinner = Spinner("dots", text="Running AI agent...")
    with Live(spinner, console=console, refresh_per_second=10):
        await coro
