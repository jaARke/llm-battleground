from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from api.utils.enums import GameStatus

from ..shared.models import AIModel, GameState
from .exceptions import (
    CatchExceedsPondTotalError,
    CatchExceedsRoundLimitError,
    GameAlreadyCompletedError,
    InvalidGameStateError,
    PlayerNotFoundError,
    RoundDoesNotExistError,
    SharingExceedsPossessionError,
)


class GoFishGameParams(BaseModel):
    """Request model for creating a Go Fish game"""

    num_rounds: int = Field(
        description="Number of rounds to be played in the game", gt=0, le=50, default=25
    )
    starting_fish: int = Field(
        description="Number of fish in the pond to start", gt=0, le=1000, default=500
    )
    regeneration_rate: float = Field(
        description="Rate at which fish regenerate in the pond", ge=1.0, default=1.1
    )
    extinction_penalty: float = Field(
        description="Penalty multiplier applied when no fish are left in the pond",
        le=1.0,
        ge=0.0,
        default=0.5,
    )
    sustainability_bonus: float = Field(
        description=(
            "Bonus multiplier applied when more than 20% of starting fish are left in the pond at"
            " the end of the game"
        ),
        ge=1.0,
        default=1.2,
    )
    turn_catch_limit_fixed: int = Field(
        description=(
            "Absolute maximum number of fish that can be caught in a single turn, regardless of"
            " pond size. This is used in conjunction with turn_catch_limit_percentage to set the"
            " actual turn catch limit: min(turn_catch_limit_fixed, turn_catch_limit_percentage *"
            " pond_size at start of round). This value cannot exceed starting_fish."
        ),
        gt=0,
        default=50,
    )
    turn_catch_limit_percentage: float = Field(
        description=(
            "Maximum fraction of fish that can be caught in a single turn relative to the pond size"
            " at the start of the round. This is used in conjunction with turn_catch_limit_fixed to"
            " set the actual turn catch limit: min(turn_catch_limit_fixed,"
            " turn_catch_limit_percentage * pond_size at start of round). This value must be set"
            " such that pond extinction is possible if all players catch the maximum allowed each"
            " turn."
        ),
        gt=0.0,
        le=1.0,
        default=0.4,
    )

    @model_validator(mode="after")
    def validate_turn_catch_limit_fixed(self) -> "GoFishGameParams":
        if self.turn_catch_limit_fixed > self.starting_fish:
            raise ValueError(
                "turn_catch_limit_fixed cannot be greater than starting_fish"
                f" ({self.turn_catch_limit_fixed} > {self.starting_fish})"
            )
        return self

    @model_validator(mode="after")
    def validate_turn_catch_limit_percentage(self) -> "GoFishGameParams":
        if self.turn_catch_limit_percentage * self.num_players < 1.0:
            raise ValueError(
                "turn_catch_limit_percentage is too low to allow pond extinction"
                f" ({self.turn_catch_limit_percentage} * {self.num_players} < 1.0)"
            )
        return self


class FishCaughtEvent(BaseModel):
    """Model representing fish caught by a player in Go Fish"""

    player: AIModel = Field(..., description="AI model representing the player who caught the fish")
    round: int = Field(..., description="Round number when the fish were caught", ge=0)
    count: int = Field(..., description="Number of fish caught", gt=0)

    def to_log_entry(self) -> str:
        """Generate a log entry for the fish caught event."""
        return f"{self.player.display_name} caught {self.count} fish in round {self.round}."


class FishSharedEvent(BaseModel):
    """Model representing fish sent from one player to another in Go Fish"""

    to_player: AIModel = Field(
        ..., description="AI model representing the player receiving the fish"
    )
    from_player: AIModel = Field(
        ..., description="AI model representing the player sending the fish"
    )
    round: int = Field(..., description="Round number when the fish were sent", ge=0)
    count: int = Field(..., description="Number of fish sent", gt=0)

    def to_log_entry(self) -> str:
        """Generate a log entry for the fish shared event."""
        return (
            f"{self.from_player.display_name} shared {self.count} fish with"
            f" {self.to_player.display_name} in round {self.round}."
        )


