"""Module represents base class for loading properties and work with translation."""

from crossgame.api.lang_provider import LangProvider


class BaseAppWidget(LangProvider):
    """Base App class created to provide functionality of loading properties and manage language variables retrival."""

    def __init__(self, app_lang: str) -> None:
        """Initialize LangProvider class and adds properties for calculating rows/cols.

        Args:
            app_lang (str): Language to be loaded
        """
        LangProvider.__init__(self, app_lang)
        self.number_rows = 1
        self.number_cols = 1
