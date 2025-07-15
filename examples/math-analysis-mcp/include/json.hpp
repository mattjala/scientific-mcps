#pragma once
#include <string>
#include <map>
#include <vector>
#include <variant>
#include <memory>

namespace json {
    class Value;
    
    using Object = std::map<std::string, Value>;
    using Array = std::vector<Value>;
    using Null = std::nullptr_t;
    
    class Value {
    public:
        using ValueType = std::variant<Null, bool, int, double, std::string, Array, Object>;
        
        Value() : value_(nullptr) {}
        Value(bool v) : value_(v) {}
        Value(int v) : value_(v) {}
        Value(double v) : value_(v) {}
        Value(const std::string& v) : value_(v) {}
        Value(const char* v) : value_(std::string(v)) {}
        Value(const Array& v) : value_(v) {}
        Value(const Object& v) : value_(v) {}
        
        bool is_null() const { return std::holds_alternative<Null>(value_); }
        bool is_bool() const { return std::holds_alternative<bool>(value_); }
        bool is_int() const { return std::holds_alternative<int>(value_); }
        bool is_double() const { return std::holds_alternative<double>(value_); }
        bool is_string() const { return std::holds_alternative<std::string>(value_); }
        bool is_array() const { return std::holds_alternative<Array>(value_); }
        bool is_object() const { return std::holds_alternative<Object>(value_); }
        
        bool as_bool() const { return std::get<bool>(value_); }
        int as_int() const { return std::get<int>(value_); }
        double as_double() const { return std::get<double>(value_); }
        const std::string& as_string() const { return std::get<std::string>(value_); }
        const Array& as_array() const { return std::get<Array>(value_); }
        const Object& as_object() const { return std::get<Object>(value_); }
        
        Array& as_array() { return std::get<Array>(value_); }
        Object& as_object() { return std::get<Object>(value_); }
        
        Value& operator[](const std::string& key) {
            if (!is_object()) {
                value_ = Object{};
            }
            return std::get<Object>(value_)[key];
        }
        
        Value& operator[](size_t index) {
            if (!is_array()) {
                value_ = Array{};
            }
            auto& arr = std::get<Array>(value_);
            if (index >= arr.size()) {
                arr.resize(index + 1);
            }
            return arr[index];
        }
        
        std::string to_string() const;
        
    private:
        ValueType value_;
    };
    
    Value parse(const std::string& json_str);
    std::string stringify(const Value& value);
}