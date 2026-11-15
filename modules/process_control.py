"""Apply explicit local process actions using the current account's OS permissions."""

import math
import os

import psutil


class ProcessControlError(Exception):
    """An action could not be applied to the selected process."""


def control_process(pid, created_at, action):
    """Recheck identity and protected processes before sending one OS request.

    psutil's control methods also check PID reuse immediately before signalling.
    A return value confirms that the request was sent, not that a process exited.
    """
    if action not in ('suspend', 'resume', 'terminate'):
        raise ProcessControlError('Choose Suspend, Resume, or Terminate.')
    if (type(pid) is not int or pid <= 1 or isinstance(created_at, bool)
            or not isinstance(created_at, (int, float)) or not math.isfinite(created_at)
            or created_at <= 0):
        raise ProcessControlError('This process identity is invalid or protected. Select a current process.')
    try:
        current = psutil.Process(os.getpid())
        protected = {current.pid, *(parent.pid for parent in current.parents())}
        if pid in protected:
            raise ProcessControlError('The dashboard and its parent processes are protected.')
        target = psutil.Process(pid)
        if target.create_time() != created_at or not target.is_running():
            raise ProcessControlError('The selected process has exited or its PID was reused. Select it again.')
        if target.status() in (psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD):
            raise ProcessControlError('This process has already exited. Wait for its parent to collect its exit status.')
        # Do not allow managing another account's processes through this app.
        if target.username() != current.username():
            raise ProcessControlError('Only processes owned by the dashboard account can be managed.')
        getattr(target, action)()
    except psutil.NoSuchProcess as error:
        raise ProcessControlError('The selected process has exited. Refresh and select a current process.') from error
    except psutil.AccessDenied as error:
        raise ProcessControlError('The operating system denied access. No permission override was attempted.') from error
    except (psutil.Error, OSError, NotImplementedError) as error:
        raise ProcessControlError(f'The operating system could not apply this action: {error}') from error
    return f'{action.capitalize()} request sent to PID {pid}. Check its status in the next reading.'
