# Security: Chrome on Android requestFullscreen then back or forward navigation on BFcache page able to hide omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [40224936](https://issues.chromium.org/issues/40224936) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Navigation>BFCache |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2022-05-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**   
After requestFullscreen then run window.history.back() to perform back navigation to page stored in BFcache, interestingly with proper timing it will hide Chrome omnibox while Android status bar still remain visible.  
  
As legitimate omnibox is hidden, attacker able to

## Attachments

- deleted (application/octet-stream, 0 B)
- [Chrome on Android - requestFullScreen then back on BFCache page able to hide omnibox.mp4](attachments/Chrome on Android - requestFullScreen then back on BFCache page able to hide omnibox.mp4) (video/mp4, 1.2 MB)
- [spoofpage.html](attachments/spoofpage.html) (text/plain, 32.6 KB)
- [testcase1.html](attachments/testcase1.html) (text/plain, 772 B)
- [testcase2.html](attachments/testcase2.html) (text/plain, 769 B)
- [back-delayed.html](attachments/back-delayed.html) (text/plain, 482 B)
- [back-direct.html](attachments/back-direct.html) (text/plain, 234 B)
- [success.log](attachments/success.log) (text/plain, 5.0 KB)
- [failed.log](attachments/failed.log) (text/plain, 10.1 KB)
- [exitpersistentfullscreen.patch](attachments/exitpersistentfullscreen.patch) (text/plain, 1.1 KB)
- [omnibox-hidden1.txt](attachments/omnibox-hidden1.txt) (text/plain, 7.5 KB)
- [omnibox-hidden2.txt](attachments/omnibox-hidden2.txt) (text/plain, 7.5 KB)
- [omnibox-restored-with-animation1.txt](attachments/omnibox-restored-with-animation1.txt) (text/plain, 9.1 KB)
- [omnibox-restored-with-animation2.txt](attachments/omnibox-restored-with-animation2.txt) (text/plain, 9.1 KB)
- [omnibox-restored-without-animation1.txt](attachments/omnibox-restored-without-animation1.txt) (text/plain, 6.0 KB)
- [omnibox-restored-without-animation2.txt](attachments/omnibox-restored-without-animation2.txt) (text/plain, 6.0 KB)
- [app.js](attachments/app.js) (text/plain, 462 B)
- [args.gn](attachments/args.gn) (application/octet-stream, 451 B)
- [back-delayed.html](attachments/back-delayed_53166138.html) (text/plain, 442 B)
- [omnibox-hidden1.txt](attachments/omnibox-hidden1_53166149.txt) (text/plain, 5.9 KB)
- [back-delayed html to Hide Omnibox on Chrome Dev.mp4](attachments/back-delayed html to Hide Omnibox on Chrome Dev.mp4) (video/mp4, 837.0 KB)
- [omnibox-hidden2.txt](attachments/omnibox-hidden2_53166163.txt) (text/plain, 6.1 KB)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40224936)*
