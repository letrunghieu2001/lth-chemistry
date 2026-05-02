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
                Giáo viên xuất sắc
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
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Book className="h-5 w-5 text-primary mr-2" />
                        Nền Tảng Học Thuật Vững Chắc
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Cựu học sinh chuyên Hóa THPT Chuyên KHTN (ĐHQGHN)
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          GPA Hóa học luôn đạt 9.8+ - Học sinh xuất sắc toàn khóa 2019
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Star className="h-5 w-5 text-gold mr-2" fill="currentColor" />
                        Phương Pháp Giảng Dạy Độc Đáo
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          2 bằng Cử nhân loại Giỏi tại Đại Học Kinh Tế Quốc Dân, chuyên ngành: Quản trị Kinh doanh & Công nghệ thông tin
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Phương pháp giảng dạy logic, hệ thống và dễ tiếp thu
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Calendar className="h-5 w-5 text-primary mr-2" />
                        Kinh Nghiệm Thực Tiễn
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          6+ năm giảng dạy Hóa học chuyên sâu
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Thành viên đội ngũ phát triển Nền tảng Trường học số Quốc gia
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Ứng dụng tư duy phân tích vào thiết kế bài giảng và hệ thống
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <MessageCircle className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Cam Kết Đồng Hành
                      </h4>
                        <ul className="font-vietnam text-muted-foreground space-y-2">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Hỗ trợ học viên 24/7
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Vừa là giáo viên, vừa là người cố vấn tận tâm trên hành trình chinh phục Hóa học.
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-6 border-t space-y-3">
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
                  <Button
                    asChild
                    variant="outline"
                    className="w-full border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-colors font-vietnam font-semibold py-3 rounded-full"
                  >
                    <a
                      href="https://bob-portfolio.lovable.app/"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Xem Portfolio Của Thầy
                    </a>
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
