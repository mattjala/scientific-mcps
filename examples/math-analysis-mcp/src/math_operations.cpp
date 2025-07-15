#include "math_operations.hpp"
#include <algorithm>
#include <cmath>
#include <numeric>
#include <stdexcept>
#include <map>

namespace math_ops {
    
    Statistics calculate_statistics(const std::vector<double>& data) {
        if (data.empty()) {
            throw std::runtime_error("Cannot calculate statistics for empty dataset");
        }
        
        Statistics stats;
        stats.count = data.size();
        
        // Calculate mean
        stats.mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();
        
        // Calculate variance and standard deviation
        double variance_sum = 0.0;
        for (double val : data) {
            variance_sum += (val - stats.mean) * (val - stats.mean);
        }
        stats.variance = variance_sum / data.size();
        stats.std_dev = std::sqrt(stats.variance);
        
        // Calculate min and max
        auto minmax = std::minmax_element(data.begin(), data.end());
        stats.min = *minmax.first;
        stats.max = *minmax.second;
        stats.range = stats.max - stats.min;
        
        // Calculate median
        std::vector<double> sorted_data = data;
        std::sort(sorted_data.begin(), sorted_data.end());
        
        if (sorted_data.size() % 2 == 0) {
            stats.median = (sorted_data[sorted_data.size()/2 - 1] + sorted_data[sorted_data.size()/2]) / 2.0;
        } else {
            stats.median = sorted_data[sorted_data.size()/2];
        }
        
        // Calculate mode (most frequent value)
        std::map<double, int> frequency;
        for (double val : data) {
            frequency[val]++;
        }
        
        auto max_freq = std::max_element(frequency.begin(), frequency.end(),
            [](const auto& a, const auto& b) { return a.second < b.second; });
        stats.mode = max_freq->first;
        
        return stats;
    }
    
