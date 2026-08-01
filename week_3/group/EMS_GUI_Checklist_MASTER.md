# Checklist Kiểm thử GUI – EMS (Bản gộp chính thức nhóm)

**Task 1A – sản phẩm nhóm · 48 mục · phiên bản v1 (gộp)**

| | |
| --- | --- |
| **File nguồn đã gộp** | `EMS_GUI_Checklist_Share.md` (20 mục · GUI-xx) · `EMS_GUI_Checklist_Contribution_02.md` (16 mục · ADD-xx) · `EMS_GUI_Checklist_Addendum_16.md` (16 mục · GUI-xx bổ sung) |
| **Tổng số mục sau gộp** | 48 (sau khi loại 4 mục trùng + gộp nội dung 1 mục) |
| **Phân bổ IA** | IA-01 = 12 · IA-02 = 13 · IA-03 = 12 · IA-04 = 11 |
| **Ngày gộp** | 29/07/2026 |
| **Trạng thái** | Bản chính thức nhóm — sẵn sàng dùng cho Task 1B của mọi thành viên |

**Người đóng góp:**

| Người đóng góp | MSSV | Kịch bản | Số mục gốc |
| --- | --- | --- | --- |
| Phạm Anh Hào | 23127362 | A – Admin tạo và quản lý sự kiện | 20 |
| Nguyễn Hồng Quân | 22127345 | B – User đăng ký tham gia sự kiện | 16 |
| Lê Quang Phúc | 23127102 | C - Admin quản lý người dùng | 16 |

---

## 1. Đây là gì

Đây là **checklist GUI dùng chung chính thức** của nhóm cho Task 1A, gộp từ ba bản đóng góp cá nhân, đã **khử trùng lặp** theo đúng yêu cầu đề bài (§6, Task 1A: *"Dùng AI sinh bộ ban đầu, sau đó review phản biện... Nộp checklist đã gộp"*). Mọi thành viên dùng **đúng bản này** (không dùng lại ba file gốc riêng lẻ) để chạy Task 1B trên các màn hình mình phụ trách.

Bốn interface aspect dùng làm chiều phủ (không đổi so với các bản gốc):

| Mã | Tên | Phạm vi |
| --- | --- | --- |
| **IA-01** | Chuẩn UI chung | Layout, canh lề, typography, màu sắc, nhất quán, i18n EN/VI, empty/loading |
| **IA-02** | Forms | Nhãn trường, validation, vị trí báo lỗi, trường bắt buộc, upload, rich-text |
| **IA-03** | Navigation | Menu, breadcrumb, tab, sidebar, kéo-thả, back/return, deep link |
| **IA-04** | Feedback / State | Toast, badge, dialog xác nhận, progress bar, màu trạng thái, real-time |

---

## 2. Cách dùng checklist này (không đổi so với bản gốc)

- Đánh dấu **Passed** / **Failed** / **N/A** cho **từng mục ở từng màn hình**.
- Mục **Failed** → bắt buộc ghi lý do vào cột Notes **và** đính kèm ảnh chụp.
- Mục **N/A** → vẫn giữ nguyên dòng, ghi rõ lý do không áp dụng. **Không xoá dòng.**
- Mục **Passed** → không cần ảnh, không bắt buộc ghi chú.
- Mọi lỗi tìm được phải nộp lên Google Form **và** gộp vào Bug & Usability Findings Log (§7 đề bài).
- Cột **Xuất xứ** cho biết mục này đến từ đóng góp cá nhân nào và ID gốc — giữ lại để truy vết khi cần giải trình ở vấn đáp.

---

## 3. Nhật ký gộp & khử trùng lặp

Đối chiếu toàn bộ 52 mục ứng viên (20 + 16 + 16), phát hiện **5 trường hợp trùng/chồng lấn nội dung**. Xử lý theo nguyên tắc: *giữ bản diễn đạt cụ thể hơn, gộp phần bổ sung có giá trị, xoá phần lặp lại thuần tuý.*

| # | Mục bị gộp/loại | Trùng với | Lý do trùng | Cách xử lý |
| --- | --- | --- | --- | --- |
| 1 | `GUI-01-008` (định dạng ngày/giờ/số nhất quán) | `ADD-01-004` (dữ liệu nghiệp vụ nhất quán tên/đơn vị/thứ tự/icon) | Cả hai đều kiểm tra tính nhất quán của **cùng một dữ liệu** khi hiển thị ở nhiều nơi (list/detail/form/export); định dạng ngày-giờ-số chỉ là một trường hợp con của "dữ liệu nghiệp vụ" | **Gộp**: đưa yêu cầu về định dạng ngày/giờ/số vào mục hợp nhất `GUI-01-06`, không giữ ID riêng |
| 2 | `GUI-02-008` — vế 2 ("rời trang khi có thay đổi chưa lưu sẽ có cảnh báo") | `ADD-02-004` (cảnh báo rời form còn thay đổi chưa lưu qua Back/Cancel/menu/refresh/đóng tab) | Cùng kiểm tra một hành vi: cảnh báo trước khi mất dữ liệu form chưa lưu | **Xoá vế trùng**, chỉ giữ lại vế 1 (form dài chia section rõ tiêu đề) làm mục riêng `GUI-02-12`, viết lại cách kiểm chứng cho đúng phạm vi còn lại |
| 3 | `GUI-03-008` (deep link vượt quyền) | `ADD-03-003` (màn hình từ chối truy cập/tài nguyên không khả dụng không tạo ngõ cụt) | `ADD-03-003` đã bao trùm cả trường hợp deep link vượt quyền lẫn tài nguyên bị xoá/hết hạn; cách kiểm chứng gốc của `ADD-03-003` cũng đã gồm bước "mở URL bằng tài khoản không đủ quyền" | **Gộp**: giữ diễn đạt rộng của `ADD-03-003` làm mục `GUI-03-08`, bổ sung câu kiểm chứng cụ thể về deep link từ bản gốc `GUI-03-008` |
| 4 | `GUI-04-007` (progress bar + chống double-submit) | `GUI-04-004` (progress bar đã nằm trong danh sách thành phần phi văn bản cần có nhãn) và `ADD-04-001` (chống gửi trùng khi đang xử lý) | Cả hai vế của mục này đều là bản rút gọn/lặp của hai mục đã có sẵn ở nơi khác | **Xoá toàn bộ mục**; câu "không cho double-submit dù đang hiển thị spinner/progress" được gộp vào cách kiểm chứng của `GUI-04-06` (`ADD-04-001` cũ) |
| 5 | `GUI-04-008` (toast tự tắt, đóng tay, không chồng lấp) | `ADD-04-002` (toast/banner xếp theo mức quan trọng, không che nội dung, đóng được, không trùng lặp) | Cùng kiểm tra hành vi hiển thị/đóng/xếp chồng của toast; `ADD-04-002` diễn đạt đầy đủ và cụ thể hơn (có thêm tiêu chí không che nội dung thiết yếu) | **Xoá mục**, nội dung đã được `ADD-04-002` phủ đầy đủ hơn |

