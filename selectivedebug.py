# -*- coding: utf-8 -*-

# Copyright © 2018 Zipcar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: selectivedebug
    callback_type: stdout
    requirements:
      - set as stdout_callback
    short_description: Ansible screen output that combines the powers of the plugins 'debug' and 'selective'
    extends_documentation_fragment:
      - default_callback
    description:
        - This callback outputs stdout/stderr in a more "raw" format that makes it easier to read
        - It only does this for tasks that have failed or that have been tagged with `always_log`
        - Output for skipped tasks can be suppressed with the `display_skipped_hosts` option
'''

from ansible.plugins.callback.debug import CallbackModule as DebugCallback

class CallbackModule(DebugCallback):
    '''
    Inherit from the 'debug' module to get its nice stdout/stderr output.

    Add in a basic (hacky) version of the functionality of selective.
    '''

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'selectivedebug'

    def v2_runner_on_ok(self, result):
        if 'always_log' in result._task.tags:
            # Bit of a hack, based on reading the 'default' module and examining under what conditions it will call the '_dump_results' method that the 'debug' module overrides
            result._result['_ansible_verbose_always'] = True
        return super(CallbackModule, self).v2_runner_on_ok(result)
