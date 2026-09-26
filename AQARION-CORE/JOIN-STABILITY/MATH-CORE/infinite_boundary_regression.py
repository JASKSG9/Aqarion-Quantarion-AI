"""
INFINITE BOUNDARY REGRESSION
Implementation for AQARION Join Stability Framework
Version 2.0 - 2026-09-25

This module implements regression analysis for infinite boundary conditions
in join operations, with proper handling of asymptotic behavior and
convergence rates.
"""

import numpy as np
from scipy.optimize import minimize, curve_fit
from scipy.integrate import quad
import warnings

warnings.filterwarnings('ignore')


class InfiniteBoundaryRegression:
    """
    Performs regression analysis on infinite boundary conditions.
    
    Attributes:
        x_data: Input data points
        y_data: Output data points
        decay_rate: Estimated decay rate α
        asymptotic_value: Estimated φ_∞(y)
        coefficients: Regression coefficients
    """
    
    def __init__(self, x_data, y_data):
        """
        Initialize regression with data.
        
        Args:
            x_data: Array of x values
            y_data: Array of y values
        """
        self.x_data = np.asarray(x_data)
        self.y_data = np.asarray(y_data)
        self.decay_rate = None
        self.asymptotic_value = None
        self.coefficients = None
        self.residuals = None
        
    def estimate_asymptotic_value(self):
        """
        Estimate φ_∞(y) from data.
        
        Returns:
            Estimated asymptotic value
        """
        # Use mean of largest x values as estimate
        n = len(self.x_data)
        tail_size = max(5, int(0.1 * n))
        
        sorted_indices = np.argsort(self.x_data)
        tail_indices = sorted_indices[-tail_size:]
        
        self.asymptotic_value = np.mean(self.y_data[tail_indices])
        return self.asymptotic_value
    
    def estimate_decay_rate(self):
        """
        Estimate decay rate α using exponential regression.
        
        Returns:
            Estimated decay rate
        """
        self.estimate_asymptotic_value()
        
        # Transform data: y - φ_∞ = C * exp(-α*x)
        y_centered = self.y_data - self.asymptotic_value
        
        # Filter positive values
        mask = y_centered > 0
        x_filtered = self.x_data[mask]
        y_filtered = y_centered[mask]
        
        if len(x_filtered) < 2:
            self.decay_rate = 1.0
            return self.decay_rate
        
        # Log transform: log(y - φ_∞) = log(C) - α*x
        log_y = np.log(np.abs(y_filtered) + 1e-10)
        
        # Linear regression on log scale
        coeffs = np.polyfit(x_filtered, log_y, 1)
        self.decay_rate = -coeffs[0]
        
        return self.decay_rate
    
    def exponential_model(self, x, C, alpha):
        """
        Exponential decay model: φ(x) = φ_∞ + C * exp(-α*x)
        
        Args:
            x: Input value
            C: Amplitude coefficient
            alpha: Decay rate
            
        Returns:
            Model prediction
        """
        return self.asymptotic_value + C * np.exp(-alpha * x)
    
    def fit_exponential(self):
        """
        Fit exponential decay model to data.
        
        Returns:
            Tuple of (C, alpha) coefficients
        """
        self.estimate_decay_rate()
        
        # Initial guess
        y_diff = self.y_data[0] - self.asymptotic_value
        C0 = y_diff if y_diff > 0 else 1.0
        alpha0 = self.decay_rate if self.decay_rate > 0 else 1.0
        
        try:
            popt, _ = curve_fit(
                self.exponential_model,
                self.x_data,
                self.y_data,
                p0=[C0, alpha0],
                maxfev=5000
            )
            self.coefficients = popt
            self.residuals = self.y_data - self.exponential_model(
                self.x_data, *popt
            )
            return popt
        except Exception as e:
            print(f"Fit failed: {e}")
            return None
    
    def polynomial_model(self, x, coeffs):
        """
        Polynomial decay model.
        
        Args:
            x: Input value
            coeffs: Polynomial coefficients
            
        Returns:
            Model prediction
        """
        return self.asymptotic_value + np.sum([
            c * (x ** (-i)) for i, c in enumerate(coeffs)
        ])
    
    def fit_polynomial(self, degree=2):
        """
        Fit polynomial decay model.
        
        Args:
            degree: Degree of polynomial decay
            
        Returns:
            Polynomial coefficients
        """
        self.estimate_asymptotic_value()
        
        # Transform: (y - φ_∞) = sum(c_i * x^(-i))
        y_centered = self.y_data - self.asymptotic_value
        
        # Create design matrix
        X = np.column_stack([self.x_data ** (-i) for i in range(1, degree + 1)])
        
        # Solve least squares
        coeffs, _, _, _ = np.linalg.lstsq(X, y_centered, rcond=None)
        self.coefficients = coeffs
        
        return coeffs
    
    def predict(self, x_new, model='exponential'):
        """
        Make predictions on new data.
        
        Args:
            x_new: New input values
            model: 'exponential' or 'polynomial'
            
        Returns:
            Predicted values
        """
        if self.coefficients is None:
            if model == 'exponential':
                self.fit_exponential()
            else:
                self.fit_polynomial()
        
        x_new = np.asarray(x_new)
        
        if model == 'exponential':
            return self.exponential_model(x_new, *self.coefficients)
        else:
            return np.array([
                self.polynomial_model(x, self.coefficients) for x in x_new
            ])
    
    def compute_error_bound(self):
        """
        Compute error bound for predictions.
        
        Returns:
            Error bound estimate
        """
        if self.residuals is None:
            return None
        
        rmse = np.sqrt(np.mean(self.residuals ** 2))
        return rmse
    
    def convergence_rate(self):
        """
        Estimate convergence rate.
        
        Returns:
            Convergence rate (decay exponent)
        """
        if self.decay_rate is not None:
            return self.decay_rate
        else:
            self.estimate_decay_rate()
            return self.decay_rate
    
    def summary(self):
        """
        Print summary of regression results.
        """
        print("=" * 60)
        print("INFINITE BOUNDARY REGRESSION SUMMARY")
        print("=" * 60)
        print(f"Data points: {len(self.x_data)}")
        print(f"X range: [{self.x_data.min():.4f}, {self.x_data.max():.4f}]")
        print(f"Y range: [{self.y_data.min():.4f}, {self.y_data.max():.4f}]")
        print(f"\nAsymptotic value (φ_∞): {self.asymptotic_value:.6f}")
        print(f"Decay rate (α): {self.decay_rate:.6f}")
        
        if self.coefficients is not None:
            print(f"Coefficients: {self.coefficients}")
        
        if self.residuals is not None:
            rmse = np.sqrt(np.mean(self.residuals ** 2))
            print(f"RMSE: {rmse:.6e}")
            print(f"R²: {1 - np.var(self.residuals)/np.var(self.y_data):.6f}")
        
        print("=" * 60)


# Example usage
if __name__ == "__main__":
    # Generate synthetic data with exponential decay
    x = np.linspace(0, 10, 100)
    y_true = 5.0 + 2.0 * np.exp(-0.5 * x)
    y = y_true + np.random.normal(0, 0.1, len(x))
    
    # Perform regression
    regressor = InfiniteBoundaryRegression(x, y)
    regressor.fit_exponential()
    regressor.summary()
    
    # Make predictions
    x_new = np.array([15, 20, 25])
    predictions = regressor.predict(x_new)
    print(f"\nPredictions at x={x_new}: {predictions}")
