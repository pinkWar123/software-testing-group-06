# Checklist Kiểm thử GUI — EMS

**Bản đóng góp cá nhân · 16 mục bổ sung · phiên bản v1**

| | |
| --- | --- |
| **Người đóng góp** | `[Nguyễn Hồng Quân — 22127345]` |
| **Kịch bản phụ trách** | B — User registers to attend an event |
| **Màn hình đã nhận** | B1 · Home / events listing; B2 · Event detail page; B3 · Registration form |
| **Ngày** | 28/07/2026 |
| **Trạng thái** | Chờ người đóng góp rà soát thực tế và gộp vào checklist chung |
| **Phân bổ IA** | IA-01 = 4 · IA-02 = 4 · IA-03 = 4 · IA-04 = 4 |

---

## 1. Mục đích

Đây là phần đóng góp **16 mục mới** để gộp với 20 mục trong
`EMS_GUI_Checklist_Share.md`. Các mục được xây dựng từ:

- Nielsen — *10 Usability Heuristics for User Interface Design*;
- Norman — *6 nguyên tắc thiết kế*: Visibility, Feedback, Affordance,
  Mapping, Constraints và Consistency;
- Shneiderman — *8 Golden Rules of Interface Design*.

Mỗi mục được viết thành một điều kiện có thể quan sát và đánh dấu
**Passed / Failed / N/A**. ID dùng tiền tố `ADD` để không trùng với dãy `GUI`
của file hiện tại; nhóm có thể đánh số lại sau khi gộp.

---

## 2. Checklist — 16 mục bổ sung

### IA-01 · Chuẩn UI chung

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên |
| --- | --- | --- | --- | --- |
| **ADD-01-001** | Thuật ngữ, nhãn và thông báo dùng ngôn ngữ quen thuộc với người tổ chức/người tham dự sự kiện; không hiển thị tên trường cơ sở dữ liệu, mã trạng thái nội bộ hoặc thuật ngữ kỹ thuật khi không có giải thích | Rà tiêu đề, nhãn nút, badge, thông báo và dialog trên các màn hình; đặc biệt kiểm tra lỗi API, vai trò và trạng thái sự kiện/yêu cầu hỗ trợ | Nielsen #2 — Match between system and the real world; Norman — Mapping | Cao |
| **ADD-01-002** | Mỗi màn hình có thứ bậc thị giác rõ: tiêu đề, nội dung chính và hành động chính nổi bật; hành động phụ/phá huỷ không cạnh tranh với hành động chính; thông tin không liên quan hoặc lặp lại được lược bỏ | Quan sát màn hình ở kích thước desktop và mobile; xác định trong 5 giây mục đích trang và hành động chính, rồi kiểm tra các nội dung/nút trùng lặp hoặc gây nhiễu | Nielsen #8 — Aesthetic and minimalist design; Shneiderman #8 — Reduce short-term memory load | Cao |
| **ADD-01-003** | Thành phần tương tác thể hiện đúng khả năng sử dụng: nút, liên kết, vùng kéo-thả và hàng có thể mở chi tiết nhìn ra là có thể thao tác; nội dung tĩnh không tạo cảm giác có thể bấm; trạng thái disabled khác biệt rõ với trạng thái bình thường | Quan sát mà chưa bấm để dự đoán thành phần nào tương tác được, sau đó dùng chuột/bàn phím kiểm chứng; kiểm tra các nút disabled, vùng upload và hàng trong bảng | Norman — Affordance, Visibility; Nielsen #6 — Recognition rather than recall | Cao |
| **ADD-01-004** | Cùng một dữ liệu nghiệp vụ được trình bày nhất quán về tên gọi, đơn vị, thứ tự và biểu tượng ở danh sách, trang chi tiết, form và file export (ví dụ: ngày giờ, số chỗ, vai trò, trạng thái) | Chọn một Event/User/Support Request, đối chiếu cùng dữ liệu ở danh sách, chi tiết, form chỉnh sửa và file export; ghi nhận mọi chỗ đổi tên, đổi đơn vị hoặc mâu thuẫn giá trị | Nielsen #4 — Consistency and standards; Norman — Consistency | Cao |

