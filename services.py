import product_pb2
import product_pb2_grpc
from .models import Product, Category
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class ProductService(product_pb2_grpc.ProductServiceServicer):
    
    # Create a new product
    def CreateProduct(self, request, context):
        try:
            category = Category.objects.get(id=request.category_id)
            product = Product.objects.create(
                title=request.title,
                price=request.price,
                image=request.image,
                description=request.description,
                category=category,
            )
            return product_pb2.ProductResponse(
                id=product.id,
                title=product.title,
                price=product.price,
                image=product.image.url if product.image else '',
                description=product.description,
                category_id=product.category.id,
            )
        except ObjectDoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Category not found")
            return product_pb2.ProductResponse()

    # Get a product by ID
    def GetProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            return product_pb2.ProductResponse(
                id=product.id,
                title=product.title,
                price=product.price,
                image=product.image.url if product.image else '',
                description=product.description,
                category_id=product.category.id,
            )
        except ObjectDoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.ProductResponse()

    # Update an existing product
    def UpdateProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            category = Category.objects.get(id=request.category_id)
            
            product.title = request.title
            product.price = request.price
            product.image = request.image
            product.description = request.description
            product.category = category
            product.save()

            return product_pb2.ProductResponse(
                id=product.id,
                title=product.title,
                price=product.price,
                image=product.image.url if product.image else '',
                description=product.description,
                category_id=product.category.id,
            )
        except ObjectDoesNotExist as e:
            if 'Category' in str(e):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Category not found")
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product not found")
            return product_pb2.ProductResponse()

    # Delete a product by ID
    def DeleteProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
            product.delete()
            return product_pb2.EmptyResponse()  # Return an empty response upon successful deletion
        except ObjectDoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.EmptyResponse()
