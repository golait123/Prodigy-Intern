import getpass
import string


def assess_password_strength(password):
    """Efficiently assesses password strength based on length and character diversity."""
    if not password:
        return {'strength': 'Very Weak', 'feedback': ['Password is empty'], 'score': 0}

    length = len(password)
    has_upper = has_lower = has_digit = has_special = False

    # Single pass through password to check all character types
    for char in password:
        if not has_upper and char.isupper():
            has_upper = True
        elif not has_lower and char.islower():
            has_lower = True
        elif not has_digit and char.isdigit():
            has_digit = True
        elif not has_special and char in string.punctuation:
            has_special = True

        # Early exit if all character types are found
        if has_upper and has_lower and has_digit and has_special:
            break

    # Efficient length scoring using arithmetic
    length_points = min(3, length // 8 + length // 12 + length // 16)

    # Calculate total score
    criteria_points = sum([has_upper, has_lower, has_digit, has_special])
    total_score = length_points + criteria_points

    # Generate feedback
    feedback = []
    if length < 8:
        feedback.append("Password is too short (minimum 8 characters required).")
    else:
        feedback.append(f"Password length: {length} characters.")

    if not has_upper:
        feedback.append("Uppercase letters are missing.")
    if not has_lower:
        feedback.append("Lowercase letters are missing.")
    if not has_digit:
        feedback.append("Numbers are missing.")
    if not has_special:
        feedback.append("Special characters are missing.")

    # Determine strength category
    if total_score <= 2:
        strength = "Weak"
    elif total_score <= 4:
        strength = "Moderate"
    elif total_score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        'strength': strength,
        'feedback': feedback,
        'score': total_score
    }


def main():
    password = getpass.getpass("Enter password to assess: ")
    result = assess_password_strength(password)
    print("\nPassword Strength:", result['strength'])
    print("Feedback:")
    for msg in result['feedback']:
        print(f" - {msg}")


if __name__ == "__main__":
    main()