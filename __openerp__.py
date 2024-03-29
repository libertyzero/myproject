# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name" : "MyProject Management",
    "version" : "1.1",
    "author" : "OpenERP SA",
    "category" : "Generic Modules/Inventory Control",
    "depends" : ["base", "jasper_reports", "analytic"],

    
    "description": """
    This is the base module for managing products and pricelists in OpenERP.

    Products support variants, different pricing methods, suppliers
    information, make to stock/order, different unit of measures,
    packaging and properties.

    Pricelists support:
    * Multiple-level of discount (by product, category, quantities)
    * Compute price based on different criteria:
        * Other pricelist,
        * Cost price,
        * List price,
        * Supplier price, ...
    Pricelists preferences by product and/or partners.

    Print product labels with barcode.
    """,
    
    
    'data': [
        'myproject_view_oldserver.xml',
        # 'myproject_view_newserver.xml',
        'myproject_view.xml',
        'myproject_view_project_main.xml',
        'myproject_view_project_budget.xml',
        'myproject_view_project_project_price.xml',
    ],
    'css': ['static/src/css/myproject.css'],
    # 'test' : ['test/create_old_server_data.yml'],
    'demo': ['myproject_demo.xml',],
    'installable': True,
    'active': False,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
