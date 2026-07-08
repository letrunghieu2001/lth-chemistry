# Hướng dẫn Setup – Tự động đăng Facebook cho LTH Chemistry

> Setup 1 lần duy nhất (~10 phút). Sau đó hệ thống tự chạy mỗi ngày.

## Tổng quan

Hệ thống tự động:
1. Chạy mỗi ngày lúc 5:30 AM (giờ VN) qua GitHub Actions
2. AI (Gemini) viết nội dung bài đăng cho THCS + THPT
3. Tạo ảnh branded (có logo LTH Chemistry)
4. Đăng lên Facebook Page (sáng 6:30 AM + tối 8:00 PM)

Bạn không cần làm gì sau khi setup xong.

---

## Bước 1: Lấy Gemini API Key (30 giây)

1. Truy cập: https://aistudio.google.com/apikey
2. Đăng nhập bằng tài khoản Google
3. Nhấn **"Create API Key"**
4. Chọn project bất kỳ (hoặc tạo mới)
5. **Copy API key** (dạng `AIzaSy...`) – lưu lại, sẽ dùng ở Bước 4

> ⚠️ Free tier cho phép 15 requests/phút, 1500 requests/ngày. Hệ thống chỉ dùng 2 requests/ngày.

---

## Bước 2: Tạo Facebook App (5 phút)

### 2.1 Đăng ký Meta Developer

1. Truy cập: https://developers.facebook.com
2. Đăng nhập bằng tài khoản Facebook **đang quản lý** Page LTH Chemistry
3. Nếu chưa đăng ký Developer, làm theo hướng dẫn trên màn hình để hoàn tất

### 2.2 Tạo App

