# Reading local files and cross-origin resources through an extension that only has the "downloads" permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40095862](https://issues.chromium.org/issues/40095862) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2019-07-30 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The "downloads" permission is used by extensions to manage user's downloads but given that it is possible to set any filename for downloaded resources through it, you can use tricks from issues like <https://crbug.com/chromium/848123> and <https://crbug.com/chromium/788936> to read local files and cross-origin resources.

Reading local files is a bit trickier than cross-origin resources because it is only possible to download local files and rename them using "chrome.downloads.download" if the user has the "Allow access to file URLs" setting enabled.

Luckily we can use "chrome.downloads.onDeterminingFilename" to listen for downloads and only then rename the files. This also works for local files even if the "Allow access to file URLs" setting is not enabled (this is probably a bug).

Triggering the download of a local resource so it can be intercepted by the listener can be achieved by redirecting a local file to a different local file that Chrome is not able to display (e.g. binaries), because this makes the file be downloaded, which in turn ends up firing the "DeterminingFilename" event.

Having all that in mind, the attack to read local files would look like this:

1. User installs an extension that only asks the "downloads" permission.
2. Using "chrome.downloads.download" an HTML containing the payload is downloaded.
3. Using the "chrome.downloads.onChanged" listener the full path of the local file is retrieved.
4. Using "chrome.tabs.create" we open the HTML file we just downloaded locally.
5. This HTML file will set the set the cookie "<script>alert('Exfiltration code here')</script>=1337", forcing it to be written into /home/user/.config/google-chrome/Default/Cookies
6. After the cookie is set, the page is redirected to /home/user/.config/google-chrome/Default/Cookies. Given Chrome is not able to display this page, it ends up being downloaded.
7. The "DeterminingFilename" event will fire, allowing the attacker to rename the file from "Cookies" to "leak.html".
8. The attacker's local HTML file is redirected to "leak.html" and the javascript code that was inserted earlier in the Cookies file will trigger, allowing an attacker to leak the information.

Leaking a cross-origin resource is way easier:

1. We find an endpoint/page that allows user-controlled content and then we insert our payload there (this can be done using the script technique mentioned above or the CSS exfiltration technique described in <https://crbug.com/chromium/788936>).
2. User installs an extension that only asks the "downloads" permission.
3. Using "chrome.downloads.download" we download the endpoint as HTML (or CSS if using the technique described in <https://crbug.com/chromium/788936>).
4. We redirect the user to the HTML that was just downloaded.
5. The javascript code that was inserted earlier will trigger, allowing an attacker to leak the information.

On <https://bugs.chromium.org/p/chromium/issues/detail?id=848123#c51> it is mentioned other local files that can be exfiltrated as well as the methods used.

I have only prepared a PoC for the cross-origin read attack, but if necessary I can create one for the local file read.

**VERSION**  

Version 75.0.3770.142 (Official Build) (64-bit)  

Version 77.0.3860.5 (Official Build) dev (64-bit)

**REPRODUCTION CASE**

1. Download extension.zip and load it into Chrome.
2. An alert will show up containing the secret token from <https://lbherrera.github.io/lab/file-to-leak.json>

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

This bug is subject to a 90 day disclosure deadline. After 90 days elapse  

or a patch has been made broadly available (whichever is earlier), the bug  

report will become visible to the public.

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 1.1 KB)

## Timeline

### do...@chromium.org (2019-07-30)

Seems to me the open question here is whether the "downloads" permission should also permit the renaming of local downloaded files via chrome.downloads.onDeterminingFilename() even though the file permission isn't there. +extensions folks, do you have thoughts?

I'm setting a low severity because of the need to install an extension, which already gives you quite a lot of elevated privilege over the drive-by web.

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2019-07-31)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2019-07-31)

I am not sure if I understand the POC. We initiate the download of a JSON resource, rename it to html, open a tab to it, where it gets interpreted as an html file. How does that lead to leaking of the cross origin resource to an extension?

### he...@gmail.com (2019-07-31)

The JSON resource that is used in the PoC was meant to simulate an endpoint that returns a JSON containing user-controlled content. The javascript code inserted there under normal circumstances would be safe, but by using the "downloads" permission we can make it be interpreted as HTML, which was something the server was not expecting.