**Kết quả:** 52 mục ứng viên → loại 4 mục, gộp nội dung 1 mục → **48 mục chính thức**, vẫn cân bằng giữa bốn IA (12/13/12/11) và giữ được toàn bộ giá trị kiểm thử của cả ba bản đóng góp.

**Lưu ý cho các mục "trông giống nhau nhưng KHÔNG gộp"** — để nhóm không hiểu nhầm là bỏ sót khử trùng:

- `GUI-02-09` (`ADD-02-004`, cảnh báo khi **chủ động** rời form qua Back/Cancel/refresh) và `GUI-02-13` (`GUI-02-009` cũ, **autosave/draft** khi reload hoặc chuyển tab do sự cố mạng) — kiểm hai **kịch bản lỗi khác nhau** (chủ động vs. bị động mất dữ liệu), nên giữ tách biệt.
- `GUI-01-09` (`GUI-01-005` cũ, mật độ/khoảng trắng trên màn hình nhiều dữ liệu) và `GUI-01-03` (`ADD-01-002`, thứ bậc thị giác + hành động chính nổi bật) — cùng dựa trên Nielsen #8 nhưng kiểm hai khía cạnh khác nhau (mật độ hiển thị vs. phân cấp ưu tiên nội dung), nên giữ tách biệt.
- `GUI-04-10` (`GUI-04-006` cũ, cập nhật real-time không phá scroll/focus) và `GUI-04-04` (thành phần phi văn bản có nhãn thay thế, gồm cả real-time update) — `GUI-04-04` kiểm việc **có nhãn/giá trị thay thế**, `GUI-04-10` kiểm **hành vi không làm gián đoạn thao tác** khi dữ liệu tự cập nhật — khác góc độ, giữ tách biệt.
- `GUI-04-11` (`GUI-04-009` cũ, ba cách đóng overlay nhất quán: Esc/click-outside/nút X trên **nhiều loại overlay khác nhau**) và `GUI-03-02` (điều hướng bàn phím tổng quát cho form/dialog, gồm Esc đóng dialog) — `GUI-03-02` kiểm hành vi bàn phím nói chung, `GUI-04-11` kiểm **tính nhất quán giữa các loại overlay** (lightbox, vé QR, dialog xác nhận) cụ thể, giữ tách biệt nhưng có liên hệ.

---

## 4. Checklist chính thức – 48 mục

