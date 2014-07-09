# import time
# from xml.sax.saxutils import escape
# from openerp import tools
# from openerp.osv import fields, osv
# from openerp.tools.translate import _
# import psycopg2
# import calendar
# from lxml import etree

# class analytic_account_old(osv.osv):
# 	_name = 'myproject.analytic_account_old'
# 	_columns = {
# 		'analytic_code' : fields.char('Code', size=20),
# 		'analytic_name' : fields.char('Analytic Name', size=30),
# 		'account_line_ids' : fields.one2many('myproject.account_line_old', 'account_line_id', 'Account Line IDS'),
# 	}
# 	_rec_name = 'analytic_code'

# analytic_account_old()

# class account_line_old(osv.osv):
# 	_name = 'myproject.account_line_old'
# 	_columns = {
# 		'account_line_id' : fields.integer('Line ID'),
# 		'description' : fields.char('Description', size=30),
# 		'current_cost' : fields.float('Current Cost'),
# 		'current_revenue' : fields.float('Current Revenue'),
# 		'date' : fields.date('Date'),
# 		'analytic_id' : fields.many2one('myproject.analytic_account_old', 'Analytic ID'),

# 	}
# 	def default_get(self, cr, uid, fields, context=None):
# 		print '==================default_get old_line============='
# 		print context
# 		res = super(account_line_old, self).default_get(cr, uid, fields, context=context)
	
# 		return res
	
# analytic_account_old()

# class analytic_account_new(osv.osv):
# 	_name = 'myproject.analytic_account_new'
# 	_columns = {
# 		'analytic_code' : fields.char('Code', size=20),
# 		'analytic_name' : fields.char('Analytic Name', size=30),
# 		'account_line_ids' : fields.one2many('myproject_account_line_new', 'line_id', 'Account Line IDS'),
# 	}
# 	_rec_name = 'analytic_code'

# analytic_account_new()

# class account_line_new(osv.osv):
# 	_name = 'myproject.account_line_new'
# 	_columns = {
# 		'line_id' : fields.char('Line ID', size=20),
# 		'description' : fields.char('Description', size=30),
# 		'current_cost' : fields.float('Current Cost'),
# 		'current_revenue' : fields.float('Current Revenue'),
# 		'date' : fields.date('Date'),
# 		'analytic_id' : fields.many2one('myproject.analytic_account_new', 'Analytic ID'),

# 	}
# analytic_account_new()

# class project(osv.osv):
# 	_name = 'myproject.project'

# 	def _get_max_year(self,cr, uid, ids):
# 		max_year = self.pool.get('myproject.project_year').search(cr, uid, [])
# 		max_year = self.pool.get('myproject.project_year').read(cr, uid, int(max(max_year)), [])
# 		print max_year
# 		res = []
# 		res.append(max_year['id'])
# 		res.append(max_year['name'])
# 		print res
# 		return res

# 	def get_completion_detail(self,cr, uid, ids, analytic_id, select_year):
# 		line_list = []
# 		if analytic_id != 0:
# 			account_line_ids = self.pool.get('myproject.account_line_old').search(cr, uid, [('analytic_id','=',int(analytic_id))])
# 			print account_line_ids
# 			dict_date = {}
# 			for id in account_line_ids:
# 				account_line = self.pool.get('myproject.account_line_old').read(cr, uid, id,['current_cost','current_revenue','date'])
# 				year = account_line['date'][0:4]
# 				print year
# 				if year == select_year:
# 					month = account_line['date'][5:7]
# 					if month not in dict_date.keys():
# 						dict_date[month] = {'current_cost' : 0.0,
# 										'current_revenue' : 0.0 } 
# 						dict_date[month]['current_cost'] += account_line['current_cost']
# 						dict_date[month]['current_revenue'] += account_line['current_revenue']
					

# 			dict_month = dict((k,v) for k,v in enumerate(calendar.month_abbr))

# 			for k,v in dict_date.iteritems():
				
# 				if int(k) < 10:
					