In reality, almost any page that contains user-controlled content can be read by inserting javascript code (like shown in the PoC) or by inserting a CSS property in the page and then downloading it as CSS (like was done in https://crbug.com/chromium/788936).

### ka...@chromium.org (2019-07-31)

But wouldn't the extension already require host permissions to the endpoint to insert a CSS/JS payload on the endpoint?

### he...@gmail.com (2019-07-31)

The idea is to insert the CSS/JS payload before the attack. We would be using the server functionality to add it and not the extension. Maybe looking into this video will help clarify the attack (it used the same concept described in this bug to read cross-origin resources): https://www.youtube.com/watch?v=67nWiqIl5bc

Reading Chrome's cookies file would work similarly. We would create a cookie named "<script>alert('payload')</script>=1337" which ends up writing the JS code to /home/user/.config/google-chrome/Default/Cookies. Then, we download and rename the file to HTML and open a tab to it. This allows stealing all the cookies of a user by simply installing an extension with the "downloads" permission, without requiring any other user interaction.

### ka...@chromium.org (2019-08-01)

Hmm ok. https://crbug.com/chromium/989774 is similar but with an easier repro (but requires file access). meacer@: Do we generally merge the bugs in such cases?

Here, it seems at least we should require access to the file scheme to rename downloaded files. 

Assigning to one of the download API owners for now.

[Monorail components: UI>Browser>Downloads]

### qi...@chromium.org (2019-08-01)

would it make more sense to requiring extensions to have file permission to open a file url or totally block extensions from opening a file url? changing the download file name doesn't seem to be the culprit here, but opening it is the main issue.

Even if renaming a download requires file access permission, many users will blindly accept it as it is very reasonable for a  download extension to require file access. So blocking extensions from opening a file URL seems like a much better fix here, and it will also prevent extensions from opening other files on users' file system.

### he...@gmail.com (2019-08-01)

I could be wrong but as far as I know, there is no easy way for an extension to ask file access permission, they have to visit chrome://extensions and enable it manually.

I think blocking extensions from opening file URLs would be security positive, but I am not sure if it would be sufficient to fix this. Wouldn't that increase the user interaction needed to perform the attack but still allow it to happen? The attacker could wait for a user to download an HTML file, block it and then download their payload in its place.

### qi...@chromium.org (2019-08-01)

Could you explain a little bit on how "download the payload in place" would allow attackers to read local files? And if it works, does requiring file access permission for download renaming will change anything? 

Another alternative to block your PoC is to disallow download rename from changing file extensions. So arbitrary file cannot be renamed to .html files. But I am not sure whether that will prevent other attacks. 

### he...@gmail.com (2019-08-01)

If extensions were blocked to open local files you would need to somehow make the user open your HTML payload locally to launch the attack. If you waited for the user to download an HTML file, blocked the download and then downloaded your payload with the same name of the file the user was trying to download you could trick them into opening your payload locally.

After that, the attack would happen in the same way if extensions were able to rename local files without having the file access permission. Requiring it would be another mitigation, but I guess doesn't fix the issue either.

### he...@gmail.com (2019-08-02)

The alternative you suggested of disallowing extensions from renaming the extension of downloads would work. I can't think of any way to read cross-origin resources or local files if that was disabled.

Maybe only allowing the rename of downloads that match the origins that were declared on the manifest would be a good idea?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d980ff895e19d3d7c792861d1de3851b2d2d7414

commit d980ff895e19d3d7c792861d1de3851b2d2d7414
Author: Min Qin <qinmin@chromium.org>
Date: Tue Aug 13 18:37:27 2019

Don't allow plugins to change file extensions arbitrarily

Currently extensions are allowed to use the download API to override
downloaded file extensions. This causes some security issues
as file with dangerous extensions can be override to safe extensions
and bypassing dangerous prompt. And there are also other possible
attacks using this feature.
This CL blocks plugings from changing the file extensions to an
arbitrary one. The mime type will be used to determine the final
extension. However, it is possible for plugins to remove the
extensions from the final file name.

BUG=989078

Change-Id: Idd28510d3db191f40bbe24256d64449856e4644f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1740048
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Ben Hayden <benjhayden@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#686498}

[modify] https://crrev.com/d980ff895e19d3d7c792861d1de3851b2d2d7414/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/d980ff895e19d3d7c792861d1de3851b2d2d7414/chrome/browser/extensions/api/downloads/downloads_api_browsertest.cc


### jd...@chromium.org (2019-08-21)

qinmin@: does the patch you submitted take care of this? What remains?

### qi...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### he...@gmail.com (2019-08-23)

I was looking into the severity guidelines and I think this bug may fall under the medium severity given "Medium severity bugs allow attackers to read or modify limited amounts of information" [...] "or exposure of sensitive user information that an attacker can exfiltrate. Bugs that would normally be rated at a higher severity level with unusual mitigating factors may be rated as medium severity".

I also found a "similar" report (https://crbug.com/chromium/810220) that required an extension to have the "<all_urls>" permission to be able to read local files (more privilege than the "downloads" permission imo) and it was marked as a medium severity bug. What do you folks think?

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### he...@gmail.com (2019-09-26)

Hi! Any updates from the panel? Thanks!

### jd...@chromium.org (2019-09-26)

Thanks for your patience. The panel hasn't forgotten about this, and I promise you'll get a response pretty promptly once a decision has been made. :-)

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $2,000 for this report :) 

### na...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-28)

This issue was migrated from crbug.com/chromium/989078?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095862)*
