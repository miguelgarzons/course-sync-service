from rest_framework.views import APIView
from rest_framework.response import Response
from course_sync_service.app.core.infrastructure.docs.docs import core_api_post_schema,core_api_get_schema
from course_sync_service.app.core.application.factory.strategy_factory import StrategyFactory
from course_sync_service.app.core.infrastructure.out.serializers_map import output_serializer_for
from course_sync_service.app.core.infrastructure.input.serializers_map import input_serializer_for

class CoreAPIView(APIView):

    @core_api_get_schema()
    def get(self, request, *args, **kwargs):
        return self._process(request)

    @core_api_post_schema()
    def post(self, request, *args, **kwargs):
        return self._process(request)


    def _process(self, request):
        # Todo viene por query params
        data = request.query_params

        action = data.get("wsfunction")
        serializer = input_serializer_for(action, request.method, data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)

        strategy = StrategyFactory.get_strategy(action)
        result = strategy.execute(serializer.validated_data)
        response_data = output_serializer_for(action, result)

        return Response(response_data)




