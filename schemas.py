from marshmallow import Schema, fields

#__Plain__

#user
class PlainUserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(load_only=True)
    phone = fields.Str()
    birthday = fields.Date()
    city = fields.Str()
    country = fields.Str()

#admin
class AdminSchema(Schema):
    email = fields.Str()
    password = fields.Str(load_only=True) #load_only --> user can write it but no return

#product
class PlainProductSchema(Schema):
    product_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    price = fields.Int()
    amount = fields.Int()
    image = fields.Str()

#seller
class PlainSellerSchema(PlainUserSchema):
    seller_id = fields.Int(load_only=True)
    national_id = fields.Str()
    bank_acc = fields.Str()
    brand_name = fields.Str()

#category
class PlainCatSchema(Schema):
    cat_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    Product_cat = fields.Nested(PlainProductSchema(), dump_only=True, many=True)
    
class PlainCCatSchema(Schema):
    cat_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()

#event
class PlainEventSchema(Schema):
    event_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    duration = fields.Str()
    date = fields.Date()

#order
class PlainOrderSchema(Schema):
    order_id = fields.Int(dump_only=True)
    date = fields.Date()
    amount = fields.Int()
    block_no = fields.Int()
    street = fields.Str()
    city = fields.Str()
    country = fields.Str()


#course
class PlainCourseSchema(Schema):
    course_id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    duration = fields.Str()

#payment
class PlainPaymentSchema(Schema):
    payment_id = fields.Int(dump_only=True)
    date = fields.Date()
    amount = fields.Int()
    method = fields.Str()
    card_name = fields.Str()
    card_number = fields.Int()
    exp_month = fields.Str()
    exp_year = fields.Int()
    cvv = fields.Int()

#plan
class PlainPlanSchema(Schema):
    plan_id = fields.Int(dump_only=True)
    name = fields.Str()
    duration = fields.Str()

#video
class PlainVideoSchema(Schema):
    video_id = fields.Int(dump_only=True)
    number = fields.Int()
    video = fields.Str()
    description = fields.Str()

class UserSchema(PlainUserSchema):
    # role = fields.Nested(PlainRoleSchema(), dump_only=True)
    order_buyer = fields.Nested(PlainOrderSchema(), dump_only=True)
    plan = fields.List(fields.Nested(PlainPlanSchema()), dump_only=True)
    event = fields.List(fields.Nested(PlainEventSchema()), dump_only=True)
    course = fields.List(fields.Nested(PlainCourseSchema()), dump_only=True)

class PlanSchema(Schema):
    learner = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

class CourseSchema(Schema):
    cat_id = fields.Int(load_only=True)
    cat = fields.Nested(PlainCatSchema(), dump_only=True)
    video_course = fields.Nested(PlainVideoSchema(), dump_only=True)
    learner = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)

#__association tables__

class LearnerPlanSchema(Schema):
    learner = fields.Nested(UserSchema)
    plan = fields.Nested(PlanSchema)

class LearnerCourseSchema(Schema):
    learner = fields.Nested(UserSchema)
    course = fields.Nested(CourseSchema)


# class RoleSchema(Schema):
#     user_id = 
#     user =

#category
class CatSchema(Schema):
    Product_cat = fields.Nested(PlainProductSchema(), dump_only=True)
    
class CategoryUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    

class CCategoryUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()


class CourseUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    duration = fields.Str()

#product
class ProductSchema(PlainProductSchema):
    cat_id = fields.Int(required=False, load_only=True)
    seller_id = fields.Int(required=False, load_only=True)
    event_id = fields.Int(required=False, load_only=True)
    #relations
    seller = fields.Nested(PlainSellerSchema(), dump_only=True)
    cat = fields.Nested(PlainCatSchema(), dump_only=True)
    event = fields.Nested(PlainEventSchema(), dump_only=True)
    order = fields.List(fields.Nested(PlainOrderSchema()), dump_only=True)

#course
class CourseSchema(PlainCourseSchema):
    cat_id = fields.Int(required=False, load_only=True)
    cat = fields.Nested(PlainCCatSchema(), dump_only=True)
    video_course = fields.Nested(PlainVideoSchema(), dump_only=True)
    learner = fields.List(fields.Nested(PlainCourseSchema()), dump_only=True)

#video
class VideoSchema(PlainVideoSchema):
    course_id = fields.Int(required=False, load_only=True)
    course = fields.Nested(PlainVideoSchema(), dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    price = fields.Int()
    amount = fields.Int()
    image = fields.Str()

# Order
class OrderSchema(Schema):
    #Fks
    buyer_id = fields.Int(required=True, load_only=True)
    #relations
    buyer = fields.Nested(PlainUserSchema(), dump_only=True)
    payment = fields.Nested(PlainPaymentSchema(), dump_only=True)
    product = fields.List(fields.Nested(PlainProductSchema()), dump_only=True)

class OrderProductSchema(Schema):
    order = fields.Nested(OrderSchema)
    product = fields.Nested(ProductSchema)
