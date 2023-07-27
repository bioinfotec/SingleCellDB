# import rpy2.robjects as robjects

# # Define a Python function that calls an R function for linear regression
# def perform_linear_regression(x, y):
#     # Load the R library for linear regression
#     robjects.r('library(stats)')

#     # Convert Python lists to R vectors
#     x_r = robjects.FloatVector(x)
#     y_r = robjects.FloatVector(y)

#     # Call the R function for linear regression
#     lm_model = robjects.r('lm')(formula='y ~ x', data=robjects.DataFrame({'x': x_r, 'y': y_r}))

#     # Get the coefficients from the linear regression model
#     coefficients = lm_model.rx2('coefficients')

#     return coefficients

# if __name__ == "__main__":
#     # Sample data
#     x_data = [1.0, 2.0, 3.0, 4.0, 5.0]
#     y_data = [2.0, 4.0, 6.0, 8.0, 10.0]

#     # Call the Python function to perform linear regression
#     result = perform_linear_regression(x_data, y_data)

#     # Print the coefficients obtained from the linear regression
#     print(f"Intercept: {result[0]}")
#     print(f"Slope: {result[1]}")


from django.core.paginator import Paginator

objects = ['john', 'paul', 'george', 'ringo', 'jane', 'joe', 'jill', 'jack']
p = Paginator(objects, 2)
print(p)