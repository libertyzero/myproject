from openerp import tools
from openerp.tests import common

class Test_Connect_61(common.TransactionCase):
	''' Prepare data from demo(7) and erppeek(61)'''
	def setUp(self):
		super(Test_Connect_61, self).setUp()
		cr, uid = self.cr, self.uid

		#Set Registry
		self.analytic_account = self.registry('myproject.analytic_account_old')
		self.account_line = self.registry('myproject.account_line_old')
		self.myproject = self.registry('myproject.project')

		# Ref to demo Data
		self.account_A_ref = self.registry('ir.model.data').get_object_reference(cr, uid, 'myproject', 'analytic_account_A')
		self.account_A_line_ref = self.registry('ir.model.data').get_object_reference(cr, uid, 'myproject', 'account_line_01')

		self.account_A_id = self.account_A_ref and self.account_A_ref[1] or False
		self.account_A_line_id = self.account_A_line_ref and self.account_A_line_ref[1] or False

		# Create Dict Test data
		self.test_exist_account = [{
			'id' : 20,
			'code': 'A-000',
			'name':'Analytic Account A',
			}]
		self.test_not_exist_account = [{
			'id' : 21,
			'code': 'A-001',
			'name':'Analytic Account B',
			}]
		self.test_both_exist_not_account = [{
			'id' : 20,
			'code': 'A-000',
			'name':'Analytic Account A',
			},{
			'id' : 21,
			'code': 'A-001',
			'name':'Analytic Account B',
			}]

	def test_01_myproject(self):
		''' Case01: import exist data, Not insert to database'''
		cr, uid = self.cr, self.uid
		list_test_ids = []
		list_test_ids.append(self.test_exist_account[0]['id'])
		result = self.myproject.diff_analytic_account(cr, uid, list_test_ids, [20], self.test_exist_account)
		self.assertTrue(result == [])

	def test_02_myproject(self):
		''' Case02: import not exist data, Insert to database'''
		cr, uid = self.cr, self.uid
		list_test_ids = []
		list_test_ids.append(self.test_not_exist_account[0]['id'])
		result = self.myproject.diff_analytic_account(cr, uid, list_test_ids, [20], self.test_not_exist_account)
		self.assertTrue(result == [21])

	def test_03_myproject(self):
		''' Case03: import not exist data and exist data, Insert only not exist'''
		cr, uid = self.cr, self.uid
		list_test_ids = [20,21]
		result = self.myproject.diff_analytic_account(cr, uid, list_test_ids, [20], self.test_both_exist_not_account)
		self.assertTrue(result == [21])

	def test_04_myproject(self):
		''' Case 04: Select analytic account in selection box,and auto fill analytic_name in name box'''
		cr, uid = self.cr, self.uid
		self.test_03_myproject() # Contunue from test03
		self.account_A = self.analytic_account.browse(cr, uid, self.account_A_id, context=None)
		result = self.myproject.select_analytic_id(cr,uid,[],self.account_A_id)
		# Check Insert selected line data
		self.account_A_line = self.account_line.browse(cr, uid, self.account_A_line_id, context=None)

		# Check analytic_name
		self.assertEqual(result['value']['analytic_name'], 'Analytic Account A')
		# Check completion
		