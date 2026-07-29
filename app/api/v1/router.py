from fastapi import APIRouter
from app.api.v1.endpoints import auth, oauth, users, organizations, github, graph, collector, agents, health, chat, notifications, analytics, monitoring

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(users.router)
api_router.include_router(organizations.router)
api_router.include_router(github.router)
api_router.include_router(graph.router)
api_router.include_router(collector.router)
api_router.include_router(agents.router)
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(notifications.router)
api_router.include_router(analytics.router)









