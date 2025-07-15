#pragma once
#include <vector>
#include <string>
#include "json.hpp"

namespace math_ops {
    
    // Statistical operations
    struct Statistics {
        double mean;
        double median;
        double mode;
        double std_dev;
        double variance;
        double min;
        double max;
        double range;
        size_t count;
    };
    
    Statistics calculate_statistics(const std::vector<double>& data);
    
    // Linear algebra operations
    using Matrix = std::vector<std::vector<double>>;
    using Vector = std::vector<double>;
    
    Matrix multiply_matrices(const Matrix& a, const Matrix& b);
    Vector multiply_matrix_vector(const Matrix& m, const Vector& v);
    double dot_product(const Vector& a, const Vector& b);
    Matrix transpose(const Matrix& m);
    double determinant(const Matrix& m);
    
    // Numerical analysis
    double integrate_simpson(const std::vector<double>& y_values, double h);
    Vector differentiate_numerical(const std::vector<double>& y_values, double h);
    std::vector<double> polynomial_fit(const std::vector<double>& x, const std::vector<double>& y, int degree);
    
    // Utility functions
    json::Value statistics_to_json(const Statistics& stats);
    json::Value matrix_to_json(const Matrix& m);
    json::Value vector_to_json(const Vector& v);
    
    Matrix json_to_matrix(const json::Value& json_val);
    Vector json_to_vector(const json::Value& json_val);
}