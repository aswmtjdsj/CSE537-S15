import os, sys, copy

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

if __name__ == '__main__':
    """
    main function
    """

    # common help variables
    command_help = 'To run this program, you should type {python} ./handle.py [file_name] {{<--method> [method_name]}}'
    method_list = ['BS', 'BS_FC', 'BS_FC_CP', 'ALL']
    data_part_info = ['Time each course is taking place', 'Course recitations', 'Course details', 'Course requirements', 'TA responsibilities', 'TA skills']
    rect_period = 90
    debug = False # whether to print auxillary information

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
        # data structure for re-mapping
        course_mapping = {}
        TA_mapping = {}

        # parse data file
        data_cnt = 0
        TA_list = []
        print 'Parsing data file {0} ...'.format(file_name)
        with open(file_name) as data_file:
            if debug == True:
                print '{0}. {1}:'.format(data_cnt + 1, data_part_info[data_cnt])
            for line in data_file:
                # handle new line to parse different parts of data file
                if line == '\n':
                    data_cnt += 1
                    if debug == True:
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
                    if debug == True:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 1:
                    # handle course recitations 
                    course_item = course_mapping[data[0]]
                    day = data[1::2]
                    time = data[2::2]
                    course_item.rec_list = zip(day, time)
                    if debug == True:
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
                    if debug == True:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 3:
                    # handle course requirements
                    course_item = course_mapping[data[0]]
                    requirement_list = data[1:]
                    course_item.require_skills = requirement_list
                    if debug == True:
                        print course_mapping[course_item.course_id]

                elif data_cnt == 4:
                    # handle TA responsibilities 
                    TA_item = TA()
                    TA_item.name = data[0]
                    day = data[1::2]
                    time = data[2::2]
                    TA_item.taken_list = zip(day, time)
                    TA_mapping[TA_item.name] = TA_item
                    if debug == True:
                        print TA_mapping[TA_item.name]

                else:
                    # handle TA skill list 
                    TA_item = TA_mapping[data[0]]
                    skill_list = data[1:]
                    TA_item.skill_list = skill_list
                    if debug == True:
                        print TA_mapping[TA_item.name]
            if debug == True:
                for key, value in course_mapping.items():
                    print key, value
                for key, value in TA_mapping.items():
                    print key, value

    except Exception as e:
        raise e

    try:
        # build CSP
        TA_course_relation = {}
        course_TA_relation = {}
        for course_item in course_mapping.values():
            if course_item.course_id not in course_TA_relation:
                course_TA_relation[course_item.course_id] = []
            for TA_item in TA_mapping.values():
                if TA_item.name not in TA_course_relation:
                    TA_course_relation[TA_item.name] = []
                # constraints
                flag = True # suppose this TA can be assigned to this course
                # 1. TA should have free time during course recitation
                if TA_item.taken_list != None:
                    if course_item.rec_list != None:
                        for taken_time in TA_item.taken_list:
                            if taken_time in course_item.rec_list:
                                flag = False
                                break
                    # 2. TA should have free time during course time if course need TA
                    if course_item.need_TA == True:
                        for taken_time in TA_item.taken_list:
                            if taken_time in course_item.time_list:
                                flag = False
                                break
                # 3. course num_TA
                if course_item.num_TA < 1:
                    TA_may_assign = [0.5]
                else:
                    TA_may_assign = [0.5, 1]
                # 4. TA should have all skills required by course
                if (TA_item.skill_list == None and course_item.require_skills != None) or (TA_item.skill_list != None and course_item.require_skills != None and not set(course_item.require_skills).issubset(set(TA_item.skill_list))):
                    flag = False
                # 5. recitation is 90 min long <--- useless?
                if debug == True and flag == True:
                    print course_item.course_id, TA_item.name
                # according to flag, to decide possible assignment
                if flag == True:
                    TA_course_relation[TA_item.name].append(zip([course_item.course_id]*len(TA_may_assign), TA_may_assign))
                    course_TA_relation[course_item.course_id].append(zip([TA_item.name]*len(TA_may_assign), TA_may_assign))

        if True: #debug == True:
            print '\nTA --- Course'
            for key, value in TA_course_relation.items():
                print '{0}: {1}, {2}'.format(key, value, len(value))

            print '\nCourse --- TA'
            for key, value in course_TA_relation.items():
                print '{0}: {1}, {2}'.format(key, value, len(value))

    except Exception as e:
        raise e
    
    try:
        # call solving CSP

        # suppose every couse needs to be assigned fully with number of TA(s), otherwise failed
        # without this assumption, this cannot be modeled as CSP
        # build to_be_assigned_CSP
        CSP = {} # target to fulfilled
        for key, value in course_mapping.items():
            CSP[key] = value.num_TA
            if debug == True:
                print key, CSP[key]

        print ''

        def BacktrackingSearch(csp):
            """
            solving CSP using Backtracking Search
            """
            assignment = {} # 'CSE101': [('TA1', 0.5), ('TA2', 1)]
            TA_assigned = {} # 'TA1': ['CSE101', 0.5), ('CSE537', 0.5)]

            def RecursiveBS(assignment, TA_assigned, csp): # assignment involves two parts, course assigned and TA assigned
                """
                Recursively solving BS
                """
                # test complete
                if len(assignment) == len(csp) and {x:sum([y[1] for y in assignment[x]]) if len(assignment[x]) != 0 else 0 for x in assignment} == csp:
                    return assignment, TA_assigned # complete assignment
                # for each unassigned var in CSP
                var = ''
                for key, value in csp.items():
                    temp = (sum([x[1] for x in assignment[key]]) if key in assignment and len(assignment[key]) != 0 else 0) # find course still needed assignment
                    if temp < value:
                        # this var can be assigned
                        if debug == True:
                            print key, value, temp
                        var = key
                        break

                for possible_TA_assigned in course_TA_relation[var]: # find un-selected vars in CSP graph
                    for possible_to_do in possible_TA_assigned:
                        TA, TA_num = possible_to_do # detect consistency
                        if (sum([x[1] for x in TA_assigned[TA]]) if TA in TA_assigned and len(TA_assigned[TA]) != 0 else 0) + TA_num <= 1 and not (var in [x[0] for x in TA_assigned[TA]] if TA in TA_assigned else []): # the number of course that a TA can be assigned cannot be greater than 1, and a TA cannot be assigned to the same course twice or more
                            if var in assignment: # course has been in assignment 
                                assignment[var].append(possible_to_do)
                            else: # new course assignment
                                assignment[var] = [possible_to_do]

                            # update TA_assigned
                            if TA in TA_assigned: # TA has been assigned
                                TA_assigned[TA].append((var, TA_num))
                            else: # TA has not been assigned
                                TA_assigned[TA] = [(var, TA_num)]

                            print 'Current TA-course-number: {0}-{1}-{2}'.format(var, TA, TA_num)
                            print 'course assignment: ', assignment
                            print 'TA assignment: ', TA_assigned 
                            print ''

                            result = RecursiveBS(assignment, TA_assigned, csp)

                            if result != None:
                                return result
                            assignment[var].remove(possible_to_do) # zoo keeping
                            TA_assigned[TA].remove((var, TA_num))

                return None # failure

            return RecursiveBS(assignment, TA_assigned, csp)

        def BacktrackingSearchWithForwardChecking(csp, possible_course_TA):
            """
            solving CSP using Backtracking Search, optimized by forward checking
            """
            assignment = {} # sample, 'CSE101': [('TA1', 0.5), ('TA2', 1)]
            TA_assigned = {} # sample, 'TA1': ['CSE101', 0.5), ('CSE537', 0.5)]

            print 'BS_FC init'
            print 'course assignment: ', assignment
            print 'TA assignment: ', TA_assigned 
            print 'Possible course TA selection: ', possible_course_TA
            print ''

            def RecursiveBS_FC(assignment, TA_assigned, csp, possible_course_TA): # assignment involves two parts, course assigned and TA assigned
                """
                Recursively solving BS
                """
                # test complete
                if len(assignment) == len(csp) and {x:sum([y[1] for y in assignment[x]]) if len(assignment[x]) != 0 else 0 for x in assignment} == csp:
                    return assignment, TA_assigned # complete assignment
                # for each unassigned var in CSP
                var = ''
                for key, value in csp.items():
                    temp = (sum([x[1] for x in assignment[key]]) if key in assignment and len(assignment[key]) != 0 else 0) # find course still needed assignment
                    if temp < value:
                        # this var can be assigned
                        if debug == True:
                            print key, value, temp
                        var = key
                        break

                # TODO: MRV optimization
                for possible_TA_assigned in possible_course_TA[var]: # find un-selected vars in CSP graph
                    for possible_to_do in possible_TA_assigned:
                        TA, TA_num = possible_to_do # detect consistency
                        if (sum([x[1] for x in TA_assigned[TA]]) if TA in TA_assigned and len(TA_assigned[TA]) != 0 else 0) + TA_num <= 1 and not (var in [x[0] for x in TA_assigned[TA]] if TA in TA_assigned else []): # the number of course that a TA can be assigned cannot be greater than 1, and a TA cannot be assigned to the same course twice or more
                            if var in assignment: # course has been in assignment 
                                assignment[var].append(possible_to_do)
                            else: # new course assignment
                                assignment[var] = [possible_to_do]

                            # update TA_assigned
                            if TA in TA_assigned: # TA has been assigned
                                TA_assigned[TA].append((var, TA_num))
                            else: # TA has not been assigned
                                TA_assigned[TA] = [(var, TA_num)]

                            print 'Current TA-course-number: {0}-{1}-{2}'.format(var, TA, TA_num)
                            print 'course assignment: ', assignment
                            print 'TA assignment: ', TA_assigned 

                            # forward checking
                            possible_course_TA_copy = copy.deepcopy(possible_course_TA)
                            # print possible_course_TA_copy

                            go_on = True # suppose not eliminated
                            for course_checked, TA_possible in possible_course_TA_copy.items():
                                # if course_checked in assignment :#and sum([y[1] for y in assignment[course_checked]]) < csp[course_checked]:
                                for i, TA_separate_possible in enumerate(TA_possible):
                                    TA_separate_possible = [(x[0], x[1] - TA_num if x[0] == TA and x[1] > sum([x[1] for x in TA_assigned[TA]]) else x[1]) for x in TA_separate_possible]
                                    TA_separate_possible = filter(lambda x: x[1] > 0, TA_separate_possible)
                                    TA_possible[i] = TA_separate_possible

                                TA_possible = filter(lambda x: x != None and x != [] and len(x) != 0, TA_possible)

                                # print course_checked, sum([max(map(lambda y: y[1], x)) for x in TA_possible])
                                # elinimation in advance, when no values can be selected for some var
                                if sum([max(map(lambda y: y[1], x)) for x in TA_possible]) == 0:
                                    print course_checked, 'no candidate values, failed in advance'
                                    go_on = False
                                    break

                                possible_course_TA_copy[course_checked] = TA_possible

                            if go_on == True:
                                print 'Possible course TA selection: ', possible_course_TA_copy
                                print ''

                                result = RecursiveBS_FC(assignment, TA_assigned, csp, possible_course_TA_copy)

                                if result != None:
                                    return result

                            assignment[var].remove(possible_to_do) # zoo keeping
                            TA_assigned[TA].remove((var, TA_num))

                return None # failure

            return RecursiveBS_FC(assignment, TA_assigned, csp, possible_course_TA)

        if method_name == 'BS':
            result = BacktrackingSearch(CSP)
        elif method_name == 'BS_FC':
            result = BacktrackingSearchWithForwardChecking(CSP, course_TA_relation)
        elif method_name == 'BS_FC_CP':
            pass
        else:
            result_1 = BacktrackingSearch(CSP)
            result_2 = BacktrackingSearchWithForwardChecking(CSP, course_TA_relation)
            if result_1 != result_2:
                raise Exception('Different answer, something wrong!')
            else:
                result = result_2
        
        if result != None:
            print '\nSolved!\n'
            course_assigned, TA_assigned = result
            for key, value in TA_assigned.items():
                print '{0},'.format(key),
                for course, num in value:
                    print '{0}, {1}'.format(course, num),
                print ''

            print ''
            for key, value in course_assigned.items():
                print '{0},'.format(key),
                for TA, num in value:
                    print '{0}, {1}'.format(TA, num),
                print ''
            print ''
        else:
            print ''
            print 'Failed. CSP cannot be solved!'

    except Exception as e:
        raise e