# 					month_name = dict_month[int(k[1:])]
# 				else:
# 					month_name = dict_month[int(k)]
# 				line_list.append((0,0,{'period':month_name,
# 									'current_cost':v['current_cost'],
# 									'current_revenue':v['current_revenue'],
# 									'accu_cost' : v['current_cost']*2,
# 									'accu_revenue' : v['current_revenue']*2,
# 									'est_cost' : v['current_cost']*10,
# 									'est_revenue' : v['current_revenue']*10,
# 									}))
# 		print '----------------------'
# 		print line_list
# 		return line_list

# 	def select_completion_detail(self,cr, uid, ids, analytic_id, select_year_id):
# 		print '=======_select_completion_detail==========='
# 		vals = {}
# 		line_list = []
# 		print ids
# 		print analytic_id
# 		print select_year_id
# 		if not select_year_id:
# 			select_year_id = self._get_max_year(cr, uid, ids)[0]
# 		select_year = self.pool.get('myproject.project_year').read(cr, uid, select_year_id,[])
# 		print select_year
# 		if type(select_year) == list:
# 			select_year = select_year[0]['name']
# 		else:
# 			select_year = select_year['name']
# 		print select_year
# 		vals = {'completion_detail' : self.get_completion_detail(cr,uid,ids,analytic_id,select_year)}
# 		# if analytic_id != 0:
# 		# 	account_line_ids = self.pool.get('myproject.account_line_old').search(cr, uid, [('analytic_id','=',int(analytic_id))])
# 		# 	print account_line_ids
# 		# 	dict_date = {}
# 		# 	for id in account_line_ids:
# 		# 		account_line = self.pool.get('myproject.account_line_old').read(cr, uid, id,['current_cost','current_revenue','date'])
# 		# 		year = account_line['date'][0:4]
# 		# 		print year
# 		# 		if year == select_year:
# 		# 			month = account_line['date'][5:7]
# 		# 			if month not in dict_date.keys():
# 		# 				dict_date[month] = {'current_cost' : 0.0,
# 		# 								'current_revenue' : 0.0 } 
# 		# 				dict_date[month]['current_cost'] += account_line['current_cost']
# 		# 				dict_date[month]['current_revenue'] += account_line['current_revenue']
					

# 		# 	dict_month = dict((k,v) for k,v in enumerate(calendar.month_abbr))

# 		# 	for k,v in dict_date.iteritems():
				
# 		# 		if int(k) < 10:
					
# 		# 			month_name = dict_month[int(k[1:])]
# 		# 		else:
# 		# 			month_name = dict_month[int(k)]
# 		# 		line_list.append((0,0,{'period':month_name,
# 		# 							'current_cost':v['current_cost'],
# 		# 							'current_revenue':v['current_revenue'],
# 		# 							'accu_cost' : v['current_cost']*2,
# 		# 							'accu_revenue' : v['current_revenue']*2,
# 		# 							'est_cost' : v['current_cost']*10,
# 		# 							'est_revenue' : v['current_revenue']*10,
# 		# 							}))
# 		# print '----------------------'
# 		# print line_list
# 		# vals = {'completion_detail' : line_list}
# 		return { 'value' : vals}

# 	def _cal_sum_project_price(self, cr, uid, ids, name, arg, context=None):
# 		print '===========_cal_sum_project_price==============='
# 		# Function for field sum_project_price
# 		# Select all amount of project_price_line (In DB) and sum it
# 		res = {}
# 		for this_project in self.browse(cr, uid, ids):
# 			print this_project.id
# 			item_ids = self.pool.get('myproject.project_price').search(cr, uid, [('project_id','=',this_project.id)])
# 			sum_price = 0.0
# 			for item_id in item_ids:
# 				price_item = self.pool.get('myproject.project_price').read(cr, uid, item_id, ['amount'])
# 				price_line_ids = self.pool.get('myproject.project_price_line').search(cr,uid, [('project_price_id','=',price_item['id'])])
# 				for price_id in price_line_ids:
# 					price = self.pool.get('myproject.project_price_line').read(cr, uid, price_id, ['amount'])
# 					print price
# 					sum_price += price['amount']
# 			print sum_price
# 			res[this_project.id] = sum_price
# 		return res

