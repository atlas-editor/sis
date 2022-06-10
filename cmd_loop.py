from collections import defaultdict
from smtplib import SMTPException
import sys
import data_access
import mail
from student import Student

class ParserException(Exception):
    pass


class GenericLoop:

    def __init__(self, prompt='> ') -> None:
        self.prompt = prompt
        self.conn = data_access.create_connection('data/main.db')

    def start(self):
        while True:
            try:
                user_input = input(self.prompt)
            except EOFError:
                print()
                return

            if user_input == 'exit':
                return
            if user_input == '':
                continue

            try:
                self.parser(user_input)
            except ParserException as e:
                print(e)


class MainLoop(GenericLoop):
    def parser(self, s):
        tokens = s.split()

        if tokens[0] == 'ls':
            self.list()
        elif tokens[0] == 'select':
            _id = tokens[1]
            SelectLoop(_id).start()
        elif tokens[0] == 'grading':
            print('(gradingloop not yet implemented)')
            # GradingLoop().start()
        elif tokens[0] == 'help':
            if len(tokens) == 1:
                print('List of commands (type help <command>):\
                    \n=======================================\
                    \nls select grading')
            elif tokens[1] == 'ls':
                print('List all students')
            elif tokens[1] == 'select':
                print('Opens a subshell for student administration')
            elif tokens[1] == 'grading':
                print('Opens a subshell for grading')
            else:
                raise ParserException(f'unrecognized command: {" ".join(tokens[1:])}')
        else:
            raise ParserException(f'unrecognized command: {s}')

    def list(self):
        students = data_access.list_students(self.conn)
        for i in students:
            print(' '.join([str(x) for x in i]))


class SelectLoop(GenericLoop):
    def __init__(self, _id) -> None:
        super().__init__()
        db_info = data_access.find_student_by_id(self.conn, _id)
        self.student = Student(*db_info[:5])
        self.student.grades = db_info[6:]
        name = ''.join(db_info[3].lower().split())
        self.prompt = f'(@{name})> '
        
    def parser(self, s):
        tokens = s.split()

        if tokens[0] == 'info':
            print(self.student)
        elif tokens[0] == 'grades':
            self.plot_grades()
        elif tokens[0] == 'mail':
            self.mail()
        elif tokens[0] == 'help':
            if len(tokens) == 1:
                print('List of commands (type help <command>):\
                    \n=======================================\
                    \ninfo grades mail')
            elif tokens[1] == 'info':
                print('Show info about the student')
            elif tokens[1] == 'grades':
                print('Show student grades as a graph with their score')
            elif tokens[1] == 'mail':
                print('Send an email to this student')
            else:
                raise ParserException(f'unrecognized command: {" ".join(tokens[1:])}')
        else:
            raise ParserException(f'unrecognized command: {s}')

    def plot_grades(self):
        grades = self.student.grades
        N = len(grades)
        d = defaultdict(list)
        res = [[' ']*N for _ in range(11)]

        for i in range(N):
            d[grades[i]].append(i)

        for i in range(10, -1, -1):
            for j in range(N):
                if j in d[i] or (i != 10 and res[10-i-1][j]) == 'o':
                    res[10-i][j] = 'o'

        for j, i in enumerate(res):
            print(f'{str(10-j).rjust(2)} |', end='')
            print('  '.join(i))

        print('-'*(3 + (3*N)))

        print('HW#', ' '.join([str(i).ljust(2)
              for i in range(1, N+1)]), end='\n\n')

        print(f'score: {self.student.score():.2f}')

    def mail(self):
        subject = input('Subject: ')
        print('Message:')
        message = sys.stdin.read()

        print('='*(9 + len(subject)))
        print(f'Subject: {subject}\n\nTo: {self.student.email}\n\n{message}')
        print('='*(9 + len(subject)))

        i = input(f'Do you really wish to send the email (y/n)? ')
        if i == 'y':
            try:
                mail.send_email(message, self.student.email, subject)
                print(f'Email successfully sent to {self.student.email}')
            except SMTPException as e:
                print(e)


class GradingLoop(GenericLoop):
    def __init__(self) -> None:
        super().__init__('(grading)> ')

        raise NotImplementedError('gradingloop not yet implemented')

    def parser(self, s):
        pass
