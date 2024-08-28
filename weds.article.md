# A Dimwit’s Guide to Calculus Optimization Problem Mastery

As a mathematically challenged student of mathematics, I have found myself constantly tripped up by calculus optimization problems. After hours of banging my thick head against such problems, I have come up with a systematic approach that enables me to solve these pretty reliably.  This article presents that approach, and is targeted to those who have found themselves in the same boat as me: understanding the basic principles optimziation, able to successfully solve some problems, but still failing to consistently nail exam questions on the topic.

## What Are Optimization Problems?

Any time you have inputs into a process that can be measured in terms of some scalar value, and you want to find the value of those inputs which result in either the highest or lowest value possible, you are probably dealing with a problem that can be solved via optimization.

**Example Applications:**

- **Economics:** Business professionals might need to figure out the optimal price for a new product. Too high, and no one buys it; too low, and they sell at a loss.
- **Engineering:** An engineer might be tasked with the design of a container that holds the most volume with the least amount of material.
- **Machine Learning:** A data scientist might need to optimize the cost function of a machine learning model. The cost function measures the error between the predicted outputs and the actual data, and the goal is to minimize this error.

## Process Overview

The diagram below provides an overview of my approach to solving optimization problems. The terms **Constraint Expression** and **Objective Function** might not be commonly used in textbooks, but I think they are helpful concepts for framing the problem correctly before carrying out the mechanical steps of differentiation, setting the first derivative to zero and solving for the target variable, applying the second derivative test, etc.

To illustrate these concepts, let's consider a practical example: designing a poster where you want to minimize the amount of paper used. The poster must have a printed area of exactly 50 square inches, and there must be a 2-inch margin on each side (left and right) and a 4-inch margin on the top and bottom. In this context:

- The **Constraint Expression** captures the requirement that the printed area is fixed at 50 square inches. Specifically, this is given by:

```
xy = 50
```

where $x$ and $y$ are the width and height of the printed area, respectively.

- The **Objective Function** represents the total area of the paper, including the margins, which we want to minimize. Given the 2-inch margin on the sides and 4-inch margin on the top and bottom, the total dimensions of the paper are $x_{	ext{total}} = x + 4$ and $y_{	ext{total}} = y + 8$. The Objective Function is:

```
	ext{Area}_{	ext{paper}} = (x + 4) 	imes (y + 8)
```

## Solving the Paper Dimensions Example

To solve the problem of minimizing the total area of paper used for a poster with specific margin requirements, we’ll follow these steps:

### Step 1: Identify the Constraint Expression

As explained above, the constraint can be expressed using the general formula for the area of a rectangle:

```
xy = 50
```

where $x$ and $y$ are the width and height of the printed area, respectively.

### Step 2: Identify the Objective Function

The Objective Function, representing the total area of the paper including margins, is:

```
	ext{Area}_{	ext{paper}} = (x + 4) 	imes (y + 8)
```

### Step 3: Derive the Constrained Objective Function in Terms of One Variable

Using the constraint $y = rac{50}{x}$, we substitute into the Objective Function to express it in terms of $x$ only:

```
	ext{Area}_{	ext{paper}}(x) = (x + 4) 	imes \left(rac{50}{x} + 8ight)
```

This simplifies to:

```
	ext{Area}_{	ext{paper}}(x) = 8x + rac{200}{x} + 82
```

### Step 4: Differentiate the Constrained Objective Function

Now, differentiate the Constrained Objective Function with respect to $x$ to find the critical points. The derivative is:

```
rac{dA}{dx} = rac{d}{dx} \left(8x + rac{200}{x} + 82ight) = 8 - rac{200}{x^2}
```

### Step 5: Find Critical Points

To find the critical points, set the derivative equal to zero:

```
8 - rac{200}{x^2} = 0
```

Next, multiply both sides of the equation by $x^2$ to eliminate the denominator:

```
8x^2 - 200 = 0
```

Solve for $x$ using the quadratic formula:

```
x = \sqrt{rac{200}{8}} = \sqrt{25} = 5
```

This yields the critical point $x = 5$.

### Step 6: Apply the Second Derivative Test

To confirm that $x = 5$ is indeed a minimum, we apply the second derivative test. We first compute the second derivative of the Constrained Objective Function:

```
rac{d^2A}{dx^2} = rac{d}{dx} \left(8 - rac{200}{x^2}ight) = rac{400}{x^3}
```

Since $rac{400}{x^3}$ is positive for all positive $x$, the function is concave up at $x = 5$, confirming that this is a minimum.

### Step 7: Verify and Interpret the Solution

Substitute $x = 5$ back into the expression for $y$:

```
y = rac{50}{5} = 10
```

The total paper dimensions are:

- **Total width:** $x_{	ext{total}} = 5 + 4 = 9$
- **Total height:** $y_{	ext{total}} = 10 + 8 = 18$

This solution minimizes the total paper area while satisfying the printed area constraint.

## Applying the Method to Different Scenarios

Now that you understand the steps, let's apply the method to a series of increasingly complex optimization problems. These challenges will help reinforce the process and give you practice with different types of constraints and objective functions.

### Challenge 1: Minimize the Surface Area of a Cylinder

**Problem Statement:**

You are designing a cylindrical can that must hold exactly 500 cubic centimeters of liquid. You want to minimize the surface area of the can (including the top and bottom). What are the optimal dimensions for the can?

**Questions:**

1. What is the Objective Function for the surface area of the cylinder?
2. What is the Constraint Expression? Express it mathematically.
3. Using the Constraint Expression, rewrite the Objective Function in terms of a single variable.

### Challenge 2: Maximize the Volume of a Box with a Fixed Surface Area

**Problem Statement:**

You are constructing an open-top rectangular box with a square base. The material for the base costs $1 per square foot, and the material for the sides costs $2 per square foot. You have $100 to spend. What are the dimensions that maximize the volume of the box?

**Questions:**

1. What is the Objective Function for the volume of the box?
2. What is the Constraint Expression? Express it mathematically.
3. Using the Constraint Expression, rewrite the Objective Function in terms of a single variable.

### Challenge 3: Minimize the Cost of a Pipeline

**Problem Statement:**

A company needs to lay a pipeline from an oil rig located 10 miles offshore to a refinery on the coast 20 miles down the shore from the point closest to the rig. Laying the pipeline underwater costs $500,000 per mile, while laying it on land costs $300,000 per mile. What is the minimum cost to lay the pipeline?

**Questions:**

1. What is the Objective Function for the total cost of laying the pipeline?
2. What is the Constraint Expression? Express it mathematically.
3. Using the Constraint Expression, rewrite the Objective Function in terms of a single variable.

### Challenge 4: Minimize the Perimeter of a Fenced Area

**Problem Statement:**

You need to fence in a rectangular area of 1000 square feet that is adjacent to a long, straight wall. You only need to fence three sides of the rectangle (two parallel sides and one side perpendicular to the wall). What dimensions will minimize the length of the fence required?

**Questions:**

1. What is the Objective Function for the perimeter of the fence?
2. What is the Constraint Expression? Express it mathematically.
3. Using the Constraint Expression, rewrite the Objective Function in terms of a single variable.

## High-Level Solutions to Example Problems

Here are the high-level solutions to the example problems:

I won't bore you with the detailed steps because—to me at least—the hard part is the problem setup: correctly identifying the Constraint and Objective Functions, and finally, deriving the Constrained Objective Function in terms of one variable.

My other reason is that rather than giving you a fish, I'd rather teach you to fish. (You like fish, right?). So, what I suggest, if you can't work out the detailed solutions to the three problems below, is that you go *directly* to an AI chat application and ask for a solution.