# 	def _cal_sum_budget(self, cr, uid, ids, name, arg, context=None):
# 		print '===========_cal_sum_budget==============='
# 		# Function for field sum_budget
# 		# Select all amount of budget (In DB) and sum it
# 		res = {}
# 		for this_project in self.browse(cr, uid, ids):
# 			print this_project.id
# 			item_ids = self.pool.get('myproject.budget').search(cr, uid, [('project_id','=',this_project.id)])
# 			sum_budget = 0.0
# 			for item_id in item_ids:
# 				bath = self.pool.get('myproject.budget').read(cr, uid, item_id, ['amount_bath'])
# 				print bath
# 				sum_budget += bath['amount_bath']
# 			print sum_budget
# 			res[this_project.id] = sum_budget
# 		return res

# 	def _completion_detail(self, cr, uid, ids, name, arg, context=None):
# 		print '=====completion detail==========='
# 		# Function for field completion_detail, to show completion data of selected analytic id
# 		# Input analytic_id, select_year
# 		# Call method select_completion_detail to query data with analytic_id and select_year
# 		# Use After save data, redirect to show data page
# 		res = {}
# 		print arg
# 		print ids
# 		if ids != []:
# 			this_analytic_id = self.pool.get('myproject.project').read(cr, uid, ids, ['analytic_id'])
# 			print 'analy id: ', this_analytic_id[0]['analytic_id']
# 			#res[ids[0]] = self.get_completion_detail(cr,uid,ids, int(this_analytic_id[0]['analytic_id']), self._get_max_year(cr, uid,ids)[0])
# 		return res

# 	def _get_selection(self, cr, uid, context=None):
# 		print '====get_selection==========='
# 		print context
# 		# Function for field selection, to create select choice
# 		# Run when open form, after save data
# 		# Simulate another server situation
# 		# Hand code python to query data from another server and put to selection choice 
# 		list_res = []
# 		#if 'view_type' in context and context['view_type'] == 'form':
# 		# Work! but get error when create project
# 		try:
# 			conn = psycopg2.connect("dbname='litu7' user='openerp' host='localhost' password='password'")
# 		except:
# 			print "I am unable to connect to the database"
		
# 		try:
# 			cur = conn.cursor()
# 			cur.execute("""SELECT * from myproject_analytic_account_old""")
# 		except:
# 			print "I can't SELECT from myproject_analytic_account_old"
		
# 		rows = cur.fetchall()
# 		print rows
		
# 		for item in rows:
# 			list_res.append((str(item[0]),item[6]))
		
# 		return list_res

# 	# def _project_price_detail(self, cr, uid, ids, name, arg, context=None):
# 	# 	print '=====project price detail==========='
# 	# 	# Not Use
# 	# 	res = {}
# 	# 	print ids
# 	# 	cr.execute('SELECT currency,rate, tt.sum_amount, id FROM myproject_project_price t JOIN (SELECT project_price_id,sum(amount) as sum_amount FROM myproject_project_price_line group by project_price_id) tt ON t.id = tt.project_price_id WHERE t.project_id = %s;', ids)
# 	# 	main_rows = cr.fetchall()
# 	# 	print main_rows
# 	# 	line_list = []
# 	# 	p_line_list = [(0,0,{'type':'ABCDE','amount':125})]
# 	# 	for row in main_rows:
			
# 	# 		s_id = [row[3]]
# 	# 		print s_id
# 	# 		cr.execute('SELECT type,amount FROM myproject_project_price_line WHERE project_price_id = %s', s_id)
# 	# 		sub_row = cr.fetchall()
# 	# 		main_dict = {}
# 	# 		main_dict = {'currency':row[0],
# 	# 								'rate':row[1],
# 	# 								'total_by_currency' : row[2],
# 	# 					}
# 	# 		sub_line_list = []
# 	# 		for s_row in sub_row:
# 	# 			sub_line_list.append((0,0,{'type':s_row[0], 'amount':s_row[1]}))

# 	# 		main_dict['project_price_line_ids'] = sub_line_list
# 	# 		line_list.append((0,0,main_dict))
# 	# 	res[ids[0]] = line_list
# 	# 	return res

