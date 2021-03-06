# -*- coding: utf-8 -*-
# Copyright 2016 Nick Boultbee
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

from quodlibet import _
from quodlibet.order import Order


class Repeat(Order):
    """Repeat, in some way, over a supplied `Order`"""

    def __init__(self, wrapped):
        super(Repeat, self).__init__()
        assert isinstance(wrapped, Order)
        self.wrapped = wrapped

    def next(self, playlist, iter):
        raise NotImplementedError

    def set(self, playlist, iter):
        return self.wrapped.set(playlist, iter)

    def previous(self, playlist, iter):
        return self.wrapped.previous(playlist, iter)

    def reset(self, playlist):
        return self.wrapped.reset(playlist)

    def __str__(self):
        return "<%s ∘ %s>" % (self.display_name, self.wrapped.display_name)


class RepeatSongForever(Repeat):
    """Repeats the same song forever (aka "repeat one").
    Explicit next calls will "break out" of the repeat
    which is probably what the user wanted"""

    name = "repeat_song"
    display_name = _("Repeat track")
    accelerated_name = _("Repeat track")

    def next(self, playlist, iter):
        return iter

    def next_explicit(self, playlist, iter):
        return self.wrapped.next_explicit(playlist, iter)


class RepeatListForever(Repeat):
    """Repeats the playlist forever once it's finished"""

    name = "repeat_all"
    display_name = _("Repeat all")
    accelerated_name = _("Repeat all")

    def next(self, playlist, iter):
        next = self.wrapped.next(playlist, iter)
        if next:
            return next
        self.wrapped.reset(playlist)
        return playlist.get_iter_first()
