# Day 3 - 1st September 2026
# Mini Project 3 - Password Strength Checker

print("===== PASSWORD STRENGTH CHECK =====")
password = input("Enter Your password: ")

# Creating Checking Variable

has_uppercase = False
has_lowercase = False
has_number = False
has_special = False
has_space = False

# Checking every character

for character in password:
    if character.isupper():
        has_uppercase = True

    elif character.islower():
        has_lowercase = True

    elif character.isdigit():
        has_number = True

    elif character.isspace():
        has_space = True

    else:
        has_special = True


# Score Calculation
score = 0

if len(password) >= 8:
    score += 1

if has_uppercase:
    score += 1

if has_lowercase:
    score += 1

if has_number:
    score += 1

if has_special:
    score += 1


# Determine Password Strength

if score <= 2:
    strength = "Weak"

elif score <= 4:
    strength = "Medium"

else:
    strength = "Strong"


# Display Result

print("\n=================================")
print("        PASSWORD CHECKER")
print("=================================")

print("\nPassword Analysis")
print("--------------------")

print("Length: ", len(password))

if len(password) >= 8:
    print("Minimum Length: YES")

else:
    print("Minimum Length: NO")


print("Uppercase:", "Yes" if has_uppercase else "No")
print("Lowercase:", "Yes" if has_lowercase else "No")
print("Number:", "Yes" if has_number else "No")
print("Special Character:", "Yes" if has_special else "No")
print("Contains Space:", "Yes" if has_space else "No")

print("\nScore:", score, "/ 5")
print("Strength:", strength)

print("================================")
