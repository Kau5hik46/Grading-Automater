from os import getcwd
from copy import deepcopy as dcopy
from math import ceil
from iohandling import *

pwd = getcwd


class User(object):
    weightage = []
    max_marks = []

    def __init__(self, row):
        self.slnum = row[0]
        self.name = row[2]
        self.roll = row[1]
        self.marks = row[3:]
        if self.name == "Max Marks":
            User.max_marks = self.marks
        if self.name == "Weightage":
            User.weightage = [float(x) for x in self.marks]

    def adjust(self):
        if self.name == "Max Marks":
            self.adjusted = [
                "Converted to 100" for i in range(len(self.max_marks))]
            self.total = "total"
            self.adjusted.append(self.total)
            return
        if self.name == "Weightage":
            self.adjusted = self.weightage
            self.total = round(sum(self.adjusted), 2)

            self.adjusted.append(self.total)
            return

        self.adjusted = []
        for i in range(len(self.max_marks)):
            tmp = float(
                self.marks[i]) * float(User.weightage[i]) / float(User.max_marks[i])
            tmp = round(tmp, 2)
            self.adjusted.append(tmp)
        self.total = round(sum(self.adjusted), 2)
        self.adjusted.append(self.total)

    def make_row(self):
        self.row = []
        self.row.append(self.slnum)
        self.row.append(self.roll)
        self.row.append(self.name)
        self.row = self.row + self.marks
        self.row = self.row + self.adjusted
        # print(self.row)
        return self.row


class inputObj(object):
    """Contains individual accessible elements of the csv file"""

    def __init__(self, filename, iapc):
        self.filename = filename
        self.raw_data = csvhandler(filename)
        self.raw_data.read_from_file()
        self.max_marks = User(self.raw_data.input_data[1])
        self.weightage = User(self.raw_data.input_data[0])
        self.iapc = iapc
        # self.make_temp()

    def make_temp(self, filename="TEMP.csv"):
        self.temp = csvhandler(
            filename, headers=self.raw_data.headers + self.raw_data.headers[3:])
        for i in self.raw_data.input_data:
            uobj = User(i)
            uobj.adjust()
            self.temp.output_data.append(uobj.make_row())
        # print(self.temp.output_data)
        self.temp.make_csv(filename)

    def grade_sort_total(self, filename="grade_sort_total.csv"):
        self.grade_sort_total = csvhandler(
            filename, headers=self.raw_data.headers + self.raw_data.headers[3:])
        self.grade_sort_total.output_data = dcopy(self.temp.output_data[2:])
        print(self.grade_sort_total.output_data)
        self.grade_sort_total.output_data.sort(
            key=lambda x: x[-1], reverse=True)
        c = 1
        for i in self.grade_sort_total.output_data:
            if c == 1:
                i.append(0)
            else:
                i.append(
                    round(self.grade_sort_total.output_data[c - 2][-2] - i[-1], 2))
            i[0] = c
            c += 1

        self.grade_sort_total.output_data = self.temp.output_data[:2] + \
            self.grade_sort_total.output_data
        self.grade_sort_total.output_data[1].append("difference")
        self.grade_sort_total.output_data[1].append("grade")

    def grade_sort_roll(self, filename="grade_sort_roll.csv"):
        self.grade_sort_roll = csvhandler(
            filename, headers=self.raw_data.headers + self.raw_data.headers[3:])
        self.grade_sort_roll.output_data = dcopy(self.temp.output_data[2:])
        self.grade_sort_roll.output_data.sort(
            key=lambda x: x[1], reverse=False)
        c = 1
        for i in self.grade_sort_roll.output_data:
            if c == 1:
                i.append(0)
            else:
                i.append(
                    round(self.grade_sort_roll.output_data[c - 2][-2] - i[-1], 2))
            i[0] = c
            c += 1

        self.grade_sort_roll.output_data = self.temp.output_data[:2] + \
            self.grade_sort_roll.output_data
        # self.grade_sort_roll.make_csv(filename)

    def make_grades(self):
        size = len(self.grade_sort_total.output_data)
        c = 0
        d = 0
        self.count = [0, 0, 0, 0, 0, 0, 0]
        self.grades = {}
        for i in range(2, size):
            if c == (int(self.iapc[d][1]) * size) // 100:
                d += 1
                c = 0

            self.grade_sort_total.output_data[i].append(self.iapc[d][0])
            self.grades[self.grade_sort_total.output_data[i]
                        [1]] = self.iapc[d][0]
            c += 1
            self.count[d] += 1

        # print(self.count)
        # print(self.grades)

    def make_iapc(self):
        self.iapc_output = csvhandler("iapc_output.csv")
        self.iapc_output.output_data = [x for x in self.iapc]
        for i in range(0, 7):
            self.iapc_output.output_data[i][1] = self.count[i]
        self.iapc_output.make_csv()

    def make_op1(self):
        self.grade_sort_total()
        self.make_grades()

        self.grade_sort_total.make_csv()

    def make_op2(self):
        self.grade_sort_roll()
        for row in self.grade_sort_roll.output_data:
            if row[1] != "reserved":
                row.append(self.grades[row[1]])
        self.grade_sort_roll.make_csv()


if __name__ == "__main__":
    root_dir = pwd()
    open_dir("inputs")

    iapc = csvhandler("iapc.csv")
    iapc.read_from_file(ignore=True)
    iapc = iapc.input_data

    ip = inputObj("input.csv", iapc)

    open_dir(root_dir)
    open_dir("outputs")
    ip.make_temp()
    ip.make_op1()
    ip.make_op2()
    ip.make_iapc()