### IA-01 · Chuẩn UI chung (12 mục)

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên | Người tạo |
| --- | --- | --- | --- | --- | --- |
| GUI-01-01 | Layout, canh lề, typography và bảng màu nhất quán giữa các màn hình cùng loại (list, form, chi tiết) | Mở lần lượt vài màn hình cùng loại ở cả bốn nhóm A–D, so vị trí tiêu đề, khoảng cách, cỡ/kiểu chữ và màu | Norman – Consistency; Nielsen #4 | Cao | Phạm Anh Hào (GUI-01-001) |
| GUI-01-02 | Thuật ngữ, nhãn và thông báo dùng ngôn ngữ quen thuộc với người tổ chức/người tham dự sự kiện; không hiển thị tên trường cơ sở dữ liệu, mã trạng thái nội bộ hoặc thuật ngữ kỹ thuật khi không có giải thích | Rà tiêu đề, nhãn nút, badge, thông báo và dialog trên các màn hình; đặc biệt kiểm tra lỗi API, vai trò và trạng thái sự kiện/yêu cầu hỗ trợ | Nielsen #2 – Match between system and the real world; Norman – Mapping | Cao | Nguyễn Hồng Quân (ADD-01-001) |
| GUI-01-03 | Mỗi màn hình có thứ bậc thị giác rõ: tiêu đề, nội dung chính và hành động chính nổi bật; hành động phụ/phá huỷ không cạnh tranh với hành động chính; thông tin không liên quan hoặc lặp lại được lược bỏ | Quan sát màn hình ở kích thước desktop và mobile; xác định trong 5 giây mục đích trang và hành động chính, rồi kiểm tra các nội dung/nút trùng lặp hoặc gây nhiễu | Nielsen #8 – Aesthetic and minimalist design; Shneiderman #8 – Reduce short-term memory load | Cao | Nguyễn Hồng Quân (ADD-01-002) |
| GUI-01-04 | Thành phần tương tác thể hiện đúng khả năng sử dụng: nút, liên kết, vùng kéo-thả và hàng có thể mở chi tiết nhìn ra là có thể thao tác; nội dung tĩnh không tạo cảm giác có thể bấm; trạng thái disabled khác biệt rõ với trạng thái bình thường | Quan sát mà chưa bấm để dự đoán thành phần nào tương tác được, sau đó dùng chuột/bàn phím kiểm chứng; kiểm tra các nút disabled, vùng upload và hàng trong bảng | Norman – Affordance, Visibility; Nielsen #6 – Recognition rather than recall | Cao | Nguyễn Hồng Quân (ADD-01-003) |
| GUI-01-05 | Icon dùng cùng một ý nghĩa và cùng một hình dạng ở mọi nơi xuất hiện (icon xoá, sửa, export, thông báo… không đổi hình giữa các màn hình) | Liệt kê các icon lặp lại trên Events, Users, Support Requests, Dashboard; đối chiếu hình dạng và hành động gắn với từng icon | Nielsen #4; Norman – Signifiers | Trung bình | Lê Quang Phúc (GUI-01-002, bản bổ sung 16 mục) |
| GUI-01-06 | Cùng một dữ liệu nghiệp vụ được trình bày nhất quán về tên gọi, đơn vị, thứ tự, biểu tượng **và** định dạng ngày/giờ/số (dấu phân cách nghìn/thập phân, 12h/24h) giữa danh sách, trang chi tiết, form và file export | Chọn một Event/User/Support Request, đối chiếu cùng dữ liệu ở danh sách, chi tiết, form chỉnh sửa và file export; đặc biệt so sánh cùng một mốc thời gian hoặc con số (VD: thời gian sự kiện, số người đăng ký) hiển thị ở list, detail, vé QR và file Excel; ghi nhận mọi chỗ đổi tên, đổi đơn vị hoặc mâu thuẫn giá trị/định dạng | Nielsen #4 – Consistency and standards; Norman – Consistency, Mapping | Cao | Nguyễn Hồng Quân (ADD-01-004) + Lê Quang Phúc (GUI-01-008, đã gộp) |
| GUI-01-07 | Khi đổi EN ↔ VI, toàn bộ nhãn, thông báo lỗi và trạng thái đều được dịch, không tràn/vỡ layout, thuộc tính `lang` đổi theo, và ngày giờ/số được định dạng theo locale đang chọn một cách nhất quán trên mọi màn hình | Chuyển ngôn ngữ trên nhiều màn hình, rà chuỗi còn sót, kiểm tra tràn chữ và `lang`; đối chiếu cùng một mốc thời gian sự kiện hiển thị ở danh sách, trang chi tiết, vé và audit log ở cả hai ngôn ngữ | Nielsen #2; WCAG 3.1.2 | Cao | Phạm Anh Hào (GUI-01-003) |
| GUI-01-08 | Trạng thái rỗng và trạng thái đang tải hiển thị thông báo/placeholder có ý nghĩa (kèm gợi ý hành động), không để vùng trắng trơn | Lọc/tìm ra tập rỗng hoặc mở màn hình sau khi dữ liệu reset; tải chậm để quan sát loading | Nielsen #1 | Trung bình | Phạm Anh Hào (GUI-01-004) |
| GUI-01-09 | Mật độ thông tin và khoảng trắng hợp lý trên các màn hình nhiều dữ liệu (KPI Dashboard, bảng danh sách, panel cấu hình) — không chồng chữ, không chật đến mức khó phân biệt hàng/cột | Mở Dashboard và các bảng danh sách ở độ phân giải desktop chuẩn, kiểm tra khoảng cách dòng, cột, thẻ KPI có bị dính vào nhau không | Nielsen #8 (Aesthetic and minimalist design) | Trung bình | Lê Quang Phúc (GUI-01-005) |
| GUI-01-10 | Ở bề rộng màn hình hẹp (≈320–480 px), nội dung tự sắp xếp lại mà không phải cuộn ngang, bảng danh sách vẫn đọc được đủ thông tin, dialog nằm gọn trong khung nhìn và đóng được, mọi vùng chạm đạt kích thước tối thiểu | Thu cửa sổ về 320 px hoặc dùng chế độ thiết bị di động trên các danh sách Events/Users/Support, form Add/Edit Event và một dialog xác nhận; kiểm tra cuộn ngang, cách bảng thu gọn, nút đóng dialog và kích thước vùng chạm | WCAG 1.4.10; WCAG 2.5.5 | Cao | Phạm Anh Hào (GUI-01-006) |
| GUI-01-11 | Văn bản và thành phần giao diện đạt tỷ lệ tương phản tối thiểu so với nền, thứ tự heading đi liền mạch không nhảy cấp, và mọi nút chỉ có icon đều có tên trợ năng mô tả hành động | Dùng công cụ đo tương phản trên nhãn, badge, chữ trên nền màu; rà cây heading của vài trang bằng trình kiểm tra phần tử; kiểm tra từng nút icon (xoá, sửa, đóng lightbox, chuyển ngôn ngữ) xem có nhãn văn bản | WCAG 1.4.3; WCAG 1.3.1; WCAG 4.1.2 | Cao | Phạm Anh Hào (GUI-01-007) |
| GUI-01-12 | Tiêu đề tab trình duyệt, favicon và logo hiển thị đúng, nhất quán trên mọi màn hình, tiêu đề tab phản ánh đúng ngữ cảnh đang xem | Chuyển qua các màn hình khác nhau (Dashboard, Event detail, Support detail…), quan sát tiêu đề tab trình duyệt có đổi theo nội dung không | Nielsen #1; Shneiderman #1 | Thấp | Lê Quang Phúc (GUI-01-009) |