# 	def _budget_detail(self, cr, uid, ids, name, arg, context=None):
# 		print '=====budget detail==========='
# 		# Function one2many for budget_detial, show budget data
# 		# Will change type of field to one2many
# 		res = {}
# 		print ids
# 		cr.execute('SELECT description,qty,unit_price,currency,rate,amount,amount_bath FROM myproject_budget WHERE project_id = %s ORDER BY description', ids)
# 		rows = cr.fetchall()
# 		print rows
# 		line_list = []
# 		for row in rows:
# 			line_list.append((0,0,{ 'description' : row[0],
# 									'qty' : row[1],
# 									'unit_price' : row[2],
# 									'currency': row[3],
# 									'rate': row[4],
# 									'amount': row[5],
# 									'amount_bath': row[6],
# 									}))
# 		res[ids[0]] = line_list
# 		return res

# 	def _year_completion(self, cr, uid, ids, name, arg, context=None):
# 		res = {}
		
# 		return res

# 	_columns = {
# 		'project_id' : fields.integer('ID'),
# 		'analytic_id' : fields.selection(_get_selection, 'Analytic ID', required=True),
# 		'analytic_name' : fields.char('Analytic Name', size=30),
# 		'type' : fields.selection([('project','Project'), ('service', 'Service')], 'Type'),
# 		'sum_project_price' : fields.function(_cal_sum_project_price, method=True, type="float", string="Project Price", readonly=True),
# 		'sum_budget' : fields.function(_cal_sum_budget, method=True, type="float", string="Budget", readonly=True),
# 		'completion_detail' : fields.function(_completion_detail, method=True, type="one2many", relation="myproject.temp_completion", string="Completion"),
# 		#'test_selection' : fields.selection(_get_selection, 'Selectio', required=True),
# 		'project_price_detail' : fields.one2many('myproject.project_price', 'project_id', 'Project Price Ids'),
# 		'budget_detail' : fields.one2many('myproject.budget', 'project_id', 'Budget Ids'),
# 		#'project_price_detail' : fields.function(_project_price_detail, method=True, type="one2many", relation="myproject.project_price", string="Project Price"),
# 		#'budget_detail' : fields.function(_budget_detail, method=True, type="one2many", relation="myproject.budget", string="Budget"),
# 		#'year_completion' : fields.function(_test, method=True, type="selection", string="Year", relation="myproject.project_year"),
# 		'year_completion': fields.function(_year_completion, method=True, type="many2one", relation='myproject.project_year', string="Year"),
# 		#'year_completion': fields.many2one('myproject.project_year', 'Year'),
# 		'state': fields.selection([('draft', 'Draft')], 'State', required=True, readonly=True),
		
# 		 #Addition Field
# 		'customer' : fields.char('Customer', size=30),
# 		'contact' : fields.char('Contact', size=30),
# 		'contact_no' : fields.char('Contact No.', size=20),
# 		'contact_date' : fields.date('Contact Date'),
# 		'start_date' : fields.date('Start Date'),
# 		'end_date' : fields.date('End Date'),
# 		'cost_center' : fields.char('Cost Center'),
# 		'project_manager' : fields.char('Project Manager'),
# 	}

# 	_defaults = {
# 		'state' : lambda *a: 'draft',
# 	}
# 	_rec_name = 'project_id'

# 	def create(self, cursor, user, values, context=None):
# 		print '============create================='
# 		print values
# 		print '----'
# 		res_id = super(project, self).create(cursor, user, values, context)
# 		print 'res_id: ',res_id
# 		return res_id

# 	def write(self, cursor, user, id, values, context=None):
# 		print '==================write==============='
# 		return super(project, self).write(cursor, user, id, values, context)


