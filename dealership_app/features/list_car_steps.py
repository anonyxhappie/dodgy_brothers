from aloe import step, world

@step('I am on the home page')
def step_get_home_page(self):
    world.response = world.client.get('/')
    print('world.response-->', world.response)