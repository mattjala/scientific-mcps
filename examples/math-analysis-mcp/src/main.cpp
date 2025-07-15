#include "mcp_server.hpp"
#include "math_operations.hpp"
#include <iostream>
#include <stdexcept>

int main() {
    try {
        mcp::Server server("MathAnalysisMCP", "1.0.0");
        
        // Register statistical analysis tool
        json::Value stats_schema;
        stats_schema["type"] = "object";
        stats_schema["properties"]["data"]["type"] = "array";
        stats_schema["properties"]["data"]["items"]["type"] = "number";
        stats_schema["required"] = json::Value(json::Array{"data"});
        
        server.register_tool("calculate_statistics", 
            "Calculate comprehensive statistics (mean, median, mode, standard deviation, etc.) for a dataset",
            stats_schema,
            [](const json::Value& params) -> json::Value {
                if (!params.is_object() || params.as_object().find("data") == params.as_object().end()) {
                    throw std::runtime_error("Missing 'data' parameter");
                }
                
                std::vector<double> data = math_ops::json_to_vector(params.as_object().at("data"));
                math_ops::Statistics stats = math_ops::calculate_statistics(data);
                return math_ops::statistics_to_json(stats);
            }
        );
        
        // Register matrix multiplication tool
        json::Value matrix_mult_schema;
        matrix_mult_schema["type"] = "object";
        matrix_mult_schema["properties"]["matrix_a"]["type"] = "array";
        matrix_mult_schema["properties"]["matrix_b"]["type"] = "array";
        matrix_mult_schema["required"] = json::Value(json::Array{"matrix_a", "matrix_b"});
        
        server.register_tool("multiply_matrices",
            "Multiply two matrices using standard matrix multiplication",
            matrix_mult_schema,
            [](const json::Value& params) -> json::Value {
                if (!params.is_object()) {
                    throw std::runtime_error("Invalid parameters");
                }
                
                const auto& obj = params.as_object();
                if (obj.find("matrix_a") == obj.end() || obj.find("matrix_b") == obj.end()) {
                    throw std::runtime_error("Missing matrix parameters");
                }
                
                math_ops::Matrix a = math_ops::json_to_matrix(obj.at("matrix_a"));
                math_ops::Matrix b = math_ops::json_to_matrix(obj.at("matrix_b"));
                
                math_ops::Matrix result = math_ops::multiply_matrices(a, b);
                return math_ops::matrix_to_json(result);
            }
        );
        
        // Register matrix-vector multiplication tool
        json::Value matvec_schema;
        matvec_schema["type"] = "object";
        matvec_schema["properties"]["matrix"]["type"] = "array";
        matvec_schema["properties"]["vector"]["type"] = "array";
        matvec_schema["required"] = json::Value(json::Array{"matrix", "vector"});
        
        server.register_tool("multiply_matrix_vector",
            "Multiply a matrix by a vector",
            matvec_schema,
            [](const json::Value& params) -> json::Value {
                if (!params.is_object()) {
                    throw std::runtime_error("Invalid parameters");
                }
                
                const auto& obj = params.as_object();
                if (obj.find("matrix") == obj.end() || obj.find("vector") == obj.end()) {
                    throw std::runtime_error("Missing matrix or vector parameters");
                }
                
                math_ops::Matrix matrix = math_ops::json_to_matrix(obj.at("matrix"));
                math_ops::Vector vector = math_ops::json_to_vector(obj.at("vector"));
                
                math_ops::Vector result = math_ops::multiply_matrix_vector(matrix, vector);
                return math_ops::vector_to_json(result);
            }
        );
        
        // Register polynomial fitting tool
        json::Value polyfit_schema;
        polyfit_schema["type"] = "object";
        polyfit_schema["properties"]["x_values"]["type"] = "array";
        polyfit_schema["properties"]["y_values"]["type"] = "array";
        polyfit_schema["properties"]["degree"]["type"] = "integer";
        polyfit_schema["required"] = json::Value(json::Array{"x_values", "y_values", "degree"});
        
        server.register_tool("polynomial_fit",
            "Fit a polynomial of specified degree to data points using least squares",
            polyfit_schema,
            [](const json::Value& params) -> json::Value {
                if (!params.is_object()) {
                    throw std::runtime_error("Invalid parameters");
                }
                
                const auto& obj = params.as_object();
                if (obj.find("x_values") == obj.end() || obj.find("y_values") == obj.end() || 
                    obj.find("degree") == obj.end()) {
                    throw std::runtime_error("Missing required parameters");
                }
                
                std::vector<double> x = math_ops::json_to_vector(obj.at("x_values"));
                std::vector<double> y = math_ops::json_to_vector(obj.at("y_values"));
                
                int degree;
                if (obj.at("degree").is_int()) {
                    degree = obj.at("degree").as_int();
                } else {
                    throw std::runtime_error("Degree must be an integer");
                }
                
                std::vector<double> coefficients = math_ops::polynomial_fit(x, y, degree);
                
                json::Value result;
                result["coefficients"] = math_ops::vector_to_json(coefficients);
                result["degree"] = degree;
                result["equation"] = "y = ";
                
                // Build equation string
                std::string equation = "y = ";
                for (int i = coefficients.size() - 1; i >= 0; i--) {
                    if (i < (int)coefficients.size() - 1) {
                        equation += (coefficients[i] >= 0) ? " + " : " - ";
                        equation += std::to_string(std::abs(coefficients[i]));
                    } else {
                        equation += std::to_string(coefficients[i]);
                    }
                    
                    if (i > 1) {
                        equation += "x^" + std::to_string(i);
                    } else if (i == 1) {
                        equation += "x";
                    }
                }
                
                result["equation"] = equation;
                return result;
            }
        );
        
        // Register numerical differentiation tool
        json::Value diff_schema;
        diff_schema["type"] = "object";
        diff_schema["properties"]["y_values"]["type"] = "array";
        diff_schema["properties"]["step_size"]["type"] = "number";
        diff_schema["required"] = json::Value(json::Array{"y_values", "step_size"});
        
        server.register_tool("numerical_differentiate",
            "Compute numerical derivative of discrete data points",
            diff_schema,
            [](const json::Value& params) -> json::Value {
                if (!params.is_object()) {
                    throw std::runtime_error("Invalid parameters");
                }
                
                const auto& obj = params.as_object();
                if (obj.find("y_values") == obj.end() || obj.find("step_size") == obj.end()) {
                    throw std::runtime_error("Missing required parameters");
                }
                
                std::vector<double> y = math_ops::json_to_vector(obj.at("y_values"));
                
                double h;
                if (obj.at("step_size").is_double()) {
                    h = obj.at("step_size").as_double();
                } else if (obj.at("step_size").is_int()) {
                    h = obj.at("step_size").as_int();
                } else {
                    throw std::runtime_error("Step size must be a number");
                }
                
                math_ops::Vector derivative = math_ops::differentiate_numerical(y, h);
                
                json::Value result;
                result["derivative"] = math_ops::vector_to_json(derivative);
                result["step_size"] = h;
                result["points"] = (int)y.size();
                
                return result;
            }
        );
        
        // Run the server
        server.run();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}