### IA-02 · Forms (13 mục)

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên | Người tạo |
| --- | --- | --- | --- | --- | --- |
| GUI-02-01 | Mọi trường bắt buộc được đánh dấu nhất quán bằng một quy ước duy nhất, và quy ước đó được giải thích | Rà toàn bộ trường trên nhiều form (Add/Edit Event, đăng ký, support), đối chiếu ký hiệu trường bắt buộc | Nielsen #4 | Cao | Phạm Anh Hào (GUI-02-001) |
| GUI-02-02 | Mọi input có nhãn nhìn thấy được và liên kết chương trình với trường (`<label for>` ↔ `id` duy nhất) | Dùng trình kiểm tra phần tử/đọc màn hình trên vài form, xác nhận từng input có label gắn đúng và id không trùng | WCAG 1.3.1; Nielsen #6 | Cao | Phạm Anh Hào (GUI-02-002) |
| GUI-02-03 | Lỗi validation hiện ngay cạnh trường sai, mô tả cụ thể và gợi ý cách sửa (không chỉ báo lỗi chung ở đầu form) | Bỏ trống/nhập sai từng trường (gồm ràng buộc ngày giờ chéo), quan sát vị trí và nội dung thông báo lỗi | Nielsen #9; Norman – Feedback | Cao | Phạm Anh Hào (GUI-02-003) |
| GUI-02-04 | Upload ảnh/file kiểm soát và truyền đạt ràng buộc (tỷ lệ 4:3 & 24:9, định dạng, dung lượng); từ chối file sai kèm thông báo rõ | Thử upload ảnh sai tỷ lệ, sai định dạng, quá dung lượng ở form Event và support; đọc thông báo trả về | Nielsen #5; Norman – Constraints | Cao | Phạm Anh Hào (GUI-02-004) |
| GUI-02-05 | Mọi điều khiển chọn giá trị (dropdown đơn/đa chọn, checkbox, radio, toggle, date-time picker, number input, textarea, rich-text editor, thang sao 1–5) thể hiện rõ giá trị đang chọn, thao tác được bằng bàn phím, và nạp lại đúng giá trị đã lưu khi mở lại ở chế độ Edit | Trên form Add/Edit Event, cấu hình đăng ký, form đăng ký và form đánh giá: đặt giá trị cho từng loại điều khiển bằng chuột rồi bằng bàn phím, lưu, mở lại bản ghi và đối chiếu giá trị hiển thị | Norman – Visibility; WCAG 2.1.1; Nielsen #6 | Cao | Phạm Anh Hào (GUI-02-005) |
| GUI-02-06 | Định dạng, giới hạn và ví dụ nhập liệu cần thiết được hiển thị **trước khi** người dùng nhập; placeholder chỉ là ví dụ, không thay thế nhãn hoặc hướng dẫn quan trọng | Kiểm tra các trường ngày giờ, Max Slots, Member Code, email, nội dung Rich-Text và attachment; đặt con trỏ/nhập thử để xem hướng dẫn có biến mất khiến người dùng phải nhớ hay không | Nielsen #5 – Error prevention; Nielsen #6 – Recognition rather than recall; Norman – Visibility, Constraints | Cao | Nguyễn Hồng Quân (ADD-02-001) |
| GUI-02-07 | Giá trị mặc định giúp giảm thao tác nhưng phải an toàn và phù hợp ngữ cảnh; hệ thống không tự chọn thay người dùng đối với vai trò, đồng ý/consent, publish, block, delete hoặc lựa chọn có hậu quả lớn | Mở form ở trạng thái tạo mới và chỉnh sửa; rà tất cả giá trị được điền/chọn sẵn, thử lưu mà không thay đổi rồi đánh giá hậu quả | Nielsen #5 – Error prevention; Shneiderman #5 – Prevent errors; Norman – Constraints | Cao | Nguyễn Hồng Quân (ADD-02-002) |
| GUI-02-08 | Các trường phụ thuộc nhau phản ánh ràng buộc ngay khi giá trị liên quan thay đổi: lựa chọn không hợp lệ bị ngăn hoặc vô hiệu hoá và có giải thích ngắn, thay vì chờ đến lúc Submit mới báo lỗi | Thay đổi cặp ngày bắt đầu/kết thúc, thời gian đăng ký/check-in, Max Slots/Waitlist và toggle vai trò; quan sát trường phụ thuộc, giá trị cũ và thông báo giải thích | Nielsen #5 – Error prevention; Norman – Constraints, Mapping, Feedback | Cao | Nguyễn Hồng Quân (ADD-02-003) |
| GUI-02-09 | Khi **chủ động** rời form còn thay đổi chưa lưu bằng Back, Cancel, menu, refresh hoặc đóng tab, hệ thống cảnh báo rõ và cho phép tiếp tục chỉnh sửa; chọn ở lại không được làm mất dữ liệu đã nhập | Sửa ít nhất hai trường nhưng chưa lưu, lần lượt thử Back, Cancel, đổi menu và refresh; kiểm tra dialog, nút "ở lại/rời đi" và nội dung form sau khi chọn ở lại | Nielsen #3 – User control and freedom; Shneiderman #6 – Permit easy reversal of actions | Cao | Nguyễn Hồng Quân (ADD-02-004) |
| GUI-02-10 | Toolbar rich-text editor (bold, italic, list, chèn ảnh/link) phản ánh đúng trạng thái vùng văn bản đang chọn, và nội dung định dạng được giữ nguyên sau khi lưu và tải lại | Bôi đen từng đoạn văn bản khác nhau trong mô tả sự kiện, áp định dạng, lưu, mở lại bản ghi và đối chiếu định dạng có còn đúng không | Norman – Feedback; Nielsen #1 | Cao | Lê Quang Phúc (GUI-02-006) |
| GUI-02-11 | Trường optional, trường disabled (do chưa đủ điều kiện) và trường readonly được phân biệt rõ bằng thị giác lẫn markup (`aria-disabled`, `readonly`), không chỉ đơn thuần "không bấm được" | Rà các form có trường điều kiện (VD: vai trò phụ chỉ bật khi chọn role tương ứng), kiểm tra bằng DOM/inspector và bằng mắt xem có phân biệt được optional/disabled/readonly | Nielsen #4; WCAG 4.1.2 | Trung bình | Lê Quang Phúc (GUI-02-007) |
| GUI-02-12 | Form dài (nhiều section: thumbnail, banner, rich-text, ngày giờ, registration…) được chia thành các phần có tiêu đề rõ ràng, giúp người dùng định vị đang ở phần nào khi cuộn | Mở form Add/Edit Event, cuộn qua toàn bộ chiều dài form, kiểm tra mỗi section có heading/label phân tách rõ, không bị trộn lẫn giữa các nhóm trường khác nhau | Nielsen #6 – Recognition rather than recall; Norman – Mapping | Trung bình | Lê Quang Phúc (GUI-02-008, đã rút gọn — xem Nhật ký gộp §3) |
| GUI-02-13 | Dữ liệu đang nhập dở không bị mất khi **bị động** gặp sự cố: tải lại trang do lỗi mạng tạm thời hoặc chuyển tab rồi quay lại (autosave/draft hoặc khôi phục được nội dung) | Nhập dở form Add/Edit Event hoặc form support request, chuyển tab/reload trong thời gian ngắn, quay lại kiểm tra dữ liệu còn hay mất | Nielsen #5; Norman – User control | Trung bình | Lê Quang Phúc (GUI-02-009) |

