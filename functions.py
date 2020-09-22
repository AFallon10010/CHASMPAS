# CHASMPAS functions


def get_branch_level(pid, responses):
    branch_level = 0
    for i in responses:
        if i['presentationId'] == pid:
            return branch_level
        branch_level += 1
        if branch_level >= len(responses):
            return None


def mpanlparse(file, data, testdict):
    """
    This function will parse though the MPANL test type and return a dictionary of values
    for the mpanlsData branch

    :param file:
    :param data:
    :param testdict:
    :return: dictionary
    """
    tmp_dict = testdict
    test_results = data['testResults']
    protocol_id = test_results['protocol']['id']
    test_date = test_results['protocol']['date']
    version = test_results['protocol']['version']
    tablet_uuid = test_results['tabletUUID']
    responses = test_results['responses']
    subject_id = responses[1]['response']
    test_type = responses[2]['response']

    # parse the static variables into the tmp_dict
    tmp_dict['filename'] = file
    tmp_dict['protocolId'] = protocol_id
    tmp_dict['version'] = version
    tmp_dict['tabletUUID'] = tablet_uuid
    tmp_dict['testType'] = test_type
    tmp_dict['subjectId'] = subject_id
    tmp_dict['testDate'] = test_date
    for i in responses:
        try:
            if i['presentationId'] == 'MPANLs' and isinstance(i['mpanlsData'], list):
                # lets grab the mpanlsdata list
                branch = i['mpanlsData']
                # set a variable to hold branch number
                branch_level = 0
                # pass the dictionary into the tmp_dict
                for item in branch:
                    if 'freq' in item:
                        freq = item['freq']
                    else:
                        freq = 'No Found'
                    if 'level' in item:
                        level = item['level']
                    else:
                        level = 'Not Found'
                    if 'limit' in item:
                        limit = item['limit']
                    else:
                        limit = 'Not Found'
                    if 'att' in item:
                        att = item['att']
                    else:
                        att = 'Not Found'
                    if 'levelUnderWAHTS' in item:
                        level_under_wahts = item['levelUnderWAHTS']
                    else:
                        level_under_wahts = 'Not Found'
                    if 'noiseFloor' in item:
                        noise_floor = item['noiseFloor']
                    else:
                        noise_floor = 'Not Found'
                    # add the values to the tmp_dictionary
                    tmp_dict['mpanlsData_'+str(branch_level)+'_freq'] = freq
                    tmp_dict['mpanlsData_' + str(branch_level) + '_level'] = level
                    tmp_dict['mpanlsData_' + str(branch_level) + '_limit'] = limit
                    tmp_dict['mpanlsData_' + str(branch_level) + '_att'] = att
                    tmp_dict['mpanlsData_' + str(branch_level) + '_levelUnderWAHTS'] = level_under_wahts
                    tmp_dict['mpanlsData_' + str(branch_level) + '_noiseFloor'] = noise_floor
                    branch_level += 1
        except KeyError:
            return False
    return tmp_dict


