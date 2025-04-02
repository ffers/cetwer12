


from flask import request, abort

BLOCKED_PATHS = [
    ".env", ".git", ".aws", ".docker", ".idea", "config", "backup",
    ".env.local", ".env.dev", ".env.prod", ".env.test", ".env.stage",
    ".env.backup", ".env.dist", ".env.ci", ".git/config", ".aws/credentials"
]

def security_blocker(app):
    @app.before_request
    def block_suspicious_paths():
        path = request.path.lower()
        for bad in BLOCKED_PATHS:
            if bad in path:
                abort(403)