### IA-03 · Navigation (12 mục)

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên | Người tạo |
| --- | --- | --- | --- | --- | --- |
| GUI-03-01 | Breadcrumb/nút back/return đưa về đúng màn hình cha, và deep link tới chi tiết mở đúng đối tượng | Đi sâu vào chi tiết (event, user, request) rồi back; mở trực tiếp một deep link và đối chiếu đối tượng | Nielsen #3; Shneiderman #3 | Trung bình | Phạm Anh Hào (GUI-03-001) |
| GUI-03-02 | Điều hướng bàn phím hoạt động: thứ tự tab hợp lý theo dòng đọc, viền focus nhìn thấy được, Esc đóng dialog, focus không thoát khỏi dialog đang mở | Chỉ dùng Tab/Shift-Tab/Esc duyệt form và dialog, quan sát vòng focus và viền focus | WCAG 2.4.7; WCAG 2.1.2; Shneiderman #3 | Cao | Phạm Anh Hào (GUI-03-002) |
| GUI-03-03 | Cấu trúc điều hướng (sidebar/menu/tab) đồng nhất và giữ nguyên vị trí khi chuyển giữa các khu vực, phản ánh đúng phân quyền đang đăng nhập | Đăng nhập bằng các vai trò khác nhau, chuyển khu vực, kiểm tra menu ổn định và chỉ hiện mục được phép | Nielsen #4; Norman – Mapping | Trung bình | Phạm Anh Hào (GUI-03-003) |
| GUI-03-04 | Vị trí đang đứng được hiển thị rõ: mục menu/tab tương ứng được đánh dấu active và tiêu đề trang khớp nhãn menu | Duyệt từng mục menu/tab, kiểm tra highlight active và đối chiếu tiêu đề trang với nhãn | Nielsen #1; Shneiderman #1 | Cao | Phạm Anh Hào (GUI-03-004) |
| GUI-03-05 | Mọi danh sách/bảng hiển thị rõ tiêu chí tìm kiếm và bộ lọc đang áp dụng cùng tổng số kết quả, phân trang cho biết trang hiện tại trên tổng số trang, và bộ tiêu chí này được giữ nguyên khi quay lại từ màn hình chi tiết | Trên các danh sách Events / Users / Support Requests: nhập từ khoá, chọn bộ lọc, sang trang 2, mở một bản ghi rồi bấm back → kiểm tra chip/nhãn tiêu chí, số kết quả, chỉ báo trang và trạng thái sau khi quay lại | Nielsen #1; Shneiderman #3 | Cao | Phạm Anh Hào (GUI-03-005) |
| GUI-03-06 | Các chức năng được nhóm và đặt tên theo mục tiêu của người dùng, không theo cấu trúc kỹ thuật của hệ thống; những chức năng liên quan nằm gần nhau và các nhóm khác nhau được phân tách rõ | Nhờ người chưa quen EMS chỉ vị trí để tạo sự kiện, đăng ký, lấy QR, quản lý user hoặc xử lý support mà không hướng dẫn; ghi nhận mục bị tìm sai hoặc nhãn gây hiểu nhầm | Nielsen #2 – Match between system and the real world; Nielsen #6 – Recognition rather than recall; Norman – Mapping | Cao | Nguyễn Hồng Quân (ADD-03-001) |
| GUI-03-07 | Tác vụ thường xuyên có đường đi hiệu quả cho người dùng thành thạo (VD: hành động trực tiếp trên từng hàng, thao tác hàng loạt hoặc phím tắt khi phù hợp) nhưng không làm rối luồng cơ bản của người mới | So bước để thực hiện cùng một tác vụ lặp lại trên nhiều bản ghi; kiểm tra hành động nhanh có dễ tìm, có nhãn rõ và không buộc người mới phải học phím tắt hay không | Nielsen #7 – Flexibility and efficiency of use; Shneiderman #2 – Enable frequent users to use shortcuts | Trung bình | Nguyễn Hồng Quân (ADD-03-002) |
| GUI-03-08 | Màn hình từ chối truy cập (do không đủ quyền) hoặc báo tài nguyên không còn khả dụng (đã xoá/hết hạn chia sẻ/deep link vượt quyền) không trở thành "ngõ cụt": hệ thống giải thích ngắn gọn tình trạng và cung cấp đường điều hướng hợp lệ về khu vực người dùng có quyền truy cập, không buộc họ chỉ dựa vào nút Back của trình duyệt | Đăng nhập bằng tài khoản không phải admin, dán trực tiếp URL của một trang quản trị (VD: danh sách Users) vào thanh địa chỉ; đồng thời truy cập deep link tới bản ghi đã xoá/không còn chia sẻ và dùng liên kết đã hết hiệu lực; kiểm tra thông báo cùng CTA về danh sách, dashboard hoặc khu vực an toàn phù hợp | Nielsen #3 – User control and freedom; Nielsen #9 – Help users recognize, diagnose, and recover from errors; Norman – Mapping | Cao | Nguyễn Hồng Quân (ADD-03-003) + Lê Quang Phúc (GUI-03-008, đã gộp) |
| GUI-03-09 | Điều khiển tuân theo quy ước Web: liên kết dùng để chuyển trang, nút dùng để thực hiện hành động; đích mở tab/cửa sổ mới được báo trước; Back không tự gửi lại form hay lặp lại hành động đã hoàn tất | Duyệt các liên kết, nút icon, Preview, Export và liên kết ngoài; mở đích rồi dùng Back/Forward để kiểm tra có điều hướng bất ngờ, submit lại hoặc tạo bản ghi trùng không | Nielsen #4 – Consistency and standards; Norman – Affordance, Consistency | Cao | Nguyễn Hồng Quân (ADD-03-004) |
| GUI-03-10 | Kéo-thả sắp xếp lại (VD: thứ tự vai trò phụ trong cấu hình đăng ký) có phản hồi thị giác rõ trong lúc kéo, và thứ tự mới được giữ nguyên sau khi lưu/tải lại | Kéo-thả để đổi thứ tự trong panel cấu hình vai trò phụ, quan sát chỉ báo vị trí thả trong lúc kéo, lưu rồi tải lại trang để đối chiếu thứ tự | Norman – Feedback/Visibility; WCAG 2.5.1 | Trung bình | Lê Quang Phúc (GUI-03-006) |
| GUI-03-11 | Ô tìm kiếm, bộ lọc và nút sắp xếp trên các danh sách thao tác được hoàn toàn bằng bàn phím và có nhãn cho trình đọc màn hình, không chỉ dùng được bằng chuột | Dùng Tab/Enter/phím mũi tên để nhập từ khoá tìm kiếm, mở dropdown lọc, chọn tiêu chí sắp xếp trên danh sách Events/Users/Support mà không chạm chuột | WCAG 2.1.1; WCAG 4.1.2 | Cao | Lê Quang Phúc (GUI-03-007) |
| GUI-03-12 | Trạng thái đóng/mở của sidebar (nếu có thể thu gọn) được giữ nguyên khi điều hướng giữa các trang trong cùng phiên làm việc | Thu gọn sidebar, chuyển qua vài trang khác nhau trong cùng phiên đăng nhập, kiểm tra sidebar có tự bung lại không | Nielsen #4; Norman – Mapping | Thấp | Lê Quang Phúc (GUI-03-009) |

