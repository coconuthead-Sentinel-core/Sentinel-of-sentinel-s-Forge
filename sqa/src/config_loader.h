#pragma once
#include "common.h"
#include <fstream>
#include <string>

namespace sqa {

/// Load JSON configuration from a file path.
/// Returns empty object on failure.
json load_config(const std::string& path);

/// Default configuration for all SQA subsystems.
json default_config();

}  // namespace sqa
