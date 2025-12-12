adk_web:
		uv run adk web --session_service_uri sqlite+aiosqlite:////${HOME}/session.db --artifact_service_uri file://${HOME}/Downloads

main:
		uv run ./main.py