### IA-04 · Feedback / State (11 mục)

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên | Người tạo |
| --- | --- | --- | --- | --- | --- |
| GUI-04-01 | Mọi hành động phá huỷ/khó hồi phục (xoá, chặn, reset, huỷ đăng ký) đều có dialog xác nhận nêu rõ đối tượng bị tác động | Bấm xoá/chặn/reset/huỷ, đọc dialog xem có nêu tên đối tượng cụ thể và cho phép huỷ thao tác | Shneiderman #6; Nielsen #3 | Cao | Phạm Anh Hào (GUI-04-001) |
| GUI-04-02 | Mọi hành động của người dùng đều có phản hồi tức thời (toast/loading/đổi trạng thái) xác nhận thành công hoặc thất bại | Thực hiện lưu/publish/đăng ký/gửi request và các thao tác dài (Export Excel, Preview), quan sát có phản hồi trong thời gian hợp lý | Nielsen #1; Norman – Feedback; Shneiderman #3 | Cao | Phạm Anh Hào (GUI-04-002) |
| GUI-04-03 | Trạng thái (Draft/Published, Registered/Pending/Confirmed/Waitlisted…) được thể hiện bằng nhãn chữ kèm màu, không chỉ dựa vào màu, và cùng một trạng thái luôn dùng cùng một màu/nhãn toàn hệ thống | Đối chiếu badge trạng thái ở các màn hình khác nhau; kiểm tra mọi badge có nhãn chữ và ánh xạ màu–trạng thái nhất quán | WCAG 1.4.1; Norman – Consistency | Trung bình | Phạm Anh Hào (GUI-04-003) |
| GUI-04-04 | Mọi thành phần truyền tin không bằng văn bản hoặc tự thay đổi (KPI card, progress bar, carousel, barcode/QR, lightbox ảnh, audit log, notification dot, cập nhật real-time) đều có nhãn/văn bản thay thế nêu rõ ý nghĩa và giá trị, cho phép dừng hoặc điều khiển nội dung tự chạy, và phản ánh dữ liệu mới mà không cần tải lại thủ công | Mở dashboard, trang chủ có carousel, vé QR, lightbox ảnh trong support request và audit log: kiểm tra alt/nhãn kèm giá trị (`Đã đăng ký / tối đa`, % tiến trình, số thông báo), thử dừng carousel, tạo thay đổi ở tab khác để xem dữ liệu/chấm thông báo tự cập nhật | WCAG 1.1.1; WCAG 2.2.2; Nielsen #1; Norman – Feedback | Trung bình | Phạm Anh Hào (GUI-04-004) |
| GUI-04-05 | Khi mất mạng, hết phiên đăng nhập hoặc tải dữ liệu thất bại, hệ thống báo bằng ngôn ngữ người dùng đang chọn, nêu rõ cách khắc phục (thử lại / đăng nhập lại), không hiển thị mã lỗi thô, và không làm mất dữ liệu người dùng đang nhập dở | Ngắt mạng giữa lúc lưu form nhiều section; để phiên hết hạn rồi bấm một hành động; chặn một request tải danh sách → quan sát thông báo, tuỳ chọn thử lại và nội dung form sau khi lỗi | Nielsen #9; Shneiderman #5; Norman – Feedback | Cao | Phạm Anh Hào (GUI-04-005) |
| GUI-04-06 | Trong lúc Submit hoặc xử lý yêu cầu, điều khiển gây hành động lặp được khoá hoặc chống gửi trùng nhưng vẫn thể hiện rõ đang xử lý; bấm nhanh nhiều lần không tạo nhiều event, đăng ký, support request hoặc phản hồi giống nhau; với các hành động có progress bar/spinner riêng (Export, Publish), progress hiển thị đúng tiến trình và nút vẫn khoá cho tới khi xử lý xong | Làm chậm mạng rồi nhấp đúp/nhấn Enter nhiều lần vào Save, Register, Send Request và Respond; kiểm tra trạng thái nút và số bản ghi được tạo; quan sát progress bar/spinner của Export/Publish có phản ánh đúng tiến trình không | Nielsen #5 – Error prevention; Norman – Feedback, Constraints; Shneiderman #5 – Prevent errors | Cao | Nguyễn Hồng Quân (ADD-04-001) |
| GUI-04-07 | Khi phản hồi được trình bày bằng toast/banner tạm thời, thông báo được xếp theo mức quan trọng, không che nội dung hoặc điều khiển thiết yếu, tồn tại đủ lâu để đọc, có thể đóng khi cần và không xuất hiện nhiều bản trùng cho cùng một sự kiện | Kích hoạt nhiều toast/banner thành công, cảnh báo và lỗi liên tiếp ở viewport desktop/mobile; kiểm tra thứ tự xếp chồng, thời gian hiển thị, khả năng đóng và tiếp tục thao tác, phần nội dung bị che và số thông báo sinh ra cho một sự kiện | Nielsen #8 – Aesthetic and minimalist design; Nielsen #3 – User control and freedom; Shneiderman #1 – Strive for consistency | Trung bình | Nguyễn Hồng Quân (ADD-04-002) |
| GUI-04-08 | Hành động có thể đảo ngược cung cấp Undo, Restore hoặc đường khôi phục rõ ràng trong khoảng thời gian hợp lý; dialog xác nhận không phải cơ chế bảo vệ duy nhất khi việc khôi phục khả thi | Thử thay đổi trạng thái, bỏ duyệt, xoá nháp hoặc huỷ đăng ký; tìm Undo/Restore và xác nhận dữ liệu/trạng thái được phục hồi đúng | Nielsen #3 – User control and freedom; Shneiderman #6 – Permit easy reversal of actions | Cao | Nguyễn Hồng Quân (ADD-04-003) |
| GUI-04-09 | Khi hoàn tất một quy trình nhiều bước, hệ thống tạo cảm giác kết thúc rõ ràng bằng bản tóm tắt kết quả/đối tượng, mã hoặc trạng thái mới và hành động tiếp theo phù hợp; người dùng không phải đoán quy trình đã xong hay chưa | Hoàn tất tạo/publish event, đăng ký tham dự và gửi/giải quyết support request; kiểm tra trang hoặc dialog kết quả, định danh bản ghi, trạng thái và CTA tiếp theo | Shneiderman #4 – Design dialogs to yield closure; Nielsen #1 – Visibility of system status; Norman – Feedback | Cao | Nguyễn Hồng Quân (ADD-04-004) |
| GUI-04-10 | Dữ liệu cập nhật real-time (log check-in, chấm thông báo, audit log) chèn thêm mục mới mà không làm nhảy vị trí cuộn hoặc mất focus người dùng đang thao tác | Mở tab Check-in hoặc audit log, tạo một sự kiện cập nhật từ tab/thiết bị khác, quan sát vị trí cuộn và focus hiện tại có bị xáo trộn không | Nielsen #1; WCAG 2.2.2 | Trung bình | Lê Quang Phúc (GUI-04-006) |
| GUI-04-11 | Các lớp overlay (lightbox ảnh trong support request, vé QR, dialog xác nhận) đều đóng được nhất quán bằng Esc, click ra ngoài và nút đóng (X) — không lớp nào thiếu một trong ba cách | Mở lần lượt lightbox ảnh, vé QR/barcode, dialog xác nhận; thử đóng bằng cả ba cách trên từng overlay | Shneiderman #3 (Consistency); liên hệ GUI-03-02 | Trung bình | Lê Quang Phúc (GUI-04-009) |

