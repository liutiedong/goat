import json
from itertools import combinations
from itertools import product
import random

# 4 digit 9000*9000
# select 400000 which is 0.5%
# x = 410000  # number of pairs to select
# nums = list(range(1000, 10000))  # list of all possible 4-digit numbers
# pairs = random.sample(list(combinations(nums, 2)), x)  # select x unique pairs at random

# nums = list(range(100000, 1000000)) 
# pairs = random.sample(list(answer(nums, repeat=2)), x) 

################
# 0512: 400000
# pairs = \
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(2,7) for j in range(i,13-i) for k in range(5000)] +\
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(4,7) for j in range(i,13-i) for k in range(10000)] +\
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(i-1)+1, 10**i-1)) for i in range(4,7) for k in range(10000)] +\
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(i-1)+1, 10**i-1)) for i in range(4,5) for k in range(10000)]
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(4,5) for j in range(8,9) for k in range(10000)]
# [(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(i-1)+1, 10**i-1)) for i in range(6,7) for k in range(10000)]

# 0519
pairs = \
[(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(2,7) for j in range(i,13-i) for k in range(10000)] +\
[(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(4,7) for j in range(i,13-i) for k in range(20000)] +\
[(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(j-1)+1, 10**j-1)) for i in range(5,7) for j in range(i,13-i) for k in range(20000)] +\
[(random.randint(10**(i-1)+1, 10**i-1), random.randint(10**(i-1)+1, 10**i-1)) for i in range(3,7) for k in range(20000)] 



random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size
print("Multi-digit Multiplication: ",train_size)
# "instruction": "3948 * 7994 = ",
# "cot": "3948 * (7000 + 900 + 90 + 4) = 3948 * 7000 + 3948 * 900 + 3948 * 90 + 3948 * 4 = 27636000 + 3553200 + 355320 + 15792 = ",
# "output": "31560312"

data = []

for num1, num2 in pairs:
    answer = num1 * num2
    
    if random.random() < 0.5:

        num1, num2 = num2, num1

    instruction = f"{num1} * {num2} = "

    
    if num2 > num1:
        num1, num2 = num2, num1

    num_digits_1 = len(str(num1))
    num_digits_2 = len(str(num2))

    if num1 % (10 ** (num_digits_1-1)) == 0 or num2 % (10 ** (num_digits_2-1)) == 0:
    	cot_add = instruction + str(answer)
    	cot_no_add = str(answer)
    	output_str = str(answer)

    else: 
	    num2_digits = [int(d) for d in str(num2)]

	    breakdown_terms = [d* 10**(len(num2_digits)-i-1) for i, d in enumerate(num2_digits) if d != 0]
	    breakdown = f"""{num1} * ({" + ".join(str(x) for x in breakdown_terms)})"""

	    distributive_law = " + ".join([f"{num1} * {x}" for x in breakdown_terms])
	    
	    summation_terms = [num1 * x for x in breakdown_terms]
	    summation = " + ".join(str(x) for x in summation_terms)


	    sum_result = sum(summation_terms)
	    assert(answer == sum_result)

	    cot_no_add = f"{breakdown} = {distributive_law} = {summation} = {sum_result}"

	    step = ""

	    while summation_terms:
	        first = summation_terms.pop(0)
	        if not summation_terms:
	            output = first
	            break
	        summation_terms[0] = first + summation_terms[0]
	        step = step + " + ".join([f"{x}" for x in summation_terms]) 
	        if len(summation_terms)>=2:
	            step = step + " = "

	    assert(output == answer)

	    output_str = str(sum_result)

	    cot = instruction + f"{breakdown} = {distributive_law} = {summation} = "
	    cot_add = cot + step

    data.append({"question": instruction, "cot": cot_add, "answer": output_str, "type": "mul_nxm"})



with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)

############### no. of sample okay!
# previous
# pairs = \
# [(random.randint(0, 10**i), random.randint(0, 10**j)) for i in range(1,13) for j in range(1,13) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(3,9) for j in range(9,13) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(9,13) for j in range(9,13) for k in range(2000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(11,13) for j in range(11,13) for k in range(2000)]

