mcqs = {
    1: {
        "question": "Python is an ______ language?",
        "options": {
            "a": "Compiled",
            "b": "Interpreted",
            "c": "Assembly",
            "d": "Machine code"
        },
        "answer": "b"
    },
    2: {
        "question": "Which of these is NOT a valid Python variable name?",
        "options": {
            "a": "my_var",
            "b": "_var",
            "c": "2nd_var",
            "d": "var2"
        },
        "answer": "c"
    },
    3: {
        "question": "What is the output of `print(3 * 'hi')`?",
        "options": {
            "a": "hihihi",
            "b": "3hi",
            "c": "Error",
            "d": "hi hi hi"
        },
        "answer": "a"
    },
    4: {
        "question": "Which operator is used for exponentiation?",
        "options": {
            "a": "^",
            "b": "*",
            "c": "**",
            "d": "^^"
        },
        "answer": "c"
    },
    5: {
        "question": "What does the `range(3)` function return?",
        "options": {
            "a": "[0, 1, 2]",
            "b": "[1, 2, 3]",
            "c": "(0, 1, 2)",
            "d": "sequence of 0, 1, 2"
        },
        "answer": "d"
    },
    6: {
        "question": "Which method removes and returns the last item from a list?",
        "options": {
            "a": "remove()",
            "b": "pop()",
            "c": "delete()",
            "d": "clear()"
        },
        "answer": "b"
    },
    7: {
        "question": "What does `'hello'.upper()` return?",
        "options": {
            "a": "'Hello'",
            "b": "'HELLO'",
            "c": "'hello'",
            "d": "Error"
        },
        "answer": "b"
    },
    8: {
        "question": "Which is used to open a file for writing?",
        "options": {
            "a": "'r'",
            "b": "'w'",
            "c": "'a'",
            "d": "'x'"
        },
        "answer": "b"
    },
    9: {
        "question": "What is the output of `bool('False')`?",
        "options": {
            "a": "False",
            "b": "True",
            "c": "Error",
            "d": "None"
        },
        "answer": "b"
    },
    10: {
        "question": "Which collection is unordered and unindexed?",
        "options": {
            "a": "List",
            "b": "Tuple",
            "c": "Dictionary",
            "d": "Set"
        },
        "answer": "d"
    },
    11:{
        "question":"Python dictionary ka syntax kaisa hota hai?",
        "options": {
            "a": "square brackets [] mein",
            "b": "curly braces {} mein",
            "c": "parentheses () mein",
            "d": "angle brackets <> mein"
        },
        "answer" : "b"
    }
}
a = 0
for i in range(1,len("queston_id")):
    question_id = i
    print(f"Question-{i}",mcqs[question_id]["question"])
    for option , text in mcqs[question_id]["options"].items():
        print(f"{option}-{text}")
    ans=str(input("Enter u option: "))
    if mcqs[question_id]["answer"] == ans:
        print("\n\nCongratulation Your given Answer is Correct and u got 2 point\n\n")
        a +=2
    else:
        print("\nOhOh Unfortunately Your answer is Wrong\n")
        print(f"You got {a} points\n")
        print("Please Try again\n")
        break
