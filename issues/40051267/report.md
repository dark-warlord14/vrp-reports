# pdfium (XFA): wrong object type in CXFA_FFPageView::GetPageViewRect

| Field | Value |
|-------|-------|
| **Issue ID** | [40051267](https://issues.chromium.org/issues/40051267) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-16 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
xfa/fxfa/cxfa_ffpageview.cpp:123:43: runtime error: member call on address 0x563873f7b9c0 which does not point to an object of type 'CXFA_ViewLayoutItem'
0x563873f7b9c0: note: object is of type 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'
 00 00 00 00  48 78 05 71 38 56 00 00  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'

    #0 0x563870677840 in CXFA_FFPageView::GetPageViewRect() const xfa/fxfa/cxfa_ffpageview.cpp:123:43
    #1 0x56387069a8a9 in CXFA_FFWidget::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_ffwidget.cpp:294:23
    #2 0x56387064f21d in CXFA_FFField::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_fffield.cpp:54:27
    #3 0x56387069b48d in CXFA_FFWidget::InvalidateRect() xfa/fxfa/cxfa_ffwidget.cpp:368:24
    #4 0x5638706a2083 in CXFA_FWLAdapterWidgetMgr::RepaintWidget(CFWL_Widget*) xfa/fxfa/cxfa_fwladapterwidgetmgr.cpp:24:14
    #5 0x5638707be44a in CFWL_WidgetMgr::RepaintWidget(CFWL_Widget*, CFX_RectF const&) xfa/fwl/cfwl_widgetmgr.cpp:151:15
    #6 0x5638707bb502 in CFWL_Widget::RepaintRect(CFX_RectF const&) xfa/fwl/cfwl_widget.cpp:310:17
    #7 0x5638707709d9 in CFWL_Edit::HideCaret(CFX_RectF*) xfa/fwl/cfwl_edit.cpp:928:5
    #8 0x56387077072d in CFWL_Edit::~CFWL_Edit() xfa/fwl/cfwl_edit.cpp:59:5
    #9 0x5638707667d5 in CFWL_DateTimeEdit::~CFWL_DateTimeEdit() xfa/fwl/cfwl_datetimeedit.cpp:22:39
    #10 0x56387076f969 in std::__1::default_delete<CFWL_DateTimeEdit>::operator()(CFWL_DateTimeEdit*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #11 0x56387076f801 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::reset(CFWL_DateTimeEdit*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #12 0x563870767d27 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #13 0x563870767e64 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:59:1
    #14 0x563870767eb5 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:57:45
    #15 0x56387062589a in std::__1::default_delete<CFWL_Widget>::operator()(CFWL_Widget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #16 0x563870625731 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::reset(CFWL_Widget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #17 0x563870622587 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #18 0x56387064efe0 in CXFA_FFField::~CXFA_FFField() xfa/fxfa/cxfa_fffield.cpp:50:29
    #19 0x563870690b98 in CXFA_FFTextEdit::~CXFA_FFTextEdit() xfa/fxfa/cxfa_fftextedit.cpp:43:1
    #20 0x563870635065 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #21 0x5638706350a5 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #22 0x56387067020a in std::__1::default_delete<CXFA_FFWidget>::operator()(CXFA_FFWidget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #23 0x5638706700a1 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::reset(CXFA_FFWidget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #24 0x563870669e37 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #25 0x5638707d9c85 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #26 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #27 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #28 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #29 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #30 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #31 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #32 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #33 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #34 0x5638707d9c9f in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #35 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #36 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #37 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #38 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #39 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #40 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #41 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #42 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #43 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #44 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #45 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #46 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #47 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #48 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #49 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #50 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #51 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #52 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #53 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #54 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #55 0x56387081c749 in fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem>::operator()(CXFA_ViewLayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #56 0x56387081c5e1 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::reset(CXFA_ViewLayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #57 0x56387081c577 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #58 0x563870807235 in fxcrt::RetainPtr<CXFA_ViewLayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #59 0x56387081e22a in std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >::destroy(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1920:64
    #60 0x56387081e200 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::integral_constant<bool, true>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1782:18
    #61 0x56387081e1e0 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1619:14
    #62 0x56387081e17c in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destruct_at_end(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/vector:426:9
    #63 0x56387081e0a8 in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::clear() buildtools/third_party/libc++/trunk/include/vector:369:29
    #64 0x56387081de4f in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~__vector_base() buildtools/third_party/libc++/trunk/include/vector:463:9
    #65 0x5638708075fd in std::__1::vector<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~vector() buildtools/third_party/libc++/trunk/include/vector:555:5
    #66 0x5638708074cb in CXFA_ViewLayoutProcessor::~CXFA_ViewLayoutProcessor() xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:349:1
    #67 0x563870805c8a in std::__1::default_delete<CXFA_ViewLayoutProcessor>::operator()(CXFA_ViewLayoutProcessor*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #68 0x563870805b71 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::reset(CXFA_ViewLayoutProcessor*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #69 0x563870803e57 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #70 0x563870803e12 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #71 0x563870803e85 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #72 0x56387063db7a in std::__1::default_delete<CXFA_Document::LayoutProcessorIface>::operator()(CXFA_Document::LayoutProcessorIface*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #73 0x56387063da11 in std::__1::unique_ptr<CXFA_Document::LayoutProcessorIface, std::__1::default_delete<CXFA_Document::LayoutProcessorIface> >::reset(CXFA_Document::LayoutProcessorIface*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #74 0x563870841e77 in CXFA_Document::ClearLayoutData() xfa/fxfa/parser/cxfa_document.cpp:1288:22
    #75 0x56387097cf11 in CPDFXFA_Context::SetFormFillEnv(CPDFSDK_FormFillEnvironment*) fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:127:29
    #76 0x56386ebb902b in FPDFDOC_ExitFormFillEnvironment fpdfsdk/fpdf_formfill.cpp:350:15
    #77 0x56386eb11115 in FPDFFormHandleDeleter::operator()(fpdf_form_handle_t__*) public/cpp/fpdf_deleters.h:48:5
    #78 0x56386eb11001 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::reset(fpdf_form_handle_t__*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #79 0x56386eb0c127 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #80 0x56386eb03801 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:980:1
    #81 0x56386eb0100f in main samples/pdfium_test.cc:1179:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1042915.pdf](attachments/chromium-1042915.pdf) (application/pdf, 938 B)
- [chromium-1042915.evt](attachments/chromium-1042915.evt) (application/octet-stream, 127 B)

## Timeline

### pd...@gmail.com (2020-01-16)

Two additional follow-up reports.

(1)

xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:42:7: runtime error: member call on address 0x563873f7b9c0 which does not point to an object of type 'CXFA_LayoutItem'
0x563873f7b9c0: note: object is of type 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'
 00 00 00 00  48 78 05 71 38 56 00 00  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'

    #0 0x563870806a5c in CXFA_ViewLayoutItem::GetPageSize() const xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:42:7
    #1 0x5638706777e8 in CXFA_FFPageView::GetPageViewRect() const xfa/fxfa/cxfa_ffpageview.cpp:123:43
    #2 0x56387069a8a9 in CXFA_FFWidget::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_ffwidget.cpp:294:23
    #3 0x56387064f21d in CXFA_FFField::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_fffield.cpp:54:27
    #4 0x56387069b48d in CXFA_FFWidget::InvalidateRect() xfa/fxfa/cxfa_ffwidget.cpp:368:24
    #5 0x5638706a2083 in CXFA_FWLAdapterWidgetMgr::RepaintWidget(CFWL_Widget*) xfa/fxfa/cxfa_fwladapterwidgetmgr.cpp:24:14
    #6 0x5638707be44a in CFWL_WidgetMgr::RepaintWidget(CFWL_Widget*, CFX_RectF const&) xfa/fwl/cfwl_widgetmgr.cpp:151:15
    #7 0x5638707bb502 in CFWL_Widget::RepaintRect(CFX_RectF const&) xfa/fwl/cfwl_widget.cpp:310:17
    #8 0x5638707709d9 in CFWL_Edit::HideCaret(CFX_RectF*) xfa/fwl/cfwl_edit.cpp:928:5
    #9 0x56387077072d in CFWL_Edit::~CFWL_Edit() xfa/fwl/cfwl_edit.cpp:59:5
    #10 0x5638707667d5 in CFWL_DateTimeEdit::~CFWL_DateTimeEdit() xfa/fwl/cfwl_datetimeedit.cpp:22:39
    #11 0x56387076f969 in std::__1::default_delete<CFWL_DateTimeEdit>::operator()(CFWL_DateTimeEdit*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #12 0x56387076f801 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::reset(CFWL_DateTimeEdit*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #13 0x563870767d27 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #14 0x563870767e64 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:59:1
    #15 0x563870767eb5 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:57:45
    #16 0x56387062589a in std::__1::default_delete<CFWL_Widget>::operator()(CFWL_Widget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #17 0x563870625731 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::reset(CFWL_Widget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #18 0x563870622587 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #19 0x56387064efe0 in CXFA_FFField::~CXFA_FFField() xfa/fxfa/cxfa_fffield.cpp:50:29
    #20 0x563870690b98 in CXFA_FFTextEdit::~CXFA_FFTextEdit() xfa/fxfa/cxfa_fftextedit.cpp:43:1
    #21 0x563870635065 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #22 0x5638706350a5 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #23 0x56387067020a in std::__1::default_delete<CXFA_FFWidget>::operator()(CXFA_FFWidget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #24 0x5638706700a1 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::reset(CXFA_FFWidget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #25 0x563870669e37 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #26 0x5638707d9c85 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #27 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #28 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #29 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #30 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #31 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #32 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #33 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #34 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #35 0x5638707d9c9f in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #36 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #37 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #38 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #39 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #40 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #41 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #42 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #43 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #44 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #45 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #46 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #47 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #48 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #49 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #50 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #51 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #52 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #53 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #54 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #55 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #56 0x56387081c749 in fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem>::operator()(CXFA_ViewLayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #57 0x56387081c5e1 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::reset(CXFA_ViewLayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #58 0x56387081c577 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #59 0x563870807235 in fxcrt::RetainPtr<CXFA_ViewLayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #60 0x56387081e22a in std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >::destroy(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1920:64
    #61 0x56387081e200 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::integral_constant<bool, true>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1782:18
    #62 0x56387081e1e0 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1619:14
    #63 0x56387081e17c in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destruct_at_end(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/vector:426:9
    #64 0x56387081e0a8 in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::clear() buildtools/third_party/libc++/trunk/include/vector:369:29
    #65 0x56387081de4f in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~__vector_base() buildtools/third_party/libc++/trunk/include/vector:463:9
    #66 0x5638708075fd in std::__1::vector<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~vector() buildtools/third_party/libc++/trunk/include/vector:555:5
    #67 0x5638708074cb in CXFA_ViewLayoutProcessor::~CXFA_ViewLayoutProcessor() xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:349:1
    #68 0x563870805c8a in std::__1::default_delete<CXFA_ViewLayoutProcessor>::operator()(CXFA_ViewLayoutProcessor*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #69 0x563870805b71 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::reset(CXFA_ViewLayoutProcessor*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #70 0x563870803e57 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #71 0x563870803e12 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #72 0x563870803e85 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #73 0x56387063db7a in std::__1::default_delete<CXFA_Document::LayoutProcessorIface>::operator()(CXFA_Document::LayoutProcessorIface*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #74 0x56387063da11 in std::__1::unique_ptr<CXFA_Document::LayoutProcessorIface, std::__1::default_delete<CXFA_Document::LayoutProcessorIface> >::reset(CXFA_Document::LayoutProcessorIface*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #75 0x563870841e77 in CXFA_Document::ClearLayoutData() xfa/fxfa/parser/cxfa_document.cpp:1288:22
    #76 0x56387097cf11 in CPDFXFA_Context::SetFormFillEnv(CPDFSDK_FormFillEnvironment*) fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:127:29
    #77 0x56386ebb902b in FPDFDOC_ExitFormFillEnvironment fpdfsdk/fpdf_formfill.cpp:350:15
    #78 0x56386eb11115 in FPDFFormHandleDeleter::operator()(fpdf_form_handle_t__*) public/cpp/fpdf_deleters.h:48:5
    #79 0x56386eb11001 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::reset(fpdf_form_handle_t__*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #80 0x56386eb0c127 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #81 0x56386eb03801 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:980:1
    #82 0x56386eb0100f in main samples/pdfium_test.cc:1179:5

(2)

../../xfa/fxfa/layout/cxfa_layoutitem.h:31:43: runtime error: member access within address 0x563873f7b9c0 which does not point to an object of type 'const CXFA_LayoutItem'
0x563873f7b9c0: note: object is of type 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'
 00 00 00 00  48 78 05 71 38 56 00 00  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'fxcrt::RetainedTreeNode<CXFA_LayoutItem>'

    #0 0x56386f3bd17e in CXFA_LayoutItem::GetFormNode() const xfa/fxfa/layout/cxfa_layoutitem.h:31:43
    #1 0x56387080672f in CXFA_ViewLayoutItem::GetPageSize() const xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:42:7
    #2 0x5638706777e8 in CXFA_FFPageView::GetPageViewRect() const xfa/fxfa/cxfa_ffpageview.cpp:123:43
    #3 0x56387069a8a9 in CXFA_FFWidget::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_ffwidget.cpp:294:23
    #4 0x56387064f21d in CXFA_FFField::GetBBox(CXFA_FFWidget::FocusOption) xfa/fxfa/cxfa_fffield.cpp:54:27
    #5 0x56387069b48d in CXFA_FFWidget::InvalidateRect() xfa/fxfa/cxfa_ffwidget.cpp:368:24
    #6 0x5638706a2083 in CXFA_FWLAdapterWidgetMgr::RepaintWidget(CFWL_Widget*) xfa/fxfa/cxfa_fwladapterwidgetmgr.cpp:24:14
    #7 0x5638707be44a in CFWL_WidgetMgr::RepaintWidget(CFWL_Widget*, CFX_RectF const&) xfa/fwl/cfwl_widgetmgr.cpp:151:15
    #8 0x5638707bb502 in CFWL_Widget::RepaintRect(CFX_RectF const&) xfa/fwl/cfwl_widget.cpp:310:17
    #9 0x5638707709d9 in CFWL_Edit::HideCaret(CFX_RectF*) xfa/fwl/cfwl_edit.cpp:928:5
    #10 0x56387077072d in CFWL_Edit::~CFWL_Edit() xfa/fwl/cfwl_edit.cpp:59:5
    #11 0x5638707667d5 in CFWL_DateTimeEdit::~CFWL_DateTimeEdit() xfa/fwl/cfwl_datetimeedit.cpp:22:39
    #12 0x56387076f969 in std::__1::default_delete<CFWL_DateTimeEdit>::operator()(CFWL_DateTimeEdit*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #13 0x56387076f801 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::reset(CFWL_DateTimeEdit*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #14 0x563870767d27 in std::__1::unique_ptr<CFWL_DateTimeEdit, std::__1::default_delete<CFWL_DateTimeEdit> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #15 0x563870767e64 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:59:1
    #16 0x563870767eb5 in CFWL_DateTimePicker::~CFWL_DateTimePicker() xfa/fwl/cfwl_datetimepicker.cpp:57:45
    #17 0x56387062589a in std::__1::default_delete<CFWL_Widget>::operator()(CFWL_Widget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #18 0x563870625731 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::reset(CFWL_Widget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #19 0x563870622587 in std::__1::unique_ptr<CFWL_Widget, std::__1::default_delete<CFWL_Widget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #20 0x56387064efe0 in CXFA_FFField::~CXFA_FFField() xfa/fxfa/cxfa_fffield.cpp:50:29
    #21 0x563870690b98 in CXFA_FFTextEdit::~CXFA_FFTextEdit() xfa/fxfa/cxfa_fftextedit.cpp:43:1
    #22 0x563870635065 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #23 0x5638706350a5 in CXFA_FFDateTimeEdit::~CXFA_FFDateTimeEdit() xfa/fxfa/cxfa_ffdatetimeedit.cpp:27:43
    #24 0x56387067020a in std::__1::default_delete<CXFA_FFWidget>::operator()(CXFA_FFWidget*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #25 0x5638706700a1 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::reset(CXFA_FFWidget*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #26 0x563870669e37 in std::__1::unique_ptr<CXFA_FFWidget, std::__1::default_delete<CXFA_FFWidget> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #27 0x5638707d9c85 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #28 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #29 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #30 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #31 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #32 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #33 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #34 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #35 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #36 0x5638707d9c9f in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:26:1
    #37 0x5638707da065 in CXFA_ContentLayoutItem::~CXFA_ContentLayoutItem() xfa/fxfa/layout/cxfa_contentlayoutitem.cpp:24:51
    #38 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #39 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #40 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #41 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #42 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #43 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #44 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #45 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #46 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #47 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #48 0x56386f3bee79 in fxcrt::ReleaseDeleter<CXFA_LayoutItem>::operator()(CXFA_LayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #49 0x56386f3bed11 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::reset(CXFA_LayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #50 0x56386f3beca7 in std::__1::unique_ptr<CXFA_LayoutItem, fxcrt::ReleaseDeleter<CXFA_LayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #51 0x56386f3bec75 in fxcrt::RetainPtr<CXFA_LayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #52 0x563870803b23 in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::~RetainedTreeNode() core/fxcrt/retained_tree_node.h:54:7
    #53 0x563870803323 in CXFA_LayoutItem::~CXFA_LayoutItem() xfa/fxfa/layout/cxfa_layoutitem.cpp:48:1
    #54 0x563870806271 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #55 0x5638708062d5 in CXFA_ViewLayoutItem::~CXFA_ViewLayoutItem() xfa/fxfa/layout/cxfa_viewlayoutitem.cpp:27:43
    #56 0x56386f3bf07e in fxcrt::RetainedTreeNode<CXFA_LayoutItem>::Release() core/fxcrt/retained_tree_node.h:71:7
    #57 0x56387081c749 in fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem>::operator()(CXFA_ViewLayoutItem*) const core/fxcrt/retain_ptr.h:20:47
    #58 0x56387081c5e1 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::reset(CXFA_ViewLayoutItem*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #59 0x56387081c577 in std::__1::unique_ptr<CXFA_ViewLayoutItem, fxcrt::ReleaseDeleter<CXFA_ViewLayoutItem> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #60 0x563870807235 in fxcrt::RetainPtr<CXFA_ViewLayoutItem>::~RetainPtr() core/fxcrt/retain_ptr.h:25:7
    #61 0x56387081e22a in std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >::destroy(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1920:64
    #62 0x56387081e200 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::integral_constant<bool, true>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1782:18
    #63 0x56387081e1e0 in void std::__1::allocator_traits<std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::destroy<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >(std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> >&, fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/memory:1619:14
    #64 0x56387081e17c in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::__destruct_at_end(fxcrt::RetainPtr<CXFA_ViewLayoutItem>*) buildtools/third_party/libc++/trunk/include/vector:426:9
    #65 0x56387081e0a8 in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::clear() buildtools/third_party/libc++/trunk/include/vector:369:29
    #66 0x56387081de4f in std::__1::__vector_base<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~__vector_base() buildtools/third_party/libc++/trunk/include/vector:463:9
    #67 0x5638708075fd in std::__1::vector<fxcrt::RetainPtr<CXFA_ViewLayoutItem>, std::__1::allocator<fxcrt::RetainPtr<CXFA_ViewLayoutItem> > >::~vector() buildtools/third_party/libc++/trunk/include/vector:555:5
    #68 0x5638708074cb in CXFA_ViewLayoutProcessor::~CXFA_ViewLayoutProcessor() xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:349:1
    #69 0x563870805c8a in std::__1::default_delete<CXFA_ViewLayoutProcessor>::operator()(CXFA_ViewLayoutProcessor*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #70 0x563870805b71 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::reset(CXFA_ViewLayoutProcessor*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #71 0x563870803e57 in std::__1::unique_ptr<CXFA_ViewLayoutProcessor, std::__1::default_delete<CXFA_ViewLayoutProcessor> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #72 0x563870803e12 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #73 0x563870803e85 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor() xfa/fxfa/layout/cxfa_layoutprocessor.cpp:31:45
    #74 0x56387063db7a in std::__1::default_delete<CXFA_Document::LayoutProcessorIface>::operator()(CXFA_Document::LayoutProcessorIface*) const buildtools/third_party/libc++/trunk/include/memory:2378:5
    #75 0x56387063da11 in std::__1::unique_ptr<CXFA_Document::LayoutProcessorIface, std::__1::default_delete<CXFA_Document::LayoutProcessorIface> >::reset(CXFA_Document::LayoutProcessorIface*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #76 0x563870841e77 in CXFA_Document::ClearLayoutData() xfa/fxfa/parser/cxfa_document.cpp:1288:22
    #77 0x56387097cf11 in CPDFXFA_Context::SetFormFillEnv(CPDFSDK_FormFillEnvironment*) fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:127:29
    #78 0x56386ebb902b in FPDFDOC_ExitFormFillEnvironment fpdfsdk/fpdf_formfill.cpp:350:15
    #79 0x56386eb11115 in FPDFFormHandleDeleter::operator()(fpdf_form_handle_t__*) public/cpp/fpdf_deleters.h:48:5
    #80 0x56386eb11001 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::reset(fpdf_form_handle_t__*) buildtools/third_party/libc++/trunk/include/memory:2633:7
    #81 0x56386eb0c127 in std::__1::unique_ptr<fpdf_form_handle_t__, FPDFFormHandleDeleter>::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2587:19
    #82 0x56386eb03801 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:980:1
    #83 0x56386eb0100f in main samples/pdfium_test.cc:1179:5


### pd...@gmail.com (2020-01-16)

Triggering this requires moderate user interaction.

1. Click date field.
2. Remove focus for the field (by tabbing to a different field or otherwise).
3. Restore focus to the date field (by tabbing back or otherwise).
4. Click date field twice.

It's likely possible to automate steps 2-3 in FormCalc by calling setFocus() on the first event.

I'm attaching the event file to use with pdfium_test.

### pd...@gmail.com (2020-01-16)

Note: Chrome doesn't use XFA.

### ct...@chromium.org (2020-01-16)

tsepez@ could you take a look at this report and recommend a Severity? I'm not sure what the implications of this error would be for pdfium. My guess would be Medium, but mitigated by the significant interaction requirement so marking this as Severity-Low for now.

Reporter: Does this reproduce on current Stable (M-79) or Canary (M-81)?

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2020-01-17)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-01-22)

