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
                  alt="Thầy Lê Trung Hiếu"
                  className="w-full h-full rounded-2xl object-cover"
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
                        Nền Tảng Kiến Thức Đỉnh Cao
                      </h4>
                      <div className="font-vietnam text-muted-foreground space-y-3">
                        <p>
                          • Cựu học sinh lớp chuyên Hóa - THPT Chuyên Khoa Học Tự Nhiên (ĐHQGHN), một trong những "cái nôi" đào tạo nhân tài hàng đầu Việt Nam.
                        </p>
                        <p>
                          • Luôn duy trì GPA Hóa học trên 9.8 và GPA tổng kết trên 9.4 suốt 3 năm cấp 3.
                        </p>
                        <p>
                          • Vinh dự nhận danh hiệu "Học sinh xuất sắc toàn khóa" khối chuyên Hóa năm 2019.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <Star
                      className="h-6 w-6 text-gold mt-1 flex-shrink-0"
                      fill="currentColor"
                    />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Tư Duy Sư Phạm Hiện Đại & Đa Chiều
                      </h4>
                      <div className="font-vietnam text-muted-foreground space-y-3">
                        <p>
                          • Tốt nghiệp 2 bằng Cử nhân loại Giỏi tại Đại học Kinh Tế Quốc Dân: Quản trị Kinh doanh & Công nghệ thông tin.
                        </p>
                        <p>
                          • Sự kết hợp độc đáo này mang đến một phương pháp giảng dạy logic, hệ thống, dễ hiểu của một chuyên gia IT và khả năng truyền đạt, thấu hiểu tâm lý học sinh của một nhà quản trị.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <Calendar className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Kinh Nghiệm Giảng Dạy
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        Hơn 6 năm kinh nghiệm giảng dạy Hóa học với đam mê cháy bỏng. Đã giúp hàng trăm học sinh đạt điểm cao và đậu vào các trường đại học uy tín.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <MessageCircle className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Cam Kết
                      </h4>
                      <p className="font-vietnam text-muted-foreground">
                        Không chỉ là một người thầy, mà còn là một người anh, một người cố vấn tận tâm trên con đường học tập của mỗi học viên. Luôn đồng hành và hỗ trợ 24/7.
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
