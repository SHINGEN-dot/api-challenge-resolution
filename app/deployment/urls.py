from handlers import tmc as tmcHandler


production_plan = (r"/productionplan", tmcHandler.ProductionPlan)


def get_urls_for_deploy():
    apps = list()
    apps.append(production_plan)
    return apps
