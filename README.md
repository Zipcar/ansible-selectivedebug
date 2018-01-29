# Selective Debug

**selectivedebug** is an Ansible Output Callback Plugin that combines the powers of the plugins [`selective`](http://docs.ansible.com/ansible/devel/plugins/callback/selective.html), [`debug`](http://docs.ansible.com/ansible/devel/plugins/callback/debug.html), and [`skippy`](http://docs.ansible.com/ansible/devel/plugins/callback/skippy.html).

## Features

* Output stdout/stderr as raw output, not wrapped in quotes or json (exactly like `debug` does)
* Don't output jobs that are skipped at all (exactly like `skippy`)
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
  tags:
    - always_log
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
