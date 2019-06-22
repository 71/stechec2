// SPDX-License-Identifier: GPL-2.0-or-later
// Copyright (c) 2012 Association Prologin <association@prologin.org>
#pragma once

#include <cstdint>
#include <list>
#include <memory>
#include <unordered_map>

#include <utils/buffer.hh>
#include <utils/log.hh>

#include "action.hh"

namespace rules {

class Actions
{
public:
    static constexpr size_t MAX_ACTIONS = 1024;

    // To handle unserialization of multiple Actions, we have to be able to
    // instantiate the corresponding objects
    void register_action(uint32_t action_id, ActionFactory action_factory);

    // Serialization/Unserialization
    void handle_buffer(utils::Buffer& buf);

    void add(IAction_sptr action)
    {
        if (actions_.size() >= MAX_ACTIONS)
            FATAL("Too many actions (>%d) sent during this turn.", MAX_ACTIONS);
        actions_.push_back(action);
    }

    void cancel() { actions_.pop_back(); }

    size_t size() const { return actions_.size(); }

    void clear() { actions_.clear(); }

    const IActionList& actions() const { return actions_; }

private:
    IActionList actions_;
    std::unordered_map<uint32_t, ActionFactory> action_factory_;
};

} // namespace rules
