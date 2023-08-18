# from datetime import datetime

# a = [
#     (5, datetime(2023, 1, 4, 2, 34, 29, 400000), 'MIRZAPUR', 3, 1)
    
# ]

# b = [
#     (19, datetime(2023, 1, 3, 17, 8, 29, 400000), 'MIRZAPUR', 3, 1),
#     (22, datetime(2023, 1, 4, 14, 34, 29, 400000), 'MIRZAPUR', 3, 1),
#     (23, datetime(2023, 1, 4, 2, 51, 29, 400000), 'MIRZAPUR', 3, 1),
#     (5, datetime(2023, 1, 4, 2, 34, 29, 400000), 'MIRZAPUR', 3, 1)
# ]

# # Extract the tuples from list 'a'
# tuples_a = set(a)

# # Remove matching tuples from list 'b'
# b = [item for item in b if item not in tuples_a]

# print(b)
from datetime import datetime

a = (
    5,
    datetime(2023, 1, 4, 2, 34, 29, 400000),
    1,
    'MIRZAPUR',
    3
)

b = [
    (19, datetime(2023, 1, 3, 17, 8, 29, 400000), 'MIRZAPUR', 3, 1),
    (22, datetime(2023, 1, 4, 14, 34, 29, 400000), 'MIRZAPUR', 3, 1),
    (23, datetime(2023, 1, 4, 2, 51, 29, 400000), 'MIRZAPUR', 3, 1),
    (5, datetime(2023, 1, 4, 2, 14, 29, 400000), 'MIRZAPUR', 3, 1)
]

output = [item for item in b if item[0] != a[0]]
print(output)
h = 