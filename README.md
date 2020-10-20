# Selective Debug

**selectivedebug** is an Ansible Output Callback Plugin that combines the powers of the plugins [`selective`](https://docs.ansible.com/ansible/latest/plugins/callback/selective.html) and [`debug`](https://docs.ansible.com/ansible/latest/plugins/callback/debug.html). It is useful if you want to see readable multi-line output from some (but not all) successful tasks.

**NB:** A previous version of this plugin also didn't display output for skipped tasks, like the [`skippy`](https://docs.ansible.com/ansible/latest/plugins/callback/skippy.html) plugin. This functionality is now optional and is no longer the default behaviour. If you are upgrading from an older version, see the Usage section below on how to configure `display_skipped_hosts` if you want to preserve this behaviour.

## Features

* Output stdout/stderr as raw output, not wrapped in quotes or json (exactly like `debug` does)
* Optionally don't display output for jobs that are skipped (in the same way `default` and `debug` support)
* Optionally output stdout/stderr from tasks that succeeded, on task-by-task basis (not exactly like `selective`)

## Usage

Configure this as your stdout callback in `ansible.cfg` in [the usual way](http://docs.ansible.com/ansible/devel/plugins/callback.html):

```ini
stdout_callback = selectivedebug
```

To output stdout/stderr for a task even if it succeeds, add the `always_log` tag to the task:

```yaml
- name: a task whose output we always want to log
  script: foobar.sh
  tags: [always_log]
```

To show no output for tasks that are skipped, add this to your `ansible.cfg`:

```ini
display_skipped_hosts = no
```

## Example output

With the default output plugin:

```
PLAY [all] *****************************************************************************************************************************************************************************************************************************************

TASK [a task we only run on some machines] *********************************************************************************************************************************************************************************************************
skipping: [machine-b]
changed: [machine-a]

TASK [task that sometimes fails, and we only want to log it if it fails] ***************************************************************************************************************************************************************************
changed: [machine-a]
fatal: [machine-b]: FAILED! => {"changed": true, "failed": true, "rc": 1, "stderr": "Shared connection to machine-b closed.\r\n", "stdout": "This script outputs useful debugging information when it fails\r\nOn multiple lines\r\n", "stdout_lines": ["This script outputs useful debugging information when it fails", "On multiple lines"]}
...ignoring

TASK [task that sometimes fails, but we always want to log its output regardless] ******************************************************************************************************************************************************************
changed: [machine-b]
fatal: [machine-a]: FAILED! => {"changed": true, "failed": true, "rc": 1, "stderr": "Shared connection to machine-a closed.\r\n", "stdout": "This script outputs useful information even when it succeeds\r\nOn multiple lines\r\nFor example a legacy script that is dishonest about its return code\r\nSo if there is a problem, you want to be able to read these logs later\r\n", "stdout_lines": ["This script outputs useful information even when it succeeds", "On multiple lines", "For example a legacy script that is dishonest about its return code", "So if there is a problem, you want to be able to read these logs later"]}

PLAY RECAP *****************************************************************************************************************************************************************************************************************************************
machine-a                  : ok=2    changed=2    unreachable=0    failed=1
machine-b                  : ok=2    changed=2    unreachable=0    failed=0
```

With the **selectivedebug** output plugin:

```
PLAY [all] *****************************************************************************************************************************************************************************************************************************************

TASK [a task we only run on some machines] *********************************************************************************************************************************************************************************************************
changed: [machine-a]

TASK [task that sometimes fails, and we only want to log it if it fails] ***************************************************************************************************************************************************************************
changed: [machine-a]
fatal: [machine-b]: FAILED! => {
    "changed": true,
    "failed": true,
    "rc": 1
}

STDOUT:

This script outputs useful debugging information when it fails
On multiple lines



STDERR:

Shared connection to machine-b closed.


...ignoring

TASK [task that sometimes fails, but we always want to log its output regardless] ******************************************************************************************************************************************************************
changed: [machine-b] => {
    "changed": true,
    "rc": 0
}

STDOUT:

This script outputs useful information even when it succeeds
On multiple lines
For example a legacy script that is dishonest about its return code
So if there is a problem, you want to be able to read these logs later



STDERR:

Shared connection to machine-b closed.


fatal: [machine-a]: FAILED! => {
    "changed": true,
    "failed": true,
    "rc": 1
}

STDOUT:

This script outputs useful information even when it succeeds
On multiple lines
For example a legacy script that is dishonest about its return code
So if there is a problem, you want to be able to read these logs later



STDERR:

Shared connection to machine-a closed.



PLAY RECAP *****************************************************************************************************************************************************************************************************************************************
machine-a                  : ok=2    changed=2    unreachable=0    failed=1
machine-b                  : ok=2    changed=2    unreachable=0    failed=0
```
