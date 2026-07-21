import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Star, Calendar, Book, MessageCircle } from "lucide-react";

const TeacherSection = () => {
  return (
    <section id="teacher" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Người Dẫn Dắt –{" "}
            <span className="gradient-text">Thầy Lê Trung Hiếu</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-3xl mx-auto">
            Hơn {new Date().getFullYear() - 2019} năm gắn bó với bục giảng, thầy Hiếu không chỉ dạy kiến thức
            mà còn truyền cho các em ngọn lửa đam mê với Hóa học. Với thầy,
            mỗi học trò đều là một câu chuyện riêng cần được lắng nghe và đồng hành.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: Teacher Image */}
          <div className="flex justify-center animate-slide-up">
            <div className="relative">
              <div className="w-80 h-80 rounded-3xl bg-gradient-to-br from-primary/10 to-primary-dark/10 p-2 flex items-center justify-center">
                <img
                  src="/lovable-uploads/fd9015f2-43d2-4e3c-85de-28b9afb79e4b.png"
                  alt={`Thầy Lê Trung Hiếu – Thầy giáo dạy Hóa học hơn ${new Date().getFullYear() - 2019} năm kinh nghiệm, cựu học sinh chuyên Hóa ĐHQGHN`}
                  className="w-full h-full rounded-2xl object-cover"
                  title="Thầy Lê Trung Hiếu – Dạy Hóa THCS chuyên & THPT tại LTH Chemistry"
                />
              </div>

              {/* Floating badges */}
              <div className="absolute -top-4 -right-4 bg-gold text-gold-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float">
                {new Date().getFullYear() - 2019}+ năm kinh nghiệm
              </div>
              <div
                className="absolute -bottom-4 -left-4 bg-primary text-primary-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float"
                style={{ animationDelay: "1s" }}
              >
                Thầy giáo tâm huyết
              </div>
            </div>
          </div>

          {/* Right: Teacher Info */}
          <div className="animate-fade-in">
            <Card className="border-2 hover:border-primary/20 transition-all duration-300">
              <CardContent className="p-8">
                <h3 className="font-quicksand font-bold text-2xl mb-6 gradient-text">
                  Về Thầy Hiếu
                </h3>

                <div className="space-y-6">
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Book className="h-5 w-5 text-primary mr-2" />
                        Nền Tảng Học Thuật
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Cựu học sinh chuyên Hóa THPT Chuyên KHTN (ĐHQGHN)
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          GPA Hóa học luôn đạt 9.8+ – Học sinh xuất sắc toàn khóa 2019
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          <span className="inline-flex items-center flex-wrap gap-1">
                            Thành viên đội ngũ phát triển
                            <a
                              href="https://truonghocsoquocgia.vn"
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1 text-primary hover:text-primary-dark underline underline-offset-2 font-medium transition-colors"
                            >
                              <img
                                src="/lovable-uploads/logo-512x512.png"
                                alt="Logo Trường học số Quốc gia"
                                className="w-5 h-5 object-contain inline-block"
                              />
                              Nền tảng Trường học số Quốc gia
                            </a>
                          </span>
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Star className="h-5 w-5 text-gold mr-2" fill="currentColor" />
                        Tư Duy Giảng Dạy Khác Biệt
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          2 bằng Cử nhân loại Giỏi tại ĐH Kinh Tế Quốc Dân (Quản trị Kinh doanh & Công nghệ thông tin)
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Kết hợp tư duy logic hệ thống với phương pháp truyền đạt gần gũi, dễ tiếp thu
                        </li>
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-3 flex items-center">
                        <Calendar className="h-5 w-5 text-primary mr-2" />
                        Hành Trình Giảng Dạy
                      </h4>
                      <ul className="font-vietnam text-muted-foreground space-y-2 ml-7">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Hơn {new Date().getFullYear() - 2019} năm dạy Hóa học cho học sinh THCS luyện thi chuyên và THPT lớp 10–12
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Ứng dụng tư duy phân tích vào thiết kế bài giảng và hệ thống lộ trình học tập
                        </li>
                      </ul>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <MessageCircle className="h-6 w-6 text-primary mt-1 flex-shrink-0" />
                    <div>
                      <h4 className="font-vietnam font-semibold text-lg mb-2">
                        Cam Kết Với Học Trò
                      </h4>
                        <ul className="font-vietnam text-muted-foreground space-y-2">
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Hỗ trợ học trò bất cứ lúc nào qua Zalo, Messenger
                        </li>
                        <li className="flex items-start">
                          <span className="text-primary mr-2 mt-1">•</span>
                          Không chỉ là thầy giáo, mà còn là người anh đồng hành trên mỗi chặng đường học tập
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-6 border-t flex flex-col sm:flex-row gap-3">
                  <Button
                    onClick={() =>
                      document
                        .getElementById("contact")
                        ?.scrollIntoView({ behavior: "smooth" })
                    }
                    className="flex-1 gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-3 rounded-full"
                  >
                    Kết Nối Với Thầy Ngay
                  </Button>
                  <Button
                    asChild
                    variant="outline"
                    className="flex-1 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-colors font-vietnam font-semibold py-3 rounded-full"
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
