import requests
import typer
import threading
import time
import pathlib
import rich.console
import rich.prompt
import rich.status
import rich.progress

app = typer.Typer()
console = rich.console.Console()
ready = threading.Event()
abort = False


def download_thread(name, file, token, tid, progress: rich.progress.Progress):
    global abort

    tries = 0
    while True:
        try:
            with requests.get(f"https://opendata.nationalrail.co.uk{file}", stream=True, headers={
                "X-Auth-Token": token
            }) as res:
                res.raise_for_status()
                progress.update(tid, total=int(res.headers['Content-Length']))

                with open(name, "wb") as disk:
                    for chunk in res.iter_content(chunk_size=1024):
                        progress.update(tid, advance=len(chunk))
                        disk.write(chunk)
            return
        except requests.exceptions.HTTPError as e:
            tries += 1

            if tries > 2:
                progress.log(f"{file}: Too many errors, aborting")
                abort = True
                return

            progress.log(f"{file}: Error {e.response.status_code}, retrying in {tries ** 2}s (attempt {tries})")
            time.sleep(tries ** 2)
        except Exception as e:
            progress.log(f"{file}: {str(e)}")
            abort = True
            return
        finally:
            ready.set()


@app.command()
def command(
        fares: pathlib.Path = typer.Option(
            None,
            dir_okay=False,
            writable=True
        ),
        routeing: pathlib.Path = typer.Option(
            None,
            dir_okay=False,
            writable=True
        ),
        timetable: pathlib.Path = typer.Option(
            None,
            dir_okay=False,
            writable=True
        ),
        username: str = None,
        password: str = None
):
    if not (fares or routeing or timetable):
        raise typer.BadParameter("Nothing to do. Please specify at least one of --fares, --routeing or --timetable.")

    if not username:
        username = rich.prompt.Prompt.ask("Username")

    if not password:
        password = rich.prompt.Prompt.ask("Password", password=True)

    status = rich.status.Status("Logging in")
    status.start()

    res = requests.post("https://opendata.nationalrail.co.uk/authenticate", data={
        "username": username,
        "password": password
    }, headers={
        "Accept": "application/json"
    })

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status.stop()
        console.log(f"Error {e.response.status_code}. Did you enter the right credentials?")
        raise typer.Abort()

    json = res.json()

    status.stop()

    files = dict()

    if fares:
        files[fares] = "/api/staticfeeds/2.0/fares"

    if routeing:
        files[routeing] = "/api/staticfeeds/2.0/routeing"

    if timetable:
        files[timetable] = "/api/staticfeeds/3.0/timetable"

    with rich.progress.Progress(
        rich.progress.SpinnerColumn(),
        rich.progress.TextColumn("{task.description}"),
        rich.progress.BarColumn(),
        rich.progress.DownloadColumn(),
        rich.progress.TransferSpeedColumn(),
        rich.progress.TimeElapsedColumn(),
        rich.progress.TimeRemainingColumn()
    ) as progress:
        tasks = dict()
        threads = list()

        for name in files.keys():
            tasks[name] = progress.add_task(name, total=None)

        for name, file in files.items():
            thread = threading.Thread(target=download_thread, args=(name, file, json.get('token'), tasks[name], progress), daemon=True)
            thread.start()

            threads.append(thread)

        while not abort:
            running = False
            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                else:
                    running = True
            if not running:
                break

        if abort:
            raise typer.Abort()


