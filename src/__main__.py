import requests
import typer
import threading
import rich.console
import rich.prompt
import rich.status
import rich.progress

app = typer.Typer()
console = rich.console.Console()


def download_thread(name, file, token, tid, progress):
    with requests.get(f"https://opendata.nationalrail.co.uk{file}", stream=True, headers={
        "X-Auth-Token": token
    }) as res:
        res.raise_for_status()
        progress.update(tid, total=int(res.headers['Content-Length']))

        with open(name, "wb") as disk:
            for chunk in res.iter_content(chunk_size=1024):
                progress.update(tid, advance=len(chunk))
                disk.write(chunk)


@app.command()
def command(
    fares: str = typer.Option(""),
    routeing: str = typer.Option(""),
    timetable: str = typer.Option(""),
    username: str = None,
    password: str = None
):
    if not (fares or routeing or timetable):
        console.log("Nothing to do. Exiting.")
        exit(1)

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
    except Exception as e:
        status.stop()
        raise e

    json = res.json()
    console.log(json)

    status.stop()

    files = dict()

    if fares != "":
        files[fares] = "/api/staticfeeds/2.0/fares"

    if routeing != "":
        files[routeing] = "/api/staticfeeds/2.0/routeing"

    if timetable != "":
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
            thread = threading.Thread(target=download_thread, args=(name, file, json.get('token'), tasks[name], progress))
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    app()