---

## 5. Nguồn tham khảo tổng hợp

| Nguồn | Dùng cho các mục |
| --- | --- |
| Nielsen, J. – *10 Usability Heuristics for User Interface Design* | GUI-01-01, 01-02, 01-03, 01-04, 01-06, 01-07, 01-08, 01-10, 01-11, 01-12, 02-01, 02-02, 02-03, 02-04, 02-05, 02-06, 02-07, 02-08, 02-09, 02-10, 02-11, 02-12, 02-13, 03-01, 03-03, 03-04, 03-05, 03-06, 03-07, 03-08, 03-09, 03-12, 04-01, 04-02, 04-04, 04-05, 04-06, 04-07, 04-08, 04-09, 04-10 |
| Norman, D. – *The Design of Everyday Things* (6 nguyên tắc: Visibility, Feedback, Affordance, Mapping, Constraints, Consistency) | GUI-01-01, 01-02, 01-04, 01-06, 02-03, 02-04, 02-05, 02-06, 02-07, 02-08, 02-13, 03-03, 03-06, 03-08, 03-09, 03-10, 03-12, 04-02, 04-03, 04-04, 04-05, 04-06, 04-09 |
| Shneiderman, B. – *Eight Golden Rules of Interface Design* | GUI-01-03, 01-12, 03-01, 03-02, 03-04, 03-05, 03-07, 03-09, 04-01, 04-02, 04-05, 04-06, 04-07, 04-08, 04-09, 04-11 |
| W3C – *WCAG 2.1* | GUI-01-07, 01-10, 01-11, 02-02, 02-05, 02-11, 03-02, 03-10, 03-11, 04-03, 04-04, 04-10 |
| ISTQB Foundation Level Syllabus | Thuật ngữ và khái niệm kiểm thử chung |
| Slide môn học – *GUI + Usability + Compatibility Testing (AI-First, Combined)* | Khung bốn interface aspect IA-01…IA-04 |

