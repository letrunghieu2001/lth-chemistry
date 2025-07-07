import { MessageCircle } from 'lucide-react';

const Footer = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="bg-primary-dark text-primary-foreground py-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* Logo & Slogan */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <img 
                src="/lovable-uploads/296625a8-a982-414c-a91b-493ea9f62b60.png" 
                alt="LTH Chemistry Logo" 
                className="h-12 w-auto brightness-0 invert"
              />
              <div>
                <h3 className="font-quicksand font-bold text-xl">LTH Chemistry</h3>
                <p className="font-vietnam text-sm opacity-90">
                  Khơi dậy đam mê Hóa học
                </p>
              </div>
            </div>
            <p className="font-vietnam text-sm opacity-80 leading-relaxed">
              Trung tâm dạy Hóa học chất lượng cao, giúp học sinh cấp 3 đạt điểm số xuất sắc 
              và vào được trường đại học mơ ước.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-quicksand font-bold text-lg mb-4">Liên Kết Nhanh</h4>
            <ul className="space-y-2">
              <li>
                <button 
                  onClick={() => scrollToSection('benefits')}
                  className="font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
                >
                  Lợi Ích
                </button>
              </li>
              <li>
                <button 
                  onClick={() => scrollToSection('teacher')}
                  className="font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
                >
                  Giảng Viên
                </button>
              </li>
              <li>
                <button 
                  onClick={() => scrollToSection('achievements')}
                  className="font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
                >
                  Thành Tích
                </button>
              </li>
              <li>
                <button 
                  onClick={() => scrollToSection('courses')}
                  className="font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
                >
                  Khóa Học
                </button>
              </li>
              <li>
                <button 
                  onClick={() => scrollToSection('contact')}
                  className="font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
                >
                  Liên Hệ
                </button>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-quicksand font-bold text-lg mb-4">Thông Tin Liên Hệ</h4>
            <div className="space-y-2">
              <div className="font-vietnam text-sm">
                <div className="opacity-80 mb-1">Địa chỉ:</div>
                <div>123 Đường ABC, Quận XYZ, Hà Nội</div>
              </div>
              <div className="font-vietnam text-sm">
                <div className="opacity-80 mb-1">Hotline:</div>
                <div className="font-semibold">0123 456 789</div>
              </div>
              <div className="font-vietnam text-sm">
                <div className="opacity-80 mb-1">Email:</div>
                <div>contact@lthchemistry.vn</div>
              </div>
              <div className="font-vietnam text-sm">
                <div className="opacity-80 mb-1">Giờ làm việc:</div>
                <div>Thứ 2 - CN: 8:00 - 22:00</div>
              </div>
            </div>
          </div>

          {/* Social Media */}
          <div>
            <h4 className="font-quicksand font-bold text-lg mb-4">Kết Nối Với Chúng Tôi</h4>
            <div className="space-y-3">
              <a 
                href="https://zalo.me/0123456789"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
              >
                <div className="w-8 h-8 bg-primary-foreground/20 rounded-full flex items-center justify-center">
                  <MessageCircle className="h-4 w-4" />
                </div>
                <span>Zalo: 0123 456 789</span>
              </a>
              
              <a 
                href="https://m.me/lthchemistry"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
              >
                <div className="w-8 h-8 bg-primary-foreground/20 rounded-full flex items-center justify-center">
                  <MessageCircle className="h-4 w-4" />
                </div>
                <span>Facebook Messenger</span>
              </a>
              
              <a 
                href="mailto:contact@lthchemistry.vn"
                className="flex items-center space-x-3 font-vietnam text-sm opacity-80 hover:opacity-100 transition-opacity"
              >
                <div className="w-8 h-8 bg-primary-foreground/20 rounded-full flex items-center justify-center">
                  <MessageCircle className="h-4 w-4" />
                </div>
                <span>Gmail</span>
              </a>
            </div>

            <div className="mt-6 pt-6 border-t border-primary-foreground/20">
              <p className="font-vietnam text-xs opacity-60">
                Theo dõi chúng tôi để cập nhật thông tin mới nhất về khóa học và 
                các chương trình ưu đãi.
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-6 border-t border-primary-foreground/20 text-center">
          <p className="font-vietnam text-sm opacity-80">
            © 2024 LTH Chemistry. Tất cả quyền được bảo lưu. 
            <span className="mx-2">|</span>
            Thiết kế bởi Lovable
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;