# # 0512
# pairs = \
# [(random.randint(0, 10**i), random.randint(0, 10**j)) for i in range(1,17) for j in range(1,17) for k in range(500)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(1,10) for j in range(10,17) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(6,12) for j in range(12,17) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(12,17) for j in range(12,17) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(15,17) for j in range(15,17) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(6,7) for j in range(6,7) for k in range(5000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(12,13) for j in range(12,13) for k in range(5000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(12,13) for j in range(16,17) for k in range(5000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(16,17) for j in range(16,17) for k in range(5000)]

# 0519
pairs = \
[(random.randint(0, 10**i), random.randint(0, 10**j)) for i in range(1,16) for j in range(i,16) for k in range(1000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(3,16) for j in range(i,16) for k in range(2000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(6,16) for j in range(i,16) for k in range(3000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(9,16) for j in range(i,16) for k in range(3000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(12,16) for j in range(i,16) for k in range(3000)] 

random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size

print("Addition: ",train_size)
pairs_train = pairs[:train_size]

pairs_test = pairs[train_size:]

data = []

for num1, num2 in pairs:

    answer = num1 + num2

    if random.random()<0.5:
        num1, num2 = num2, num1  
    
    instruction = f"{num1} + {num2} = " 
    cot = f"{num1} + {num2} = {answer}"
    output = str(answer)


    data.append({"question": instruction, "cot": cot, "answer": output, "type": "add"})


with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)


#######
# pairs = \
# [(random.randint(0, 10**i), random.randint(0, 10**j)) for i in range(1,13) for j in range(1,13) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(3,9) for j in range(9,13) for k in range(1000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(9,13) for j in range(9,13) for k in range(2000)] +\
# [(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(11,13) for j in range(11,13) for k in range(2000)]

### 0519
pairs = \
[(random.randint(0, 10**i), random.randint(0, 10**j)) for i in range(1,16) for j in range(i,16) for k in range(1000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(3,16) for j in range(i,16) for k in range(2000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(6,16) for j in range(i,16) for k in range(3000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(9,16) for j in range(i,16) for k in range(3000)] +\
[(random.randint(10**(i-1), 10**i), random.randint(10**(j-1), 10**j)) for i in range(12,16) for j in range(i,16) for k in range(3000)] 

random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size

print("Subtraction: ", train_size)
pairs_train = pairs[:train_size]

pairs_test = pairs[train_size:]

data = []

for num1, num2 in pairs:
    if random.random()<0.5:
        num1, num2 = num2, num1 

    answer = num1 - num2

    instruction = f"{num1} - {num2} = " 
    cot = f"{num1} - {num2} = {answer}"
    output = str(answer)


    data.append({"question": instruction, "cot": cot, "answer": output, "type": "sub"})


with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)


# ##### 0512
# pairs = \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(2,16) for k in range(10000)] + \
# [(0, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
# [(1, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
# [(10, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
# [(random.randint(1, 9), random.randint(1, 9)) for k in range(1000)]
pairs = \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(2,5) for k in range(4000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(5,8) for k in range(8000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(8,12) for k in range(12000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(12,17) for k in range(16000)] + \
[(0, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
[(1, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
[(10, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,16) for k in range(500)] + \
[(random.randint(1, 9), random.randint(1, 9)) for k in range(500)]




random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size

print("nx1 Multiplication: ",train_size)
pairs_train = pairs[:train_size]

pairs_test = pairs[train_size:]

data = []

for num1, num2 in pairs:
    if random.random()<0.5:
        num1, num2 = num2, num1 

    if random.random() < 0.1:
        num1 = num1 * (10**random.randint(1,6))
    answer = num1 * num2 

    instruction = f"{num1} * {num2} = " 
    cot = f"{num1} * {num2} = {answer}"
    output = str(answer)


    data.append({"question": instruction, "cot": cot, "answer": output, "type": "mul_nx1"})



with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)


# ############# divide 700900
# pairs = \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,12) for k in range(50000)] + \
# [(1, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,12) for k in range(10000)] + \
# [(10, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,12) for k in range(10000)] + \
# [(random.randint(1, 10), random.randint(1, 10)) for k in range(1000)]

# 0511 sample:570000 too much: 20% okay
# pairs = \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,6) for k in range(10000)] + \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j-1)) for j in range(6,10) for k in range(20000)] + \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j-1)) for j in range(10,15) for k in range(40000)] + \
# [(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j-1)) for j in range(15,17) for k in range(50000)] + \
# [(1, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,17) for k in range(5000)] + \
# [(10, random.randint(10**(j-1)+1, 10**j-1)) for j in range(2,17) for k in range(5000)] + \
# [(random.randint(1, 10), random.randint(1, 10)) for k in range(1000)]


# 0512: up to 16 digit: 380900
pairs = \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(1,5) for k in range(4000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(5,8) for k in range(8000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(8,12) for k in range(12000)] + \
[(random.randint(2, 9), random.randint(10**(j-1)+1, 10**j)) for j in range(12,17) for k in range(16000)] + \
[(1, random.randint(10**(j-1)+1, 10**j)) for j in range(1,17) for k in range(500)] + \
[(10, random.randint(10**(j-1)+1, 10**j)) for j in range(1,17) for k in range(500)] + \
[(0, random.randint(10**(j-1)+1, 10**j)) for j in range(1,17) for k in range(100)] + \
[(random.randint(1, 10), random.randint(1, 10)) for k in range(500)]


random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size

print("n/1 Division: ", train_size)
pairs_train = pairs[:train_size]

pairs_test = pairs[train_size:]

data = []

for num1, num2 in pairs:

    if num1 > 0 and random.random() < 0.5: 
        remainder = random.randint(0, num1-1)
    else:
        remainder = 0
    answer = num1 * num2 + remainder

    instruction = f"{answer} / {num1} = " 
    cot = instruction + str(num2) + " R " + str(remainder) if remainder!=0 else instruction + str(num2)
    output = str(num2) + " R " + str(remainder) if remainder!=0 else str(num2)


    data.append({"question": instruction, "cot": cot, "answer": output, "type": "div_n/1"})


with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)


#########divide cot


### 0512
pairs = \
[(random.randint(10**(j-1), 10**j), random.randint(11, 10**i)) for i in range(2, 7) for j in range(i+1, i+7) for k in range(10000)] +\
[(random.randint(10**(j-1), 10**j), random.randint(11, 10**i)) for i in range(2, 7) for j in range(2, i+7) for k in range(1000)]


# # 452395 / 3423 = 10
# pairs = [(64*139+18 ,64)]

# random.shuffle(pairs)

test_size = 100
train_size = len(pairs)-test_size

print("Multi-digit Division", train_size)
pairs_train = pairs[:train_size]

pairs_test = pairs[train_size:]

data = []

for num1, num2 in pairs:

    quotient = num1 // num2
    remainder = num1 % num2

    if num1 > num2 and random.random()<0.1: 
        num1 = num1 - remainder
        quotient = num1 // num2
        remainder = num1 % num2

    instruction = f"{num1} / {num2} = " 

    if quotient == 0:
        cot = f"{num1} / {num2} = {quotient} R {remainder}"
        output = f"{quotient} R {remainder}"
    elif num1 == num2:
        cot = f"{num1} / {num2} = {quotient}"
        output = f"{quotient}"        

    else:
        step = ""
        cot = ""
        left = num1

        i = 0
        computed_q = 0

        while left>=num2:
            
            if int(str(quotient)[i])!=0:

                intermediate = int(str(quotient)[i] + "0" * (len(str(quotient))-1-i))

                answer = num2 * intermediate

                new_left = left - answer

                step = f"{left} - {num2} * {intermediate} = {left} - {answer} = {new_left}\n"

                cot = cot + step
                
                left = new_left

                computed_q = computed_q + intermediate

            i = i+1

        assert(left == remainder)
        assert(computed_q == quotient)

        if remainder!=0:
            cot = cot + f"Therefore, {num1} / {num2} = {quotient} R {remainder}"
            output = f"{quotient} R {remainder}"
        else:
            cot = cot + f"Therefore, {num1} / {num2} = {quotient}"
            output = f"{quotient}"




    data.append({"question": instruction, "cot": cot, "answer": output, "type": "div_n/m"})


with open("train_final_0519.json", "a") as f:
    json.dump(data[:train_size], f, indent=4)



with open("test_final_0519.json", "a") as f:
    json.dump(data[train_size:], f, indent=4)