# 	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
# 		print '==================fields_view_get======================='
# 		print view_type
# 		context['view_type'] = view_type
# 		result = super(project, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
# 		# if view_type == 'form':
# 		# 	doc = etree.XML(result['arch'])
# 		# 	xml_start = etree.Element("div")
# 		# 	print '==============fields_view_get==================='
# 		# 	print doc
# 		# 	print '-------------------'
# 		# 	print xml_start
# 		# 	xml_no_pref_1 = etree.Element("div")
# 		# 	xml_no_pref_1.set('class','oe_inline oe_lunch_intro')
# 		# 	xml_no_pref_2 = etree.Element("h3")
# 		# 	xml_no_pref_2.text = _("Year: ")
# 		# 	xml_no_pref_3 = etree.Element("p")
# 		# 	xml_no_pref_3.set('class','oe_grey')
# 		# 	xml_no_pref_3.text = _("Select a product and put your order comments on the note.")
# 		# 	xml_no_pref_4 = etree.Element("p")
# 		# 	xml_no_pref_4.set('class','oe_grey')
# 		# 	xml_no_pref_4.text = _("Your favorite meals will be created based on your last orders.")
# 		# 	xml_no_pref_5 = etree.Element("p")
# 		# 	xml_no_pref_5.set('class','oe_grey')
# 		# 	xml_no_pref_5.text = _("Don't forget the alerts displayed in the reddish area")
# 		# 	#structure Elements
# 		# 	xml_start.append(xml_no_pref_1)
# 		# 	xml_no_pref_1.append(xml_no_pref_2)
# 		# 	xml_no_pref_1.append(xml_no_pref_3)
# 		# 	xml_no_pref_1.append(xml_no_pref_4)
# 		# 	xml_no_pref_1.append(xml_no_pref_5)
# 		# 	first_node = doc.xpath("//div[@name='preferences']")
# 		# 	print first_node
# 		# 	if first_node and len(first_node)>0:
# 		# 		first_node[0].append(xml_start)
# 		# 	result['arch'] = etree.tostring(doc)
# 		# 	print result['arch']
# 		return result

# 	def project_price_detail_change(self, cursor, user, ids, one2many_list):
# 		# For project_price one2many, when data in table has change(add,edit,delete)
# 		# call this to calculate new sum_project_price by sum saved date and not saved data
# 		vals = {}
# 		print one2many_list
# 		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
# 		sum_price = 0.0
# 		for ind, price_list in enumerate(one2many_list):
# 			print price_list
# 			print price_list[1]
# 			if price_list[0] == 4:
# 				# 4 => have exist
# 				price_item_ids = self.pool.get('myproject.project_price_line').search(cursor, user, [('project_price_id','=',price_list[1])])
# 				print price_item_ids
# 				for price_item_id in price_item_ids:
# 					price_item = self.pool.get('myproject.project_price_line').read(cursor, user, price_item_id,['amount'])
# 					print price_item
# 					sum_price += price_item['amount']
# 			elif price_list[0] == 2:
# 				# 2 => delete from tree
# 				del(one2many_list[ind])
# 				print one2many_list
# 			else:
# 				# 0 => add new to tree or 1 => edit
# 				price_item = price_list[2]['project_price_line_ids']
# 				for price in price_item:
# 					sum_price += price[2]['amount']
# 		print sum_price
# 		vals = {'sum_project_price' : sum_price}
# 		print vals
# 		return { 'value' : vals}

# 	def budget_detail_change(self, cursor, user, ids, one2many_list):
# 		# For Budget one2many, when data in table has change(add,edit,delete)
# 		# call this to calculate new sum_project_price by sum saved date and not saved data
# 		vals = {}
# 		print one2many_list
# 		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
# 		sum_price = 0.0
# 		for ind, price_list in enumerate(one2many_list):
# 			print price_list
# 			print price_list[1]
# 			if price_list[0] == 4:
# 				# 4 => have exist				
# 				price_item = self.pool.get('myproject.budget').read(cursor, user, price_list[1],['amount_bath'])
# 				print price_item
# 				sum_price += price_item['amount_bath']
# 			elif price_list[0] == 2:
# 				# 2 => delete from tree
# 				del(one2many_list[ind])
# 				print one2many_list
# 			else:
# 				# 0 => add new to tree or 1 => edit
# 				sum_price += price_list[2]['amount_bath']
# 		print sum_price
# 		vals = {'sum_budget' : sum_price}
# 		print vals
# 		return { 'value' : vals}



