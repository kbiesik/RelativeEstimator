from aiohttp import web
import json
import aiohttp_cors

routes = web.RouteTableDef()


async def root_handler(request):
    return web.HTTPFound('/index.html')


async def issues_file(request):
    with open("./temp/issues.json", 'r') as f:
        values = json.load(f);
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