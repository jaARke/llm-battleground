from pathlib import Path
from typing import Annotated

from langchain_core.tools import tool
from pydantic import Field

from .exceptions import (
    CatchExceedsPondTotalError,
    CatchExceedsRoundLimitError,
    PlayerNotFoundError,
    SharingExceedsPossessionError,
)
from .models import (
    FishCaughtEvent,
    FishSharedEvent,
    GoFishGameState,
    MessageSentEvent,
)

TURN_CONTEXT_PROMPT_FILE = Path(__file__).parent / "prompts" / "turn_context.txt"


class GoFishGameGraph:
    def __init__(self, game_state: GoFishGameState) -> None:
        self.game_state = game_state

    @tool(name="catch_fish")
    def _catch_fish_tool(
        self,
        amount: Annotated[
            int,
            Field(
                ge=0,
                description=(
                    "Number of fish to catch. This number must exceed neither the number of fish in"
                    " the pond nor the current round's catch limit."
                ),
            ),
        ],
    ) -> str:
        """
        Catch fish from the shared pond.
        You can only catch as many fish as are available in the pond and within the current round's catch limit.
        Consider the sustainability of the pond - if it goes extinct, the extinction penalty will be applied to all players' scores.
        Other players are able to see how many fish you catch.
        """
        # Get current player state
        player = self.game_state.get_current_player()

        # Construct the event
        event = FishCaughtEvent(
            player=player,
            round=self.game_state.current_round,
            count=amount,
        )

        # Attempt the catch
        try:
            self.game_state.add_fish_caught(event)
        except CatchExceedsPondTotalError as e:
            return (
                f"No fish caught - you tried to catch {amount} fish but only {e.available_fish} are"
                f" available in the pond! Try catching {e.available_fish} or fewer."
            )
        except CatchExceedsRoundLimitError as e:
            return (
                f"No fish caught - you tried to catch {amount} fish but the round's catch limit is"
                f" {e.round_limit}! Try catching {e.round_limit} or fewer."
            )
        except PlayerNotFoundError as e:
            # This should not happen since get_current_player validates the player
            return (
                "No fish caught - player not found! Available players:"
                f" {', '.join([p.display_name for p in e.available_players])}"
            )

        return f"Successfully caught {amount} fish"

    @tool(name="share_fish")
    def _share_fish_tool(
        self,
        recipient: Annotated[str, Field(description="Name of the player to share fish with")],
        amount: Annotated[int, Field(gt=0, description="Number of fish to share")],
    ) -> str:
        """
        Share some of your caught fish with another player.
        This could help build cooperation or help struggling players.
        You can only share fish you currently have.
        Other players are able to see how many fish you share and with whom.
        """
        # Get from_player
        from_player = self.game_state.get_current_player()

        # Get to_player
        try:
            to_player = self.game_state.get_player_by_display_name(recipient)
        except PlayerNotFoundError as e:
            return (
                f"No fish shared - recipient {recipient} not found! Available players:"
                f" {', '.join([p.display_name for p in e.available_players])}"
            )

        # Construct the event
        event = FishSharedEvent(
            to_player=to_player,
            from_player=from_player,
            round=self.game_state.current_round,
            count=amount,
        )

        # Attempt the share
        try:
            self.game_state.add_fish_shared(event)
        except SharingExceedsPossessionError as e:
            return (
                f"No fish shared - you tried to share {amount} fish but only have"
                f" {e.available_fish}!"
            )
        except PlayerNotFoundError as e:
            # This should not happen since we already validated players above
            return (
                "No fish shared - player not found! Available players:"
                f" {', '.join([p.display_name for p in e.available_players])}"
            )

        return f"Successfully shared {amount} fish with {recipient}"

    @tool(name="send_message")
    def _send_message_tool(
        self,
        recipient: Annotated[str, Field(description="Name of the player to send the message to")],
        message: Annotated[str, Field(description="Message content to send")],
    ) -> str:
        """
        Send a message to another player. Use this to coordinate strategy,
        negotiate cooperation, or communicate your intentions.
        Messages are private between players.
        """
        # Get from_player
        from_player = self.game_state.get_current_player()

        # Get to_player
        try:
            to_player = self.game_state.get_player_by_display_name(recipient)
        except PlayerNotFoundError as e:
            return (
                f"Message not sent - recipient {recipient} not found! Available players:"
                f" {', '.join([p.display_name for p in e.available_players])}"
            )

        # Construct the event
        event = MessageSentEvent(
            to_player=to_player,
            from_player=from_player,
            round=self.game_state.current_round,
            message=message,
        )

        # Attempt the send
        try:
            self.game_state.add_message_sent(event)
        except PlayerNotFoundError as e:
            # This should not happen since we already validated players above
            return (
                "Message not sent - player not found! Available players:"
                f" {', '.join([p.display_name for p in e.available_players])}"
            )

        return f"Message sent to {recipient}: {message}"

    def _build_turn_context(self) -> str:
        with open(TURN_CONTEXT_PROMPT_FILE, "r") as f:
            prompt_template = f.read()

        # TODO: Populate with actual dynamic values

    def play_turn(self) -> None:
        # TODO: Implement the logic for playing a turn in Go Fish using a langgraph agent

        # After the turn is played, advance the game state
        self.game_state.advance_turn()
