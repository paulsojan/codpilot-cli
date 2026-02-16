from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

console = Console()


async def run_with_spinner(coro):
    spinner = Spinner("dots", text="Running agent...")
    with Live(spinner, console=console, refresh_per_second=10):
        await coro