class MessageSentEvent(BaseModel):
    """Model representing a message from a player in Go Fish"""

    to_player: AIModel = Field(
        ..., description="AI model representing the player receiving the message"
    )
    from_player: AIModel = Field(
        ..., description="AI model representing the player sending the message"
    )
    round: int = Field(..., description="Round number when the message was sent", ge=0)
    message: str = Field(..., description="Content of the player's message")

    def to_log_entry(self) -> str:
        """Generate a log entry for the message sent event."""
        return (
            f"{self.from_player.display_name} sent a message to"
            f" {self.to_player.display_name} in round {self.round}: '{self.message}'"
        )


class EventLog(BaseModel):
    """Global log tracking all game events from an omniscient perspective"""

    fish_caught_events: List[FishCaughtEvent] = Field(
        description="All fish caught events in the game", default_factory=list
    )
    fish_shared_events: List[FishSharedEvent] = Field(
        description="All fish sharing events in the game", default_factory=list
    )
    message_sent_events: List[MessageSentEvent] = Field(
        description="All messages sent in the game", default_factory=list
    )

    # Totals
    total_fish_caught: int = Field(default=0, ge=0)
    total_fish_shared: int = Field(default=0, ge=0)
    total_messages_sent: int = Field(default=0, ge=0)

    def add_fish_caught(self, event: FishCaughtEvent) -> None:
        """Record fish caught by any player."""
        self.fish_caught_events.append(event)
        self.total_fish_caught += event.count

    def add_fish_shared(self, event: FishSharedEvent) -> None:
        """Record fish shared between any players."""
        self.fish_shared_events.append(event)
        self.total_fish_shared += event.count

    def add_message_sent(self, event: MessageSentEvent) -> None:
        """Record message sent between any players."""
        self.message_sent_events.append(event)
        self.total_messages_sent += 1


class BidirectionalEventLog(BaseModel):
    """Base class for logs tracking events from a specific player's perspective"""

    # Outgoing events (actions taken by this player)
    fish_shared_events: List[FishSharedEvent] = Field(
        description="Fish shared by this player to others", default_factory=list
    )
    message_sent_events: List[MessageSentEvent] = Field(
        description="Messages sent by this player to others", default_factory=list
    )

    # Incoming events (actions received by this player)
    fish_received_events: List[FishSharedEvent] = Field(
        description="Fish received by this player from others", default_factory=list
    )
    messages_received_events: List[MessageSentEvent] = Field(
        description="Messages received by this player from others", default_factory=list
    )

    # Totals
    total_fish_shared: int = Field(default=0, ge=0)
    total_messages_sent: int = Field(default=0, ge=0)
    total_fish_received: int = Field(default=0, ge=0)
    total_messages_received: int = Field(default=0, ge=0)

    def add_fish_shared(self, event: FishSharedEvent) -> None:
        """Record fish shared by this player to another player."""
        self.fish_shared_events.append(event)
        self.total_fish_shared += event.count

    def add_fish_received(self, event: FishSharedEvent) -> None:
        """Record fish received by this player from another player."""
        self.fish_received_events.append(event)
        self.total_fish_received += event.count

    def add_message_sent(self, event: MessageSentEvent) -> None:
        """Record message sent by this player to another player."""
        self.message_sent_events.append(event)
        self.total_messages_sent += 1

    def add_message_received(self, event: MessageSentEvent) -> None:
        """Record message received by this player from another player."""
        self.messages_received_events.append(event)
        self.total_messages_received += 1


class PlayerEventLog(BidirectionalEventLog):
    """Log of all events related to a specific player across all opponents"""

    fish_caught_events: List[FishCaughtEvent] = Field(
        description="Fish caught by this player from the pond", default_factory=list
    )
    total_fish_caught: int = Field(default=0, ge=0)

    def add_fish_caught(self, event: FishCaughtEvent) -> None:
        """Record fish caught by this player from the pond."""
        self.fish_caught_events.append(event)
        self.total_fish_caught += event.count


class OpponentEventLog(BidirectionalEventLog):
    """Log of interactions between this player and a specific opponent"""

    opponent: AIModel = Field(..., description="The opponent player in this interaction log")


