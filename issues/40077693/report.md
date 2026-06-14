# Security: <input type="file" directory> can trick user into uploading their entire Download/Desktop folder.

| Field | Value |
|-------|-------|
| **Issue ID** | [40077693](https://issues.chromium.org/issues/40077693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Reporter** | jo...@chromium.org |
| **Assignee** | ki...@chromium.org |
| **Created** | 2013-06-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Users can be tricked into using directory input elements (which manifest as a folder picker) without realising that they are granting upload permissions).

**VERSION**  

Chrome Version: 7 and above.  

Operating System: all desktop OSes (Linux, Mac, Chrome OS and presumably Windows).

**REPRODUCTION CASE**

1. Open attached html page.
2. Click "Select destination directory".
3. Choose your Downloads folder in the resulting directory picker.

Unknown to the user, they have actually chosen a directory in an HTML5 directory input element, and the (untrusted) webpage now has read access to all the files in the directory you selected (including subdirectories) via the File API.

While particularly savvy web/browser developers might understand that web pages don't usually provide their own UI for choosing a download directory, I expect the vast majority of users would fall for this simple spoofing attack.

This is particularly fun if you chose to download it to your Documents or Desktop folder, but I suspect most users have plenty enough confidential documents in their Downloads folders that those alone would be rich pickings for would-be attackers.

STATUS  

The concept was mentioned to me by a penetration tester, @glynwintle, so I think this can be considered "in the wild".

## Attachments

- [directory-download-spoof.html](attachments/directory-download-spoof.html) (text/html; charset=us-ascii, 35.4 KB)
- [upload-dialog.png](attachments/upload-dialog.png) (image/png; charset=binary, 83.2 KB)

## Timeline

### jo...@chromium.org (2013-06-21)

Live demo at: https://johnme.googleplex.com/static/211f7a28f73b984c20fd/index.html

### sc...@gmail.com (2013-06-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-21)

@abarth: do we know who is the lead for HTML5 input types, and/or HTML5 file input with directory upload?

### sc...@gmail.com (2013-06-21)

On Linux, the file dialog says just "Select Folder"... I wonder if we have control of that string to say something more forceful?

### sc...@gmail.com (2013-06-21)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-06-25)

webkitdirectory was made by johnnyg@, but he is not a member of Chrome team any more.


It seems webkitdirectory attribute doesn't work on Android.


### in...@chromium.org (2013-06-26)

Is this feature needed anymore ??? Was added in http://trac.webkit.org/changeset/84238

### in...@chromium.org (2013-06-27)

tkent@, thoughts on keeping this non-standard webkitdirectory around ?

### ke...@chromium.org (2013-06-27)

Can anyone involved with the file api shed some light on this?

### ki...@chromium.org (2013-06-28)

webkitdirectory is being used in Drive's Folder upload UI.  A similar trick can be used for files too, though directories could have bigger impact.  I remember there was a local discussion whether we should show an infobar or more alarming UI for file/folder upload.

The 'Select Folder' string looks to be coming from here:
https://code.google.com/p/chromium/codesearch#chromium/src/ui/base/strings/ui_strings.grd&q=IDS_SELECT_FOLDER_DIALOG_TITLE&sq=package:chromium&type=cs&l=233

### ke...@chromium.org (2013-06-28)

Thanks, kinuko@.

Is there a compelling reason to keep webkitdirectory in the project?

And either way, can you take on this bug or else help find a better owner?

### ki...@chromium.org (2013-07-01)

I'm reaching out customers of this feature (i.e. Drive Web UI and upload library folks) to ask about the impact of feature deprecation.

Related questions: how critical is this issue considered in security context?  In the end we still ask the user to pick a folder.  Is changing the "Select Folder" label on the folder picker acceptable?  (While I can imagine deprecation would be preferable)

### jo...@chromium.org (2013-07-01)

On Linux, the dialog title is "Select Folder", and the dialog's confirm button is labelled "Open".

On OS X, there is no dialog title (it slides out of the omnibox / bookmark bar), and the dialog's confirm button is labelled "Select".

On Chrome OS, the dialog title is "Select a folder to open", and the dialog's confirm button is labelled "Open".

How much control do we have over these UIs? If we could at least change the confirm buttons to "Upload" (or "Upload Folder") users might think twice. Though a more noticeable warning would be even better...

(Technically the word "upload" might be slightly confusing, as some legitimate apps, e.g. text editors, will use this to request read access to local folders but only manipulate the file locally. But of course in such cases you're still granting the app permission to upload the file, you're just trusting it not to do so...)

### ki...@chromium.org (2013-07-02)

Did some more research.  I haven't tested on all platforms, but from the source code it looks we can fix the string label on all (or most of) platforms.

On the other hand, this feature seems to have certain number of users (on Drive and on some other websites that use the same upload library), and it doesn't look like the case that we can immediately deprecate this feature.

I'm planning to work on the first option for now, i.e. changing the text label of folder picker to make it a bit more alarming.  Security folks: please ping me if changing the picker title is not enough.


### jo...@chromium.org (2013-07-02)

> please ping me if changing the picker title is not enough.

