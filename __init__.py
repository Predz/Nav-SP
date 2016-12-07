'''

'''

# Source.Python
from mathlib import Vector

# Python.3+
from os.path import isfile, getsize
from struct import unpack, calcsize

# Nav.Source.Python
from .constants import *

# Declaration of ALL
__all__ = (
    'Nav',
    'Reader',
    )

NAV_UNIQUE_NUMBER = 0xFEEDFACE

class Reader:
    """
    Reader provides the functions to be able to pull specific
    bytes from the file when required. It caches the size
    of bytes retrieved, saving the need for extra calculations
    later.

    :param fileobject file:
        File object to store.
    """

    cache = {}

    def __init__(self, file):
        "Store the file object provided."
        self.file = file

    def read(self, to_read=None, offset=None, whence=None):
        "Characters to read from the file. An offset can be specified if required."
        if offset:
            self.file.seek(offset, whence) if whence else self.file.seek(offset)
        if to_read:
            result = unpack(to_read, self.file.read(self.getsize(to_read)))
            if result and len(result) == 1:
                return result[0]
            return result
    
    @classmethod
    def getsize(cls, characters):
        "Retrieve the size of the characters provided."
        if characters in cls.cache:
            return cls.cache[characters]
        size = calcsize(characters)
        cls.cache[characters] = size
        return size

class Nav:
    """
    Reads a source engine navigvation file. Retrieving data
    on hiding spots, walkable areas, and ladders.

    :param str path:
        Path to the navigation file to process.
    :raise ValueError:
        Raised if the file location cannot be found.
    """

    cache = {}

    def __init__(self, path, grid_cell_size=300.0):
        self.path = path
        if not isfile(path) or path[-3:] != 'nav':
            raise SystemError('Cannot find navigation file ({}).'.format(path))

        self.file = open(path, 'rb')
        self.reader = Reader(self.file)
        self.read = self.reader.read
        self.grid_cell_size = grid_cell_size

        self.areas = []
        self.encounter_spots = []
        self.hiding_spots = []
        self.non_crouching_spots = []
        self.places = []

        self.offsets = {}

        number, self.version = self.read('II')

        if number != NAV_UNIQUE_NUMBER:
            raise ValueError('Unique navigation file number does not match.')

        if self.version > 3:
            self.check_bsp_validity()
            
        if self.version > 4:
            self.offsets['places'] = self.file.tell()
            self.construct_places()

        self.offsets['areas'] = self.file.tell()
        self.construct_areas()

    def check_bsp_validity(self):
        "Checks that the correspondent BSP file is valid."
        bsp_path = self.path[-3:] + 'bsp'
        bsp_size = self.read('I')
        if not isfile(bsp_path) or bsp_size != getsize(bsp_path):
            raise SystemError('Correspondent BSP file is incorrect or non-existant.')

    def construct_areas(self):
        area_count = self.read('I')
        for x in range(0, area_count):
            area = Area()
            area.id = x
            area.flags = self.read('B') if self.version <= 8 else self.read('H')

            x1, y1, z1, x2, y2, z2 = self.read('ffffff')
            vector1, vector2 = Vector(x1, y1, z1), Vector(x2, y2, z2)
            area.extent = Ray(vector1, vector2)
            area.center = area.extent.center

    def construct_places(self):
        "Generate all named places from the NAV file."
        place_count = self.read('H')
        for _ in range(0, place_count):
            length = self.read('H')
            name = self.read('{}s'.format(length))
            self.places.append(name)

class Area:
    pass
