# Opening the Sidepanel results in plaintext HTTP requests to gstatic URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40944020](https://issues.chromium.org/issues/40944020) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | d4...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2023-11-20 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


Opening the Sidepanel sends a bunch image requests to google servers in PLAINTEXT for the bookmarks. Unable to change the default view to ReadingList as before either.


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

Opening the Sidepanel sends a bunch image requests to google servers in PLAINTEXT (no TLS) for the bookmarks. Unable to change the default view to ReadingList as before either.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

ISPs or anyone else on the same network like in a public library. You have bookmarked something while on a VPN? Now the logo of that website goes in plaintext over the wire. Not just logo actually! It tries to find the main content on that page, for example if it's an Amazon product, it'll be the image of that product!!!! WTF.


---

### The cause




## Attachments

- [sidepanel-log.json](attachments/sidepanel-log.json) (text/plain, 2.0 MB)
- [images.jpeg](attachments/images.jpeg) (image/jpeg, 5.5 KB)

## Timeline

### ch...@appspot.gserviceaccount.com (2023-11-20)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-20)

Thanks for your report. It would be helpful if you could provide us a simple PoC. A video demonstrating what exactly you are seeing would also be very useful. 

### d4...@gmail.com (2023-11-20)

Use Wireshark. Open Sidepanel. Feast your eyes on all the leaks. Want me to make a video of how to turn on a computer?

### [Deleted User] (2023-11-20)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nh...@google.com (2023-11-20)

I was unable to reproduce this issue on macos canary (121.0.6137.0). Here are my reproduction steps:

1. Run /Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/sidepanel
2. Bookmark https://www.chromium.org/chromium-projects/ and https://finerelaxedmajesticmagic.neverssl.com/online/
3. Quit Chrome Canary and restart with the same --user-data-dir flag and a --log-net-log flag to capture a NetLog dump (https://www.chromium.org/for-testers/providing-network-details/)
4. click on the button next to the omnibox to open the side panel, and observe my list of bookmarks
5. Quit Chrome Canary

The resulting netlog (attached) contains no SOCKET sources for plaintext HTTP.

If you believe this is still an issue, please provide reproduction instructions and a net log, including platform and browser version. Preferably the reproduction steps start with creating a new chrome profile or --user-data-dir.

### d4...@gmail.com (2023-11-21)

I'm using Google Chrome Version 119.0.6045.159 (Official Build) (x86_64) on MacOS Catalina. (Not Chromium)

1- Please ensure the view is "Visual View", not "Compact View".
2- Please ensure there are folders with bookmarks. 

Here's a sample request (along side 10 others) that gets sent every time I open the sidebar:
`http://142.250.185.36/images?q=tbn:ANd9GcTH-5nN7HzkE-_mBJXkgTDlTbsX3OSSxKdwiXsCmhkorCscULQKG1B73_lj__jEXGe1qN5Y`

(So, for example, you can try bookmarking a Github repo into a folder to see the disaster.)

As you see, it finds the main content of the page which makes it ever so revealing.
Furthermore, I can't find a DNS query for that address, so it's resolved within Chrome. '142.250.201.132', '172.217.18.132' and '172.217.169.228' are some of the other IPs I noticed these requests get sent to.

None of my extensions have access to bookmarks, but 3 have access to all sites.

P.S. I notice an initial HTTPS packet 142.250.185.36 and then all the HTTP. So it may be a targeted attack (or optimistically, just canary testing), not triggering for everyone.

### [Deleted User] (2023-11-21)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### d4...@gmail.com (2023-11-21)

For the sample I sent you, I've a folder named X within 'All bookmarks', within which I've bookmarked 'https://github.com/aw1cks/openconnect'. If you open this link, you won't find the picture that leaks. However, in google search results, I've seen that style of picture in google images.

### d4...@gmail.com (2023-11-21)

You're a security researcher and may not like opening random links. Not to mention how that link may be dynamic and not open up from your IP at all. So I've attached the image from that link.

### d4...@gmail.com (2023-11-21)

I pinned down the domains. They're: t0.gstatic.com, t1.gstatic.com, t2.gstatic.com, t3.gstatic.com.
Furthermore, I noticed that it shows some bookmarks that appear only there and not in the bookmark manager or other usual places. I suspect I may have bookmarked those on other devices a long time ago, but don't understand why they show there only. The leaks are NOT limited to those however.
After further testing, having nested folders does not seem to be necessary for it to leak.

### d4...@gmail.com (2023-11-21)

If I switch the Sidepanel to Search, I can inspect its view, however I don't have that luxury in other modes (Bookmarks or Reading List). 
I suspect the HTTPS call before initiating the leaks is to "optimizationguide-pa.googleapis.com", but without inspector I can't be 100% sure.

### d4...@gmail.com (2023-11-21)

Ok, I blocked access to 'optimizationguide-pa.googleapis.com', and no more leaks. So if you don't see the same behavior, consult owners of that server/department for any sort of canary testing.

### pm...@chromium.org (2023-11-22)

Thanks for the additional details.
Could you provide some additional information:
generally Chrome's version and OS (chrome://version/ without any of the PII) 
Are you seing these through chrome://net-export/ ?

Having a look at the optimization guide could you report on what's logged in chrome://optimization-guide-internals/ with possibly chrome://flags/#optimization-guide-debug-logs enabled?
Looking at the implementation it does seem TLS is enforced, but the above information might help us pin point the issue.

### d4...@gmail.com (2023-11-22)

Are you looking at Google's server-side code or Chromium's when you say TLS is enforced?
These tX.gstatic.com links are certainly not kept/generated in Chrome, but rather fetched from 'optimizationguide-pa.googleapis.com'. So the problem is with Google's servers, not client-side Chrome.

### [Deleted User] (2023-11-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2023-11-25)

Hi! Could you attach a net-export log of this behavior happening? What you're describing would probably be a big problem but we can't seem to reproduce it locally.

To take a net export:
1. chrome://net-export/
2. Press "Start Logging to Disk"
3. Repro the behavior
4. Upload the resulting log file

[Monorail components: UI>Browser>TopChrome>SidePanel]

### el...@chromium.org (2023-11-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-11-25)

(I am a bot: this is an auto-cc on a security bug)

### ma...@google.com (2023-11-25)

[Empty comment from Monorail migration]

### ma...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-11-27)

[Empty comment from Monorail migration]

### ma...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-27)

[Empty comment from Monorail migration]

### ma...@google.com (2023-11-27)

We were able to repro. Steps:

1) Sign into Chrome and enable sync
2) Start netlog
3) Search for something, click on an SRP result that has an image next to it, bookmark it.
4) Open bookmarks side panel
5) Stop and inspect netlog for URL requests to http://t[0-3].gstatic.com

