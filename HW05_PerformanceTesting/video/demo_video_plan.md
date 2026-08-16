# Demo Video Plan

Unlisted YouTube upload, ≥ 6 minutes total. You may record one clip per scenario
(Load/Stress/Spike/Soak) and either upload as a playlist or concatenate — either
satisfies "you may split it into one clip per scenario." **Every clip must show
the tool (terminal running JMeter, or JMeter GUI) and Task Manager in the same
frame**, and be narrated in **your own voice, in Vietnamese** — the bullet points
below are talking points to speak from in your own words, not a script to read
verbatim (the assignment requires *your* narration; reading a fixed script
defeats that).

Screen layout for every segment: split screen or picture-in-picture — JMeter/
terminal on one side, Task Manager (Details tab, `node.exe` row visible) on the
other, both visible at once the whole time.

## Segment 0 — Intro (~15s)

Show: your face/voice only, or a title card with student ID.

Talking points (VN):
- Giới thiệu ngắn: tên, MSSV 23127102, bài HW05 Performance Testing.
- Nêu nhanh workflow được kiểm thử: đăng nhập admin → xem danh sách đơn hàng →
  cập nhật trạng thái đơn hàng (admin order management), vì sao chọn luồng này
  (tránh trùng với luồng của thành viên khác trong nhóm).

## Segment 1 — Load (~90s)

Show: `node seed_orders.js 2000` running, then the official
`jmeter -n -t 23127102_Load_20260816.jmx ...` command, JMeter's periodic
`summary = ...` console output, Task Manager alongside.

Talking points (VN):
- Giải thích Load test mô phỏng gì: 10 admin dùng hệ thống cùng lúc trong 5
  phút, ramp-up 20 giây, think-time ~2 giây giữa các thao tác — con số này mô
  phỏng một nhóm nhân viên vận hành nhỏ, không phải máy đánh liên tục.
  <!-- prettier-ignore -->
- Chỉ ra 3 nhóm endpoint trong 1 luồng: `POST /api/login` (auth-heavy),
  `GET /api/admin/orders` (read-heavy), `PUT /api/admin/orders/:id/status`
  (transactional).
- Khi test chạy xong, mở nhanh `results/load/html-report/index.html`, đọc số
  liệu chính (throughput, p95, error rate) ngay trên video.
- Nhắc: một số response `400` là bình thường (đơn hàng đã được xử lý), không
  phải lỗi — vì sao (đã sửa trong bước review, xem AI_Audit_Report.md Entry 06).

## Segment 2 — Stress (~90s)

Show: the main 80-thread group running (Task Manager CPU visibly higher than
Load), then the lockout sub-test at the end — narrate live as the 403 "locked"
response appears.

Talking points (VN):
- Giải thích Stress test: tăng tải lên 80 luồng, ramp-up nhanh hơn (15 giây),
  để tìm điểm hệ thống bắt đầu chịu áp lực.
- Nhấn mạnh phần lockout: sau 2 lần đăng nhập sai (không phải 3 lần như suy
  nghĩ thông thường — chỉ ra `login_attempts + 2` trong `server.js`), tài
  khoản admin bị khóa 180 giây — quay lại đúng lúc response 403 xuất hiện để
  chứng minh logic hoạt động thật.
- Nói rõ: sau bước này phải chạy `node reset_lockout.js` trước khi làm gì tiếp
  theo cần đăng nhập admin — demo luôn bước reset này trên camera.

## Segment 3 — Spike (~90s)

Show: the three-phase shape live — baseline (calm), then the sudden jump to 150
threads, then recovery. Task Manager CPU should visibly spike then drop.

Talking points (VN):
- Giải thích Spike test: 3 giai đoạn — baseline 5 luồng (30 giây), đột ngột
  tăng lên 150 luồng trong 3 giây (burst, 30 giây), rồi giảm về 5 luồng
  (recovery, 30 giây) — mô phỏng một đợt truy cập tăng vọt bất ngờ.
- Trong lúc burst, chỉ tay vào Task Manager: CPU/mem tăng rõ rệt.
- Sau khi xong, so sánh nhanh số liệu baseline vs. recovery — hệ thống có phục
  hồi về mức bình thường không.

## Segment 4 — Soak / endurance (~90s, time-lapse the middle)

Show: start of the 12-minute run, then a jump-cut (state on screen "đang chạy,
tua nhanh") to partway through and to the end, with 2-3 Task Manager screenshots
already captured at start/mid/end referenced or shown.

Talking points (VN):
- Giải thích mục đích soak test: không tìm điểm gãy như Stress, mà kiểm tra hệ
  thống có **giữ ổn định** trong thời gian dài (12 phút) hay không — bộ nhớ có
  tăng dần (leak) không, độ trễ có xấu đi theo thời gian không.
- Đọc số liệu cụ thể tìm được: throughput ổn định tối đa (RPS), mức bộ nhớ đỉnh
  của `node.exe` — đây là "endurance threshold" theo yêu cầu đề bài, phải nêu
  con số cụ thể, không nói chung chung.

## Segment 5 — Wrap-up (~20s)

Talking points (VN):
- Tóm tắt nhanh: 3 kịch bản + 1 soak test đã chạy, endpoint nào phát hiện vấn
  đề (nếu có bug thật sự tìm được, nêu ngắn gọn).
- Nhắc lại: AI hỗ trợ thiết kế và tạo file test plan, nhưng mọi review, sửa
  lỗi và chạy test chính thức đều do bạn thực hiện và chịu trách nhiệm.

## Checklist before recording

- [ ] Backend restarted fresh (wipes DB — re-seed after, see `EXECUTION_RUNBOOK.md`)
- [ ] Task Manager open, Details tab, `node.exe` visible
- [ ] Screen recorder capturing both windows in one frame
- [ ] Microphone tested
- [ ] `reset_lockout.js` ready to run between Stress and Spike