def tripledigitparse(data):
    """
    The triple digit information does not have any unique identifies.
    There are approximately 46 test results all with the same variable names
    We will need to find the first branch that contains the 3D test and then parse from there.
    afterwards we will have to bunch the test results in groups of 10 for the test
    and 2 groups of 3 for the practice.
    We will group on the SNR values as these are the only constants.
    SNR -1.5 and -8.5 are the three practice tests.
    SNR -7.5, -14.5, -21.5 are used for the 4 main tests (-14.5 is used twice)
    :param data: this is the json data containing all test results
    :return: list of test results. composed of currentMasker, digitScore, presentationScore, currentSNR,
             targetLevel, numberCorrect, numberIncorrect
    """
    branch_level = 0
    triple_list = []
    triple_result_list = []
    responses = data['testResults']['responses']
    for i in responses:
        if i['presentationId'] == 'threeDigitTest' and isinstance(i['response'], list):
            # if we are in a 3D branch lets get the values then add them to a list
            if 'currentMasker' in i:
                current_masker = i['currentMasker']
            else:
                current_masker = 'Not Found'
            if 'digitScore' in i:
                digit_score = i['digitScore']
            else:
                digit_score = 'Not Found'
            if 'presentationScore' in i:
                presentation_score = i['presentationScore']
            else:
                presentation_score = 'Not Found'
            if 'currentSNR' in i:
                current_snr = i['currentSNR']
            else:
                current_snr = 'Not Found'
            if 'targetLevel' in i:
                target_level = i['targetLevel']
            else:
                target_level = 'Not Found'
            if 'numberCorrect' in i:
                number_correct = i['numberCorrect']
            else:
                number_correct = 'Not Found'
            if 'numberIncorrect' in i:
                number_incorrect = i['numberIncorrect']
            else:
                number_incorrect = 'NotFound'

            tmp_list = [
                current_masker,
                digit_score,
                presentation_score,
                current_snr,
                target_level,
                number_correct,
                number_incorrect
            ]

            triple_list.append(tmp_list)

        elif i['presentationId'] == 'threeDigitTest' and i['response'] == 'Exam Results':
            # We need to add the exam results ot a separate list and will prepend it
            examresultsnr = i['page']['responseArea']['examProperties']['initialSNR']
            examresultmasker = i['page']['responseArea']['examProperties']['warmupMasker']
            examresultheader = '3D_ExamResult_' + str(examresultmasker) + str(examresultsnr)
            examresultscore = i['digitScore']

            tmp_result_list = {
                examresultheader: examresultscore
            }

            triple_result_list.append(tmp_result_list)

    else:
        branch_level += 1

    # parse the data into a dictionary
    test_number = 1
    trip_tmp_dict = {}
    for i in triple_list:
        # keys
        trip_tmp_dict['currentMasker_' + str(test_number)] = i[0]
        trip_tmp_dict['digitScore_' + str(test_number)] = i[1]
        trip_tmp_dict['presentationScore_' + str(test_number)] = i[2]
        trip_tmp_dict['currentSNR_' + str(test_number)] = i[3]
        trip_tmp_dict['targetLevel_' + str(test_number)] = i[4]
        trip_tmp_dict['numberCorrect_' + str(test_number)] = i[5]
        trip_tmp_dict['numberIncorrect_' + str(test_number)] = i[6]

        test_number += 1
    # parse the Exam results into the proper order
    trip_result_dict = {}

    a = (sorted(triple_result_list, key=lambda d: list(d.keys())))
    for d in a:
        trip_result_dict.update(d)
    return trip_tmp_dict, trip_result_dict


def flft(data):
    """
    Parse through the FLFT Right and FLFT Left branches.
    return a tuple of values that correspond to the F and L sub-branches

    :param data:
    :return: tuple of left and right F/L values
    """

    responses = data['testResults']['responses']
    flft_r_tmp = None
    flft_l_tmp = None
    for r in responses:
        if r['presentationId'] == 'FLFT_right':
            flft_r_tmp = tuple(zip(r['F'], r['L']))

    for l in responses:
        if l['presentationId'] == 'FLFT_left':
            flft_l_tmp = tuple(zip(l['F'], l['L']))

    return flft_r_tmp, flft_l_tmp


