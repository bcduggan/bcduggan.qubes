# Ansible Collection - bcduggan.qubes

Opinionated Qubes OS automation

## Nutshell

This collection contains roles and playbooks you can include in your own Ansible playbook project for Qubes OS. But you can get started with just an inventory and run the playbooks directly:


```console
user@dom0:~/qubes-playbooks$ ansible-playbook bcduggan.qubes.site
```

## Quick start from scratch

An [Ansible playbook project][ansible-playbook-project] includes an inventory and playbooks. You can define your own custom roles and playbooks in the project that use the [qubes-ansible][qubes-ansible] modules and plugins. Your project can also use roles, modules, plugins, and playbooks from collections, lke this one.

If you don't already have a playbook project for Qubes OS, you can create one that can directly use this collection's playbooks with just a few short files.

Create a virtual machine with network access to develop your Ansible project and name it _playbook-dev_. Install any editors, linters, LSPs, or other development tools in _playbook-dev_.

Create a directory for your playbook project called _qubes-playbooks_. After these setup steps, it will contain these files:

```console
user@playbook-dev:~qubes-playbooks$ tree
.
├── ansible.cfg
├── gnupg
│   └── pubring.kbx
├── inventory
│   └── hosts.yml
├── requirements.yml
```

[ansible-playbook-project]: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/developing_automation_content/creating-playbook-project

### _ansible.cfg_

_ansible.cfg_ must define `collections_path` so that _ansible-galaxy_ installs collections in the project directory:

```ini
# ansible.cfg
[defaults]
strategy=qubes_proxy
collecions_path=./
```

When you define your own _ansible.cfg_, you may also set `strategy=qubes_proxy` to ensure Ansible uses the [qubes_proxy plugin][qubes-proxy-plugin] for VM connections.

[qubes-proxy-plugin]: https://github.com/QubesOS/qubes-ansible?tab=readme-ov-file#usage

### _requirements.yml_

Add this collection and my signature to _requirements.yml_:

```yaml
---
collections:
- name: bcduggan.qubes
  version: "<bcduggan.qubes-version>"
  signatures:
    - "https://github.com/bcduggan/bcduggan.qubes/releases/download/<bcduggan.qubes-version>/bcduggan-qubes.sig"
```
| Placeholder | Substitution |
|---|---|
| `<bcduggan.qubes-version>` | Version of bcduggan.qubes collection, like `0.1.0` |

### _inventory/hosts.yml_

```ini
adminvm:
  hosts:
    localhost:
      ansible_connection: local
      ansible_host: dom0
```

### Install

Download [my public key][brian@dugga.net.asc]. And add it to a GPG keyring:

```console
user@playbook-dev:~qubes-playbooks$ mkdir --mode=0700 gnupg
user@playbook-dev:~qubes-playbooks$ GNUPGHOME=gnupg gpg --keyserver keys.openpgp.org --recv-key 5EEBC6DAB95FF8610CBF401156A1C2EEA520ECEB
```

Install this collection in your Ansible project. This will create an _ansible_collections_ directory in your project directory that contains your project's external collection dependencies:

```console
user@playbook-dev:~qubes-playbooks$ ansible-galaxy collection install --keyring gnupg/pubring.kbx --requirements-file requirements.yml
```

[brian@dugga.net.asc]: https://keys.openpgp.org/vks/v1/by-fingerprint/5EEBC6DAB95FF8610CBF401156A1C2EEA520ECEB

## Synchronize to dom0

[qubes-ansible][qubes-ansible] only works when you run Ansible directly on dom0 (for now). A copy of your Ansible project and all of its dependencies (like this collection) must exist in dom0 for this to work.

The Qubes OS documention describes how to [copy a single file from a VM to dom0][copying-to-dom0]. You need to copy the Ansible project directory from your development VM to dom0. You will probably need to do this many times as you develop playbooks, roles, and update dependencies in your Ansible project. You should entirely overwrite the Ansible project on dom0 each time you copy it from from the VM where you develop your Ansible project.

The *qvm-sync-dom0* script in this collection synchronizes directories from Qubes VMs to dom0. After you install this collection, copy *qvm-sync-dom0* from your Ansible project to dom0:

```console
root@dom0:~$ qvm-run --pass-io playbook-dev 'cat /home/user/qubes-playbooks/ansible_collections/bcduggan/qubes/qvm-sync-dom0' > /usr/local/bin/qvm-sync-dom0
````

Now you can use *qvm-sync-dom0* to synchronize your Ansible project to dom0:

```console
user@dom0:~$ qvm-sync-dom0 playbook-dev qubes-playbooks
```

[qubes-ansible]: https://github.com/QubesOS/qubes-ansible
[copying-to-dom0]: https://doc.qubes-os.org/en/latest/user/how-to-guides/how-to-copy-from-dom0.http#copying-to-dom0

## Development

Clone the git repository to the same VM where you develop your playbook project. Install in your playbook project from the _bcduggan.qubes_ clone:

```console
user@playbook-dev:~qubes-playbooks$ ansible-galaxy collection install --force ~/bcduggan.qubes
```

It is only possible to verify signatures for collections installed from Ansible Galaxy.

## Roles

### qvm_sync_dom0

## Playbooks

### site.yml
