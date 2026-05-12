"""Sanity tests for the in-memory LoopbackTransport pair.

These don't speak protobuf or the framing layer — they only verify the
contract the higher layers depend on: bidirectional, in-order, atomic
frame delivery, and an exception when the peer goes away.
"""

from __future__ import annotations

import pytest

from ligpsport.transport import TransportClosed, make_loopback_pair


async def test_round_trip() -> None:
    client, peer = make_loopback_pair()
    await client.send(b"hello")
    assert await peer.receive() == b"hello"
    await peer.send(b"world")
    assert await client.receive() == b"world"


async def test_close_unblocks_peer_receive() -> None:
    client, peer = make_loopback_pair()
    await client.close()
    with pytest.raises(TransportClosed):
        await peer.receive()


async def test_frames_iterator_terminates_on_close() -> None:
    client, peer = make_loopback_pair()
    await client.send(b"a")
    await client.send(b"b")
    await client.close()
    collected = [frame async for frame in peer.frames()]
    assert collected == [b"a", b"b"]
