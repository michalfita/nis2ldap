# nis2ldap
Smarter NIS to LDAP synchronization tool (Python)

## Description
During my attempts to run [GitLab](about.gitlab.com) I've found I need LDAP database to give users access using credential they already have in the organization.

The tool I already use is good to perform one time migration, but is not suited to perform periodical updates. I'm talking about [Migration Tools](http://www.padl.com/OSS/MigrationTools.html) that are mix of Perl and Bash scripts. During my digging I've found Python perfectly suited to do the job. That's how this project had born.

This project is focused on ability to keep LDAP records up to date with changes that may occur in NIS database. This may be useful for every organization not yet ready to drop their dependency on NIS but needing LDAP (compatible with RFC2307) available at the same time.

## Prerequisites
Install `python-ldap` in your system:
```
sudo apt-get install python-ldap
```
(Above is true for *Ubuntu* and *Debian*)
### Testing only prerequisites
To execute unit tests, install `python-mockldap` in your system:
```
sudo apt-get install python-mockldap
```
Above would work fine for *Ubuntu Vivid Vervet* and *Debian Jessie* as earlier ditributions contains too old versions of this package (< 0.2.2) or doesn't contain it at all.

## Development ##
### Plan ###
 - [ ] Initial profile creation
 - [ ] Conversions
     - [ ] Mail Alias (alias)
     - [ ] Automounter maps (automount)
     - [ ] Mounts (fstab)
     - [x] Group (group)
     - [ ] Hosts IPs (hosts)
     - [ ] NIS Netgroups (netgroup)
     - [ ] Network numbers (networks)
     - [x] Person (passwd)
     - [ ] IP Protocols (protocols)
     - [ ] RPC mapping (rpc)
     - [ ] IP Protocol Services (services)
     - [ ] Shadow Accounts & Passwords (shadow)
     - [ ] Ethernet addresses (ethers)
 - [ ] Feeding from NIS
 - [ ] Feeding from files in /etc
 - [ ] Configuration
     
## Testing
### Launching unit tests ###
```
python -m unittest discovery test
```

### Real life example ###
Try to import your NIS into LDAP using this tool. If all went without troubles, you're happy human - opan a can of beer and raise a toast.

Otherwise raise an issue with clear description what went wrong. Include a sample data we can use to diagnose the problem.

## Refereces
* http://tools.ietf.org/html/rfc2307
* https://docs.oracle.com/cd/E19513-01/806-4251-10/mapping.htm
* https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/ldap.md
* http://stackoverflow.com/questions/28302774/gitlabs-ldap-login-against-freeipa-server-stuck-in-a-set-email-loop
* https://pypi.python.org/pypi/mockldap/0.2.4