    Matrix multiply_matrices(const Matrix& a, const Matrix& b) {
        if (a.empty() || b.empty() || a[0].size() != b.size()) {
            throw std::runtime_error("Invalid matrix dimensions for multiplication");
        }
        
        size_t rows = a.size();
        size_t cols = b[0].size();
        size_t inner = a[0].size();
        
        Matrix result(rows, Vector(cols, 0.0));
        
        for (size_t i = 0; i < rows; i++) {
            for (size_t j = 0; j < cols; j++) {
                for (size_t k = 0; k < inner; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        
        return result;
    }
    
    Vector multiply_matrix_vector(const Matrix& m, const Vector& v) {
        if (m.empty() || m[0].size() != v.size()) {
            throw std::runtime_error("Invalid dimensions for matrix-vector multiplication");
        }
        
        Vector result(m.size(), 0.0);
        
        for (size_t i = 0; i < m.size(); i++) {
            for (size_t j = 0; j < v.size(); j++) {
                result[i] += m[i][j] * v[j];
            }
        }
        
        return result;
    }
    
    double dot_product(const Vector& a, const Vector& b) {
        if (a.size() != b.size()) {
            throw std::runtime_error("Vectors must have same size for dot product");
        }
        
        double result = 0.0;
        for (size_t i = 0; i < a.size(); i++) {
            result += a[i] * b[i];
        }
        
        return result;
    }
    
    Matrix transpose(const Matrix& m) {
        if (m.empty()) {
            return Matrix();
        }
        
        size_t rows = m[0].size();
        size_t cols = m.size();
        
        Matrix result(rows, Vector(cols));
        
        for (size_t i = 0; i < rows; i++) {
            for (size_t j = 0; j < cols; j++) {
                result[i][j] = m[j][i];
            }
        }
        
        return result;
    }
    
    double determinant(const Matrix& m) {
        if (m.empty() || m.size() != m[0].size()) {
            throw std::runtime_error("Matrix must be square for determinant");
        }
        
        size_t n = m.size();
        
        if (n == 1) {
            return m[0][0];
        }
        
        if (n == 2) {
            return m[0][0] * m[1][1] - m[0][1] * m[1][0];
        }
        
        // For larger matrices, use cofactor expansion
        double det = 0.0;
        for (size_t j = 0; j < n; j++) {
            // Create minor matrix
            Matrix minor(n-1, Vector(n-1));
            for (size_t r = 1; r < n; r++) {
                for (size_t c = 0, mc = 0; c < n; c++) {
                    if (c != j) {
                        minor[r-1][mc] = m[r][c];
                        mc++;
                    }
                }
            }
            
            double sign = (j % 2 == 0) ? 1.0 : -1.0;
            det += sign * m[0][j] * determinant(minor);
        }
        
        return det;
    }
    
    double integrate_simpson(const std::vector<double>& y_values, double h) {
        if (y_values.size() < 3 || y_values.size() % 2 == 0) {
            throw std::runtime_error("Simpson's rule requires odd number of points >= 3");
        }
        
        double result = y_values[0] + y_values[y_values.size() - 1];
        
        for (size_t i = 1; i < y_values.size() - 1; i++) {
            if (i % 2 == 1) {
                result += 4 * y_values[i];
            } else {
                result += 2 * y_values[i];
            }
        }
        
        return result * h / 3.0;
    }
    
    Vector differentiate_numerical(const std::vector<double>& y_values, double h) {
        if (y_values.size() < 2) {
            throw std::runtime_error("Need at least 2 points for differentiation");
        }
        
        Vector result(y_values.size());
        
        // Forward difference for first point
        result[0] = (y_values[1] - y_values[0]) / h;
        
        // Central difference for middle points
        for (size_t i = 1; i < y_values.size() - 1; i++) {
            result[i] = (y_values[i+1] - y_values[i-1]) / (2.0 * h);
        }
        
        // Backward difference for last point
        result[y_values.size() - 1] = (y_values[y_values.size() - 1] - y_values[y_values.size() - 2]) / h;
        
        return result;
    }
    
    std::vector<double> polynomial_fit(const std::vector<double>& x, const std::vector<double>& y, int degree) {
        if (x.size() != y.size() || x.size() < degree + 1) {
            throw std::runtime_error("Insufficient data points for polynomial fit");
        }
        
        size_t n = x.size();
        size_t m = degree + 1;
        
        // Create Vandermonde matrix
        Matrix A(n, Vector(m));
        for (size_t i = 0; i < n; i++) {
            for (size_t j = 0; j < m; j++) {
                A[i][j] = std::pow(x[i], j);
            }
        }
        
        // Solve normal equations: (A^T * A) * coeffs = A^T * y
        Matrix At = transpose(A);
        Matrix AtA = multiply_matrices(At, A);
        Vector Aty = multiply_matrix_vector(At, y);
        
        // Simple Gaussian elimination for square system
        std::vector<double> coeffs(m);
        Matrix augmented(m, Vector(m + 1));
        
        for (size_t i = 0; i < m; i++) {
            for (size_t j = 0; j < m; j++) {
                augmented[i][j] = AtA[i][j];
            }
            augmented[i][m] = Aty[i];
        }
        
        // Forward elimination
        for (size_t i = 0; i < m; i++) {
            for (size_t k = i + 1; k < m; k++) {
                if (augmented[i][i] != 0) {
                    double factor = augmented[k][i] / augmented[i][i];
                    for (size_t j = i; j < m + 1; j++) {
                        augmented[k][j] -= factor * augmented[i][j];
                    }
                }
            }
        }
        
        // Back substitution
        for (int i = m - 1; i >= 0; i--) {
            coeffs[i] = augmented[i][m];
            for (size_t j = i + 1; j < m; j++) {
                coeffs[i] -= augmented[i][j] * coeffs[j];
            }
            coeffs[i] /= augmented[i][i];
        }
        
        return coeffs;
    }
    
    json::Value statistics_to_json(const Statistics& stats) {
        json::Value result;
        result["mean"] = stats.mean;
        result["median"] = stats.median;
        result["mode"] = stats.mode;
        result["standard_deviation"] = stats.std_dev;
        result["variance"] = stats.variance;
        result["minimum"] = stats.min;
        result["maximum"] = stats.max;
        result["range"] = stats.range;
        result["count"] = (int)stats.count;
        return result;
    }
    
    json::Value matrix_to_json(const Matrix& m) {
        json::Array result;
        for (const auto& row : m) {
            json::Array json_row;
            for (double val : row) {
                json_row.push_back(json::Value(val));
            }
            result.push_back(json::Value(json_row));
        }
        return json::Value(result);
    }
    
    json::Value vector_to_json(const Vector& v) {
        json::Array result;
        for (double val : v) {
            result.push_back(json::Value(val));
        }
        return json::Value(result);
    }
    
    Matrix json_to_matrix(const json::Value& json_val) {
        if (!json_val.is_array()) {
            throw std::runtime_error("Expected array for matrix");
        }
        
        Matrix result;
        for (const auto& row_val : json_val.as_array()) {
            if (!row_val.is_array()) {
                throw std::runtime_error("Expected array for matrix row");
            }
            
            Vector row;
            for (const auto& val : row_val.as_array()) {
                if (val.is_int()) {
                    row.push_back(val.as_int());
                } else if (val.is_double()) {
                    row.push_back(val.as_double());
                } else {
                    throw std::runtime_error("Expected numeric value in matrix");
                }
            }
            result.push_back(row);
        }
        
        return result;
    }
    
    Vector json_to_vector(const json::Value& json_val) {
        if (!json_val.is_array()) {
            throw std::runtime_error("Expected array for vector");
        }
        
        Vector result;
        for (const auto& val : json_val.as_array()) {
            if (val.is_int()) {
                result.push_back(val.as_int());
            } else if (val.is_double()) {
                result.push_back(val.as_double());
            } else {
                throw std::runtime_error("Expected numeric value in vector");
            }
        }
        
        return result;
    }
}