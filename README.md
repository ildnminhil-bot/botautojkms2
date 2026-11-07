🎵 Jockie Music Controller
Discord bot tự động điều khiển Jockie Music thông qua User Account (self-bot).
Bạn chỉ cần gõ tên nhạc hoặc lệnh tự nhiên, bot sẽ tự động gửi m!... thay bạn.

✨ Tính năng
Tính năng

Mô tả

🎶 Phát nhạc tự nhiên

Gõ "Chuyện của mùa đông" → bot gửi m!p Chuyện của mùa đông

📋 Playlist tự động

Gõ nhiều bài cách nhau dấu phẩy "bài 1, bài 2, bài 3" → bot gửi từng dòng

🧠 Nhận diện lệnh AI

"tạm dừng" → m!pause, "tiếp theo" → m!skip, "lặp lại" → m!repeat queue...

🔄 Replay lịch sử

Gõ "phát lại" hoặc "replay 5" → bot phát lại toàn bộ hoặc N bài vừa nghe

🌐 Hỗ trợ URL

Gửi link YouTube/Spotify trực tiếp → bot chuyển m!p <url>

🚀 Deploy lên Render
Bước 1: Tạo repo GitHub
Tạo repository mới trên GitHub (private recommended).
Push toàn bộ code này lên:
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
Bước 2: Tạo project Render
Vào dashboard.render.com → New + → Background Worker.
Chọn repo vừa push.
Bước 3: Cấu hình Start Command
Ở phần Start Command, nhập:

python main.py
Bước 4: Thêm biến môi trường
Vào tab Environment, thêm các biến:

Key

Giá trị

DISCORD_TOKEN

Token User Account của bạn

OWNER_ID

Discord ID của bạn (chuỗi số)

JOCKIE_PREFIX

m!

DELAY_BETWEEN_CMDS

2.5

(Optional) TARGET_GUILD_ID, TARGET_CHANNEL_ID nếu muốn giới hạn bot chỉ hoạt động ở 1 server/channel.

Bước 5: Deploy
Nhấn Create Background Worker. Bot sẽ khởi động và hiện log Đã đăng nhập: ....

🛠️ Chạy local (test)
# 1. Clone & vào thư mục
cd jockie-controller

# 2. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Cài đặt
pip install -r requirements.txt

# 4. Tạo file .env từ mẫu
cp .env.example .env
# Sửa .env: điền DISCORD_TOKEN và OWNER_ID

# 5. Chạy
python main.py
📝 Cách dùng
Phát nhạc
Chuyện của mùa đông
→ m!p Chuyện của mùa đông

https://www.youtube.com/watch?v=xxxxx
→ m!p https://www.youtube.com/watch?v=xxxxx
Phát nhiều bài
Em gái mưa, Chuyện của mùa đông, Cô gái m52
→ m!p Em gái mưa
→ m!p Chuyện của mùa đông
→ m!p Cô gái m52
Điều khiển (tự nhiên)
Bạn gõ

Bot gửi

tạm dừng

m!pause

tiếp tục

m!resume

bài tiếp theo

m!skip

bài trước

m!previous

lặp lại danh sách

m!repeat queue

lặp bài này

m!repeat current

trộn bài

m!shuffle

xóa hết

m!clear

rồi

m!leave

vào room

m!join

danh sách

m!queue

tìm bài

m!search

tua tới 30s

m!forward (cần chỉnh sửa thêm nếu muốn parse số)

Replay lịch sử
phát lại
→ Bot phát lại toàn bộ bài đã nghe

replay 5
→ Bot phát lại 5 bài gần nhất
⚠️ Lưu ý quan trọng
Self-bot vi phạm Discord ToS. Chỉ sử dụng cho mục đích cá nhân, không spam, không public rộng.
Nếu Jockie Music không nghe bot account khác, bạn bắt buộc phải dùng User Token (self-bot).
Để lấy User Token: DevTools (F12) → Application/Storage → Local Storage → https://discord.com → copy token. Không chia sẻ token cho ai.
Bot chỉ nghe lệnh từ OWNER_ID, ngườ i khác gõ sẽ bị bỏ qua.
📁 Cấu trúc
jockie-controller/
├── main.py             # Entry point, Discord client
├── config.py           # Load biến môi trường
├── commands_data.py    # Database lệnh Jockie + alias
├── intent_engine.py    # AI fuzzy-match phân loại intent
├── history_manager.py  # Lưu/lấy lịch sử bài hát
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
🔧 Tuỳ chỉnh thêm
Thêm alias tiếng Việt: mở commands_data.py, thêm vào list aliases của lệnh muốn bổ sung.
Đổi prefix Jockie: sửa JOCKIE_PREFIX trong biến môi trường.
Delay nhanh/chậm: sửa DELAY_BETWEEN_CMDS (khuyến nghị ≥ 2s).
Made with 🎶 for Jockie Music lovers.
