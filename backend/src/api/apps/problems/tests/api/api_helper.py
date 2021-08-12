from api.apps.problems.models import Question, Category, Option


class ApiHelper:
    def create_category(self, name):
        return Category.objects.create(name=name)

    def create_question(self, category, question_type, question, correct_answer=None,
                        complexity=Question.Complexity.EASY.value, number_of_points=1, max_attempts_to_solve=None,
                        solution=None):
        return Question.objects.create(
            category=category,
            type=question_type,
            text=question,
            correct_answer=correct_answer,
            complexity=complexity,
            number_of_points=number_of_points,
            max_attempts_to_solve=max_attempts_to_solve,
            solution=solution
        )

    def create_option(self, question, value, is_correct):
        return Option.objects.create(question=question, value=value, is_correct=is_correct)
