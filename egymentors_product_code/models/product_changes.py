# -*- coding: utf-8 -*-

import re

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
from odoo.osv import expression


# Ahmed Salama Code Start ---->


class ProductAttributeInherit(models.Model):
    _inherit = "product.attribute"
    
    def unlink(self):
        color_attr = self.env.ref('product.product_attribute_2')
        treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
        
        if color_attr.id in self.ids or treatment_attr.id in self.ids:
            raise Warning(_("You are not authorized to delete Color or Treatment Attribute"))
        return super(ProductAttributeInherit, self).unlink()


class ResCompanyInherit(models.Model):
    _inherit = "res.company"
    
    company_registry = fields.Char(size=2)


class ProductCategoryInherit(models.Model):
    _inherit = "product.category"
    
    code = fields.Char(string="Code", size=2)
    category_type = fields.Selection([('fabric', 'Fabric'),
                                      ('yarn', 'Yarn'),
                                      ('other', 'Other'),
                                      ('not', 'Un-Specified')], "Category Type", default='not')
    
    @api.model
    def create(self, vals):
        """
        Inherit Category type to childs
        :param vals:
        :return: Super
        """
        print("VALS ", vals)
        if vals.get('parent_id'):
            parent_id = self.browse(vals.get('parent_id'))
            if parent_id:
                vals['category_type'] = parent_id.category_type
        return super(ProductCategoryInherit, self).create(vals)
    
    def unlink(self):
        """
        Prevent Delete one of master categories
        :return:
        """
        unlinkable_categs = [self.env.ref('egymentors_product_code.product_category_fabric'),
                             self.env.ref('egymentors_product_code.product_category_yarn'),
                             self.env.ref('egymentors_product_code.product_category_other')]
        for cat in self:
            if cat in unlinkable_categs:
                raise Warning(_("You are not authorized to delete one"
                                " of un-linkable categories (Fabric, Yarn, Other)"))
            return super(ProductCategoryInherit, self).unlink()


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    placeholder = fields.Char(compute='o_change')
    parent_categ = fields.Many2one('product.category', 'Parent Category')
    style_field = fields.Char(string="Style", size=8)
    # Cloths Parameters
    category_type = fields.Selection(related='categ_id.category_type')
    
    # Fabric Parameters
    landry_code_id = fields.Many2one('product.landry.code', "Landry Code")
    texmar_weight = fields.Many2many('texmar.weight', 'product_weight_rel', 'product_id', 'weight_id',
                                     string='SUB CATEGORY / DISCONTINUED')
    texmar_width = fields.Float("Width")
    repeat_id = fields.Many2one('product.repeat', "Repeat")
    composition_id = fields.Many2one('product.composition', "Composition")
    abrasion = fields.Char("Abrasion")
    category_id = fields.Many2one('texmar.product.category', "Category")
    sub_category_id = fields.Many2one('texmar.product.sub.category', "Under Testing 1")
    collection_id = fields.Many2many('product.collection', 'product_collection_rel', 'product_id', 'coll_id',
                                     string='Collection Year / Sample Box')
    manufacture_id = fields.Many2one('product.manufacture', "Manufacture")
    manufacture_type_id = fields.Many2one('product.manufacture.type', "Under Testing 2")
    fabric_type_id = fields.Many2one('product.fabric.type', "Fabric Type")
    usage_id = fields.Many2one('product.usage', "Usage")
    # Yarn Parameters
    texmar_color_id = fields.Many2one('product.texmar.color', "Color")
    kind_id = fields.Many2one('product.kind', "Kind")
    group_name_id = fields.Many2one('product.group.name', "Group Name")
    group_code = fields.Char(related='group_name_id.group_code')
    pant_id = fields.Many2one('product.pant', "Pant Name")
    pant_code = fields.Char(related='pant_id.pant_code')
    origin_id = fields.Many2many('product.origin', 'product_origin_rel', 'product_id', 'origin_id',
                                 string='Origin')
    under_testing_id = fields.Many2one('product.under.testing', "Under-Testing")

    @api.onchange('style_field')
    @api.depends('style_field')
    def o_change(self):
        for line in self:
            variants = line.env['product.product'].search([('product_tmpl_id.id','=',self.id.origin)])
            if len(variants) > 1:
                for variant in  variants:
                    variant.style_field = line.style_field
                    variant._generate_product_code()
        self._generate_product_code()


    @api.onchange('parent_categ', 'categ_id')
    @api.depends('categ_id.code')
    def _generate_product_code(self):
        """
		Generate code of each product using it's component
        parent categ Code from field [parent categ code] [2 digits]
        Category Code from field [Category Code] [2 digits]
        Style Code from field [Variant Style] [8 digits]
		"""
        for template in self:
            if template.parent_categ and template.parent_categ.code:
                parent_categ = template.parent_categ.code[:2]
            else:
                parent_categ = "00"
            if template.categ_id and template.categ_id.code:
                category_code = template.categ_id.code[:2]
            else:
                category_code = "00"
            if template.style_field:
                style_code = template.style_field[:8]
                barcode_style_code = template.style_field[-5:].lstrip("0")
            else:
                style_code = "00000000"
                barcode_style_code = "00000"
            
            template.default_code = "%s%s%s" % (parent_categ, category_code, style_code)
            template.barcode = "%s%s%s" % (parent_categ, category_code, barcode_style_code)
            # raise ValidationError('afafa')

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
    style_field = fields.Char(string="Style", size=8)
    default_code = fields.Char(size=18)
    barcode = fields.Char(size=15)
    parent_categ = fields.Many2one('product.category', 'Parent Category')
    category_code = fields.Char(compute='_generate_product_code', size=2,
                                help="Category Code from field [Category Code] [2 digits]")
    style_code = fields.Char(compute='_generate_product_code', size=8,
                             help="Style Code from field [Variant Style] [8 digits")
    barcode_style_code = fields.Char(compute='_generate_product_code', size=5,
                                     help="Style Code from field [Variant Style] [8 digits")
    color_code = fields.Char(compute='_generate_product_code', size=4,
                             help="Color Code from field [Variant Color Attribute] [4 digits]")
    treatment_code = fields.Char(compute='_generate_product_code', size=2,
                                 help="Treatment Code from field [Variant Treatment Attribute] [2 digits]")
    
    
    @api.onchange('parent_categ', 'categ_id', 'product_tmpl_id',
                  'product_template_attribute_value_ids')
    @api.depends('categ_id.code')
    def _generate_product_code(self):
        """
        Generate code of each product using it's component 
            parent categ Code from field [parent categ code] [2 digits]
            Category Code from field [Category Code] [2 digits]
            Style Code from field [Variant Style] [8 digits]
            Color Code from field [Variant Color Attribute] [4 digits]
            Treatment Code from field [Variant Treatment Attribute] [2 digits]
        """
        for product in self:
            color_attr = self.env.ref('product.product_attribute_2')
            treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
            if product.parent_categ and product.parent_categ.code:
                categ_code = product.parent_categ.code[:2]
            else:
                categ_code  = "00"
            if product.categ_id and product.categ_id.code:
                product.category_code = product.categ_id.code[:2]
            else:
                product.category_code = "00"
            if product.style_field:
                product.style_code = product.style_field[:8]
                product.barcode_style_code = product.style_field[-5:].lstrip("0")
            else:
                product.style_code = "00000000"
                product.barcode_style_code = "00000"
            
            for attr_val_line in product.product_template_attribute_value_ids:

                if attr_val_line.attribute_id == color_attr \
                        and attr_val_line.product_attribute_value_id:
                    product.color_code = attr_val_line.product_attribute_value_id.name[:4]
                if attr_val_line.attribute_id == treatment_attr \
                        and attr_val_line.product_attribute_value_id:
                    product.treatment_code = attr_val_line.product_attribute_value_id.name[:2]
            
            if not product.color_code:
                product.color_code = "0000"
            if not product.treatment_code:
                product.treatment_code = "00"
            product.default_code = "%s%s%s%s%s" % (categ_code, product.category_code,
                                                   product.style_code, product.color_code, product.treatment_code)
            product.barcode = "%s%s%s%s%s" % (categ_code, product.category_code,
                                            product.barcode_style_code, product.color_code,product.treatment_code)


            

