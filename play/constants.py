"""Constants for play app."""

initial_board: list[list[int]] = [
    [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # noqa WPS221
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],  # noqa WPS221
    [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # noqa WPS221
    [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],  # noqa WPS221
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
]

play_consumers_message_types_set: set = {
    'play_message',
    'ask_rival',
    'answer_rival',
    'user_message',
    'propose_draw',
    'agree_draw',
    'refuse_draw',
}

start_consumers_message_types_set: set = {
    'game_over',
    'start_playing',
    'refresh',
    'user_message',
    'propose',
    'agree',
}
