from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helper import Configuration, log


class Renderer:
    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        options = Options()
        options.headless = True

        args = [
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-setuid-sandbox",
            "--single-process",
            "--disable-crashpad",
            "--disable-web-security",
            "--disable-extensions",
        ]
        for arg in args:
            options.add_argument(arg)

        self.options = options
        self.initalize = True
        self.driver: webdriver.Chrome | None = None

    def render_molfile(self, molfile: str) -> str:
        if self.driver:
            return self.driver.execute_script(  # type: ignore
                "return renderMolfile(arguments[0])", molfile
            )
        return ""

    def init(self) -> None:
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_page_load_timeout(3000)
        self.driver.get(self.cfg.ketcher_url)
        if "Ketcher" in self.driver.title:
            self.driver.execute_script(self.cfg.script)  # type: ignore
            self.initalize = False
        else:
            raise Exception("Could not load Ketcher.")

    async def render(self, molfile: str) -> tuple[int, str]:
        try:
            if self.initalize or self.driver is None:
                self.init()
            assert self.driver and "Ketcher" in self.driver.title
            starting_time = datetime.now()
            svg = self.render_molfile(molfile)
            duration = (datetime.now() - starting_time).total_seconds()
            log(f"Rendering took {round(duration, 3)} seconds.")
            assert svg.startswith("<svg")
            return (0, svg)
        except Exception as ex:  # pylint: disable=broad-except
            log(f"Could not render molfile:\n{ex}\n--")
            return (20, "Could not render molfile.")

    def quit(self) -> None:
        if self.driver:
            try:
                self.driver.close()
            except Exception:  # pylint: disable=broad-except
                pass

    def __del__(self) -> None:
        self.quit()