I think this may be a case of calling back into a partially-destructed object from events triggered by its superclass destructor, which has already updated the vtable to that of the superclass. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-30)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a983336ddf1099e4f3ffbcdf82adca1a4be8141c

commit a983336ddf1099e4f3ffbcdf82adca1a4be8141c
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jan 30 19:14:32 2020

Null out CXFA_FF* layout item reference in layout item dtor.

First step towards avoiding a re-entry on a partially destructed
object, but does not fully fix the referenced issue.  Provides symmetry
with what happens during the constructor when the reference is set.

Bug: chromium:1042915
Change-Id: Ic561c243db31fabc95a3da1c12b451665901e4ac
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65850
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a983336ddf1099e4f3ffbcdf82adca1a4be8141c/xfa/fxfa/layout/cxfa_viewlayoutitem.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a983336ddf1099e4f3ffbcdf82adca1a4be8141c/xfa/fxfa/layout/cxfa_contentlayoutitem.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7cba1241b0736b50d43e00bde62f9d14f89f2351

commit 7cba1241b0736b50d43e00bde62f9d14f89f2351
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 30 21:47:48 2020

Roll src/third_party/pdfium 60ca7defc0eb..cf899c949229 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/60ca7defc0eb..cf899c949229

git log 60ca7defc0eb..cf899c949229 --date=short --first-parent --format='%ad %ae %s'
2020-01-30 tsepez@chromium.org Remove unused CPDF_TextState::GetShearAngle(), GetFontSizeV()
2020-01-30 tsepez@chromium.org Null out CXFA_FF* layout item reference in layout item dtor.

