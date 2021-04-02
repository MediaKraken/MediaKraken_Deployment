import psutil


def is_running_check(app_name, app_parameter=None):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if app_name.lower() in proc.name().lower():
                if app_parameter is not None:
                    if proc.cmdline()[1] == app_parameter:
                        return True
                else:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


print(is_running_check('trivy'))
print(is_running_check('bohsdfjl'))
print(is_running_check('trivy', 'server'))
