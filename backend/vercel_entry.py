try:
    from main import app as application
except Exception as e:
    # Catch startup errors (e.g., missing dependencies)
    import traceback
    traceback.print_exc()
    raise e

# Vercel looks for 'app' or 'application' or 'handler'
app = application
