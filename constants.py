'''

'''

# Python.3+
from enum import IntEnum

# Declaration of ALL
__all__ = (
    'HidingSpotFlags',
    'NavTraverseTypes',
    'NavDirTypes',
    'NavAttributeTypes',
    )

# Hiding Spot Flags
class HidingSpotFlags(IntEnum):
    IN_COVER            = 1
    GOOD_SNIPER_SPOT    = 2
    IDEAL_SNIPER_SPOT   = 4
    EXPOSED             = 8

# Nav Attribute Types
class NavAttributeTypes(IntEnum):
    CROUCH = 1
    JUMP = 2
    PRECISE = 4
    NO_JUMP = 8
    STOP = 16
    RUN = 32
    WALK = 64
    AVOID = 128
    TRANSIENT = 256
    DONT_HIDE = 512
    STAND = 1024
    NO_HOSTAGES = 2048

# Nav Direction Types
class NavDirectionTypes(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

# Nav Traverse Types
class NavTraverseTypes(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    LADDER_UP = 4
    LADDER_DOWN = 5
    JUMP = 6