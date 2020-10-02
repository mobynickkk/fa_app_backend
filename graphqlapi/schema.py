import graphene
from graphene_django import DjangoObjectType
from restapi.models import Profile, HomeTask


class ProfileType(DjangoObjectType):

    class Meta:
        model = Profile


class HomeTaskType(DjangoObjectType):

    class Meta:
        model = HomeTask


class HomeTaskInput(graphene.InputObjectType):
    id = graphene.ID()
    profile__hash = graphene.String()
    subject = graphene.String()
    deadline = graphene.Date()
    task = graphene.String()


class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType, hash=graphene.String())
    home_tasks = graphene.List(HomeTaskType, profile__hash=graphene.String())

    def resolve_profile(self, info, **kwargs):
        hash_ = kwargs.get('hash')

        if hash_ is not None:
            return Profile.objects.get(hash=hash_)

        return None

    def resolve_home_tasks(self, info, **kwargs):
        profile__hash = kwargs.get('profile__hash')

        if profile__hash is not None:
            return HomeTask.objects.filter(profile__hash=profile__hash)

        return None


class CreateHomeTask(graphene.Mutation):
    class Arguments:
        input_ = HomeTaskInput(required=True)

    ok = graphene.Boolean()
    task = graphene.Field(HomeTaskType)

    @classmethod
    def mutate(cls, root, info, input_=None):
        ok = True
        try:
            home_task_instance = HomeTask(
                subject=input_.subject,
                deadline=input_.deadline,
                task=input_.task,
                profile=Profile.objects.get(hash=input_.profile__hash)
            )
            home_task_instance.save()
            return cls(ok=ok, task=home_task_instance)
        except Profile.DoesNotExist:
            return cls(ok=False, task=None)


class UpdateHomeTask(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        input_ = HomeTaskInput(required=True)

    ok = graphene.Boolean()
    task = graphene.Field(HomeTaskType)

    @classmethod
    def mutate(cls, root, info, input_=None):
        try:
            home_task_instance = HomeTask.objects.get(pk=input_.id)
            home_task_instance.subject = input_.subject
            home_task_instance.task = input_.task
            home_task_instance.deadline = input_.deadline
            home_task_instance.save()
            return cls(ok=True, task=home_task_instance)
        except Profile.DoesNotExist:
            return cls(ok=False, task=None)


class DeleteHomeTask(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id_ = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id_):
        obj = HomeTask.objects.get(pk=id_)
        obj.delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
    create_actor = CreateHomeTask.Field()
    update_actor = UpdateHomeTask.Field()
    create_movie = DeleteHomeTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