Created with:
  gclient setdep -r src/third_party/pdfium@cf899c949229

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1042915
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I9caf79477e70d79c4558e69ec3f17b7840bed12f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2031611
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#737045}

[modify] https://crrev.com/7cba1241b0736b50d43e00bde62f9d14f89f2351/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/62c4aa4467335ea1dace102d389da1cc9a0b5f7c

commit 62c4aa4467335ea1dace102d389da1cc9a0b5f7c
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 31 00:26:54 2020

Avoid segv in CXFA_FFPageView::GetPageViewRect() after page is gone.

Take advantage of null indicator introduced at a983336d.
Partially fixes the referenced issue.

Bug: chromium:1042915
Change-Id: I4bf907d67197f8b7405aac2b3639563abba264a5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65837
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/62c4aa4467335ea1dace102d389da1cc9a0b5f7c/xfa/fxfa/cxfa_ffpageview.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51fdffd823c17bfd0e629c29e48697522b277797

commit 51fdffd823c17bfd0e629c29e48697522b277797
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jan 31 03:11:42 2020

Roll src/third_party/pdfium 04bb1f2f0353..62c4aa446733 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/04bb1f2f0353..62c4aa446733

git log 04bb1f2f0353..62c4aa446733 --date=short --first-parent --format='%ad %ae %s'
2020-01-31 tsepez@chromium.org Avoid segv in CXFA_FFPageView::GetPageViewRect() after page is gone.
2020-01-31 thestig@chromium.org Rename CPDFSDK_FormFillEnvironment::GetPermissions().
2020-01-30 thestig@chromium.org Clarify what CPDFSDK_FormFillEnvironment::GetPermissions() does.
2020-01-30 thestig@chromium.org Consolidate dimension checking code inside cpdf_dib.cpp.
2020-01-30 thestig@chromium.org Handle a case of colorspace mismatch with JPEG2000 images.

