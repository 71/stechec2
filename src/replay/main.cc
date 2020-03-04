// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (c) 2019 Association Prologin <association@prologin.org>
#include <gflags/gflags.h>

#include "replay.hh"

int main(int argc, char** argv) {
    GFLAGS_NAMESPACE::ParseCommandLineFlags(&argc, &argv, true);

    Replay replay{};
    if (!replay.check()) return EXIT_FAILURE;
    replay.run();
    return EXIT_SUCCESS;
}
