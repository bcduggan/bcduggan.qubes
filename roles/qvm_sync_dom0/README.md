Ansible Role - bcduggan.qubes.qvm_sync_dom0
=========

Install the _qvm-sync-dom0_ script on dom0 on Qubes OS. _qvm-sync-dom0_ synchronizes directories from a VM to dom0. It allows users to select specific files and subdirectories from the source directory. See _qvm-sync-dom0_'s help for more information:

    qvm-sync-dom0 --help

Requirements
------------

Apply this role to dom0 on Qubes OS, only.

Role Variables
--------------

None

Dependencies
------------

None

Example Playbook
----------------

In practice, the `hosts` value will always be localhost. Here, _dom0_ could be an _ansible_host_ value for localhost, or an inventory group that contains only localhost.

    - name: Configure dom0
      hosts: dom0
      become: true
      roles:
        - bcduggan.qubes.qvm_sync_dom0

License
-------

GPL-3.0
