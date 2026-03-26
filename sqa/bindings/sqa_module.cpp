/**
 * pybind11 module exposing the SQA v8.0 C++ core to Python.
 *
 * Imports as: import sqa_engine
 * Provides: CNO, A1FS, NNS, config loader.
 */
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "cno/cognitive_neural_overlay.h"
#include "a1fs/a1_filing_system.h"
#include "nns/nexus_node_stack.h"
#include "config_loader.h"

namespace py = pybind11;

/// Helper: convert nlohmann::json to Python dict via string round-trip.
static py::object json_to_py(const sqa::json& j) {
    py::module_ json_mod = py::module_::import("json");
    return json_mod.attr("loads")(j.dump());
}

/// Helper: convert Python dict to nlohmann::json via string round-trip.
static sqa::json py_to_json(const py::object& obj) {
    py::module_ json_mod = py::module_::import("json");
    std::string s = json_mod.attr("dumps")(obj).cast<std::string>();
    return sqa::json::parse(s);
}

PYBIND11_MODULE(sqa_engine, m) {
    m.doc() = "SQA v8.0 — Sentient Quantum Architecture C++ Core";

    // --- Config ---
    m.def("load_config", [](const std::string& path) {
        return json_to_py(sqa::load_config(path));
    }, "Load SQA configuration from JSON file");

    m.def("default_config", []() {
        return json_to_py(sqa::default_config());
    }, "Return default SQA configuration");

    // --- CognitiveStateSnapshot ---
    py::class_<sqa::CognitiveStateSnapshot>(m, "CognitiveStateSnapshot")
        .def(py::init<>())
        .def_readwrite("id", &sqa::CognitiveStateSnapshot::id)
        .def_readwrite("intent_label", &sqa::CognitiveStateSnapshot::intent_label)
        .def_readwrite("intent_score", &sqa::CognitiveStateSnapshot::intent_score)
        .def_readwrite("appraisal_valence", &sqa::CognitiveStateSnapshot::appraisal_valence)
        .def_readwrite("attention_weight", &sqa::CognitiveStateSnapshot::attention_weight)
        .def_readwrite("creativity_score", &sqa::CognitiveStateSnapshot::creativity_score)
        .def_readwrite("symbolic_tags", &sqa::CognitiveStateSnapshot::symbolic_tags)
        .def_readwrite("processing_ms", &sqa::CognitiveStateSnapshot::processing_ms)
        .def("to_dict", [](const sqa::CognitiveStateSnapshot& s) {
            sqa::json j;
            j["id"] = s.id;
            j["intent_label"] = s.intent_label;
            j["intent_score"] = s.intent_score;
            j["appraisal_valence"] = s.appraisal_valence;
            j["attention_weight"] = s.attention_weight;
            j["creativity_score"] = s.creativity_score;
            j["symbolic_tags"] = s.symbolic_tags;
            j["processing_ms"] = s.processing_ms;
            return json_to_py(j);
        });

    // --- CognitiveInput ---
    py::class_<sqa::CognitiveInput>(m, "CognitiveInput")
        .def(py::init<>())
        .def(py::init([](const std::string& id, const std::string& text) {
            sqa::CognitiveInput inp;
            inp.id = id;
            inp.text = text;
            return inp;
        }), py::arg("id"), py::arg("text"))
        .def_readwrite("id", &sqa::CognitiveInput::id)
        .def_readwrite("text", &sqa::CognitiveInput::text);

    // --- CNO ---
    py::class_<sqa::cno::CognitiveNeuralOverlay>(m, "CognitiveNeuralOverlay")
        .def(py::init<>())
        .def("configure", [](sqa::cno::CognitiveNeuralOverlay& self, py::dict cfg) {
            self.configure(py_to_json(cfg));
        })
        .def("process", &sqa::cno::CognitiveNeuralOverlay::process)
        .def("executions", &sqa::cno::CognitiveNeuralOverlay::executions)
        .def("get_rules", [](sqa::cno::CognitiveNeuralOverlay& self) {
            auto rules = self.symbolic().get_rules();
            py::list out;
            for (const auto& r : rules) {
                py::dict d;
                d["pattern"] = r.pattern;
                d["tag"] = r.tag;
                out.append(d);
            }
            return out;
        })
        .def("set_rules", [](sqa::cno::CognitiveNeuralOverlay& self, py::list rules) {
            std::vector<sqa::SymbolicRule> cpp_rules;
            for (auto& item : rules) {
                auto d = item.cast<py::dict>();
                cpp_rules.push_back({
                    d["pattern"].cast<std::string>(),
                    d["tag"].cast<std::string>()
                });
            }
            self.symbolic().set_rules(cpp_rules);
        });

    // --- A1FS ---
    py::class_<sqa::a1fs::A1FilingSystem>(m, "A1FilingSystem")
        .def(py::init<size_t>(), py::arg("capacity") = 1024)
        .def("configure", [](sqa::a1fs::A1FilingSystem& self, py::dict cfg) {
            self.configure(py_to_json(cfg));
        })
        .def("store_episodic", [](sqa::a1fs::A1FilingSystem& self,
                                   const std::string& text,
                                   const std::vector<std::string>& tags,
                                   py::dict metadata) {
            return self.store_episodic(text, tags, py_to_json(metadata));
        }, py::arg("text"), py::arg("tags") = std::vector<std::string>{},
           py::arg("metadata") = py::dict())
        .def("retrieve_similar", &sqa::a1fs::A1FilingSystem::retrieve_similar,
             py::arg("query"), py::arg("top_k") = 5)
        .def("strengthen", &sqa::a1fs::A1FilingSystem::strengthen,
             py::arg("id"), py::arg("amount") = 0.1)
        .def("link", &sqa::a1fs::A1FilingSystem::link,
             py::arg("source"), py::arg("target"),
             py::arg("type") = sqa::a1fs::RelationType::Associative,
             py::arg("weight") = 1.0)
        .def("consolidate", &sqa::a1fs::A1FilingSystem::consolidate)
        .def("snapshot", [](const sqa::a1fs::A1FilingSystem& self) {
            return json_to_py(self.snapshot());
        })
        .def("clear", &sqa::a1fs::A1FilingSystem::clear)
        .def("size", &sqa::a1fs::A1FilingSystem::size);

    // A1FS RelationType enum
    py::enum_<sqa::a1fs::RelationType>(m, "RelationType")
        .value("Causal", sqa::a1fs::RelationType::Causal)
        .value("Temporal", sqa::a1fs::RelationType::Temporal)
        .value("Semantic", sqa::a1fs::RelationType::Semantic)
        .value("Associative", sqa::a1fs::RelationType::Associative);

    // --- NNS ---
    py::class_<sqa::nns::TaskResult>(m, "TaskResult")
        .def(py::init<>())
        .def_readwrite("task_id", &sqa::nns::TaskResult::task_id)
        .def_readwrite("success", &sqa::nns::TaskResult::success)
        .def_readwrite("duration_ms", &sqa::nns::TaskResult::duration_ms)
        .def_readwrite("error", &sqa::nns::TaskResult::error)
        .def("to_dict", [](const sqa::nns::TaskResult& r) {
            sqa::json j;
            j["task_id"] = r.task_id;
            j["success"] = r.success;
            j["duration_ms"] = r.duration_ms;
            j["error"] = r.error;
            j["output"] = r.output;
            return json_to_py(j);
        });

    py::class_<sqa::nns::NexusNodeStack>(m, "NexusNodeStack")
        .def(py::init<>())
        .def("configure", [](sqa::nns::NexusNodeStack& self, py::dict cfg) {
            self.configure(py_to_json(cfg));
        })
        .def("add_node", [](sqa::nns::NexusNodeStack& self,
                             const std::string& id, py::function fn) {
            self.add_node(sqa::nns::ProcessingNode(id,
                [fn](const sqa::json& input) -> sqa::nns::TaskResult {
                    sqa::nns::TaskResult result;
                    try {
                        py::gil_scoped_acquire gil;
                        py::module_ json_mod = py::module_::import("json");
                        py::object py_input = json_mod.attr("loads")(input.dump());
                        py::object py_result = fn(py_input);
                        result.success = true;
                        std::string out_str = json_mod.attr("dumps")(py_result).cast<std::string>();
                        result.output = sqa::json::parse(out_str);
                    } catch (const std::exception& e) {
                        result.success = false;
                        result.error = e.what();
                    }
                    return result;
                }
            ));
        }, py::arg("id"), py::arg("fn"))
        .def("execute", [](sqa::nns::NexusNodeStack& self, py::dict input, bool parallel) {
            auto results = self.execute(py_to_json(input), parallel);
            py::list out;
            for (const auto& r : results) {
                py::dict d;
                d["task_id"] = r.task_id;
                d["success"] = r.success;
                d["duration_ms"] = r.duration_ms;
                d["error"] = r.error;
                py::module_ json_mod = py::module_::import("json");
                d["output"] = json_mod.attr("loads")(r.output.dump());
                out.append(d);
            }
            return out;
        }, py::arg("input"), py::arg("parallel") = true)
        .def("merge_results", [](const std::vector<sqa::nns::TaskResult>& results) {
            return json_to_py(sqa::nns::NexusNodeStack::merge_results(results));
        })
        .def("node_count", &sqa::nns::NexusNodeStack::node_count)
        .def("status", [](const sqa::nns::NexusNodeStack& self) {
            return json_to_py(self.status());
        });

    // --- Version ---
    m.attr("__version__") = "8.0.0";
    m.attr("__arch__") = "SQA v8.0 — CNO + A1FS + NNS";
}
