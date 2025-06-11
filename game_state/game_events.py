from blinker import Signal

# Signal emitted when an asteroid is mined
# Parameters:
#   - asteroid_entity: The asteroid that was mined
#   - quantity: The amount of ore that was mined
on_asteroid_mined = Signal('on_asteroid_mined') 