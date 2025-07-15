#include "json.hpp"
#include <sstream>
#include <iomanip>
#include <stdexcept>
#include <functional>

namespace json {
    
    std::string Value::to_string() const {
        return stringify(*this);
    }
    
    // Simple JSON parser - handles basic types needed for MCP
    Value parse(const std::string& json_str) {
        size_t pos = 0;
        
        std::function<void()> skip_whitespace = [&]() {
            while (pos < json_str.length() && std::isspace(json_str[pos])) {
                pos++;
            }
        };
        
        std::function<Value()> parse_value = [&]() -> Value {
            skip_whitespace();
            
            if (pos >= json_str.length()) {
                throw std::runtime_error("Unexpected end of JSON");
            }
            
            char c = json_str[pos];
            
            if (c == 'n') {
                if (json_str.substr(pos, 4) == "null") {
                    pos += 4;
                    return Value();
                }
                throw std::runtime_error("Invalid null value");
            }
            
            if (c == 't') {
                if (json_str.substr(pos, 4) == "true") {
                    pos += 4;
                    return Value(true);
                }
                throw std::runtime_error("Invalid true value");
            }
            
            if (c == 'f') {
                if (json_str.substr(pos, 5) == "false") {
                    pos += 5;
                    return Value(false);
                }
                throw std::runtime_error("Invalid false value");
            }
            
            if (c == '"') {
                pos++; // Skip opening quote
                std::string str;
                while (pos < json_str.length() && json_str[pos] != '"') {
                    if (json_str[pos] == '\\') {
                        pos++;
                        if (pos >= json_str.length()) break;
                        switch (json_str[pos]) {
                            case 'n': str += '\n'; break;
                            case 't': str += '\t'; break;
                            case 'r': str += '\r'; break;
                            case '"': str += '"'; break;
                            case '\\': str += '\\'; break;
                            default: str += json_str[pos]; break;
                        }
                    } else {
                        str += json_str[pos];
                    }
                    pos++;
                }
                if (pos >= json_str.length()) {
                    throw std::runtime_error("Unterminated string");
                }
                pos++; // Skip closing quote
                return Value(str);
            }
            
            if (c == '[') {
                pos++; // Skip opening bracket
                Array arr;
                skip_whitespace();
                
                if (pos < json_str.length() && json_str[pos] == ']') {
                    pos++; // Skip closing bracket
                    return Value(arr);
                }
                
                while (pos < json_str.length()) {
                    arr.push_back(parse_value());
                    skip_whitespace();
                    
                    if (pos >= json_str.length()) break;
                    
                    if (json_str[pos] == ']') {
                        pos++; // Skip closing bracket
                        break;
                    }
                    
                    if (json_str[pos] == ',') {
                        pos++; // Skip comma
                        continue;
                    }
                    
                    throw std::runtime_error("Expected ',' or ']' in array");
                }
                
                return Value(arr);
            }
            
            if (c == '{') {
                pos++; // Skip opening brace
                Object obj;
                skip_whitespace();
                
                if (pos < json_str.length() && json_str[pos] == '}') {
                    pos++; // Skip closing brace
                    return Value(obj);
                }
                
                while (pos < json_str.length()) {
                    // Parse key
                    Value key = parse_value();
                    if (!key.is_string()) {
                        throw std::runtime_error("Object key must be string");
                    }
                    
                    skip_whitespace();
                    if (pos >= json_str.length() || json_str[pos] != ':') {
                        throw std::runtime_error("Expected ':' after object key");
                    }
                    pos++; // Skip colon
                    
                    // Parse value
                    Value value = parse_value();
                    obj[key.as_string()] = value;
                    
                    skip_whitespace();
                    if (pos >= json_str.length()) break;
                    
                    if (json_str[pos] == '}') {
                        pos++; // Skip closing brace
                        break;
                    }
                    
                    if (json_str[pos] == ',') {
                        pos++; // Skip comma
                        continue;
                    }
                    
                    throw std::runtime_error("Expected ',' or '}' in object");
                }
                
                return Value(obj);
            }
            
            // Parse number
            if (c == '-' || std::isdigit(c)) {
                std::string num_str;
                bool is_double = false;
                
                while (pos < json_str.length() && 
                       (std::isdigit(json_str[pos]) || json_str[pos] == '-' || 
                        json_str[pos] == '+' || json_str[pos] == '.' || 
                        json_str[pos] == 'e' || json_str[pos] == 'E')) {
                    if (json_str[pos] == '.' || json_str[pos] == 'e' || json_str[pos] == 'E') {
                        is_double = true;
                    }
                    num_str += json_str[pos];
                    pos++;
                }
                
                if (is_double) {
                    return Value(std::stod(num_str));
                } else {
                    return Value(std::stoi(num_str));
                }
            }
            
            throw std::runtime_error("Invalid JSON value");
        };
        
        return parse_value();
    }
    
    std::string stringify(const Value& value) {
        if (value.is_null()) {
            return "null";
        }
        
        if (value.is_bool()) {
            return value.as_bool() ? "true" : "false";
        }
        
        if (value.is_int()) {
            return std::to_string(value.as_int());
        }
        
        if (value.is_double()) {
            std::ostringstream oss;
            oss << std::fixed << std::setprecision(6) << value.as_double();
            return oss.str();
        }
        
        if (value.is_string()) {
            std::string result = "\"";
            for (char c : value.as_string()) {
                switch (c) {
                    case '"': result += "\\\""; break;
                    case '\\': result += "\\\\"; break;
                    case '\n': result += "\\n"; break;
                    case '\t': result += "\\t"; break;
                    case '\r': result += "\\r"; break;
                    default: result += c; break;
                }
            }
            result += "\"";
            return result;
        }
        
        if (value.is_array()) {
            std::string result = "[";
            const auto& arr = value.as_array();
            for (size_t i = 0; i < arr.size(); i++) {
                if (i > 0) result += ",";
                result += stringify(arr[i]);
            }
            result += "]";
            return result;
        }
        
        if (value.is_object()) {
            std::string result = "{";
            const auto& obj = value.as_object();
            bool first = true;
            for (const auto& [key, val] : obj) {
                if (!first) result += ",";
                first = false;
                result += stringify(Value(key)) + ":" + stringify(val);
            }
            result += "}";
            return result;
        }
        
        return "null";
    }
}