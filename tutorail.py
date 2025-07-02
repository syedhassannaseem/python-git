import json
import random
from collections import defaultdict

class QuizEngine:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.attempts = defaultdict(int)
        self.completed = False
    
    def display_question(self, question_id):
        """Display question and options with proper formatting"""
        question = self.questions[question_id]
        print(f"\n{'='*40}")
        print(f"Question {question_id}: {question['question']}\n")
        for option, text in question["options"].items():
            print(f"  {option.upper()}) {text}")
    
    def validate_answer(self, question_id, user_answer):
        """Check if answer is correct with case-insensitive comparison"""
        return user_answer.lower() == self.questions[question_id]["answer"].lower()
    
    def get_user_input(self, prompt, valid_options):
        """Handle user input with validation and retries"""
        while True:
            user_input = input(prompt).strip().lower()
            if user_input in valid_options:
                return user_input
            print(f"Invalid input! Please enter one of: {', '.join(valid_options)}")
    
    def calculate_score(self, correct, question_id):
        """Calculate score with decreasing points for attempts"""
        base_points = 2
        penalty = self.attempts[question_id] * 0.5
        points = max(0, base_points - penalty)
        if correct:
            self.score += points
        return points
    
    def show_explanation(self, question_id):
        """Show explanation if available"""
        if "explanation" in self.questions[question_id]:
            print(f"\nExplanation: {self.questions[question_id]['explanation']}")
    
    def run_quiz(self, shuffle=False):
        """Run the quiz with optional question shuffling"""
        print("\n" + "="*40)
        print("PYTHON MCQ QUIZ".center(40))
        print("="*40 + "\n")
        
        question_order = list(self.questions.keys())
        if shuffle:
            random.shuffle(question_order)
        
        for question_id in question_order:
            self.attempts[question_id] += 1
            self.display_question(question_id)
            
            user_answer = self.get_user_input(
                "Your answer: ", 
                list(self.questions[question_id]["options"].keys())
            )
            
            is_correct = self.validate_answer(question_id, user_answer)
            points = self.calculate_score(is_correct, question_id)
            
            if is_correct:
                print(f"\n✅ Correct! (+{points:.1f} points)")
                self.show_explanation(question_id)
            else:
                correct_answer = self.questions[question_id]["answer"]
                print(f"\n❌ Incorrect! The correct answer was {correct_answer.upper()})")
                self.show_explanation(question_id)
                print(f"Current score: {self.score}")
                
                # Option to retry the question
                retry = self.get_user_input("Try again? (y/n): ", ['y', 'n'])
                if retry == 'y':
                    self.run_quiz(shuffle=False)  # Don't shuffle on retry
                    return
        
        self.completed = True
        self.display_final_results()
    
    def display_final_results(self):
        """Show final results with performance breakdown"""
        print("\n" + "="*40)
        print("QUIZ RESULTS".center(40))
        print("="*40)
        max_score = len(self.questions) * 2
        percentage = (self.score / max_score) * 100
        
        print(f"\nFinal Score: {self.score}/{max_score} ({percentage:.1f}%)")
        
        if percentage >= 80:
            print("🎉 Excellent performance!")
        elif percentage >= 60:
            print("👍 Good job!")
        else:
            print("💪 Keep practicing!")
        
        # Show question attempts statistics
        print("\nQuestion Attempts:")
        for q, attempts in self.attempts.items():
            print(f"Q{q}: {attempts} attempt(s)")

# Enhanced question data with explanations
questions = {
    1: {
        "question": "Python is an ______ language?",
        "options": {
            "a": "Compiled",
            "b": "Interpreted",
            "c": "Assembly",
            "d": "Machine code"
        },
        "answer": "b",
        "explanation": "Python is an interpreted language, meaning the code is executed line by line."
    },
    # ... (add all other questions with explanations)
}

# Load questions from JSON file if preferred
# with open('python_quiz.json') as f:
#     questions = json.load(f)

# Run the quiz
quiz = QuizEngine(questions)
quiz.run_quiz(shuffle=True)