from course.models import Course
from board.models import Board
from egress.models import Egress


def get_recipient_list(recipient_directorship, recipient_board, recipient_course, recipient_year, recipient_period):
    egress_list = []
    if recipient_directorship:
        for directorship in recipient_directorship:
            courses = Course.objects.filter(
                directorship__id__icontains=directorship
            )
            if courses and not recipient_year and not recipient_period:
                for course in courses:
                    boards = Board.objects.filter(
                        course__id__icontains=course.id
                    )
                    if boards:
                        for board in boards:
                            egress = Egress.objects.filter(
                                board__id__icontains=board.id
                            )
                            for egress in egress:
                                egress_list.append(egress.email)
            if courses and recipient_year and not recipient_period:
                for course in courses:
                    boards = Board.objects.filter(
                        course__id__icontains=course.id,
                        year_graduation__icontains=recipient_year
                    )
                    if boards:
                        for board in boards:
                            egress = Egress.objects.filter(
                                board__id__icontains=board.id
                            )
                            for egress in egress:
                                egress_list.append(egress.email)
            if courses and recipient_year and recipient_period:
                for course in courses:
                    boards = Board.objects.filter(
                        course__id__icontains=course.id,
                        year_graduation__icontains=recipient_year,
                        period_graduation__icontains=recipient_period
                    )
                    if boards:
                        for board in boards:
                            egress = Egress.objects.filter(
                                board__id__icontains=board.id
                            )
                            for egress in egress:
                                egress_list.append(egress.email)    

    if recipient_board:
        for board in recipient_board:
            egress = Egress.objects.filter(
                board__id__icontains=board
            )
            for egress in egress:
                egress_list.append(egress.email)

    if recipient_course:
        for course in recipient_course:
            boards = Board.objects.filter(
                course__id__icontains=course
            )
            if boards and not recipient_year and not recipient_period:
                for board in boards:
                    egress = Egress.objects.filter(
                        board__id__icontains=board.id
                    )
                    for egress in egress:
                        egress_list.append(egress.email)
            if boards and recipient_year and not recipient_period:
                for board in boards:
                    egress = Egress.objects.filter(
                        board__id__icontains=board.id,
                        year_graduation__icontains=recipient_year
                    )
                    for egress in egress:
                        egress_list.append(egress.email)
            if courses and recipient_year and recipient_period:
                for board in boards:
                    egress = Egress.objects.filter(
                        board__id__icontains=board.id,
                        year_graduation__icontains=recipient_year
                    )
                    for egress in egress:
                        egress_list.append(egress.email)

    return egress_list
