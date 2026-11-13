"""Pure payload builders for the iDotMatrix BLE protocol.

These build the same bytes as the ``modules`` classes, but without touching a
connection, so they can be sent over any transport (see ``MatrixClient``).
"""
import io
import struct
import zlib
from typing import List, Optional

from PIL import Image as PilImage

PAYLOAD_CHUNK_SIZE = 4096


def _split(data: bytes, size: int) -> List[bytes]:
    return [data[i:i + size] for i in range(0, len(data), size)]


def image_mode(mode: int = 1) -> bytearray:
    """0 = disable DIY image mode, 1 = enable it."""
    return bytearray([5, 0, 4, 1, mode % 256])


def brightness(percent: int) -> bytearray:
    if percent not in range(5, 101):
        raise ValueError("brightness must be between 5 and 100")
    return bytearray([5, 0, 4, 128, percent])


def reset() -> List[bytes]:
    return [
        bytes.fromhex("04 00 03 80"),
        bytes.fromhex("05 00 04 80 50"),
    ]


def png_bytes(file_path: str, pixel_size: Optional[int] = None) -> bytes:
    """Read a PNG, resizing it to pixel_size x pixel_size when given."""
    if pixel_size is None:
        with open(file_path, "rb") as file:
            return file.read()
    with PilImage.open(file_path) as img:
        if img.size != (pixel_size, pixel_size):
            img = img.resize((pixel_size, pixel_size), PilImage.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()


def image_payload(png_data: bytes) -> bytearray:
    chunks = _split(png_data, PAYLOAD_CHUNK_SIZE)
    idk_bytes = struct.pack("h", len(png_data) + len(chunks))
    png_len_bytes = struct.pack("i", len(png_data))
    payload = bytearray()
    for i, chunk in enumerate(chunks):
        payload.extend(idk_bytes + bytearray([0, 0, 2 if i > 0 else 0]) + png_len_bytes + chunk)
    return payload


def gif_payloads(gif_data: bytes) -> List[bytearray]:
    header = bytearray([255, 255, 1, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 5, 0, 13])
    header[5:9] = len(gif_data).to_bytes(4, byteorder="little")
    header[9:13] = zlib.crc32(gif_data).to_bytes(4, byteorder="little")
    payloads = []
    for i, chunk in enumerate(_split(gif_data, PAYLOAD_CHUNK_SIZE)):
        header[4] = 2 if i > 0 else 0
        header[0:2] = (len(chunk) + len(header)).to_bytes(2, byteorder="little")
        payloads.append(header + chunk)
    return payloads
