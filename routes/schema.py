import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from .models import Route, BusStop, Stage


# create a graphql type for Route
class RouteType(DjangoObjectType):
    class Meta:
        model = Route


# create a graphql type for Bus stop
class BusStopType(DjangoObjectType):
    class Meta:
        model = BusStop


# create a graphql type for Stage
class StageType(DjangoObjectType):
    class Meta:
        model = Stage


# create a Query type
class Query(ObjectType):
    route = graphene.Field(RouteType, id=graphene.Int())
    bus_stop = graphene.Field(BusStopType, id=graphene.Int())
    stage = graphene.Field(StageType, id=graphene.Int())

    routes = graphene.List(RouteType)
    bus_stops = graphene.List(BusStopType)
    stages = graphene.List(StageType)

    def resolve_route(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Route.objects.get(pk=id)

        return None

    def resolve_routes(self, info, **kwargs):
        return Route.objects.all()

    def resolve_bus_stop(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return BusStop.objects.get(pk=id)

        return None

    def resolve_bus_stops(self, info, **kwargs):
        return BusStop.objects.all()

    def resolve_stage(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Stage.objects.get(pk=id)

        return None

    def resolve_stages(self, info, **kwargs):
        return Stage.objects.all()


# create input types
class BusStopInput(graphene.InputObjectType):
    id = graphene.ID()
    stop_name = graphene.String()
    lat = graphene.Float()
    lon = graphene.Float()

class StageInput(graphene.InputObjectType):
    id = graphene.ID()
    stage_name = graphene.String()
    lat = graphene.Float()
    lon = graphene.Float()

class RouteInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    stops = graphene.List(BusStopInput)
    stages = graphene.List(StageInput)

# Create mutations for bus stop
class CreateBusStop(graphene.Mutation):
    class Arguments:
        input = BusStopInput(required=True)

    ok = graphene.Boolean()
    stop = graphene.Field(BusStopType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        bus_stop_instance = BusStop(stop_name=input.stop_name, lat=input.lat, lon=input.lon)
        bus_stop_instance.save()
        return CreateBusStop(ok=ok, stop=bus_stop_instance)

class UpdateBusStop(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = RouteInput(required=True)

    ok = graphene.Boolean()
    stop = graphene.Field(BusStopType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        bus_stop_instance = BusStop.objects.get(pk=id)
        if bus_stop_instance:
            ok = True
            bus_stop_instance.stop_name = input.stop_name
            bus_stop_instance.lat = input.lat
            bus_stop_instance.lon = input.lon
            bus_stop_instance.save()
            return UpdateBusStop(ok=ok, stop=bus_stop_instance)
        return UpdateBusStop(ok=ok, stop=None)


# Create mutations for stage
class CreateStage(graphene.Mutation):
    class Arguments:
        input = StageInput(required=True)

    ok = graphene.Boolean()
    stage = graphene.Field(StageType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        stage_instance = Stage(stage_name=input.stage_name, lat=input.lat, lon=input.lon)
        stage_instance.save()
        return CreateStage(ok=ok, stage=stage_instance)

class UpdateStage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = RouteInput(required=True)

    ok = graphene.Boolean()
    stage = graphene.Field(StageType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        stage_instance = Stage.objects.get(pk=id)
        if stage_instance:
            ok = True
            stage_instance.stage_name = input.stage_name
            stage_instance.lat = input.lat
            stage_instance.lon = input.lon
            stage_instance.save()
            return UpdateStage(ok=ok, stage=stage_instance)
        return UpdateStage(ok=ok, stage=None)


# Create mutations for routes
class CreateRoute(graphene.Mutation):
    class Arguments:
        input = RouteInput(required=True)

    ok = graphene.Boolean()
    route = graphene.Field(RouteType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        stops = []
        stages = []
        for stop_input in input.stops:
            stop = BusStop.objects.get(pk=stop_input.id)
            if stop is None:
                return CreateRoute(ok=False, route=None)
            stops.append(stop)
        for stage_input in input.stages:
            stage = Stage.objects.get(pk=stage_input.id)
            if stage is None:
                return CreateRoute(ok=False, route=None)
            stages.append(stage)
        route_instance = Route(
            name = input.name
        )
        route_instance.save()
        route_instance.stops.set(stops)
        route_instance.stages.set(stages)
        return CreateRoute(ok=ok, route=route_instance)

class UpdateRoute(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = RouteInput(required=True)

    ok = graphene.Boolean()
    route = graphene.Field(RouteType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        route_instance = Route.objects.get(pk=id)
        if route_instance:
            ok = True
            stops = []
            stages = []
            for stop_input in input.stops:
                stop = BusStop.objects.get(pk=stop_input.id)
                if stop is None:
                    return UpdateRoute(ok=False, route=None)
                stops.append(stop)
            for stage_input in input.stages:
                stage = Stage.objects.get(pk=stage_input.id)
                if stage is None:
                    return UpdateRoute(ok=False, route=None)
                stages.append(stage)
            route_instance.name = input.name
            route_instance.save()
            route_instance.stops.save()
            route_instance.stages.save()
            return UpdateRoute(ok=ok, route=route_instance)
        return UpdateRoute(ok=ok, route=None)

class Mutation(graphene.ObjectType):
    # create mutations
    create_route = CreateRoute.Field()
    create_bus_stop = CreateBusStop.Field()
    create_stage = CreateStage.Field()
    # update mutations
    update_route = UpdateRoute.Field()
    update_bus_stop = UpdateBusStop.Field()
    update_stage = UpdateStage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