def get_threshold_values(d, pid, v, r, f):
    """

    :param d: dictionary number in the overall list
    :param pid: string is for checking the presentationId value and making sure we are in the proper dictionary
    :param v: what value are you looking for. There is a pseudo-switch/case option
    :param r: the default dictionary containing all the responses
    :param f: filename being parsed
    :return: a dictionary of specific key/values
    """
    freq_value = {'1000': 17, '2000': 20, '3000': 22, '4000': 23, '6000': 25, '8000': 26}
    # This dictionary aligns with the frequency bands listed in the svantek dictionary
    freq = pid[-4:]
    leq = freq_value.get(freq)
    try:
        if pid != '':
            if r[d].get('presentationId') != pid:
                print(f'Test Mismatch in dictionary {d} for value {pid}, with response {v} in file {f}.')
                print(r[d].get('presentationId'))

                while True:
                    answer = input('Continue with Script [y/n]?\n')
                    if answer == 'y':

                        print('Dictionary Mismatch, adding file to errorFile variable.')
                        s = ('error', d, pid, v, f)
                        return s
                    elif answer == 'n':
                        print('Script exiting...')
                        quit()
                    else:
                        print('Please choose [y/n]')
    except IndexError:
        print('IndexError')
        print(f'dictionary {d}, value {pid}, response {v}, file {f}')
        s = ('error', d, pid, v, f)
        return s
    try:
        if v == 'Leq':
            s = r[d]['svantek']['Leq'][leq]
            return s
        elif v == 'LeqA':
            s = r[d]['svantek']['LeqA']
            return s
        elif v == 'LeqC':
            s = r[d]['svantek']['LeqC']
            return s
        elif v == 'LeqZ':
            s = r[d]['svantek']['LeqZ']
            return s
        elif v == 'overallAmbientNoise':
            s = r[d]['svantek']['overallAmbientNoise']
            return s
        elif v == 'RetSPL':
            s = r[d]['RetSPL']
            return s
        elif v == 'Units':
            s = r[d]['Units']
            return s
        elif v == 'time':
            s = r[d]['svantek']['time']
            return s
        elif v == 'response':
            s = r[d]['response']
            return s
        elif v == '0':
            s = r[d]['response'][0]
            return s
        elif v == '1':
            s = r[d]['response'][1]
            return s
        elif v == '2':
            s = r[d]['response'][2]
            return s
        elif v == '3':
            s = r[d]['response'][3]
            return s
        elif v == 'Threshold':
            s = r[d]['Threshold']
            return s
        elif v == 'ThresholdFrequency':
            s = r[d]['ThresholdFrequency']
            return s
        elif v == 'currentMasker':
            s = r[d]['currentMasker']
            return s
        elif v == 'digitScore':
            s = r[d]['digitScore']
            return s
        elif v == 'presentationScore':
            s = r[d]['presentationScore']
            return s
        elif v == 'currentSNR':
            s = r[d]['currentSNR']
            return s
        elif v == 'targetLevel':
            s = r[d]['targetLevel']
            return s
        elif v == 'numberCorrect':
            s = r[d]['numberCorrect']
            return s
        elif v == 'numberIncorrect':
            s = r[d]['numberIncorrect']
            return s
        else:
            return 'None'
    except KeyError:
        return 'Value not Found'


def testtype(data):
    """
    This function determines what kind of test was performed.
    :param data: the dictioanry of test results.
    :return:
    """
    # static variables
    test_results = data['testResults']
    responses = test_results['responses']
    test_type = responses[2]['response']

    if 'Pre' in test_type:
        return 'pre'
    elif 'Regular' in test_type:
        return 'reg'
    elif 'Post' in test_type:
        return 'pst'
    elif 'MPANL' in test_type:
        return 'mpl'
    else:
        return 'Unknown'


def parsetestfile(file, data, testtypearray, testtypedict):
    """
    Parse the json file
    :param file: name of the file being parsed
    :param data: the data dictionary form the file
    :param testtypearray: the array of values to be searched based on the test type
    :param testtypedict: the dictionary containg the key/value pairs for the output of the file
    :return: dictionary of key/value pairs
    """
    # static variables

    tmp_dict = testtypedict
    tmp_array = testtypearray
    test_results = data['testResults']
    protocol_id = test_results['protocol']['id']
    test_date = test_results['protocol']['date']
    version = test_results['protocol']['version']
    tablet_uuid = test_results['tabletUUID']
    responses = test_results['responses']
    subject_id = responses[1]['response']
    test_type = responses[2]['response']

    # parse the static variables into the tmp_dict
    tmp_dict['filename'] = file
    tmp_dict['protocolId'] = protocol_id
    tmp_dict['version'] = version
    tmp_dict['tabletUUID'] = tablet_uuid
    tmp_dict['testType'] = test_type
    tmp_dict['subjectId'] = subject_id
    tmp_dict['testDate'] = test_date

    # parse through the tmp_array which contains all the presentationID values you are searching for.
    for item in tmp_array:
        search_key = item[0]
        # call function to find if the presentationId is present and what branch it is on
        d = get_branch_level(search_key, responses)
        if d is not None:
            a = get_threshold_values(d, search_key, item[1], responses, file)
        else:
            a = 'Not Found'
        # parse through the tmp_dict and reassign the value to the appropriate key
        for k, v in tmp_dict.items():
            if k == item[2]:
                tmp_dict[item[2]] = a

    return tmp_dict
