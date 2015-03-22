import os, sys

class Course:
    """
    class to represent the property of a course
    """
    def __init__(self):
        """
        init all member vars to None
        """
        self.course_id = None
        self.time_list = None
        self.rec_list = None
        self.num_stu = None
        self.need_TA = None
        self.num_TA = None
        self.require_skills = None

    def __str__(self):
        """
        self representation for course instance
        """
        return '<{0}>: {{"time list": {1}, "recitation list": {2}, "number of students": {3}, "TA needed": {4}, "number of TA(s)": {5}, "required skills": {6}}}'.format(self.course_id, self.time_list, self.rec_list, self.num_stu, self.need_TA, self.num_TA, self.require_skills)

class TA:
    """
    class to represent the property of a TA
    """
    def __init__(self):
        self.name = None
        self.taken_list = None
        self.skill_list = None

    def __str__(self):
        """
        self representation for TA instance
        """
        return '<{0}>: {{"course taken list": {1}, "skill list": {2}}}'.format(self.name, self.taken_list, self.skill_list)

# data structure re-mapping
course_mapping = {}
TA_mapping = {}

# common help variables
command_help = 'To run this program, you should type {python} ./handle.py [file_name] {{<--method> [method_name]}}'
method_list = ['BS', 'BS_FC', 'BS_FC_CP', 'ALL']
data_part_info = ['Time each course is taking place', 'Course recitations', 'Course details', 'Course requirements', 'TA responsibilities', 'TA skills']
rect_period = 90
debug = True # whether to print auxillary information

if __name__ == '__main__':
    """
    main function
    """
    print 'Parsing command options ...'.format(sys.argv)
    method_name = ''
    file_name = ''
    try:
        # parse command options
        if len(sys.argv) < 2: # insufficient command options, at least lack of file name
            raise Exception('number of options < 2, No file specified')

        file_name = sys.argv[1]

        if len(sys.argv) > 2:
            method_opt = sys.argv[2]
            if method_opt != '--method':
                raise Exception('Unknown option: {0}'.format(sys.argv[2]))
            else:
                if len(sys.argv) < 4:
                    raise Exception('No method specified')
                else:
                    method_name = sys.argv[3]
                    if method_name not in method_list:
                        raise Exception('No such method {0}'.format(method_name))
        else:
            method_opt = method_list[-1]

    except Exception as e:
        print e
        print command_help
        exit()
    
    try:
        # parse data file
        data_cnt = 0
        TA_list = []
        print 'Parsing data file {0} ...'.format(file_name)
        with open(file_name) as data_file:
            if debug:
                print '{0}. {1}:'.format(data_cnt + 1, data_part_info[data_cnt])
            for line in data_file:
                # handle new line to parse different parts of data file
                if line == '\n':
                    data_cnt += 1
                    print '\n{0}. {1}:'.format(data_cnt + 1, data_part_info[data_cnt])
                    continue
                data = line.strip('\n,').split(', ')
                # print data

                if data_cnt == 0:
                    # handle course time
                    course_item = Course()
                    course_item.course_id = data[0]
                    day = data[1::2]
                    time = data[2::2]
                    course_item.time_list = zip(day, time)
                    course_mapping[course_item.course_id] = course_item
                    if debug:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 1:
                    # handle course recitations 
                    course_item = course_mapping[data[0]]
                    day = data[1::2]
                    time = data[2::2]
                    course_item.rec_list = zip(day, time)
                    if debug:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 2:
                    # handle course details
                    course_item = course_mapping[data[0]]
                    course_item.num_stu = int(data[1])
                    course_item.need_TA = True if data[2] == 'yes' else False
                    if course_item.num_stu < 25:
                        course_item.num_TA = 0
                    elif course_item.num_stu <= 40:
                        course_item.num_TA = 0.5
                    elif course_item.num_stu <= 60:
                        course_item.num_TA = 1.5
                    else:
                        course_item.num_TA = 2
                    if debug:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 3:
                    # handle course requirements
                    course_item = course_mapping[data[0]]
                    requirement_list = data[1:]
                    course_item.require_skills = requirement_list
                    print course_mapping[course_item.course_id]

                elif data_cnt == 4:
                    # handle TA responsibilities 
                    TA_item = TA()
                    TA_item.name = data[0]
                    day = data[1::2]
                    time = data[2::2]
                    TA_item.taken_list = zip(day, time)
                    TA_mapping[TA_item.name] = TA_item
                    if debug:
                        print TA_mapping[TA_item.name]

                else:
                    # handle TA skill list 
                    TA_item = TA_mapping[data[0]]
                    skill_list = data[1:]
                    TA_item.skill_list = skill_list
                    if debug:
                        print TA_mapping[TA_item.name]

    except Exception as e:
        raise e

    try:
        # build CSP
        pass
    except Exception as e:
        raise e