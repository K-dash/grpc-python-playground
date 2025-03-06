from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Silent Patient"),
        BookRecommendation(id=2, title="The Maltese Falcon"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=3, title="The Time Machine"),
        BookRecommendation(id=4, title="The War of the Worlds"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=5, title="The 7 Habits of Highly Effective People"),
        BookRecommendation(id=6, title="The Power of Now"),
    ],
}

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_result = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_result)

        return RecommendationResponse(recommendations=books_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