### IA-02 · Forms

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên |
| --- | --- | --- | --- | --- |
| **ADD-02-001** | Định dạng, giới hạn và ví dụ nhập liệu cần thiết được hiển thị **trước khi** người dùng nhập; placeholder chỉ là ví dụ, không thay thế nhãn hoặc hướng dẫn quan trọng | Kiểm tra các trường ngày giờ, Max Slots, Member Code, email, nội dung Rich-Text và attachment; đặt con trỏ/nhập thử để xem hướng dẫn có biến mất khiến người dùng phải nhớ hay không | Nielsen #5 — Error prevention; Nielsen #6 — Recognition rather than recall; Norman — Visibility, Constraints | Cao |
| **ADD-02-002** | Giá trị mặc định giúp giảm thao tác nhưng phải an toàn và phù hợp ngữ cảnh; hệ thống không tự chọn thay người dùng đối với vai trò, đồng ý/consent, publish, block, delete hoặc lựa chọn có hậu quả lớn | Mở form ở trạng thái tạo mới và chỉnh sửa; rà tất cả giá trị được điền/chọn sẵn, thử lưu mà không thay đổi rồi đánh giá hậu quả | Nielsen #5 — Error prevention; Shneiderman #5 — Prevent errors; Norman — Constraints | Cao |
| **ADD-02-003** | Các trường phụ thuộc nhau phản ánh ràng buộc ngay khi giá trị liên quan thay đổi: lựa chọn không hợp lệ bị ngăn hoặc vô hiệu hoá và có giải thích ngắn, thay vì chờ đến lúc Submit mới báo lỗi | Thay đổi cặp ngày bắt đầu/kết thúc, thời gian đăng ký/check-in, Max Slots/Waitlist và toggle vai trò; quan sát trường phụ thuộc, giá trị cũ và thông báo giải thích | Nielsen #5 — Error prevention; Norman — Constraints, Mapping, Feedback | Cao |
| **ADD-02-004** | Khi rời form còn thay đổi chưa lưu bằng Back, Cancel, menu, refresh hoặc đóng tab, hệ thống cảnh báo rõ và cho phép tiếp tục chỉnh sửa; chọn ở lại không được làm mất dữ liệu đã nhập | Sửa ít nhất hai trường nhưng chưa lưu, lần lượt thử Back, Cancel, đổi menu và refresh; kiểm tra dialog, nút “Ở lại/Rời đi” và nội dung form sau khi chọn ở lại | Nielsen #3 — User control and freedom; Shneiderman #6 — Permit easy reversal of actions | Cao |

### IA-03 · Navigation

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên |
| --- | --- | --- | --- | --- |
| **ADD-03-001** | Các chức năng được nhóm và đặt tên theo mục tiêu của người dùng, không theo cấu trúc kỹ thuật của hệ thống; những chức năng liên quan nằm gần nhau và các nhóm khác nhau được phân tách rõ | Nhờ người chưa quen EMS chỉ vị trí để tạo sự kiện, đăng ký, lấy QR, quản lý user hoặc xử lý support mà không hướng dẫn; ghi nhận mục bị tìm sai hoặc nhãn gây hiểu nhầm | Nielsen #2 — Match between system and the real world; Nielsen #6 — Recognition rather than recall; Norman — Mapping | Cao |
| **ADD-03-002** | Tác vụ thường xuyên có đường đi hiệu quả cho người dùng thành thạo (ví dụ: hành động trực tiếp trên từng hàng, thao tác hàng loạt hoặc phím tắt khi phù hợp) nhưng không làm rối luồng cơ bản của người mới | So số bước để thực hiện cùng một tác vụ lặp lại trên nhiều bản ghi; kiểm tra hành động nhanh có dễ tìm, có nhãn rõ và không buộc người mới phải học phím tắt hay không | Nielsen #7 — Flexibility and efficiency of use; Shneiderman #2 — Enable frequent users to use shortcuts | Trung bình |
| **ADD-03-003** | Màn hình từ chối truy cập hoặc báo tài nguyên không còn khả dụng không trở thành “ngõ cụt”: hệ thống giải thích ngắn gọn tình trạng và cung cấp đường điều hướng hợp lệ về khu vực người dùng có quyền truy cập, không buộc họ chỉ dựa vào nút Back của trình duyệt | Mở URL bằng tài khoản không đủ quyền, truy cập deep link tới bản ghi đã xoá/không còn được chia sẻ và dùng liên kết đã hết hiệu lực; kiểm tra thông báo cùng CTA về danh sách, dashboard hoặc khu vực an toàn phù hợp | Nielsen #3 — User control and freedom; Nielsen #9 — Help users recognize, diagnose, and recover from errors; Norman — Mapping | Cao |
| **ADD-03-004** | Điều khiển tuân theo quy ước Web: liên kết dùng để chuyển trang, nút dùng để thực hiện hành động; đích mở tab/cửa sổ mới được báo trước; Back không tự gửi lại form hay lặp lại hành động đã hoàn tất | Duyệt các liên kết, nút icon, Preview, Export và liên kết ngoài; mở đích rồi dùng Back/Forward để kiểm tra có điều hướng bất ngờ, submit lại hoặc tạo bản ghi trùng không | Nielsen #4 — Consistency and standards; Norman — Affordance, Consistency | Cao |

