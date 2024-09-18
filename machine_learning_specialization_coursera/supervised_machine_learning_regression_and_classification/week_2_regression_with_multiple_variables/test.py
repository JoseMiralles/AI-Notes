# %% [markdown]
# # Vectorization
# 
# Vectorized code is a programming technique that performs mathematical operations on multiple components of a vector at once. Vectorized code can make code faster, more concise, and easier to maintain. It can also be more portable and clean. Vectorize code can improve performance when run in GPUs instead of CPUs.

# %% [markdown]
# ## Parameters and features
# 
# $b$ is a number.
# 
# $ \overrightarrow w = [w_1, w_2, w_3] $
# 
# $ \overrightarrow x = [x_1, x_2, x_3] $
# 
# These can be represented in Python using Numpy:

# %%
import numpy as np

b = 4
w = np.array([ 1.0, 2.5, -3.3 ])
x = np.array([ 10, 20, 30 ])

# %% [markdown]
# ## Running model without vectorization (Naive approach)
# 
# $ f _ {\overrightarrow w, b} ( \overrightarrow x ) = \sum\limits_{j = 1} ^ n w_j x_j + b$

# %%
n = len(w)
f = 0

for j in range (0, n):

    f = f + w[j] * x[j]

f = f + b

print(f'Prediction: {f * 1000}')

# %% [markdown]
# ## Running model with vectorization (Optimized approach)
# 
# $ f_{ \overrightarrow w, b } ( \overrightarrow x ) = \overrightarrow w \bullet \overrightarrow x + b$

# %%
f = 0
f = np.dot(w, x) + b

print(f'Prediction: {f * 1000}')

# %% [markdown]
# # Numpy data creation routines
# 
# 

# %%
# NumPy routines which allocate memory and fill arrays with value
a = np.zeros(4);                print(f"np.zeros(4) :   a = {a}, a shape = {a.shape}, a data type = {a.dtype}\n")
a = np.zeros((4,3));             print(f"np.zeros(4,3) :  \na =\n {a},\na shape = {a.shape}, a data type = {a.dtype}\n")
a = np.random.random_sample((4,3)); print(f"np.random.random_sample(4, 3): \na =\n {a},\n a shape = {a.shape}, a data type = {a.dtype}")

# %%
# Some data creation routines do not take a shape tuple:
# NumPy routines which allocate memory and fill arrays with value but do not accept shape as input argument
a = np.arange(4.);              print(f"np.arange(4.):     a = {a}, a shape = {a.shape}, a data type = {a.dtype}")
a = np.random.rand(4);          print(f"np.random.rand(4): a = {a}, a shape = {a.shape}, a data type = {a.dtype}")

# %%
# Values can be specified manually.
# NumPy routines which allocate memory and fill with user specified values
a = np.array([5,4,3,2]);  print(f"np.array([5,4,3,2]):  a = {a},     a shape = {a.shape}, a data type = {a.dtype}")
a = np.array([5.,4,3,2]); print(f"np.array([5.,4,3,2]): a = {a}, a shape = {a.shape}, a data type = {a.dtype}")

# %% [markdown]
# # Numpy operations on vectors

# %%
#vector indexing operations on 1-D vectors
a = np.arange(10)
print(a)

#access an element
print(f"a[2].shape: {a[2].shape} a[2]  = {a[2]}, Accessing an element returns a scalar")

# access the last element, negative indexes count from the end
print(f"a[-1] = {a[-1]}")

# %% [markdown]
# # Vector Slicing

# %%
#vector slicing operations
a = np.arange(10)
print(f"a         = {a}")

#access 5 consecutive elements (start:stop:step)
c = a[2:7:1];     print("a[2:7:1] = ", c)

# access 3 elements separated by two 
c = a[2:7:2];     print("a[2:7:2] = ", c)

# access all elements index 3 and above
c = a[3:];        print("a[3:]    = ", c)

# access all elements below index 3
c = a[:3];        print("a[:3]    = ", c)

# access all elements
c = a[:];         print("a[:]     = ", c)

# %% [markdown]
# # Single vector operations

# %%
a = np.array([1,2,3,4])
print(f"a             : {a}")
# negate elements of a
b = -a 
print(f"b = -a        : {b}")

# sum all elements of a, returns a scalar
b = np.sum(a) 
print(f"b = np.sum(a) : {b}")

b = np.mean(a)
print(f"b = np.mean(a): {b}")

b = a**2
print(f"b = a**2      : {b}")

# %% [markdown]
# ### Vector Vector element-wise operations

# %%
a = np.array([ 1, 2, 3, 4])
b = np.array([-1,-2, 3, 4])
print(f"Binary operators work element wise: {a + b}")

# Both arrays have to be of the same size.
c = np.array([1, 2])
try:
    d = a + c
except Exception as e:
    print(e)

# %% [markdown]
# ### Scalar Vector operations

# %%
a = np.array([1, 2, 3, 4])

# multiply a by a scalar
b = 5 * a 
print(f"b = 5 * a : {b}")

# %%



