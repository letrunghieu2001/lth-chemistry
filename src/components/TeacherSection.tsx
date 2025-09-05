import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Star, Calendar, Book, MessageCircle } from "lucide-react";

const TeacherSection = () => {
  return (
    <section id="teacher" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Về Giảng Viên -{" "}
            <span className="gradient-text">Thầy Lê Trung Hiếu</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-3xl mx-auto">
            Với hơn 6 năm kinh nghiệm giảng dạy và đam mê cháy bỏng với Hóa học, thầy không chỉ là một người thầy, mà còn là một người anh, một người cố vấn tận tâm trên con đường học tập của mỗi học viên.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: Teacher Image */}
          <div className="flex justify-center animate-slide-up">
            <div className="relative">
              <div className="w-80 h-80 rounded-3xl bg-gradient-to-br from-primary/10 to-primary-dark/10 p-2 flex items-center justify-center">
                <img
                  src="/lovable-uploads/fd9015f2-43d2-4e3c-85de-28b9afb79e4b.png"
                  alt="Thầy Lê Trung Hiếu - Giảng viên Hóa học 6+ năm kinh nghiệm, cựu học sinh chuyên Hóa ĐHQGHN"
                  className="w-full h-full rounded-2xl object-cover"
                  title="Thầy Lê Trung Hiếu - Giảng viên Hóa học chuyên nghiệp tại LTH Chemistry"
                />
              </div>

              {/* Floating badges */}
              <div className="absolute -top-4 -right-4 bg-gold text-gold-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float">
                6+ năm kinh nghiệm
              </div>
              <div
                className="absolute -bottom-4 -left-4 bg-primary text-primary-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float"
                style={{ animationDelay: "1s" }}
              >
                Học sinh xuất sắc
              </div>
            </div>
          </div>

          {/* Right: Teacher Info */}
          <div className="animate-fade-in">
            <Card className="border-2 hover:border-primary/20 transition-all duration-300">
              <CardContent className="p-8">
                <h3 className="font-quicksand font-bold text-2xl mb-6 gradient-text">
                  Thông Tin Chi Tiết
                </h3>

                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <Book className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Nền Tảng Học Thuật Vững Chắc
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        Cựu học sinh chuyên Hóa THPT Chuyên KHTN (ĐHQGHN) với GPA Hóa học 9.8+, đạt danh hiệu "Học sinh xuất sắc toàn khóa" năm 2019.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <Star
                      className="h-6 w-6 text-gold mt-1 flex-shrink-0"
                      fill="currentColor"
                    />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Phương Pháp Giảng Dạy Độc Đáo
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        Kết hợp 2 bằng Cử nhân loại Giỏi (Quản trị Kinh doanh & CNTT) tạo nên phương pháp giảng dạy logic, hệ thống và dễ tiếp thu.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <Calendar className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Kinh Nghiệm Thực Tiễn
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        6+ năm giảng dạy Hóa học và hiện tại đang làm Business Analyst tại dự án Nền tảng Trường học số Quốc gia, ứng dụng tư duy phân tích vào thiết kế bài giảng khoa học.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <MessageCircle className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Cam Kết Đồng Hành
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        Hỗ trợ học viên 24/7, không chỉ là giảng viên mà còn là người cố vấn tận tâm trên hành trình chinh phục Hóa học.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-6 border-t">
                  <Button
                    onClick={() =>
                      document
                        .getElementById("contact")
                        ?.scrollIntoView({ behavior: "smooth" })
                    }
                    className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-3 rounded-full"
                  >
                    Kết Nối Với Thầy Ngay
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default TeacherSection;
