// SPDX-License-Identifier: GPL-2.0-or-later
#include <stdlib.h>

#include "actions.hh"
#include "api.hh"

// global used in interface.cc
Api* api;

Api::Api(GameState* game_state, rules::Player_sptr player)
    : game_state_(game_state), player_(player)
{
    api = this;
}

// @@GEN_HERE@@