### IA-04 · Feedback / State

| ID | Mục kiểm tra | Cách kiểm chứng | Nguồn | Ưu tiên |
| --- | --- | --- | --- | --- |
| **ADD-04-001** | Trong lúc Submit hoặc xử lý yêu cầu, điều khiển gây hành động lặp được khoá hoặc chống gửi trùng nhưng vẫn thể hiện rõ đang xử lý; bấm nhanh nhiều lần không tạo nhiều event, đăng ký, support request hoặc phản hồi giống nhau | Làm chậm mạng rồi nhấp đúp/nhấn Enter nhiều lần vào Save, Register, Send Request và Respond; kiểm tra trạng thái nút và số bản ghi được tạo | Nielsen #5 — Error prevention; Norman — Feedback, Constraints; Shneiderman #5 — Prevent errors | Cao |
| **ADD-04-002** | Khi phản hồi được trình bày bằng toast/banner tạm thời, thông báo được xếp theo mức quan trọng, không che nội dung hoặc điều khiển thiết yếu, tồn tại đủ lâu để đọc, có thể đóng khi cần và không xuất hiện nhiều bản trùng cho cùng một sự kiện | Kích hoạt nhiều toast/banner thành công, cảnh báo và lỗi liên tiếp ở viewport desktop/mobile; kiểm tra thứ tự xếp chồng, thời gian hiển thị, khả năng đóng và tiếp tục thao tác, phần nội dung bị che và số thông báo sinh ra cho một sự kiện | Nielsen #8 — Aesthetic and minimalist design; Nielsen #3 — User control and freedom; Shneiderman #1 — Strive for consistency | Trung bình |
| **ADD-04-003** | Hành động có thể đảo ngược cung cấp Undo, Restore hoặc đường khôi phục rõ ràng trong khoảng thời gian hợp lý; dialog xác nhận không phải cơ chế bảo vệ duy nhất khi việc khôi phục khả thi | Thử thay đổi trạng thái, bỏ duyệt, xoá nháp hoặc huỷ đăng ký; tìm Undo/Restore và xác nhận dữ liệu/trạng thái được phục hồi đúng | Nielsen #3 — User control and freedom; Shneiderman #6 — Permit easy reversal of actions | Cao |
| **ADD-04-004** | Khi hoàn tất một quy trình nhiều bước, hệ thống tạo cảm giác kết thúc rõ ràng bằng bản tóm tắt kết quả/đối tượng, mã hoặc trạng thái mới và hành động tiếp theo phù hợp; người dùng không phải đoán quy trình đã xong hay chưa | Hoàn tất tạo/publish event, đăng ký tham dự và gửi/giải quyết support request; kiểm tra trang hoặc dialog kết quả, định danh bản ghi, trạng thái và CTA tiếp theo | Shneiderman #4 — Design dialogs to yield closure; Nielsen #1 — Visibility of system status; Norman — Feedback | Cao |

---

## 3. Đối chiếu tránh trùng với 20 mục hiện tại

