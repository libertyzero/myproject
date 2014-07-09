import time
from xml.sax.saxutils import escape
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import psycopg2
import calendar
from lxml import etree
import erppeek
import openerp.addons.decimal_precision as dp
import datetime

class analytic_account_old(osv.osv):
	_name = 'myproject.analytic_account_old'
	_columns = {
		'analytic_code' : fields.char('Code', size=128),
		'analytic_name' : fields.char('Analytic Name', size=128),
		'account_line_ids' : fields.one2many('myproject.account_line_old', 'account_line_id', 'Account Line IDS'),
		'ref_analytic_id' : fields.integer('Ref ID'),
	}
	_rec_name = 'analytic_name'

analytic_account_old()

class account_line_old(osv.osv):
	_name = 'myproject.account_line_old'
	_columns = {
		'account_line_id' : fields.integer('Line ID'),
		'name': fields.char('Description', size=256, required=True),
        'year': fields.char('Year',size=4),
        'amount': fields.float('Amount', required=True, help='Calculated by multiplying the quantity and the price given in the Product\'s cost price. Always expressed in the company main currency.', digits_compute=dp.get_precision('Account')),
       	'period_id' : fields.char('Period', size=10),
       	'account_id': fields.many2one('myproject.analytic_account_old', 'Analytic Account', required=True, ondelete='restrict', select=True, domain=[('type','<>','view')]),
    	'cost' : fields.float('Cost', required=True, digits_compute=dp.get_precision('Account')),
    	'revenue' : fields.float('Revenue', required=True, digits_compute=dp.get_precision('Account')),
    	'ref_line_id' : fields.integer('Ref Line ID'),
    	'ref_account_id' : fields.integer('Ref Account ID'),
    }

	def default_get(self, cr, uid, fields, context=None):
		print '==================default_get old_line============='
		print context
		res = super(account_line_old, self).default_get(cr, uid, fields, context=context)
	
		return res
	
analytic_account_old()

