# Setup

add a new user-ssh key (https://github.com/settings/keys) to your `~/.ssh/` folder (`~/.ssh/deploy_git`)
add this to `~/.ssh/config`:
```
Host git
	Hostname github.com
	IdentityFile ~/.ssh/deploy_git
	IdentitiesOnly yes
	AddKeysToAgent yes
```
maybe you have to change the https-urls of submodules to ssh-urls

guide may be incomplete