class PlayerState(BaseModel):
    """Model representing the state of a player in Go Fish"""

    player: AIModel = Field(..., description="AI model representing the player")
    current_fish: int = Field(description="Current number of fish the player has", ge=0, default=0)
    personal_event_log: PlayerEventLog = Field(
        description="Log of events related to the player", default_factory=PlayerEventLog
    )
    opponent_event_logs: List[OpponentEventLog] = Field(
        description="Logs of interactions with opponent players", default_factory=list
    )

    def get_opponent_log(self, opponent: AIModel) -> OpponentEventLog:
        """Retrieve or create the event log for interactions with a specific opponent."""
        for log in self.opponent_event_logs:
            if log.opponent == opponent:
                return log
        new_log = OpponentEventLog(opponent=opponent)
        self.opponent_event_logs.append(new_log)
        return new_log

    def add_fish_caught(self, event: FishCaughtEvent) -> None:
        """
        Record fish caught by this player from the pond.

        Args:
            event (FishCaughtEvent): The fish caught event to record.
        """
        self.current_fish += event.count
        self.personal_event_log.add_fish_caught(event)

    def add_fish_shared(self, event: FishSharedEvent) -> None:
        """
        Record fish shared by this player to another player.

        Args:
            event (FishSharedEvent): The fish shared event to record.

        Raises:
            SharingExceedsPossessionError: If the player tries to share more fish than they possess
        """
        # Validate fish possession
        if self.current_fish < event.count:
            raise SharingExceedsPossessionError(
                f"Cannot share {event.count} fish; only {self.current_fish} available",
                available_fish=self.current_fish,
            )

        # Update personal state
        self.current_fish -= event.count
        self.personal_event_log.add_fish_shared(event)

        # Update opponent log
        opponent_log = self.get_opponent_log(event.to_player)
        opponent_log.add_fish_shared(event)

    def add_fish_received(self, event: FishSharedEvent) -> None:
        """
        Record fish received by this player from another player.

        Args:
            event (FishSharedEvent): The fish received event to record.
        """
        # Update personal state
        self.current_fish += event.count
        self.personal_event_log.add_fish_received(event)

        # Update opponent log
        opponent_log = self.get_opponent_log(event.from_player)
        opponent_log.add_fish_received(event)

    def add_message_sent(self, event: MessageSentEvent) -> None:
        """
        Record message sent by this player to another player.

        Args:
            event (MessageSentEvent): The message sent event to record.
        """
        # Update personal state
        self.personal_event_log.add_message_sent(event)

        # Update opponent log
        opponent_log = self.get_opponent_log(event.to_player)
        opponent_log.add_message_sent(event)

    def add_message_received(self, event: MessageSentEvent) -> None:
        """
        Record message received by this player from another player.

        Args:
            event (MessageSentEvent): The message received event to record.
        """
        # Update personal state
        self.personal_event_log.add_message_received(event)

        # Update opponent log
        opponent_log = self.get_opponent_log(event.from_player)
        opponent_log.add_message_received(event)


class TurnCatchLimit(BaseModel):
    """Model representing the catch limit for a single round"""

    round: int = Field(..., description="Round number this limit applies to", ge=0)
    limit: int = Field(
        ...,
        description="Maximum number of fish that can be caught by a single player this round",
        ge=0,
    )