class project(osv.osv):
	_name = 'myproject.project'

	def get_analytic_line_list(self,cr, uid, ids, analytic_id, select_year):
		print '--------get_analytic_line_list------------------'
		print analytic_id, select_year
		analytic_line_ids = self.pool.get('myproject.account_line_old').search(cr,uid,[('ref_account_id','=',analytic_id),('year','=',select_year)])
		line_list = []
		print analytic_line_ids
		if analytic_line_ids!= []:
			# Group By Period_id
			group_period = {}
			for line_id in analytic_line_ids:
				item = self.pool.get('myproject.account_line_old').browse(cr,uid,line_id)
				if item.period_id not in group_period:
					group_period[item.period_id] = {'current_cost' : 0.0, 'current_revenue' : 0.0, 'period' : item.period_id}
				group_period[item.period_id]['current_cost'] += item.cost
				group_period[item.period_id]['current_revenue'] += item.revenue
			print group_period

			# Put to line_list
			for item in group_period:
				line_list.append((0,0,group_period[item]))

		return line_list

	def _get_max_year(self,cr, uid, ids):
		# max_year = self.pool.get('myproject.project_year').search(cr, uid, [])
		# max_year = self.pool.get('myproject.project_year').read(cr, uid, int(max(max_year)), [])
		# print max_year
		res = []
		# res.append(max_year['id'])
		# res.append(max_year['name'])
		# print res
		return res

	def get_completion_detail(self,cr, uid, ids, analytic_id, select_year):
		line_list = []
		# if analytic_id != 0:
		# 	account_line_ids = self.pool.get('myproject.account_line_old').search(cr, uid, [('analytic_id','=',int(analytic_id))])
		# 	print account_line_ids
		# 	dict_date = {}
		# 	for id in account_line_ids:
		# 		account_line = self.pool.get('myproject.account_line_old').read(cr, uid, id,['current_cost','current_revenue','date'])
		# 		year = account_line['date'][0:4]
		# 		print year
		# 		if year == select_year:
		# 			month = account_line['date'][5:7]
		# 			if month not in dict_date.keys():
		# 				dict_date[month] = {'current_cost' : 0.0,
		# 								'current_revenue' : 0.0 } 
		# 				dict_date[month]['current_cost'] += account_line['current_cost']
		# 				dict_date[month]['current_revenue'] += account_line['current_revenue']
					

		# 	dict_month = dict((k,v) for k,v in enumerate(calendar.month_abbr))

		# 	for k,v in dict_date.iteritems():
				
		# 		if int(k) < 10:
					
		# 			month_name = dict_month[int(k[1:])]
		# 		else:
		# 			month_name = dict_month[int(k)]
		# 		line_list.append((0,0,{'period':month_name,
		# 							'current_cost':v['current_cost'],
		# 							'current_revenue':v['current_revenue'],
		# 							'accu_cost' : v['current_cost']*2,
		# 							'accu_revenue' : v['current_revenue']*2,
		# 							'est_cost' : v['current_cost']*10,
		# 							'est_revenue' : v['current_revenue']*10,
		# 							}))
		# print '----------------------'
		# print line_list
		return line_list

	def select_completion_detail(self,cr, uid, ids, analytic_id, select_year_id):
		print '=======_select_completion_detail==========='
		vals = {}
		print analytic_id
		print select_year_id
		if analytic_id:
			ref_analytic_id = self.pool.get('myproject.analytic_account_old').browse(cr,uid,analytic_id)
			ref_analytic_id = ref_analytic_id.ref_analytic_id
			if not select_year_id:
				year = str(datetime.datetime.now().year)
			else:
				year = self.pool.get('myproject.project_year').browse(cr,uid,select_year_id)
				year = year.name
			print year
			vals = {'completion_detail' : self.get_analytic_line_list(cr,uid,ids,ref_analytic_id,year)}
		return { 'value' : vals}

	def _cal_sum_project_price(self, cr, uid, ids, name, arg, context=None):
		print '===========_cal_sum_project_price==============='
		# Function for field sum_project_price
		# Select all amount of project_price_line (In DB) and sum it
		res = {}
		# for this_project in self.browse(cr, uid, ids):
		# 	print this_project.id
		# 	item_ids = self.pool.get('myproject.project_price').search(cr, uid, [('project_id','=',this_project.id)])
		# 	sum_price = 0.0
		# 	for item_id in item_ids:
		# 		price_item = self.pool.get('myproject.project_price').read(cr, uid, item_id, ['amount'])
		# 		price_line_ids = self.pool.get('myproject.project_price_line').search(cr,uid, [('project_price_id','=',price_item['id'])])
		# 		for price_id in price_line_ids:
		# 			price = self.pool.get('myproject.project_price_line').read(cr, uid, price_id, ['amount'])
		# 			print price
		# 			sum_price += price['amount']
		# 	print sum_price
		#	res[this_project.id] = sum_price
		return res

	def _cal_sum_budget(self, cr, uid, ids, name, arg, context=None):
		print '===========_cal_sum_budget==============='
		# Function for field sum_budget
		# Select all amount of budget (In DB) and sum it
		res = {}
		# for this_project in self.browse(cr, uid, ids):
		# 	print this_project.id
		# 	item_ids = self.pool.get('myproject.budget').search(cr, uid, [('project_id','=',this_project.id)])
		# 	sum_budget = 0.0
		# 	for item_id in item_ids:
		# 		bath = self.pool.get('myproject.budget').read(cr, uid, item_id, ['amount_bath'])
		# 		print bath
		# 		sum_budget += bath['amount_bath']
		# 	print sum_budget
		# 	res[this_project.id] = sum_budget
		return res

	def _completion_detail(self, cr, uid, ids, name, arg, context=None):
		print '=====completion detail==========='
		# Function for field completion_detail, to show completion data of selected analytic id
		# Input analytic_id, select_year
		# Call method select_completion_detail to query data with analytic_id and select_year
		# Call When Start Server, After save data, redirect to show data page
		res = {}
		# print arg
		print ids
		if ids != []:
			this_analytic_id = self.pool.get('myproject.project').read(cr, uid, ids, ['analytic_id'])
			print this_analytic_id
			this_analytic_id = this_analytic_id[0]['analytic_id']
			if this_analytic_id:
				ref_analytic_id = self.pool.get('myproject.analytic_account_old').browse(cr,uid,this_analytic_id)
				ref_analytic_id = ref_analytic_id.ref_analytic_id
				print ref_analytic_id
				res[ids[0]] = self.get_analytic_line_list(cr,uid,ids,ref_analytic_id,str(datetime.datetime.now().year))
		return res

	def _get_selection(self, cr, uid, context=None):
		print '====get_selection==========='
		# print context
		# # Function for field selection, to create select choice
		# # Run when open form, after save data
		# # Simulate another server situation
		# # Hand code python to query data from another server and put to selection choice 
		# list_res = []
		# #if 'view_type' in context and context['view_type'] == 'form':
		# # Work! but get error when create project
		# try:
		# 	conn = psycopg2.connect("dbname='litu7' user='openerp' host='localhost' password='password'")
		# except:
		# 	print "I am unable to connect to the database"
		
		# try:
		# 	cur = conn.cursor()
		# 	cur.execute("""SELECT * from myproject_analytic_account_old""")
		# except:
		# 	print "I can't SELECT from myproject_analytic_account_old"
		
		# rows = cur.fetchall()
		# print rows
		
		# for item in rows:
		# 	list_res.append((str(item[0]),item[6]))
		
		return list_res

	def _budget_detail(self, cr, uid, ids, name, arg, context=None):
		print '=====budget detail==========='
		# Function one2many for budget_detial, show budget data
		# Will change type of field to one2many
		res = {}
		# print ids
		# cr.execute('SELECT description,qty,unit_price,currency,rate,amount,amount_bath FROM myproject_budget WHERE project_id = %s ORDER BY description', ids)
		# rows = cr.fetchall()
		# print rows
		# line_list = []
		# for row in rows:
		# 	line_list.append((0,0,{ 'description' : row[0],
		# 							'qty' : row[1],
		# 							'unit_price' : row[2],
		# 							'currency': row[3],
		# 							'rate': row[4],
		# 							'amount': row[5],
		# 							'amount_bath': row[6],
		# 							}))
		# res[ids[0]] = line_list
		return res

	def _year_completion(self, cr, uid, ids, name, arg, context=None):
		res = {}
		
		return res

	_columns = {
		'project_id' : fields.integer('ID'),
		'analytic_id' : fields.many2one('myproject.analytic_account_old', 'Analytic ID'),
		'analytic_name' : fields.char('Analytic Name', size=30),
		'type' : fields.selection([('project','Project'), ('service', 'Service')], 'Type'),
		'sum_project_price' : fields.function(_cal_sum_project_price, method=True, type="float", string="Project Price", readonly=True),
		'sum_budget' : fields.function(_cal_sum_budget, method=True, type="float", string="Budget", readonly=True),
		'completion_detail' : fields.function(_completion_detail, method=True, type="one2many", relation="myproject.temp_completion", string="Completion"),
		'project_price_detail' : fields.one2many('myproject.project_price', 'project_id', 'Project Price Ids'),
		'budget_detail' : fields.one2many('myproject.budget', 'project_id', 'Budget Ids'),
		'year_completion': fields.function(_year_completion, method=True, type="many2one", relation='myproject.project_year', string="Year"),
		'state': fields.selection([('draft', 'Draft')], 'State', required=True, readonly=True),
		
		 #Addition Field
		'customer' : fields.char('Customer', size=30),
		'contact' : fields.char('Contact', size=30),
		'contact_no' : fields.char('Contact No.', size=20),
		'contact_date' : fields.date('Contact Date'),
		'start_date' : fields.date('Start Date'),
		'end_date' : fields.date('End Date'),
		'cost_center' : fields.char('Cost Center'),
		'project_manager' : fields.char('Project Manager'),
	}

	_defaults = {
		'state' : lambda *a: 'draft',
	}
	_rec_name = 'project_id'

	def create(self, cursor, user, values, context=None):
		print '============create================='
		print values
		print '----'
		res_id = super(project, self).create(cursor, user, values, context)
		print 'res_id: ',res_id
		return res_id

	def write(self, cursor, user, id, values, context=None):
		print '==================write==============='
		return super(project, self).write(cursor, user, id, values, context)


	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		print '==================fields_view_get======================='
		print view_type
		context['view_type'] = view_type
		result = super(project, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
		return result

	def project_price_detail_change(self, cursor, user, ids, one2many_list):
		# For project_price one2many, when data in table has change(add,edit,delete)
		# call this to calculate new sum_project_price by sum saved date and not saved data
		vals = {}
		print one2many_list
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		sum_price = 0.0
		for ind, price_list in enumerate(one2many_list):
			print price_list
			print price_list[1]
			if price_list[0] == 4:
				# 4 => have exist
				price_item_ids = self.pool.get('myproject.project_price_line').search(cursor, user, [('project_price_id','=',price_list[1])])
				print price_item_ids
				for price_item_id in price_item_ids:
					price_item = self.pool.get('myproject.project_price_line').read(cursor, user, price_item_id,['amount'])
					print price_item
					sum_price += price_item['amount']
			elif price_list[0] == 2:
				# 2 => delete from tree
				del(one2many_list[ind])
				print one2many_list
			else:
				# 0 => add new to tree or 1 => edit
				price_item = price_list[2]['project_price_line_ids']
				for price in price_item:
					sum_price += price[2]['amount']
		print sum_price
		vals = {'sum_project_price' : sum_price}
		print vals
		return { 'value' : vals}

	def budget_detail_change(self, cursor, user, ids, one2many_list):
		# For Budget one2many, when data in table has change(add,edit,delete)
		# call this to calculate new sum_project_price by sum saved date and not saved data
		vals = {}
		print one2many_list
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		sum_price = 0.0
		for ind, price_list in enumerate(one2many_list):
			print price_list
			print price_list[1]
			if price_list[0] == 4:
				# 4 => have exist				
				price_item = self.pool.get('myproject.budget').read(cursor, user, price_list[1],['amount_bath'])
				print price_item
				sum_price += price_item['amount_bath']
			elif price_list[0] == 2:
				# 2 => delete from tree
				del(one2many_list[ind])
				print one2many_list
			else:
				# 0 => add new to tree or 1 => edit
				sum_price += price_list[2]['amount_bath']
		print sum_price
		vals = {'sum_budget' : sum_price}
		print vals
		return { 'value' : vals}



	def select_analytic_id(self, cursor, user, ids, analytic_id):
		print '======select_analytic_id============'
		# On change for field analytic_id
		# get analytic_id and call select_completion_detail to fill data in another field and 
		# show completion data in table with max_year
		vals = {}
		print analytic_id
		if analytic_id:
			# analytic_id will be False, When saved data and redirect to show data page
			# Get all line_ids with analytic ref id
			account = self.pool.get('myproject.analytic_account_old').read(cursor,user, int(analytic_id), ['analytic_name','ref_analytic_id'])
			print account
			ref_analytic_id = account['ref_analytic_id']

			client = erppeek.Client('http://192.168.70.5:8080','psp_test','admin_precise','smg')
			ana_acc_61 = client.model('account.analytic.line')
			ana_acc_61_ids = ana_acc_61.search([('account_id','=',ref_analytic_id)])
			print ana_acc_61_ids

			#Check Diff
			ana_acc_7 = self.pool.get('myproject.account_line_old')
			ana_acc_7_items = ana_acc_7.read(cursor,user,ana_acc_7.search(cursor,user,[]),[])
			ana_acc_7_ids = [item['ref_line_id'] for item in ana_acc_7_items]
			print ana_acc_7_ids

			diff_items = set(ana_acc_61_ids).difference(set(ana_acc_7_ids))
			diff_items = list(diff_items)
			print diff_items

			# Save All line to 7 db
			if diff_items != []:
				for line_id in diff_items:
					res = {}
					line_item = ana_acc_61.browse(line_id)
					res['name'] = line_item.name
					res['year'] = line_item.date[0:4]
					res['amount'] = line_item.amount
					res['cost'] =  line_item.amount if line_item.amount < 0.0 else 0.0
					res['revenue'] = line_item.amount if line_item.amount > 0.0 else 0.0
					res['account_id'] = account['id']
					res['ref_account_id'] = ref_analytic_id
					res['period_id'] = line_item.period_id.code
					res['ref_line_id'] = line_item.id
					ana_acc_7.create(cursor,user,res)
					


			# max_year = self._get_max_year(cursor,user,ids)
			# print max_year
			max_year = str(datetime.datetime.now().year)
			vals = {'analytic_name' : account['analytic_name'],
					'completion_detail' : self.get_analytic_line_list(cursor,user,ids,ref_analytic_id,max_year),
					#'year_completion' : (max_year,max_year), #from on_change,Call select_completion_detail agian
					}
		else:
			print 'id= false'
			
		return { 'value' : vals}
	
	def default_get(self, cr, uid, fields, context=None):
		print '==================default_get============='
		res = super(project, self).default_get(cr, uid, fields, context=context)
		print fields
		print res

		# print fields
		# max_year = self._get_max_year(cr,uid,ids)
		# res['year_completion'] = (max_year, max_year)
		# print '--------------------'
		return res

	def diff_analytic_account(self, cr, uid, ana_acc_61_ids, ana_acc_7_ids, ana_acc_61_items):
		# Find Diff between 61 ids and exist ids
		diff_ids = set(ana_acc_61_ids).difference(set(ana_acc_7_ids))
		diff_ids = list(diff_ids)
		print diff_ids
		if diff_ids != []:
			self.save_diff_analytic_account(cr, uid, diff_ids, ana_acc_61_items)

		return diff_ids

	def save_diff_analytic_account(self, cr, uid, diff_ids, ana_acc_61_items):
		# Save 61 data
		ana_acc_7 = self.pool.get('myproject.analytic_account_old')
		for diff_id in diff_ids:
			item_61 = (item for item in ana_acc_61_items if item["id"] == diff_id).next()
			diff_item = {}
			diff_item['analytic_code'] = item_61['code']
			diff_item['analytic_name'] = item_61['name']
			diff_item['ref_analytic_id'] = item_61['id']
			result = ana_acc_7.create(cr,uid,diff_item)

	def recall_analytic_account(self, cr, uid, ids, context=None):
		''' Get All account.analytic.account from 6.1 server, find diff and save to db'''
		res = {}
		# Get All data ids from database6.1
		client = erppeek.Client('http://192.168.70.5:8080','psp_test','admin_precise','smg')
		ana_acc_61 = client.model('account.analytic.account')
		ana_acc_61_items = ana_acc_61.read([])
		ana_acc_61_items = sorted(ana_acc_61_items, key=lambda k: k['id'])
		ana_acc_61_ids = [item['id'] for item in ana_acc_61_items]
		print ana_acc_61_ids
		print len(ana_acc_61_ids)

		# Get All data from this database
		ana_acc_7 = self.pool.get('myproject.analytic_account_old')
		ana_acc_7_items = ana_acc_7.read(cr,uid,ana_acc_7.search(cr,uid,[]),[])
		#print ana_acc_7_items
		ana_acc_7_ids = [item['ref_analytic_id'] for item in ana_acc_7_items]
		print ana_acc_7_ids
		print len(ana_acc_7_ids)

		# Find Diff between 61 ids and exist ids
		diff_ids = self.diff_analytic_account(cr, uid, ana_acc_61_ids, ana_acc_7_ids, ana_acc_61_items)
		
		return res
		
project()

class temp_completion(osv.osv):
	_name = 'myproject.temp_completion'
	_columns = {
		'period' : fields.char('Period', size=10),
		'current_cost' : fields.float('Cost'),
		'current_revenue' : fields.float('Revenue'),
		'accu_cost' : fields.float('Accumulated Cost'),
		'accu_revenue' : fields.float('Accumulated Revenue'),
		'est_cost' : fields.float('Estimated Cost'),
		'est_revenue' : fields.float('Estimated Revenue'),

	}
temp_completion()

class project_price(osv.osv):
	_name = 'myproject.project_price'

	# def _cal_total_by_currency(self, cr, uid, ids, name, arg, context=None):
	# 	res = {}
	# 	for item in self.browse(cr, uid, ids, context):
	# 		price_line_ids = self.pool.get('myproject.project_price_line').search(cr,uid, [('project_price_id','=',item.id)])
	# 		sum_price = 0.0
	# 		for price_id in price_line_ids:
	# 			price = self.pool.get('myproject.project_price_line').read(cr, uid, price_id, ['amount'])
	# 			print price
	# 			sum_price += price['amount']
	# 		print sum_price
	# 		res[item.id] = sum_price
	# 	return res


	_columns = {
		'project_id' : fields.many2one('myproject.project', 'Project ID'),
		'substation' : fields.char('Substation', size=50),
		'type' : fields.char('Type', size=50),
		'item' : fields.char('Item', size=50),
		'amount' : fields.float('Amount'),
		'currency' : fields.many2one('res.currency', 'Currency'),
		'rate' : fields.float('Rate'),

		#'project_price_line_ids' : fields.one2many('myproject.project_price_line', 'project_price_id', 'Line IDS'),
		#'total_by_currency' : fields.function(_cal_total_by_currency, method=True, type="float", readonly=True, string="Total"),
	}

	def save_project_price_popup(self, cr, uid, ids, context=None):
		# action to control popup page to close after click
		return {'type':'ir.actions.act_window_close'}

	def default_get(self, cr, uid, fields, context=None):
		print '==================default_get p_p============='
		res = super(project_price, self).default_get(cr, uid, fields, context=context)
		print fields
		print context
		print '--------------------'
		return res

	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		result = super(project_price, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
		print '===============fields_view_get p_p==========='
		return result

	def create(self, cursor, user, values, context=None):
		print '=======project_price create================'
		print context
		print values
		# geif 'project_id' in context.keys():
		# 	values['project_id'] = context['project_id']		
		return super(project_price, self).create(cursor, user, values, context)


project_price()

class project_price_line(osv.osv):
	_name = 'myproject.project_price_line'
	_columns = {
		'project_price_id' : fields.many2one('myproject.project_price','Project Price ID'),
		'type' : fields.char('Type', size=30),
		'amount' : fields.float('Amount'),
	}
project_price_line()

class budget(osv.osv):
	_name = 'myproject.budget'
	_columns = {
		'project_id' : fields.many2one('myproject.project', 'Project ID'),
		'description' : fields.char('Description', size=30),
		'qty' : fields.integer('Quantity'),
		'unit_price' : fields.integer('Unit Price'),
		'currency' : fields.many2one('res.currency', 'Currency'),
		'rate' : fields.float('Rate'),
		'amount' : fields.float('Amount'),
		'amount_bath' : fields.float('Bath'),
		#'total_amount_bath' : fields.function(_cal_total_amount_bath, method=True, type="float", string="Total Bath", readonly=True),
	}

	def save_budget_popup(self, cr, uid, ids, context=None):
		# action to control popup page to close after click
		return {'type':'ir.actions.act_window_close'}

	def create(self, cursor, user, values, context=None):
		print context
		# if 'project_id' in context.keys():
		# 	values['project_id'] = context['project_id']		
		return super(budget, self).create(cursor, user, values, context)

	def test_but(self, cr, uid, ids, context=None):
		print '000000000000000000000'
		return True

	def default_get(self, cr, uid, fields, context=None):
		print '==================default_get budget============='
		res = super(budget, self).default_get(cr, uid, fields, context=context)
		print fields
		print context
		print '--------------------'
		return res

	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
		result = super(budget, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
		print '===============fields_view_get budget==========='
		return result


budget()

class project_main(osv.osv):
	_name="myproject.project_main"
	_columns = {
		'analytic_id' : fields.many2one('myproject.analytic_account_old', 'Analytic ID'),
		'analytic_name' : fields.char('Analytic Name', size=128),
		'type' : fields.selection([('project','Project'), ('service', 'Service')], 'Type'),
		'project_price_detail' : fields.one2many('myproject.project_price', 'project_id', 'Project Price Ids'),
		
	}
	def recall_analytic_account(self, cr, uid, ids, context=None):
		''' Get All account.analytic.account from 6.1server, find diff and save to db'''
		res = {}
		# Get All data ids from database6.1
		client = erppeek.Client('http://192.168.70.5:8080','psp_test','admin_precise','smg')
		ana_acc_61 = client.model('account.analytic.account')
		ana_acc_61_items = ana_acc_61.read([])
		ana_acc_61_items = sorted(ana_acc_61_items, key=lambda k: k['id'])
		ana_acc_61_ids = [item['id'] for item in ana_acc_61_items]
		print ana_acc_61_ids
		print len(ana_acc_61_ids)

		# Get All data from this database
		ana_acc_7 = self.pool.get('myproject.analytic_account_old')
		#print ana_acc_7.search(cr,uid,[])
		ana_acc_7_items = ana_acc_7.read(cr,uid,ana_acc_7.search(cr,uid,[]),[])
		#print ana_acc_7_items
		ana_acc_7_ids = [item['ref_analytic_id'] for item in ana_acc_7_items]
		print ana_acc_7_ids
		print len(ana_acc_7_ids)

		# Find Diff between 61 ids and exist ids
		diff_ids = set(ana_acc_61_ids).difference(set(ana_acc_7_ids))
		diff_ids = list(diff_ids)
		print diff_ids
		# Save 61 data
		
		if diff_ids != []:
			print 'Add'
			for diff_id in diff_ids:
				item_61 = (item for item in ana_acc_61_items if item["id"] == diff_id).next()
				diff_item = {}
				diff_item['analytic_code'] = item_61['code']
				diff_item['analytic_name'] = item_61['name']
				diff_item['ref_analytic_id'] = item_61['id']
				#print diff_item
				result = ana_acc_7.create(cr,uid,diff_item)
			#print result
		#result = ana_acc_7.create(cr,uid,{'id':777,'code':'Test-777','name':'Test-777'})
		#print result
		return res
project_main()

class project_year(osv.osv):
	_name = 'myproject.project_year'
	_columns = {
		
		'name' : fields.char('Year', size=20),
	}
	_rec_name = 'name'
project_year()