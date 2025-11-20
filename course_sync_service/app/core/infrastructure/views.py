from rest_framework.views import APIView
from rest_framework.response import Response
from course_sync_service.app.core.infrastructure.input.serializers_map import input_serializer_for
from course_sync_service.app.core.application.factory.strategy_factory import StrategyFactory
from course_sync_service.app.core.infrastructure.out.serializers_map import output_serializer_for


class CoreAPIView(APIView):

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("wsfunction")
        serializer=input_serializer_for(action)(result,many=isinstance(result, list))
        if serializer.is_valid():
            strategy = StrategyFactory.get_strategy(action)
            result = strategy.execute(serializer.validated_data)
            response_serializer = output_serializer_for(action)(result,many=isinstance(result, list))
            return Response({"status": "success", "data": response_serializer.data})
        return Response({"errors": serializer.errors}, status=400)