# 	def select_analytic_id(self, cursor, user, ids, analytic_id):
# 		print '======select_analytic_id============'
# 		# On change for field analytic_id
# 		# get analytic_id and call select_completion_detail to fill data in another field and 
# 		# show completion data in table with max_year
# 		vals = {}
# 		print analytic_id
# 		if analytic_id:
# 			# analytic_id will be False, When saved data and redirect to show data page
# 			account = self.pool.get('myproject.analytic_account_old').read(cursor,user, int(analytic_id), ['analytic_name'])
# 			print account
# 			max_year = self._get_max_year(cursor,user,ids)
# 			print max_year
# 			#res_selection = self.get_completion_detail(cursor,user,ids, int(analytic_id), max_year[0])
# 			vals = {'analytic_name' : account['analytic_name'],
# 					#'completion_detail' : res_selection,
# 					'year_completion' : (max_year[0],max_year[1]), #from on_change,Call select_completion_detail agian
# 					}
# 		else:
# 			print 'id= false'
# 			print ids
# 			print '--------------'			
# 			this_item = self.pool.get('myproject.project').read(cursor, user, ids[0], [])
# 			print this_item
# 			print ';--------------'
			
# 		return { 'value' : vals}

# 	# def change_year_completion(self, cursor, user, ids, year, analytic_id):
# 	# 	print '==========change_year_completion==========='
# 	# 	vals = {}
# 	# 	print year, analytic_id
# 	# 	if year and analytic_id:
# 	# 		= self.pool.get('myproject.account_line_old')

# 	def default_get(self, cr, uid, fields, context=None):
# 		print '==================default_get============='
# 		res = super(project, self).default_get(cr, uid, fields, context=context)
# 		print fields
# 		print res

# 		# print fields
# 		# max_year = self._get_max_year(cr,uid,ids)
# 		# res['year_completion'] = (max_year, max_year)
# 		# print '--------------------'
# 		return res
		
# project()

# class temp_completion(osv.osv):
# 	_name = 'myproject.temp_completion'
# 	_columns = {
# 		'period' : fields.char('Period', size=10),
# 		'current_cost' : fields.float('Cost'),
# 		'current_revenue' : fields.float('Revenue'),
# 		'accu_cost' : fields.float('Accumulated Cost'),
# 		'accu_revenue' : fields.float('Accumulated Revenue'),
# 		'est_cost' : fields.float('Estimated Cost'),
# 		'est_revenue' : fields.float('Estimated Revenue'),

# 	}
# temp_completion()

# class project_price(osv.osv):
# 	_name = 'myproject.project_price'

# 	def _cal_total_by_currency(self, cr, uid, ids, name, arg, context=None):
# 		res = {}
# 		for item in self.browse(cr, uid, ids, context):
# 			price_line_ids = self.pool.get('myproject.project_price_line').search(cr,uid, [('project_price_id','=',item.id)])
# 			sum_price = 0.0
# 			for price_id in price_line_ids:
# 				price = self.pool.get('myproject.project_price_line').read(cr, uid, price_id, ['amount'])
# 				print price
# 				sum_price += price['amount']
# 			print sum_price
# 			res[item.id] = sum_price
# 		return res


# 	_columns = {
# 		'project_id' : fields.many2one('myproject.project', 'Project ID'),
# 		'currency' : fields.many2one('res.currency', 'Currency'),
# 		'rate' : fields.float('Rate'),
# 		'project_price_line_ids' : fields.one2many('myproject.project_price_line', 'project_price_id', 'Line IDS'),
# 		'total_by_currency' : fields.function(_cal_total_by_currency, method=True, type="float", readonly=True, string="Total"),
# 	}

# 	def save_project_price_popup(self, cr, uid, ids, context=None):
# 		# action to control popup page to close after click
# 		return {'type':'ir.actions.act_window_close'}

# 	def default_get(self, cr, uid, fields, context=None):
# 		print '==================default_get p_p============='
# 		res = super(project_price, self).default_get(cr, uid, fields, context=context)
# 		print fields
# 		print context
# 		print '--------------------'
# 		return res

# 	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
# 		result = super(project_price, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
# 		print '===============fields_view_get p_p==========='
# 		return result

# 	def import_data(self,cr, uid, fields, datas, mode='init', current_module='', noupdate=False, context=None, filename=None):
# 		print '===========project_price import_data============='
# 		print fields
# 		print data
# 		print mode
# 		print current_module
# 		print context
# 		print file_name
# 		return super(project_price, self).import_data(cr,uid,fields,data,mode,current_module,noupdate,context,file_name)

