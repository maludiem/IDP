#pragma once

#include <type_traits>
#include <typeinfo>
#include <boost/property_tree/ptree.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace JGSL {
namespace PARAMETER {

boost::property_tree::ptree pt;

template <class T>
void Set(std::string key, T value) { pt.put(key, value); }

template <class T>
T Get(std::string key, T default_value) { return pt.get(key, default_value); }

// 添加函数重载，支持不同模型的参数设置和获取
template <class T>
void SetModelParameter(std::string model_name, std::string key, T value) {
    // 可以根据模型名称设置不同的参数
    std::string model_key = model_name + "." + key;
    pt.put(model_key, value);
}

template <class T>
T GetModelParameter(std::string model_name, std::string key, T default_value) {
    // 可以根据模型名称获取不同的参数
    std::string model_key = model_name + "." + key;
    return pt.get(model_key, default_value);
}

void Export(py::module &m) {
    m.def("Set_Parameter", &Set<bool>);
    m.def("Set_Parameter", &Set<int>);
    m.def("Set_Parameter", &Set<float>);
    m.def("Set_Parameter", &Set<double>);
    m.def("Set_Parameter", &Set<std::string>);
    m.def("Get_Parameter", &Get<bool>);
    m.def("Get_Parameter", &Get<int>);
    m.def("Get_Parameter", &Get<float>);
    m.def("Get_Parameter", &Get<double>);
    m.def("Get_Parameter", &Get<std::string>);

    // 添加导出函数来支持不同模型的参数设置和获取
    m.def("Set_Model_Parameter", &SetModelParameter<bool>);
    m.def("Set_Model_Parameter", &SetModelParameter<int>);
    m.def("Set_Model_Parameter", &SetModelParameter<float>);
    m.def("Set_Model_Parameter", &SetModelParameter<double>);
    m.def("Set_Model_Parameter", &SetModelParameter<std::string>);
    m.def("Get_Model_Parameter", &GetModelParameter<bool>);
    m.def("Get_Model_Parameter", &GetModelParameter<int>);
    m.def("Get_Model_Parameter", &GetModelParameter<float>);
    m.def("Get_Model_Parameter", &GetModelParameter<double>);
    m.def("Get_Model_Parameter", &GetModelParameter<std::string>);
}
}
}