class TexmarWeight(models.Model):
    _name = 'texmar.weight'
    _description = "SUB CATEGORY / DISCONTINUED"
    
    name = fields.Char("SUB CATEGORY / DISCONTINUED") 
    
            
class ProductLandryCode(models.Model):
    _name = 'product.landry.code'
    _description = "Landry Code"
    
    name = fields.Char("Landry Code")


class ProductRepeat(models.Model):
    _name = 'product.repeat'
    _description = "Repeat"
    
    name = fields.Char("Repeat")


class ProductComposition(models.Model):
    _name = 'product.composition'
    _description = "Composition"
    
    name = fields.Char("Composition")


class ProductCategory(models.Model):
    _name = 'texmar.product.category'
    _description = "Category"
    
    name = fields.Char("category")


class ProductSubCategory(models.Model):
    _name = 'texmar.product.sub.category'
    _description = "Sub Category"
    
    name = fields.Char("Sub Category")


class ProductCollection(models.Model):
    _name = 'product.collection'
    _description = "Collection"
    
    name = fields.Char("Collection Year / Sample Box")


class ProductManufacture(models.Model):
    _name = 'product.manufacture'
    _description = "Manufacture"
    
    name = fields.Char("Manufacture")


class ProductManufactureType(models.Model):
    _name = 'product.manufacture.type'
    _description = "Manufacture Type"
    
    name = fields.Char("Manufacture Type")
    
    
class ProductFabricType(models.Model):
    _name = 'product.fabric.type'
    _description = "Fabric Type"
    
    name = fields.Char("Fabric Type")


class ProductUsage(models.Model):
    _name = 'product.usage'
    _description = "Usage"
    
    name = fields.Char("Usage")

class ProductTexmarColor(models.Model):
    _name = 'product.texmar.color'
    _description = "Color"
    
    name = fields.Char("Color")


class ProductKind(models.Model):
    _name = 'product.kind'
    _description = "Kind"
    
    name = fields.Char("Kind")


class ProductPant(models.Model):
    _name = 'product.pant'
    _description = "Pant"
    
    name = fields.Char("Pant Name")
    pant_code = fields.Char("Pant Code")


class ProductGroupName(models.Model):
    _name = 'product.group.name'
    _description = "Group Name"
    
    name = fields.Char("Group Name")
    group_code = fields.Char("Group Code")


class ProductOrigin(models.Model):
    _name = 'product.origin'
    _description = "Origin"
    
    name = fields.Char("Origin")


class ProductUnderTesting(models.Model):
    _name = 'product.under.testing'
    _description = "Under-Testing"
    
    name = fields.Char("Under-Testing")
# Ahmed Salama Code End.
