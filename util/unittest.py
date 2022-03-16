def test1():
    import datapyp
    test_obj1 = datapyp.Datapyp()
    test_obj1.build_path('../data/unit_tests/_cache_')
    test_obj1.relocate_files('unit_tests', 'data/_cache_')
    return True


def test2():
    import logging_tool
    _ = logging_tool
    return True


def test3():
    import RepoMan
    repo = RepoMan.Module()
    repo.load(modules='unittest')
    return True


def test4():
    import ID_manager
    id_man = ID_manager.ManagementConsole()
    id_man.Add_member(target_name="unittest", number="N/A", email="N/A", address="Retro's Computer")


if __name__ == "__main__":
    # Running Unit Tests on Project modules.

    # logging_tool
    print('Start of Test 2')
    test2()
    print('End of Test 2\n')

    # RepoMan
    print('Start of Test 3.....')
    test3()
    print('.....End of Test 3\n')

    # user_management
    print('Start of Test 4.....')
    test4()
    print('.....End of Test 4\n')