1. Vào **[My Apps](https://developers.facebook.com/apps/)** → nhấn **"Create App"**
2. **Chọn Use Case**: chọn **"Other"** hoặc **"Manage everything on your Page"**
   - Nếu thấy màn hình "What do you want your app to do?", chọn mục phù hợp nhất với quản lý Page
3. **Chọn App Type**: chọn **"Business"**
4. Điền thông tin:
   - **App name**: `LTH Chemistry Auto Post`
   - **App contact email**: email của bạn
5. Nhấn **"Create App"**

### 2.3 Cấu hình Permissions

1. Trong **App Dashboard**, vào phần **Use Cases** hoặc **Permissions and Features** ở menu trái
2. Đảm bảo các permissions sau đã được thêm (nếu chưa có, nhấn **"Add"**):

| Permission | Tác dụng |
|------------|----------|
| `pages_manage_posts` | Tạo và lên lịch bài đăng |
| `pages_read_engagement` | Đọc thống kê tương tác |
| `pages_show_list` | Lấy danh sách Page bạn quản lý |

> ⚠️ Trong chế độ **Development** (mặc định), app chỉ hoạt động với tài khoản có role trên app (admin/developer). Đây là đủ cho mục đích tự động cá nhân — không cần App Review.

### 2.4 Lấy App ID và App Secret

1. Trong App Dashboard → **Settings** → **Basic**
2. **Copy App ID** (dạng số dài) – lưu lại
3. Nhấn **"Show"** bên cạnh **App Secret** → **copy** – lưu lại

### 2.5 Lấy Page ID

1. Vào Facebook Page LTH Chemistry
2. Nhấn **"About"** (Giới thiệu) hoặc **"Transparency"** (Minh bạch)
3. Kéo xuống → **Page ID** (dạng số, ví dụ: `123456789012345`)
4. **Copy Page ID** – lưu lại

---

## Bước 3: Lấy Page Access Token (5 phút)

### 3.1 Lấy User Access Token từ Graph API Explorer

1. Truy cập: https://developers.facebook.com/tools/explorer/
2. Ở dropdown **"Meta App"** (góc trên phải), chọn app `LTH Chemistry Auto Post`
3. Nhấn **"Add a Permission"** và thêm các permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
4. Nhấn **"Generate Access Token"**
5. Đăng nhập (nếu được yêu cầu) và **cấp quyền** cho tất cả Pages
6. Bạn sẽ thấy **User Access Token** trong ô "Access Token"

### 3.2 Đổi thành Long-lived User Token

User Token vừa lấy chỉ sống vài giờ. Cần đổi thành long-lived (60 ngày):

Mở tab mới trong trình duyệt, dán URL sau (thay các giá trị trong `{}`):

```
https://graph.facebook.com/v25.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-user-token}
```

> - `{app-id}`: App ID từ Bước 2.4
> - `{app-secret}`: App Secret từ Bước 2.4
> - `{short-lived-user-token}`: Token vừa copy ở Bước 3.1

Kết quả trả về JSON:
```json
{"access_token": "EAABsb...(token dài)...", "token_type": "bearer", "expires_in": 5184000}
```

**Copy giá trị `access_token`** – đây là long-lived user token.

### 3.3 Lấy Page Access Token từ Long-lived User Token

Tiếp tục dán URL sau vào trình duyệt (thay `{long-lived-user-token}`):

```
https://graph.facebook.com/v25.0/me/accounts?access_token={long-lived-user-token}
```

Kết quả trả về danh sách Pages bạn quản lý:
```json
{
  "data": [
    {
      "access_token": "EAAG...(PAGE TOKEN)...",
      "name": "LTH Chemistry",
      "id": "123456789012345"
    }
  ]
}
```

**Copy giá trị `access_token`** của Page LTH Chemistry – đây là **Page Access Token**.

> ✅ Page Access Token lấy từ long-lived user token sẽ **có hiệu lực lâu dài** (miễn là bạn vẫn là admin của Page và quyền không bị thu hồi). Nếu hết hạn, lặp lại Bước 3.

### 3.4 Kiểm tra token (tùy chọn)

Dán URL sau để xác nhận token hoạt động:

```
https://graph.facebook.com/v25.0/me?access_token={page-access-token}
```

Nếu trả về tên Page và ID → token OK ✅

---

## Bước 4: Thêm Secrets vào GitHub (2 phút)

1. Vào repo GitHub của bạn (repo chứa code `lth-chemistry`)
2. Nhấn **Settings** → **Secrets and variables** → **Actions**
3. Nhấn **"New repository secret"** và thêm 3 secrets:

| Name | Value |
|------|-------|
| `GEMINI_API_KEY` | API key từ Bước 1 |
| `FB_PAGE_ACCESS_TOKEN` | Long-lived token từ Bước 3.3 |
| `FB_PAGE_ID` | Page ID từ Bước 2.3 |

---

## Bước 5: Push code và kích hoạt (1 phút)

```bash
git add .
git commit -m "feat: add facebook automation pipeline"
git push origin main
```

Hệ thống sẽ tự chạy vào 5:30 AM ngày mai.

### Test ngay lập tức (không cần đợi)

1. Vào repo GitHub → tab **Actions**
2. Nhấn **"Daily Facebook Post"** ở sidebar trái
3. Nhấn **"Run workflow"**
4. Chọn `dry_run: true` để test không đăng thật
5. Hoặc chọn `dry_run: false` để đăng thật ngay

---

## Kiểm tra và bảo trì

### Xem logs

- Vào GitHub → Actions → nhấn vào run gần nhất → xem output

### Nếu token hết hạn

- Script sẽ fail và báo lỗi trong Actions log
- Lặp lại Bước 3 để lấy token mới
- Cập nhật secret `FB_PAGE_ACCESS_TOKEN` trong GitHub Settings

### Điều chỉnh nội dung

- Sửa file `skills/lth-facebook-content/SKILL.md` để thay đổi phong cách viết
- Sửa file `skills/lth-facebook-content/curriculum-map.md` để cập nhật chương trình
- Sửa file `automation/config.py` để thay đổi giờ đăng, màu sắc

### Tạm dừng

- Vào GitHub → Actions → "Daily Facebook Post" → nhấn **"Disable workflow"**
- Khi muốn chạy lại → nhấn **"Enable workflow"**

---

## Chi phí

| Dịch vụ | Chi phí |
|---------|---------|
| GitHub Actions | Miễn phí (2000 phút/tháng, dùng ~60 phút) |
| Gemini API | Miễn phí (free tier, dùng 2 calls/ngày) |
| Facebook Graph API | Miễn phí |
| **Tổng** | **0 đồng/tháng** |