Provisionally setting Severity-Medium, FoundIn LTS, and affected OSes.

### [Deleted User] (2023-11-27)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-11-27)

fixed by a server change which just fully rolled out

### ma...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### d4...@gmail.com (2023-11-28)

Glad to see it fixed. A few points worth mentioning:

1- The reply-to email in email updates is not always correct, and it turns out that I've twice sent emails to 'chromium@monorail-prod.appspotmail.com' instead of this particular thread, so they didn't appear here.

2- Chrome front-end team can add checks to ensure all such background fetches are secure (TLS-wrapped), otherwise blocked. (possibly as an optional flag.)

3- Please remember the last choice for the side-panel so that I don't have to keep switching to Reading-List every time I open it in a new window. Or maybe add an optional flag for it.

4- Or at the very least, please cache those images on disk so that opening the side-panel in a new window doesn't request the same images again. 

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this baseline report of user information disclosure. A p2p-vrp@ representative of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know what name or tag you would like us to use in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us! 

### d4...@gmail.com (2023-11-30)

Thank you very much! I really appreciate it.
Since this thread will become public in a couple of weeks and indexed by search engines shortly afterwards, I'd like to maintain my anonymity here. Relatively so at least.
I hope that does not get misinterpreted as an unwillingness to disclose a method of payment, however.
Thanks again!

### am...@chromium.org (2023-11-30)

Thanks for the response. Identity here is not tied to payment at. Someone from finance will reach out and you'll need to enroll in the Google payments system, but those are separate systems and do not touch the bug tracker. While we'll make a high-level note about the general existence of this issue when the fix ships in a Stable channel release (we won't acknowledge you there based on your request to remain anonymous), this issue / report itself will not be made public until 14 weeks from when it was closed as fixed, which by my math, is approximately 4 March 2024. 

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1503564?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40944020)*
