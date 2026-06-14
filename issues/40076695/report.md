# Heap-use-after-free in WebCore::ChildNodeInsertionNotifier::notifyDescendantInsertedIntoDocument

| Field | Value |
|-------|-------|
| **Issue ID** | [40076695](https://issues.chromium.org/issues/40076695) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2012-12-13 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11

Steps to reproduce the problem:
1. Upload the poc.html to your server 
2. Open chrome.exe
3. Browse to poc.html

What is the expected behavior?
No crash of the renderer process.

What went wrong?
I can't watch if it triggers some assertion which would do the analysis easier, but taking a look in the source of the poc and the stack, this bug is probably an use-after-free issue on Webkit because of the incorrectly nested tags and the insertBefore function. But just a guess.

- Jose.

Did this work before? N/A 

Chrome version: 23.0.1271.97  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)

Note that stack2.txt is the stack trace of the fuzz sample (not attached).

Tested on:

- Windows XP SP3 (fully updated) x86_32 Spanish
- Windows 7 SP1 (fully updated) x86_32 Spanish

- Chrome 23.0.1271.95 m
- Chrome 23.0.1271.97 m

## Attachments

- [poc.html](attachments/poc.html) (text/html; charset=us-ascii, 577 B)
- [stack2.txt](attachments/stack2.txt) (text/plain; charset=us-ascii, 1.1 KB)
- [stack1.txt](attachments/stack1.txt) (text/plain; charset=us-ascii, 12.3 KB)
- [poc_2.html](attachments/poc_2.html) (text/plain; charset=us-ascii, 536 B)

## Timeline

### sc...@gmail.com (2012-12-13)

@javg0x83: thanks for the report!
Do you have crash reporting enabled? If you go to chrome://crashes and send me a few crash IDs from triggering this, we can get an idea if it's use-after-free or not.

### in...@chromium.org (2012-12-13)

It is indeed a UAF. Report coming in https://cluster-fuzz.appspot.com/testcase?key=150460119.

Hajime, can you save us from another DOM doom.

### sc...@gmail.com (2012-12-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=150460119

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f88423195b0
Crash State:
  - crash stack -
  WebCore::ChildNodeInsertionNotifier::notifyDescendantInsertedIntoDocument
  WebCore::ChildNodeInsertionNotifier::notifyNodeInsertedIntoDocument
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::replaceChildrenWithFragment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150475:150548

Minimized Testcase (0.27 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97uliVuf2I17bY_VGUuEoYHv7sdzp4c2q1MoKezhWejMF7yryJ5k20C3mVkw7f-UEDIM4xjooemGVzG8TtpgQsG9o8RqLN-Aw0ugvBMyqZrvGRcV5GI64b693m_sPAAe7Ul4epHI6YehQrdaYLJFms8ikzBRR7mrMfLzBn6_oa9oRcyKc4
<script>

	function f1(){
		document.write('<form>');		document.getElementsByTagName("s")[0].innerHTML = 'foo';	}

	function f2(){
		
			document.getElementsByTagName("kbd")[0].innerHTML = 'foo';	}

</script>
<s>
	<script>f1();</script>
	<kbd>
		<script>f2();</script>
	</s>

### in...@chromium.org (2012-12-13)

Actually it regressed from haraken@'s changeset, can you please take a look at this regression.
https://trac.webkit.org/changeset/124990/

### in...@chromium.org (2012-12-13)

Actually it regressed from haraken@'s changeset, can you please take a look at this regression.
https://trac.webkit.org/changeset/124990/

### in...@chromium.org (2012-12-13)

[Empty comment from Monorail migration]

### ja...@gmail.com (2012-12-13)

@Chris: ok, i take note. So next time i'll attach the crash IDs.
@inferno: your minimized testcase is not working for me (tested on Win7 SP1 + chrome stable). No crash if it does not include the insertBefore function. I mean i have only had to use the line: document.getElementsByTagName("kbd")[0].insertBefore... for triggering your testcase.

Btw, there goes attached another sample.



### sc...@gmail.com (2012-12-13)

BTW, @javg0x83 -- been a long time, good to see you back :)

### in...@chromium.org (2012-12-13)

javg0x83@, don't worry about more repros. Our minimized testcase works reliably since it is run under a really nice memory debugging tool ASAN. You might consider this in your future fuzzing efforts. - http://www.chromium.org/developers/testing/addresssanitizer

### ha...@chromium.org (2012-12-14)

Taking a look.

### ja...@gmail.com (2012-12-14)

[Comment Deleted]

### ha...@chromium.org (2012-12-14)

The WebKit side fix is going to be landed soon.

### in...@chromium.org (2012-12-14)

http://trac.webkit.org/changeset/137702

### in...@chromium.org (2012-12-14)

Also need to merge http://trac.webkit.org/changeset/137736 and http://trac.webkit.org/changeset/137739

### cl...@chromium.org (2012-12-16)

ClusterFuzz has detected this issue as fixed in range 172836:173286.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=150460119

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f88423195b0
Crash State:
  - crash stack -
  WebCore::ChildNodeInsertionNotifier::notifyDescendantInsertedIntoDocument
  WebCore::ChildNodeInsertionNotifier::notifyNodeInsertedIntoDocument
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::replaceChildrenWithFragment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=150475:150548
Fixed: https://cluster-fuzz.appspot.com/revisions?range=172836:173286

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97uliVuf2I17bY_VGUuEoYHv7sdzp4c2q1MoKezhWejMF7yryJ5k20C3mVkw7f-UEDIM4xjooemGVzG8TtpgQsG9o8RqLN-Aw0ugvBMyqZrvGRcV5GI64b693m_sPAAe7Ul4epHI6YehQrdaYLJFms8ikzBRR7mrMfLzBn6_oa9oRcyKc4

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-12-18)

M24: http://trac.webkit.org/changeset/137971, http://trac.webkit.org/changeset/137972, http://trac.webkit.org/changeset/137974

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-26)

@javg0x83: thanks for the report!
And a $1000 Chromium Security Reward and a Happy New Year to you sir.

### ja...@gmail.com (2012-12-27)

@Chris, you're welcome. Happy New Year to you and all the team too :)

Btw, this time i prefer the money goes for the people who can't pass a happy christmas. For example:

https://secure3.convio.net/gfn/site/Donation2?idb=1315600659&df_id=1460&1460.donation=form1



### sc...@gmail.com (2012-12-29)

@javg0x83: you rock! Reward upped to $1337 and donated to the indicated charity above.

### sc...@gmail.com (2013-01-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/165864?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076695)*
