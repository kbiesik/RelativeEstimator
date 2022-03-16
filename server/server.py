from aiohttp import web
import json
import aiohttp_cors
import sys
from relative_estimator.helpers import read_config, get_logger, arg_parse

routes = web.RouteTableDef()

execution_arguments = arg_parse(sys.argv[1:])
logger = get_logger(execution_arguments)
logger.info("Jira Relative Estimator just started for generation.")

# get configuration
logger.info(f"Reading config file: {execution_arguments.config_file}")

config = read_config(execution_arguments.config_file)
output_config = dict(config['OUTPUT'])
logger.debug(json.dumps(output_config))
logger.debug(f'Found issues file: {output_config.get("file")}')

async def root_handler(request):
    return web.HTTPFound('/index.html')


async def issues_file(request):
    with open(output_config.get("file"), 'r') as f:
        values = json.load(f)
    return web.json_response(values)


app = web.Application()
app.add_routes(routes)
app.router.add_route('*', '/', root_handler)

cors = aiohttp_cors.setup(app)
resource = cors.add(app.router.add_resource("/api/issues"))
route = cors.add(
    resource.add_route("GET", issues_file), {
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True)
    })

app.add_routes([web.static('/', "../build/")])
web.run_app(app)