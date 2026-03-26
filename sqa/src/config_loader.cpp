#include "config_loader.h"
#include <spdlog/spdlog.h>

namespace sqa {

json load_config(const std::string& path) {
    try {
        std::ifstream f(path);
        if (!f.is_open()) {
            spdlog::warn("Config file not found: {}, using defaults", path);
            return default_config();
        }
        return json::parse(f);
    } catch (const std::exception& e) {
        spdlog::error("Failed to parse config {}: {}", path, e.what());
        return default_config();
    }
}

json default_config() {
    return json{
        {"global", {
            {"logLevel", "INFO"},
            {"version", "8.0.0"}
        }},
        {"cno", {
            {"appraisalEngine", {
                {"enable", true},
                {"weights", {
                    {"novelty", 0.8},
                    {"relevance", 1.0},
                    {"congruence", 1.0},
                    {"agency", 0.5},
                    {"coping", 0.7}
                }}
            }},
            {"symbolicRules", json::array({
                {{"pattern", "error"},     {"tag", "tag:anomaly"}},
                {{"pattern", "stress"},    {"tag", "tag:load"}},
                {{"pattern", "final"},     {"tag", "tag:validation"}},
                {{"pattern", "quantum"},   {"tag", "tag:domain.quantum"}},
                {{"pattern", "cognition"}, {"tag", "tag:domain.cognition"}}
            })}
        }},
        {"a1fs", {
            {"capacity", 1024},
            {"consolidation", {
                {"intervalSeconds", 3600},
                {"decayRate", 0.02},
                {"archiveThreshold", 0.05}
            }},
            {"graphBackend", "embedded"}
        }},
        {"nns", {
            {"parallelNodes", 4},
            {"maxFeedbackIterations", 3}
        }}
    };
}

}  // namespace sqa