# 	def create(self, cursor, user, values, context=None):
# 		print '=======project_price create================'
# 		print context
# 		print values
# 		# geif 'project_id' in context.keys():
# 		# 	values['project_id'] = context['project_id']		
# 		return super(project_price, self).create(cursor, user, values, context)


# project_price()

# class project_price_line(osv.osv):
# 	_name = 'myproject.project_price_line'
# 	_columns = {
# 		'project_price_id' : fields.many2one('myproject.project_price','Project Price ID'),
# 		'type' : fields.char('Type', size=30),
# 		'amount' : fields.float('Amount'),
# 	}
# project_price_line()

# class budget(osv.osv):
# 	_name = 'myproject.budget'
# 	_columns = {
# 		'project_id' : fields.many2one('myproject.project', 'Project ID'),
# 		'description' : fields.char('Description', size=30),
# 		'qty' : fields.integer('Quantity'),
# 		'unit_price' : fields.integer('Unit Price'),
# 		'currency' : fields.many2one('res.currency', 'Currency'),
# 		'rate' : fields.float('Rate'),
# 		'amount' : fields.float('Amount'),
# 		'amount_bath' : fields.float('Bath'),
# 		#'total_amount_bath' : fields.function(_cal_total_amount_bath, method=True, type="float", string="Total Bath", readonly=True),
# 	}

# 	def save_budget_popup(self, cr, uid, ids, context=None):
# 		# action to control popup page to close after click
# 		return {'type':'ir.actions.act_window_close'}

# 	def create(self, cursor, user, values, context=None):
# 		print context
# 		# if 'project_id' in context.keys():
# 		# 	values['project_id'] = context['project_id']		
# 		return super(budget, self).create(cursor, user, values, context)

# 	def test_but(self, cr, uid, ids, context=None):
# 		print '000000000000000000000'
# 		return True

# 	def default_get(self, cr, uid, fields, context=None):
# 		print '==================default_get budget============='
# 		res = super(budget, self).default_get(cr, uid, fields, context=context)
# 		print fields
# 		print context
# 		print '--------------------'
# 		return res

# 	def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
# 		result = super(budget, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
# 		print '===============fields_view_get budget==========='
# 		return result


# budget()

# class project_main(osv.osv):
# 	_name="myproject.project_main"

# 	def _get_selection(self, cr, uid, context=None):
# 		print '====get_selection==========='
# 		print context
# 		this_view = self.po
# 		list_res = []
# 		# all_item = self.pool.get('myproject.analytic_account_new')
# 		# ids = all_item.search(cr, uid, [])
# 		# for id in ids:
# 		# 	item = self.pool.get('myproject.analytic_account_new').read(cr,uid,id,['analytic_code','analytic_name'])
# 		# 	list_res.append((item['analytic_code'],item['analytic_name']))
# 		try:
# 			conn = psycopg2.connect("dbname='litu7' user='openerp' host='localhost' password='password'")
# 		except:
# 			print "I am unable to connect to the database"
		
# 		try:
# 			cur = conn.cursor()
# 			cur.execute("""SELECT * from myproject_analytic_account_old""")
# 		except:
# 			print "I can't SELECT from myproject_analytic_account_old"
		
# 		rows = cur.fetchall()
# 		print rows
		
# 		for item in rows:
# 			list_res.append((str(item[0]),item[5]))
# 		print '----list_res----'
# 		print list_res
# 		return list_res

# 	_columns = {
# 		'analytic_id' : fields.selection(_get_selection, 'Analytic ID'),
# 		'analytic_name' : fields.char('Analytic Name', size=30),
# 		'type' : fields.selection([('project','Project'), ('service', 'Service')], 'Type'),
# 		'project_price_detail' : fields.one2many('myproject.project_price', 'project_id', 'Project Price Ids'),
		
# 	}
# project_main()

# class project_year(osv.osv):
# 	_name = 'myproject.project_year'
# 	_columns = {
		
# 		'name' : fields.char('Year', size=20),
# 	}
# 	_rec_name = 'name'
# project_year()