| Nhóm nội dung đã có trong `EMS_GUI_Checklist_Share.md` | Cách phần bổ sung này tránh lặp |
| --- | --- |
| Nhất quán layout, typography và màu | `ADD-01-004` kiểm **tính nhất quán ngữ nghĩa của dữ liệu** giữa list/detail/form/export, không kiểm style |
| Label, required marker và validation cạnh trường | `ADD-02-001` kiểm **hướng dẫn/định dạng trước khi nhập**; `ADD-02-002` kiểm **giá trị mặc định**; `ADD-02-003` kiểm **phụ thuộc động giữa các trường** |
| Back/breadcrumb/deep link và giữ bộ lọc | `ADD-03-001` kiểm **kiến trúc thông tin theo mục tiêu**; `ADD-03-003` kiểm **ngõ cụt**; `ADD-03-004` kiểm **ngữ nghĩa link/button và lịch sử trình duyệt** |
| Dialog xác nhận hành động phá huỷ | `ADD-04-003` yêu cầu **khả năng hoàn tác/khôi phục sau hành động**, không chỉ xác nhận trước hành động |
| Toast/loading và phản hồi tức thời | `ADD-04-001` kiểm **chống gửi trùng**; `ADD-04-002` kiểm **khả năng đọc/đóng và mức ưu tiên thông báo**; `ADD-04-004` kiểm **closure của toàn bộ quy trình** |
| Lỗi hệ thống không làm mất dữ liệu | `ADD-02-004` kiểm trường hợp **người dùng chủ động rời form khi có thay đổi chưa lưu**, không phải lỗi mạng/hết phiên |

---

## 4. Nguồn tham khảo

1. Nielsen, J. (2024). [*10 Usability Heuristics for User Interface
   Design*](https://www.nngroup.com/articles/ten-usability-heuristics/).
   Nielsen Norman Group.
2. Norman, D. A. (2013). [*The Design of Everyday Things — Revised and
   Expanded Edition*](https://books.google.com/books/about/The_Design_of_Everyday_Things.html?id=FUdJwAEACAAJ).
   Basic Books. Các nguyên tắc dùng trong bảng: Visibility, Feedback,
   Affordance, Mapping, Constraints và Consistency.
3. Shneiderman, B., Plaisant, C., Cohen, M., Jacobs, S., & Elmqvist, N.
   (2016). [*The Eight Golden Rules of Interface
   Design*](https://www.cs.umd.edu/users/ben/goldenrules.html?LanguageId=1),
   trích *Designing the User Interface*, ấn bản thứ 6.

---

## 5. Mẫu bảng thực thi Task 1B

Ba màn hình được chọn tạo thành một luồng liên tục từ tìm sự kiện, xem thông
tin chi tiết đến đăng ký tham dự. Chúng có thể kiểm thử bằng tài khoản người
dùng thông thường và không phụ thuộc vé QR đã được cấp hoặc sự kiện đã kết
thúc.

| ID | Mục kiểm tra rút gọn | B1 Home / Events | B2 Event detail | B3 Registration form | Notes |
| --- | --- | --- | --- | --- | --- |
| ADD-01-001 | Thuật ngữ quen thuộc, không lộ mã kỹ thuật | | | | |
| ADD-01-002 | Thứ bậc thị giác và nội dung tối giản | | | | |
| ADD-01-003 | Affordance và trạng thái disabled rõ | | | | |
| ADD-01-004 | Dữ liệu nhất quán giữa các biểu diễn | | | | |
| ADD-02-001 | Hướng dẫn/định dạng có trước khi nhập | | | | |
| ADD-02-002 | Giá trị mặc định an toàn | | | | |
| ADD-02-003 | Ràng buộc giữa các trường phản ánh tức thời | | | | |
| ADD-02-004 | Cảnh báo thay đổi chưa lưu | | | | |
| ADD-03-001 | Chức năng được nhóm theo mục tiêu người dùng | | | | |
| ADD-03-002 | Đường tắt cho tác vụ thường xuyên | | | | |
| ADD-03-003 | Từ chối truy cập/tài nguyên không khả dụng không tạo ngõ cụt | | | | |
| ADD-03-004 | Link/button và lịch sử trình duyệt đúng quy ước | | | | |
| ADD-04-001 | Chống gửi trùng khi đang xử lý | | | | |
| ADD-04-002 | Toast/banner không che nội dung, đóng được, không trùng | | | | |
| ADD-04-003 | Có Undo/Restore khi khả thi | | | | |
| ADD-04-004 | Quy trình kết thúc rõ ràng | | | | |

**Quy ước:** `P` = Passed · `F` = Failed (bắt buộc Notes + ảnh) · `N/A` =
không áp dụng (bắt buộc ghi lý do).