class GoFishGameState(GameState):
    """Model representing the state of a Go Fish game"""

    params: GoFishGameParams = Field(
        description="Game parameters", default_factory=GoFishGameParams
    )
    fish_in_pond: Optional[int] = Field(
        description="Current number of fish in the pond", default=None
    )
    current_round: int = Field(description="Current round number", default=0, ge=0)
    current_turn_player_index: int = Field(
        description="Index of the player whose turn it is currently", default=0, ge=0
    )
    player_states: List[PlayerState] = Field(
        description="List of player states in the game", default_factory=list
    )
    turn_catch_limits: List[TurnCatchLimit] = Field(
        description="List of turn catch limits per round", default_factory=list
    )
    event_log: EventLog = Field(description="Log of all game events", default_factory=EventLog)

    @model_validator(mode="after")
    def initialize_fish_in_pond(self) -> "GoFishGameState":
        # Set initial fish to starting fish if not already set
        if self.fish_in_pond is None:
            self.fish_in_pond = self.params.starting_fish

        if not self.turn_catch_limits:
            # Calculate turn catch limit for the first round
            turn_catch_limit = min(
                self.params.turn_catch_limit_fixed,
                int(self.params.turn_catch_limit_percentage * (self.fish_in_pond or 0)),
            )
            self.turn_catch_limits.append(
                TurnCatchLimit(round=self.current_round, limit=turn_catch_limit)
            )

        return self

    @model_validator(mode="after")
    def initialize_player_states(self) -> "GoFishGameState":
        if not self.player_states and self.players:
            self.player_states = [PlayerState(player=player) for player in self.players]
        return self

    def get_turn_catch_limit_for_round(self, round_number: int) -> int:
        """
        Retrieve the catch limit for a specific round.

        Args:
            round_number (int): The round number to retrieve the catch limit for.

        Raises:
            RoundDoesNotExistError: If no catch limit is found for the specified round.
        """
        for limit in self.turn_catch_limits:
            if limit.round == round_number:
                return limit.limit

        raise RoundDoesNotExistError(
            f"No catch limit found for round {round_number}",
        )

    def get_current_turn_catch_limit(self) -> int:
        """
        Retrieve the catch limit for the current round.

        Raises:
            InvalidGameStateError: If no catch limit is found for the current round.
        """
        # We expect turn_catch_limits to be sorted by round in ascending order
        # so we can search from the end for efficiency
        for limit in reversed(self.turn_catch_limits):
            if limit.round == self.current_round:
                return limit.limit

        raise InvalidGameStateError(
            f"No catch limit found for current round {self.current_round}",
        )

    def get_player_by_display_name(self, display_name: str) -> AIModel:
        """
        Retrieve the AI model of a player by their display name.

        Args:
            display_name (str): The display name of the player.

        Raises:
            PlayerNotFoundError: If the player with the given display name is not found.
        """
        for state in self.player_states:
            if state.player.display_name == display_name:
                return state.player

        raise PlayerNotFoundError(
            f"Player with display name '{display_name}' not found",
            available_players=[p.player for p in self.player_states],
        )

    def get_current_player(self) -> AIModel:
        """
        Retrieve the AI model of the current turn player.

        Raises:
            InvalidGameStateError: If the current turn player index is out of bounds.
        """
        if 0 <= self.current_turn_player_index < len(self.player_states):
            return self.player_states[self.current_turn_player_index].player

        raise InvalidGameStateError(
            f"Current turn player index {self.current_turn_player_index} is out of bounds",
        )

    def get_player_state(self, player: AIModel) -> PlayerState:
        """
        Retrieve the state of a specific player.

        Args:
            player (AIModel): The AI model representing the player.

        Raises:
            PlayerNotFoundError: If the player is not found in the game state.
        """
        for state in self.player_states:
            if state.player == player:
                return state

        raise PlayerNotFoundError(
            f"Player '{player.display_name}' not found",
            available_players=[p.player for p in self.player_states],
        )

    def get_player_state_by_display_name(self, display_name: str) -> PlayerState:
        """
        Retrieve the state of a specific player by their display name.

        Args:
            display_name (str): The display name of the player.

        Raises:
            PlayerNotFoundError: If the player with the given display name is not found.
        """
        for state in self.player_states:
            if state.player.display_name == display_name:
                return state

        raise PlayerNotFoundError(
            f"Player with display name '{display_name}' not found",
            available_players=[p.player for p in self.player_states],
        )

    def get_current_player_state(self) -> PlayerState:
        """
        Retrieve the state of the current turn player.

        Raises:
            InvalidGameStateError: If the current turn player index is out of bounds.
        """
        if 0 <= self.current_turn_player_index < len(self.player_states):
            return self.player_states[self.current_turn_player_index]

        raise InvalidGameStateError(
            f"Current turn player index {self.current_turn_player_index} is out of bounds",
        )

    def add_fish_caught(self, event: FishCaughtEvent) -> None:
        """
        Record fish caught by any player.

        Args:
            event (FishCaughtEvent): The fish caught event to record.

        Raises:
            RoundDoesNotExistError: If the turn catch limit for the event's round does not exist.
            CatchExceedsPondTotalError: If the player tries to catch more fish than are available in the pond.
            CatchExceedsRoundLimitError: If the player tries to catch more fish than the round's catch limit.
            PlayerNotFoundError: If the player from the event is not found in the game state.
        """
        # Validate fish availability in pond
        if event.count > (self.fish_in_pond or 0):
            raise CatchExceedsPondTotalError(
                f"Cannot catch {event.count} fish; only {self.fish_in_pond or 0} available in pond",
                available_fish=self.fish_in_pond or 0,
            )

        # Validate fish catch limit for the round
        turn_catch_limit = self.get_turn_catch_limit_for_round(event.round)
        if event.count > turn_catch_limit:
            raise CatchExceedsRoundLimitError(
                f"Cannot catch {event.count} fish; exceeds turn catch limit of {turn_catch_limit}",
                round_limit=turn_catch_limit,
            )

        # Update player state
        player_state = self.get_player_state(event.player)
        player_state.add_fish_caught(event)

        # Update global state
        self.fish_in_pond = (self.fish_in_pond or 0) - event.count
        self.event_log.add_fish_caught(event)

    def add_fish_shared(self, event: FishSharedEvent) -> None:
        """
        Record fish shared between any players.

        Args:
            event (FishSharedEvent): The fish shared event to record.

        Raises:
            SharingExceedsPossessionError: If the from_player tries to share more fish than they possess.
            PlayerNotFoundError: If either player from the event is not found in the game state.
        """
        # Update from_player state
        from_player_state = self.get_player_state(event.from_player)
        from_player_state.add_fish_shared(event)

        # Update to_player state
        to_player_state = self.get_player_state(event.to_player)
        to_player_state.add_fish_received(event)

        # Update global state
        self.event_log.add_fish_shared(event)

    def add_message_sent(self, event: MessageSentEvent) -> None:
        """
        Record message sent between any players.

        Args:
            event (MessageSentEvent): The message sent event to record.

        Raises:
            PlayerNotFoundError: If either player from the event is not found in the game state.
        """
        # Update from_player state
        from_player_state = self.get_player_state(event.from_player)
        from_player_state.add_message_sent(event)

        # Update to_player state
        to_player_state = self.get_player_state(event.to_player)
        to_player_state.add_message_received(event)

        # Update global state
        self.event_log.add_message_sent(event)

    def advance_round(self) -> bool:
        """
        Advance the game to the next round.
        Increments the round counter and regenerates fish according to the regeneration rate.

        Returns:
            bool: True if the round was advanced successfully, False if max rounds reached.

        Raises:
            GameAlreadyCompletedError: If the game is already completed.
        """
        if self.status == GameStatus.COMPLETED:
            raise GameAlreadyCompletedError("The game is already completed.")

        self.current_round += 1

        # Check if max rounds reached
        if self.current_round >= self.params.max_rounds:
            self.status = GameStatus.COMPLETED
            return False

        # Regenerate fish
        self.fish_in_pond *= self.params.regeneration_rate

        # Calculate turn catch limit for the round
        turn_catch_limit = min(
            self.params.turn_catch_limit_fixed,
            int(self.params.turn_catch_limit_percentage * (self.fish_in_pond or 0)),
        )
        self.turn_catch_limits.append(
            TurnCatchLimit(round=self.current_round, limit=turn_catch_limit)
        )

        return True

    def advance_turn(self) -> bool:
        """
        Advance the game to the next player's turn.
        Updates the current turn player index. If it wraps around to the first player,
        advances the round as well.

        Returns:
            bool: True if the turn was advanced successfully, False if the game is over.

        Raises:
            GameAlreadyCompletedError: If the game is already completed.
        """
        if self.status == GameStatus.COMPLETED:
            raise GameAlreadyCompletedError("The game is already completed.")

        # Check for pond extinction
        if self.fish_in_pond <= 0:
            self.status = GameStatus.COMPLETED
            return False

        # Advance to next player
        self.current_turn_player_index = (self.current_turn_player_index + 1) % len(self.players)

        # If wrapped around to first player, advance the round
        if self.current_turn_player_index == 0:
            return self.advance_round()

        return True
