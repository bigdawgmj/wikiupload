import pytest

from FileManager import FileManager

def test_create():
    fm = FileManager('test')
    assert fm.path == 'test'

def test_get_files_after_date(monkeypatch):
    import os
    def mockoslistdir(path):
        return ['a.txt', 'b.txt']
    def mockosisfile(path):
        return True

    monkeypatch.setattr(os, 'listdir', mockoslistdir)
    monkeypatch.setattr(os.path, 'isfile', mockosisfile)

    fm = FileManager('/test')
    tst_files = fm.get_files_after_date('ab.txt')
    assert len(tst_files) == 1
    tst_files = fm.get_files_after_date('c.txt')
    assert len(tst_files) == 0