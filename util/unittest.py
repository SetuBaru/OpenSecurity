def test1():
    import DataControl
    test_obj1 = datapyp.DataControl()
    test_obj1.build_path('../data/unit_tests/_cache_')
    test_obj1.relocate_files('unit_tests', 'data/_cache_')
    return True


def test2():
    import LoggingTool
    _ = logging_tool
    return True


def test3():
    import RepoMan
    repo = RepoMan.Module()
    repo.load(modules='unittest')
    return True


def test4():
    import JSON_DB
    id_man = dataman.db()
    id_man.append(_target="unittest", _number="N/A", _email="N/A", _address="Retro's Computer")
    id_man.query(_target="unittest")
    id_man.remove(0)


def test5():
    from FaceID import face_id
    fid = face_id.FaceID()
    sample_path = "../data/sample_images"
    target_name = "Abubakr Osama"
    target_image = "1016112_481933078555209_200486301_n.jpg"
    fid.learn(target_image=f"{sample_path}/{target_name}/{target_image}",
              target_name="Seto Kayaba")
    fid.cram(sample_path=f"{sample_path}", target=target_name)
    fid.onStream()


def test6():
    from FaceID import adaptiveLearning
    ad = adaptiveLearning.Memory()
    ad.biometric_object = {'Abubakr Osama': []}
    ad.Save()


# Running Unit Testing.
if __name__ == "__main__":
    """ #Half-Full
    # DataControl 
    print("Start of test 1.....")
    test1()
    print(".....End of test 1\n")

    # logging_tool [Incomplete]
    print("Start of test 2.....")
    test2()
    print(".....End of test 2\n")

    # RepoMan
    print("Start of test 3.....")
    test3()
    print(".....End of test 3\n")

    # user_management [Incomplete]
    print("Start of test 4.....")
    test4()
    print(".....End of test 4\n")
    
    
    # Adaptive Learning
    print('Start of test 6.....')
    test6()
    print('.....End of test 6\n')
    
    """

    # face_id [Incomplete]
    print('Start of test 5.....')
    test5()
    print('.....End of test 5\n')