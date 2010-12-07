import test_helper

import logging
from mocktest import *
from autonose import scanner
import os, types
import sys

pickle_path = os.path.abspath('.autonose-depends.pickle')
class ScannerTest(TestCase):
	def test_should_load_saved_dependency_information(self):
		picklefile = mock('pickle file')
		mock_on(scanner).open_file.is_expected.\
			with_(pickle_path).\
			returning(picklefile.raw)
		pickle = mock('unpickled info')
		mock_on(scanner.pickle).load.is_expected.with_(picklefile.raw).returning(pickle.raw)
		
		loaded = scanner.load()
		self.assertEqual(loaded, pickle.raw)
		
	def test_should_print_a_useful_error_on_load_failure_when_pickle_exists(self):
		picklefile = mock('pickle file')
		f = open(pickle_path, 'w')
		f.write('garbage')
		f.close()
		mock_on(sys).stderr.expects('write').with_(string_matching("Failed loading \"\.autonose-depends\.pickle\"\."))
		mock_on(os).remove.is_expected.with_(pickle_path)
		logger = logging.getLogger("autonose.scanner")
		try:
			logger.setLevel(logging.CRITICAL)
			self.assertRaises(SystemExit, scanner.load, args=(1,))
		finally:
			logger.setLevel(logging.ERROR)
			try:
				os.remove(pickle_path)
			except OSError: pass
	
	def test_should_return_an_empty_dict_when_no_pickle_exists(self):
		mock_on(scanner).open_file.is_expected.raising(IOError())
		mock_on(scanner.pickle).load.is_not_expected
		mock_on(sys).stderr.is_not_expected
		
		self.assertEqual(scanner.load(), {})
	
	def test_should_save_dependency_information(self):
		picklefile = mock('pickle file')
		dependencies = mock('dependencies')
		state = mock('state').with_children(dependencies = dependencies.raw)
		mock_on(scanner).open_file.is_expected.with_(pickle_path, 'w').\
			returning(picklefile.raw)
		mock_on(scanner.pickle).dump.\
			is_expected.with_(dependencies.raw, picklefile.raw)
		picklefile.expects('close')
		scanner.save(state.raw)

	def test_should_scan_filesystem_for_updates(self):
		#TODO
		pass
	
	def test_should_delete_dependency_information_on_reset(self):
		
		mock_on(scanner.os.path).isfile.is_expected.with_(pickle_path).returning(True)
		mock_on(scanner.os).remove.is_expected.with_(pickle_path)
		scanner.reset()
	
	def test_should_only_delete_saved_dependencies_if_they_exist(self):
		mock_on(scanner.os.path).isfile.is_expected.with_(pickle_path).returning(False)
		mock_on(scanner.os).remove.is_not_expected
		scanner.reset()

