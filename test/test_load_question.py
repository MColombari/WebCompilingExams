from webcompilingexams.load_exam_information import ExamInformation
from webcompilingexams.load_question import LoadQuestion
from webcompilingexams.models import User


if __name__ == '__main__':
    qs = LoadQuestion(User(id=5), ExamInformation('/Users/mattiacolombari/Desktop/ProgettoBicocchi/WebCompilingExams/config.yaml')).load()
    print(len(qs))
    for q in qs:
        print(q)