Created with:
  gclient setdep -r src/third_party/pdfium@62c4aa446733

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1012369,chromium:1042915
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ia4975786941e334f991dd674f2c6e2b12e1aaf06
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2032616
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#737190}

[modify] https://crrev.com/51fdffd823c17bfd0e629c29e48697522b277797/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e

commit 7b8eb884cfd6da446798014671be54bc2fed305e
Author: Tom Sepez <tsepez@chromium.org>
Date: Fri Jan 31 19:50:35 2020

Make all CXFA_FFWidget observe their CXFA_FFPageview.

Although a very blunt technique, the cost shouldn't be terrible in
memory given the size of the CXFA_FFWidget itself, and shouldn't be
terrible in runtime give the rarity of the notification case. Ideally,
future memory work would improve this situation, but this safely
adding more test cases at present to guard against regressions.

Bug: chromium:1042915, chromium:1010844
Change-Id: Idd02967a8297d3bce7d35451db9ae05f79cdf3ac
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65870
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/xfa/fxfa/cxfa_ffwidget.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/xfa/fxfa/cxfa_ffwidget.h
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915_expected.txt
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915.pdf
[add] https://pdfium.googlesource.com/pdfium/+/7b8eb884cfd6da446798014671be54bc2fed305e/testing/resources/javascript/xfa_specific/bug_1042915.evt


