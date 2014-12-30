Title: 使用 Vagrant
Date: 2014-12-22 11:42:50
Modified: 2014-12-22 11:42:50
Author: zrong
Postid: $POSTID
Slug: $SLUG
Nicename: using-vagrant
Category: technology
Tags: virtualization
Attachments: $ATTACHMENTS
Posttype: post
Poststatus: publish

    -> % vagrant reload
    ==> default: Attempting graceful shutdown of VM...
    ==> default: Clearing any previously set forwarded ports...
    ==> default: Clearing any previously set network interfaces...
    ==> default: Preparing network interfaces based on configuration...
        default: Adapter 1: nat
        default: Adapter 2: hostonly
    ==> default: Forwarding ports...
        default: 22 => 2222 (adapter 1)
    ==> default: Booting VM...
    ==> default: Waiting for machine to boot. This may take a few minutes...
        default: SSH address: 127.0.0.1:2222
        default: SSH username: vagrant
        default: SSH auth method: private key
        default: Warning: Connection timeout. Retrying...
    ==> default: Machine booted and ready!
    ==> default: Checking for guest additions in VM...
        default: The guest additions on this VM do not match the installed version of
        default: VirtualBox! In most cases this is fine, but in rare cases it can
        default: prevent things such as shared folders from working properly. If you see
        default: shared folder errors, please make sure the guest additions within the
        default: virtual machine match the version of VirtualBox you have installed on
        default: your host and reload your VM.
        default:
        default: Guest Additions Version: 4.2.0
        default: VirtualBox Version: 4.3
    ==> default: Configuring and enabling network interfaces...
    ==> default: Mounting shared folders...
        default: /vagrant => /Volumes/HD1/works/hhl/openresty/quickserver
    ==> default: Machine already provisioned. Run `vagrant provision` or use the `--provision`
    ==> default: to force provisioning. Provisioners marked to run always will still run.
