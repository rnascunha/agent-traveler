install:
		@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $HOME/.local/bin/env; }

check:
		@command -v uv >- 2>&1 || ( echo "uv is not installed. Call 'make install' to install it"; exit 1; )

adk_web: check
		uv run adk web --session_service_uri sqlite+aiosqlite:////${HOME}/session.db --artifact_service_uri file://${HOME}/Downloads

main: check
		uv run ./main.py

api_server: check
		uv run adk api_server