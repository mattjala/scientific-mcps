#include "mcp_server.hpp"
#include <iostream>
#include <stdexcept>

namespace mcp {
    
    Server::Server(const std::string& name, const std::string& version) 
        : server_name_(name), server_version_(version), initialized_(false) {}
    
    void Server::register_tool(const std::string& name, const std::string& description, 
                              const json::Value& input_schema, ToolHandler handler) {
        tool_handlers_[name] = handler;
        tool_descriptions_[name] = description;
        tool_schemas_[name] = input_schema;
    }
    
    void Server::run() {
        std::string line;
        while (std::getline(std::cin, line)) {
            if (line.empty()) continue;
            
            try {
                json::Value request = json::parse(line);
                json::Value response = handle_request(request);
                
                if (!response.is_null()) {
                    write_line(json::stringify(response));
                }
            } catch (const std::exception& e) {
                json::Value error_response = create_error_response(-32700, "Parse error", json::Value());
                write_line(json::stringify(error_response));
            }
        }
    }
    
    json::Value Server::handle_request(const json::Value& request) {
        if (!request.is_object()) {
            return create_error_response(-32600, "Invalid Request", json::Value());
        }
        
        const auto& obj = request.as_object();
        
        // Check for required fields
        if (obj.find("jsonrpc") == obj.end() || obj.find("method") == obj.end()) {
            return create_error_response(-32600, "Invalid Request", json::Value());
        }
        
        if (!obj.at("jsonrpc").is_string() || obj.at("jsonrpc").as_string() != "2.0") {
            return create_error_response(-32600, "Invalid Request", json::Value());
        }
        
        if (!obj.at("method").is_string()) {
            return create_error_response(-32600, "Invalid Request", json::Value());
        }
        
        std::string method = obj.at("method").as_string();
        json::Value id = obj.find("id") != obj.end() ? obj.at("id") : json::Value();
        json::Value params = obj.find("params") != obj.end() ? obj.at("params") : json::Value();
        
        try {
            if (method == "initialize") {
                return create_success_response(handle_initialize(params), id);
            }
            
            if (!initialized_ && method != "initialize") {
                return create_error_response(-32002, "Server not initialized", id);
            }
            
            if (method == "notifications/initialized") {
                // Just acknowledge the notification
                return json::Value(); // No response for notifications
            }
            
            if (method == "tools/list") {
                return create_success_response(handle_tools_list(), id);
            }
            
            if (method == "tools/call") {
                return create_success_response(handle_tools_call(params), id);
            }
            
            return create_error_response(-32601, "Method not found", id);
        } catch (const std::exception& e) {
            return create_error_response(-32603, std::string("Internal error: ") + e.what(), id);
        }
    }
    
    json::Value Server::handle_initialize(const json::Value& params) {
        initialized_ = true;
        
        json::Value result;
        result["protocolVersion"] = "2024-11-05";
        
        json::Value capabilities;
        capabilities["tools"]["listChanged"] = true;
        capabilities["resources"]["subscribe"] = false;
        capabilities["resources"]["listChanged"] = false;
        capabilities["prompts"]["listChanged"] = false;
        capabilities["experimental"] = json::Value(json::Object{});
        
        result["capabilities"] = capabilities;
        
        json::Value server_info;
        server_info["name"] = server_name_;
        server_info["version"] = server_version_;
        
        result["serverInfo"] = server_info;
        
        return result;
    }
    
    json::Value Server::handle_tools_list() {
        json::Value result;
        json::Array tools;
        
        for (const auto& [name, handler] : tool_handlers_) {
            json::Value tool;
            tool["name"] = name;
            tool["description"] = tool_descriptions_[name];
            tool["inputSchema"] = tool_schemas_[name];
            
            json::Value output_schema;
            output_schema["type"] = "object";
            output_schema["additionalProperties"] = true;
            tool["outputSchema"] = output_schema;
            
            tools.push_back(tool);
        }
        
        result["tools"] = json::Value(tools);
        return result;
    }
    
    json::Value Server::handle_tools_call(const json::Value& params) {
        if (!params.is_object()) {
            throw std::runtime_error("Invalid params for tools/call");
        }
        
        const auto& obj = params.as_object();
        
        if (obj.find("name") == obj.end() || !obj.at("name").is_string()) {
            throw std::runtime_error("Missing or invalid tool name");
        }
        
        std::string tool_name = obj.at("name").as_string();
        
        if (tool_handlers_.find(tool_name) == tool_handlers_.end()) {
            throw std::runtime_error("Unknown tool: " + tool_name);
        }
        
        json::Value arguments = obj.find("arguments") != obj.end() ? obj.at("arguments") : json::Value();
        
        try {
            json::Value tool_result = tool_handlers_[tool_name](arguments);
            
            json::Value result;
            
            // Create content array
            json::Array content;
            json::Value content_item;
            content_item["type"] = "text";
            content_item["text"] = json::stringify(tool_result);
            content.push_back(content_item);
            
            result["content"] = json::Value(content);
            result["isError"] = false;
            result["structuredContent"] = tool_result;
            
            return result;
        } catch (const std::exception& e) {
            json::Value error_result;
            error_result["error"] = e.what();
            
            json::Array content;
            json::Value content_item;
            content_item["type"] = "text";
            content_item["text"] = json::stringify(error_result);
            content.push_back(content_item);
            
            json::Value result;
            result["content"] = json::Value(content);
            result["isError"] = false;
            result["structuredContent"] = error_result;
            
            return result;
        }
    }
    
    json::Value Server::create_error_response(int code, const std::string& message, const json::Value& id) {
        json::Value response;
        response["jsonrpc"] = "2.0";
        response["id"] = id;
        
        json::Value error;
        error["code"] = code;
        error["message"] = message;
        
        response["error"] = error;
        return response;
    }
    
    json::Value Server::create_success_response(const json::Value& result, const json::Value& id) {
        json::Value response;
        response["jsonrpc"] = "2.0";
        response["id"] = id;
        response["result"] = result;
        return response;
    }
    
    std::string Server::read_line() {
        std::string line;
        std::getline(std::cin, line);
        return line;
    }
    
    void Server::write_line(const std::string& line) {
        std::cout << line << std::endl;
        std::cout.flush();
    }
}