On OS X, the picker doesn't have a title, so this won't help there. Can you change the picker confirm button label instead or as well?

### tk...@chromium.org (2013-07-02)

> On OS X, the picker doesn't have a title, so this won't help there.

We can add a message by [NSOpenPanel setMessage:...].



### ki...@chromium.org (2013-07-02)

Yes, we can change the confirmation button label on OS X.

Current status:
GTK, GTK2 -> could change both dialog title and confirm button text.
Chrome OS -> could change both dialog title and confirm button text.
KDE -> could change dialog title only.
Mac OS X -> could change confirm button text (no dialog title).
Win, Win Aura -> haven't tested yet, but can likely change dialog title.

The string I have used:
Dialog title text: "Select a folder to upload" for ChromeOS, "Select Folder to Upload" for others (different strings for consistency with other UI)
Confirmation button: "Upload"

If these look ok I'm sending out patches for reviewers.


### ki...@chromium.org (2013-07-03)

Attaching screenshot. (This one's taken with ChromeOS build)


### ki...@chromium.org (2013-07-03)

Security folks (cevans, palmer?), John: can you take a look at the screenshot (#19) to see if such UI change would mitigate the security impact enough to keep the feature?


### jo...@chromium.org (2013-07-03)

Definitely an improvement - users will be more likely to think twice before clicking Upload.

Minor downside: it's slightly inconsistent with the <input type="file"> dialog (Open File / Open on Linux) and the <input type="file" multiple> dialog (Open Files / Open on Linux). Does it make sense to change those to match? Or maybe we can just live with this inconsistency (as those are less dangerous)?

One other thing we could potentially do (in addition) would be to show a follow-up warning/confirmation dialog if you select a very large folder, like your Documents or Downloads folder, as it's less likely you intended to upload all of that. Presumably we have to traverse the filesystem anyway when you upload a directory, so we can easily see how many files are involved (and possibly their total size) - I guess the tricky part would be coming up with a threshold for when to show the warning. For example 200 files might both annoy users uploading large folders, while not protecting users unwittingly uploading their entire (small) collection of Downloads/Documents.

### ki...@chromium.org (2013-07-03)

Thanks for the input. Both make sense, though showing warning dialog feels a bit too annoying.  Maybe infobar would be better, if we want to show something?

glen@: could I get your opinion on the possible UI changes for <input type=file>? (Please see the attachment #19 and proposal made by john on #21)

### ki...@chromium.org (2013-07-26)

New strings got lgtm, will send out patches for review.

### ki...@chromium.org (2013-07-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-07-31)

------------------------------------------------------------------------
r214588 | kinuko@chromium.org | 2013-07-31T06:33:49.102364Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/chromeos/extensions/file_manager/file_browser_private_api.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/chromeos/extensions/file_manager/file_manager_util.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/base/strings/ui_strings.grd?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/shell_dialogs/gtk/select_file_dialog_impl_gtk.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/resources/file_manager/js/file_manager.js?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/shell_dialogs/select_file_dialog_win.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/resources/file_manager/js/file_selection.js?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/libgtk2ui/select_file_dialog_impl_kde.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_view_impl.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/app/generated_resources.grd?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/shell_dialogs/gtk/select_file_dialog_impl_kde.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/file_select_helper.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/libgtk2ui/select_file_dialog_impl_gtk2.cc?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/shell_dialogs/select_file_dialog.h?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/public/common/file_chooser_params.h?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/resources/file_manager/css/file_manager.css?r1=214588&r2=214587&pathrev=214588
   M http://src.chromium.org/viewvc/chrome/trunk/src/ui/shell_dialogs/select_file_dialog_mac.mm?r1=214588&r2=214587&pathrev=214588

Change dialog texts for folder upload to explicitly indicate it's for 'Uploading'

Currently we show the same dialog title and confirm button
('Select Folder' and 'OK' or 'Open') for folder upload,
but it should more clearly tell that it's for 'uploading',
so that the user can know s/he is exposing the folder
content to the website.

This patch makes following UI string changes to make it clear:

* "Select a folder to upload" for dialog title on ChromeOS
(original text is: "Select a folder to open")
* "Select Folder to Upload" for dialog title on other platforms
(original text is: "Select Folder")
* "Upload" for dialog confirm button (original text is: "Open")

The new string texts have gotten LGTM by UI team.

BUG=252888
TEST=manual
R=avi@chromium.org, jamesr@chromium.org, sky@chromium.org, yoshiki@chromium.org

Review URL: https://codereview.chromium.org/18627002
------------------------------------------------------------------------

### in...@chromium.org (2013-07-31)

[Empty comment from Monorail migration]

### la...@google.com (2013-08-10)

Removing Merge-Approval for requests not in current milestones (28, 29, 30)

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-11-05)

Thanks for the report! Sorry that it took us so long to get back to you on this. This qualifies for a $1000 reward because even though it is a medium severity issue, your PoC demonstrated the exploitability of the issue very clearly.

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

Adding glynwintle@yahoo.com as reward recipient (original reporter via johnme@chromium.org)

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/252888?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077693)*
