import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from django.conf import settings
import django

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")  
django.setup()

from main.apps.product.models import Product
import product_pb2
import product_pb2_grpc


class ProductService(product_pb2_grpc.ProductServiceServicer):
    def CreateProduct(self, request, context):
        product = Product.objects.create(
            title=request.title,
            price=request.price,
            description=request.description,
            category_id=request.category_id
        )
        return product_pb2.ProductResponse(
            id=product.id,
            title=product.title,
            price=product.price,
            description=product.description,
            category_id=product.category_id or 0
        )

    def GetProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.ProductResponse() 

        return product_pb2.ProductResponse(
            id=product.id,
            title=product.title,
            price=float(product.price),
            description=product.description,
            category_id=product.category_id
        )
    
    def UpdateProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.ProductResponse()

        product.title = request.title
        product.price = request.price
        product.description = request.description
        product.category_id = request.category_id
        product.save()

        return product_pb2.ProductResponse(
            id=product.id,
            title=product.title,
            price=product.price,
            description=product.description,
            category_id=product.category_id or 0
        )

    def DeleteProduct(self, request, context):
        try:
            product = Product.objects.get(id=request.id)
        except Product.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.DeleteProductResponse(message="Product not found")

        product.delete()
        return product_pb2.DeleteProductResponse(message="Product deleted successfully")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)

    SERVICE_NAMES = (
        product_pb2.DESCRIPTOR.services_by_name['ProductService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051 with reflection enabled...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