### ts...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df6fd718399c5a2860b543cfa55f3c60a230c752

commit df6fd718399c5a2860b543cfa55f3c60a230c752
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jan 31 21:28:03 2020

Roll src/third_party/pdfium 62c4aa446733..7b8eb884cfd6 (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/62c4aa446733..7b8eb884cfd6

git log 62c4aa446733..7b8eb884cfd6 --date=short --first-parent --format='%ad %ae %s'
2020-01-31 tsepez@chromium.org Make all CXFA_FFWidget observe their CXFA_FFPageview.
2020-01-31 thestig@chromium.org Fix various build/include_order lint errors.
2020-01-31 thestig@chromium.org Give some .in test files better formatting.
2020-01-31 tsepez@chromium.org Remove dwCoordinatesType arg from GetPageMatrix().
2020-01-31 thestig@chromium.org Reduce the number of calls to HasPermissions().
2020-01-31 thestig@chromium.org Move permission constants to constants/access_permissions.h.
2020-01-31 dhoss@chromium.org Run tests with --disable-xfa in coverage_report.py

Created with:
  gclient setdep -r src/third_party/pdfium@7b8eb884cfd6

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1010844,chromium:1042915
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I6415f31dfba3a5156486c3f53cb14e64d455c30a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2033586
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#737460}

[modify] https://crrev.com/df6fd718399c5a2860b543cfa55f3c60a230c752/DEPS


### sh...@chromium.org (2020-02-01)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-05)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $1,000 for this report! 

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-09)

This issue was migrated from crbug.com/chromium/1042915?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051267)*
