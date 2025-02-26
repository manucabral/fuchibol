"""
The main client to interact with the library.
"""
from typing import List
from .utils import get_today
from .services import SofascoreClient
from .match_summary import MatchSummary
from .match_details import MatchDetails
from .match_team import parse_match_team, MatchTeam

class Client:
    """
    The main core class.
    """
    def __init__(self):
        """
        Initialize the client.
        """
        self.__sofascore: SofascoreClient = SofascoreClient()
    
    def get_matchs(self, date: str = None) -> List[MatchSummary]:
        """
        Get all matchs from a specific date.

        Args:
            date (str): The date to get the matchs. Format: "YYYY-MM-DD". Defaults to today.
        
        Returns:
            List[MatchSummary]: A list of MatchSummary objects.

        Note:
            If you want all match details use the get_match_by_id method.
        """
        date = date or get_today()
        events = self.__sofascore.get_events(date)
        return [
            MatchSummary(
                _id=event.get("id"),
                status=event.get("status", {}).get("description"),
                info=event.get("slug")
            )
            for event in events
        ]

    def get_match_details(self, match_id: int) -> dict:
        """
        Get all details from a specific match.

        Args:
            match_id (int): The match id.
        
        Returns:
            dict: A dictionary with all match details.
        """
        _match = self.__sofascore.get_event(match_id)
        return MatchDetails(
            _id=_match.get("id"),
            home_team=parse_match_team(_match, "homeScore", "homeTeam"),
            away_team=parse_match_team(_match, "awayScore", "awayTeam"),
        )