---

## 6. Mẫu bảng ghi kết quả (Task 1B)

Mỗi thành viên tự thay ba (hoặc hơn) cột màn hình bằng đúng phạm vi kịch bản mình phụ trách. Bảng dưới dùng **toàn bộ 48 ID chính thức** — copy nguyên bảng này, chỉ đổi tiêu đề ba cột màn hình.

| ID | Mục kiểm tra (rút gọn) | Màn hình 1 | Màn hình 2 | Màn hình 3 | Notes |
| --- | --- | --- | --- | --- | --- |
| GUI-01-01 | Layout/typography/màu nhất quán | | | | |
| GUI-01-02 | Thuật ngữ quen thuộc, không lộ mã kỹ thuật | | | | |
| GUI-01-03 | Thứ bậc thị giác, nội dung tối giản | | | | |
| GUI-01-04 | Affordance rõ, disabled khác biệt | | | | |
| GUI-01-05 | Icon nhất quán ý nghĩa | | | | |
| GUI-01-06 | Dữ liệu nghiệp vụ + định dạng ngày/giờ/số nhất quán | | | | |
| GUI-01-07 | i18n EN/VI đầy đủ, đúng locale | | | | |
| GUI-01-08 | Empty/loading state có ý nghĩa | | | | |
| GUI-01-09 | Mật độ thông tin/khoảng trắng hợp lý | | | | |
| GUI-01-10 | Responsive 320–480 px | | | | |
| GUI-01-11 | Tương phản, heading, nhãn nút icon | | | | |
| GUI-01-12 | Tab title, favicon, logo nhất quán | | | | |
| GUI-02-01 | Quy ước trường bắt buộc nhất quán | | | | |
| GUI-02-02 | Input có nhãn, label–id liên kết | | | | |
| GUI-02-03 | Lỗi validation cạnh trường, cụ thể | | | | |
| GUI-02-04 | Upload kiểm soát & truyền đạt ràng buộc | | | | |
| GUI-02-05 | Điều khiển chọn giá trị rõ, nạp lại đúng | | | | |
| GUI-02-06 | Định dạng/giới hạn hiển thị trước khi nhập | | | | |
| GUI-02-07 | Giá trị mặc định an toàn | | | | |
| GUI-02-08 | Ràng buộc chéo giữa các trường phản ánh tức thời | | | | |
| GUI-02-09 | Cảnh báo rời form khi có thay đổi chưa lưu | | | | |
| GUI-02-10 | Toolbar rich-text phản ánh đúng trạng thái | | | | |
| GUI-02-11 | Phân biệt optional/disabled/readonly | | | | |
| GUI-02-12 | Form dài chia section có tiêu đề rõ | | | | |
| GUI-02-13 | Không mất dữ liệu khi reload/chuyển tab | | | | |
| GUI-03-01 | Breadcrumb/back/deep link đúng đích | | | | |
| GUI-03-02 | Điều hướng bàn phím, focus, Esc | | | | |
| GUI-03-03 | Cấu trúc điều hướng ổn định theo phân quyền | | | | |
| GUI-03-04 | Đánh dấu vị trí đang đứng | | | | |
| GUI-03-05 | Trạng thái tìm kiếm/lọc/phân trang được giữ | | | | |
| GUI-03-06 | Chức năng nhóm theo mục tiêu người dùng | | | | |
| GUI-03-07 | Đường tắt cho tác vụ thường xuyên | | | | |
| GUI-03-08 | Từ chối truy cập/tài nguyên không khả dụng không tạo ngõ cụt | | | | |
| GUI-03-09 | Link/button đúng quy ước, Back không resubmit | | | | |
| GUI-03-10 | Kéo-thả reorder có phản hồi và bền vững | | | | |
| GUI-03-11 | Tìm kiếm/lọc/sắp xếp dùng được bằng bàn phím | | | | |
| GUI-03-12 | Trạng thái sidebar giữ nguyên khi điều hướng | | | | |
| GUI-04-01 | Dialog xác nhận cho hành động phá huỷ | | | | |
| GUI-04-02 | Phản hồi tức thời cho mọi hành động | | | | |
| GUI-04-03 | Badge trạng thái có chữ, màu nhất quán | | | | |
| GUI-04-04 | Thành phần phi văn bản có nhãn thay thế | | | | |
| GUI-04-05 | Xử lý lỗi hệ thống, không mất dữ liệu đang nhập | | | | |
| GUI-04-06 | Chống gửi trùng khi đang xử lý | | | | |
| GUI-04-07 | Toast/banner không che, đóng được, không trùng | | | | |
| GUI-04-08 | Có Undo/Restore khi khả thi | | | | |
| GUI-04-09 | Quy trình kết thúc rõ ràng (closure) | | | | |
| GUI-04-10 | Cập nhật real-time không phá scroll/focus | | | | |
| GUI-04-11 | Overlay đóng nhất quán (Esc/click-outside/X) | | | | |

**Quy ước điền:** `P` = Passed · `F` = Failed (bắt buộc kèm Notes + ảnh) · `N/A` = không áp dụng (bắt buộc kèm lý do)

---