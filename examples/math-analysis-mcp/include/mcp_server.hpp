#pragma once
#include <string>
#include <map>
#include <functional>
#include "json.hpp"

namespace mcp {
    
    class Server {
    public:
        using ToolHandler = std::function<json::Value(const json::Value& params)>;
        
        Server(const std::string& name, const std::string& version);
        
        void register_tool(const std::string& name, const std::string& description, 
                          const json::Value& input_schema, ToolHandler handler);
        
        void run();
        
    private:
        std::string server_name_;
        std::string server_version_;
        std::map<std::string, ToolHandler> tool_handlers_;
        std::map<std::string, std::string> tool_descriptions_;
        std::map<std::string, json::Value> tool_schemas_;
        bool initialized_;
        
        json::Value handle_request(const json::Value& request);
        json::Value handle_initialize(const json::Value& params);
        json::Value handle_tools_list();
        json::Value handle_tools_call(const json::Value& params);
        
        json::Value create_error_response(int code, const std::string& message, const json::Value& id = json::Value());
        json::Value create_success_response(const json::Value& result, const json::Value& id);
        
        std::string read_line();
        void write_line(const std::string& line);
    };
    
}