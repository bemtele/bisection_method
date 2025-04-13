import sympy as sp
import numpy as np

def find_valid_bounds(func, x_l, x_u, tolerance):
    valid_bounds = []
    for lower in range(int(x_l), int(x_u)):
        for upper in range(lower + 1, int(x_u) + 1):
            if func(lower) * func(upper) < 0:
                # Calculate iterations required for convergence
                iterations = int(np.ceil(np.log2((upper - lower) / (tolerance / 100))))
                valid_bounds.append((lower, upper, func(lower), func(upper), iterations))
    return valid_bounds


def bisection_method(func, initial_x_l, initial_x_u, tolerance_percent):
    print("\n**Performing Calculations**")
    print(f"Initial bounds: x_l = {initial_x_l}, x_u = {initial_x_u}, Tolerance = {tolerance_percent}%\n")

    x_l, x_u = initial_x_l, initial_x_u
    iteration = 1
    error = float('inf')  # Initialize error as infinity
    prev_midpoint = None  # To calculate error

    print("Detailed Calculations:\n")
    while error > tolerance_percent:
        midpoint = (x_l + x_u) / 2
        f_x_l = func(x_l)
        f_midpoint = func(midpoint)
        f_x_u = func(x_u)

        # Determine the next bounds
        product_l_mid = f_x_l * f_midpoint
        product_u_mid = f_x_u * f_midpoint

        if product_l_mid < 0:
            x_u = midpoint
            next_interval = "f(x_l)f(Midpoint) < 0 -> x_u = Midpoint"
        elif product_u_mid < 0:
            x_l = midpoint
            next_interval = "f(x_u)f(Midpoint) < 0 -> x_l = Midpoint"
        else:
            break  # Exact root found

        # Calculate error
        if prev_midpoint is not None:
            error = abs((midpoint - prev_midpoint) / midpoint) * 100

        # Print detailed step-by-step calculations
        print(f"Iteration {iteration}:")
        print(f"    Midpoint = ({x_l} + {x_u}) / 2 = {midpoint}")
        print(f"    f(Midpoint) = f({midpoint}) = {f_midpoint}")
        print(f"    f(x_l)f(Midpoint) = {f_x_l} * {f_midpoint} = {product_l_mid}")
        print(f"    f(x_u)f(Midpoint) = {f_x_u} * {f_midpoint} = {product_u_mid}")
        print(f"    {next_interval}")
        if prev_midpoint is not None:
            print(f"    Error = |({midpoint} - {prev_midpoint}) / {midpoint}| * 100 = {error}\n")
        else:
            print("    Error = N/A (first iteration)\n")

        # Update iteration variables
        prev_midpoint = midpoint
        iteration += 1

    # Table header
    print("\n**Results Table**")
    print(f"{'Iteration':<12}{'Lower':<15}{'Upper':<15}{'Midpoint':<15}{'Error (%)':<20}{'f(Midpoint)':<20}")
    print("-" * 85)

    # Reset variables for table
    x_l, x_u = initial_x_l, initial_x_u  # Reset bounds to the original values
    iteration = 1
    error = float('inf')  # Reset error
    prev_midpoint = None  # Reset midpoint for error calculation

    while error > tolerance_percent:
        midpoint = (x_l + x_u) / 2
        f_midpoint = func(midpoint)

        if func(x_l) * f_midpoint < 0:
            x_u = midpoint
        else:
            x_l = midpoint

        if prev_midpoint is not None:
            error = abs((midpoint - prev_midpoint) / midpoint) * 100

        # Print the results
        print(f"{iteration:<12}{x_l:<15.6f}{x_u:<15.6f}{midpoint:<15.6f}{(f'{error:.6f}' if prev_midpoint else 'N/A'):<20}{f_midpoint:<20.6f}")
        prev_midpoint = midpoint
        iteration += 1

    print("\nRoot found:", midpoint)

def main():
    print("Welcome to the Bisection Method Calculator by Boateng Oduro!")

    while True:
        # Get the function from the user
        x = sp.Symbol('x')
        func_expr = sp.sympify(input("\nEnter the function (e.g., x**3 - 3*x + 4): "))
        func = sp.lambdify(x, func_expr, 'numpy')

        # Get tolerance, bounds
        tolerance_percent = float(input("Enter the tolerance (%): "))
        x_l = float(input("Enter the lower bound (x_l): "))
        x_u = float(input("Enter the upper bound (x_u): "))

        # Find valid bounds
        valid_bounds = find_valid_bounds(func, x_l, x_u, tolerance_percent)  # Pass tolerance here
        if not valid_bounds:
            print("No valid bounds found in the given range. Please try again.")
            continue

        # Display valid bounds with estimated iterations
        print("\nValid bounds found:")
        for i, (lower, upper, f_lower, f_upper, iterations) in enumerate(valid_bounds, 1):
            print(f"{i}. x_l = {lower}, x_u = {upper}, f(x_l) = {f_lower}, f(x_u) = {f_upper}, Estimated Iterations: {iterations}")

        # Select bounds
        selected = int(input(f"\nSelect a pair of bounds (1-{len(valid_bounds)}) to proceed: ")) - 1
        x_l, x_u = valid_bounds[selected][:2]

        # Perform bisection method
        bisection_method(func, x_l, x_u, tolerance_percent)

        # Ask if the user wants to solve for another function
        another = input("\nDo you want to solve for another function? (yes/no): ").strip().lower()
        if another != 'yes':
            print("Thank you for using the Bisection Method Calculator!")
            break


if __name__ == "__main__":
    main()
