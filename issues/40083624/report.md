# Heap-use-after-free in favicon::FaviconDriverImpl::DidDownloadFavicon

| Field | Value |
|-------|-------|
| **Issue ID** | [40083624](https://issues.chromium.org/issues/40083624) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2016-1641 |
| **Reporter** | cl...@chromium.org |
| **Assignee** | pk...@chromium.org |
| **Created** | 2016-02-03 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4534142575837184

Fuzzer: attekett_surku_fuzzer
Job Type: linux_lsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61100011bde8
Crash State:
  favicon::FaviconDriverImpl::DidDownloadFavicon
  base::debug::TaskAnnotator::RunTask
  base::MessageLoop::RunTask
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96JOuDq6mLnUMa4Y-s3tV7CO117RnvRcVQWkP4vtLObV8n_YxtP2KRpxhwjwjkzT0U4wYoe928i-bEoezVIPwy3jlXOgDQ1tLiZAkKtwDgGmAKO1S9ZceGcjjUgU7EuVYDaytsiRqmzYyUTJEFKbZ_ZIMX4MQ


Additional requirements: Requires Gestures

Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-02-03)

The CF crash is unreproducible, and was likely hit by chance due to gestures, and not because of anything specific to the fuzzer itself, but

in src/components/favicon/content/content_favicon_driver.cc:

int ContentFaviconDriver::StartDownload(const GURL& url, int max_image_size) {
  if (WasUnableToDownloadFavicon(url)) {
    DVLOG(1) << "Skip Failed FavIcon: " << url;
    return 0;
  }

  bool bypass_cache = (bypass_cache_page_url_ == GetActiveURL());
  bypass_cache_page_url_ = GURL();

  return web_contents()->DownloadImage(
      url, true, max_image_size, bypass_cache,
      base::Bind(&FaviconDriverImpl::DidDownloadFavicon,
                 base::Unretained(this)));
}

The use of base::Unretained looks unsafe, as it looks like the ContentFaviconDriver could get deleted later from prerender::PrerenderManager::PeriodicCleanup() as indicated in the free stack.

+caitkp, who seems to have fixed a similar bug many moons ago.

### oc...@chromium.org (2016-02-03)

Actually, pkotwicz is probably a better person to look into this. Sorry for the spam

### ke...@chromium.org (2016-02-03)

Moving to Cr-UI since this is favicon related, please update that if there is a better component for this pkotwicz.

### ke...@chromium.org (2016-02-03)

Since that code is almost a year old, I am marking this as affecting stable.

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### pk...@chromium.org (2016-02-09)

I will look at this this week

### pk...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/75ca8ffd7bd7c58ace1144df05e1307d8d707662

commit 75ca8ffd7bd7c58ace1144df05e1307d8d707662
Author: pkotwicz <pkotwicz@chromium.org>
Date: Tue Feb 16 23:10:19 2016

Don't call WebContents::DownloadImage() callback if the WebContents were deleted

BUG=583718

Review URL: https://codereview.chromium.org/1685343004

Cr-Commit-Position: refs/heads/master@{#375700}

[modify] http://crrev.com/75ca8ffd7bd7c58ace1144df05e1307d8d707662/content/browser/web_contents/web_contents_impl.cc
[modify] http://crrev.com/75ca8ffd7bd7c58ace1144df05e1307d8d707662/content/browser/web_contents/web_contents_impl.h


### oc...@chromium.org (2016-02-16)

Thanks for fixing this, pkotwicz!

### oc...@chromium.org (2016-02-16)

(For the reward panel folks: I'm pretty sure that this bug wasn't found because of anything specific to the fuzzer, but because of CF gestures)

### cl...@chromium.org (2016-02-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-02-24)

Request merge to M-49.

### ti...@google.com (2016-02-24)

[Automated comment] Less than 2 weeks to go before stable on M49, manual review required.

### ss...@google.com (2016-02-24)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-02-24)

[Comment Deleted]

### bu...@chromium.org (2016-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e5428348c4d96e506f52614a4d37c158ac839678

commit e5428348c4d96e506f52614a4d37c158ac839678
Author: Peter Kotwicz <pkotwicz@google.com>
Date: Thu Feb 25 00:26:16 2016

Don't call WebContents::DownloadImage() callback if the WebContents were deleted

BUG=583718

Review URL: https://codereview.chromium.org/1685343004

Cr-Commit-Position: refs/heads/master@{#375700}
(cherry picked from commit 75ca8ffd7bd7c58ace1144df05e1307d8d707662)

Review URL: https://codereview.chromium.org/1730363003 .

Cr-Commit-Position: refs/branch-heads/2623@{#504}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] https://crrev.com/e5428348c4d96e506f52614a4d37c158ac839678/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/e5428348c4d96e506f52614a4d37c158ac839678/content/browser/web_contents/web_contents_impl.h


### bu...@chromium.org (2016-02-25)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/e5428348c4d96e506f52614a4d37c158ac839678

commit e5428348c4d96e506f52614a4d37c158ac839678
Author: Peter Kotwicz <pkotwicz@google.com>
Date: Thu Feb 25 00:26:16 2016


### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Hey Atte - $500 for this report.

Panel notes: Appears that bug was found from CF gestures, but it did trigger on your fuzzer first.

CVE-ID to follow and I'll put this in next week's payment run.

### ti...@google.com (2016-03-02)

CVE-2016-1641

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/583718?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083624)*
