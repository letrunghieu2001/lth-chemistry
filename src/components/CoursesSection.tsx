import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Clock, Users, BookOpen, Calendar } from "lucide-react";

const CoursesSection = () => {
  const courseData = {
    "lop-10": {
      title: "Lớp 10",
      subtitle: "Nền tảng vững chắc cho Hóa học",
      description:
        "Xây dựng nền tảng Hóa học cơ bản, giúp học sinh làm quen và yêu thích môn học.",
      schedule: "Thứ 2, 4, 6",
      duration: "2 tiếng",
      students: "8-12 học sinh/lớp",
      content: [
        "Cấu tạo nguyên tử và bảng tuần hoàn",
        "Liên kết hóa học cơ bản",
        "Phản ứng hóa học và cân bằng phương trình",
        "Mol và tính toán hóa học",
        "Các loại phản ứng vô cơ cơ bản",
      ],
      price: "Thỏa thuận",
    },
    "lop-11": {
      title: "Lớp 11",
      subtitle: "Phát triển tư duy Hóa học",
      description:
        "Nâng cao kiến thức, phát triển kỹ năng giải bài tập phức tạp và tư duy logic.",
      schedule: "Thứ 3, 5, 7",
      duration: "2 tiếng",
      students: "8-12 học sinh/lớp",
      content: [
        "Cân bằng hóa học và các yếu tố ảnh hưởng",
        "Tốc độ phản ứng và động học",
        "Hóa học hữu cơ cơ bản",
        "Điện hóa học và ăn mòn kim loại",
        "Bài tập nâng cao và thi học kỳ",
      ],
      price: "Thỏa thuận",
    },
    "lop-12": {
      title: "Lớp 12",
      subtitle: "Luyện thi THPTQG",
      description:
        "Ôn tập toàn diện, luyện đề thi THPT, đảm bảo điểm số cao trong kỳ thi.",
      schedule: "Thứ 2, 4, 6, 7",
      duration: "2 tiếng",
      students: "6-10 học sinh/lớp",
      content: [
        "Bám sát chương trình GDPT 2018 của Bộ giáo dục và đào tạo",
        "Ôn tập toàn bộ kiến thức 3 năm THPT",
        "Luyện đề thi THPTQG các năm",
        "Kỹ thuật làm bài thi trắc nghiệm",
        "Bài tập nâng cao và phát triển",
        "Tư vấn chiến lược làm bài",
      ],
      price: "Thỏa thuận",
    },
    "kem-11": {
      title: "Kèm 1-1",
      subtitle: "Học tập cá nhân hóa",
      description:
        "Chương trình học được thiết kế riêng cho từng học sinh, tập trung vào điểm yếu cá nhân.",
      schedule: "Linh hoạt theo lịch học sinh",
      duration: "2 tiếng",
      students: "1 học sinh",
      content: [
        "Đánh giá trình độ và xây dựng lộ trình",
        "Tập trung vào điểm yếu cá nhân",
        "Bài tập và đề thi cá nhân hóa",
        "Theo dõi tiến độ sát sao",
        "Hỗ trợ 24/7 qua các kênh liên lạc",
      ],
      price: "Thỏa thuận",
    },
  };

  return (
    <section id="courses" className="py-20 bg-background">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Thông Tin <span className="gradient-text">Khóa Học</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Các khóa học được thiết kế phù hợp với từng cấp độ và nhu cầu học
            tập
          </p>
        </div>

        {/* Course Tabs */}
        <Tabs defaultValue="lop-10" className="max-w-6xl mx-auto">
          <TabsList className="grid w-full grid-cols-4 gap-1 md:gap-0 mb-8 text-xs md:text-sm">
            <TabsTrigger value="lop-10" className="font-vietnam font-semibold">
              Lớp 10
            </TabsTrigger>
            <TabsTrigger value="lop-11" className="font-vietnam font-semibold">
              Lớp 11
            </TabsTrigger>
            <TabsTrigger value="lop-12" className="font-vietnam font-semibold">
              Lớp 12
            </TabsTrigger>
            <TabsTrigger value="kem-11" className="font-vietnam font-semibold">
              Kèm 1-1
            </TabsTrigger>
          </TabsList>

          {Object.entries(courseData).map(([key, course]) => (
            <TabsContent key={key} value={key} className="animate-fade-in">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Course Info */}
                <Card className="border-2 hover:border-primary/20 transition-all duration-300 flex flex-col">
                  <CardContent className="p-8 flex flex-col flex-grow">
                    <div className="mb-6">
                      <h3 className="font-quicksand font-bold text-2xl gradient-text mb-2">
                        {course.title}
                      </h3>
                      <h4 className="font-vietnam font-semibold text-lg text-primary-dark mb-3">
                        {course.subtitle}
                      </h4>
                      <p className="font-vietnam text-muted-foreground leading-relaxed">
                        {course.description}
                      </p>
                    </div>

                    <div className="space-y-4 mb-6">
                      <div className="flex items-center space-x-3">
                        <Calendar className="h-5 w-5 text-primary" />
                        <span className="font-vietnam text-sm">
                          <strong>Lịch học:</strong> {course.schedule}
                        </span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Clock className="h-5 w-5 text-primary" />
                        <span className="font-vietnam text-sm">
                          <strong>Thời lượng:</strong> {course.duration}
                        </span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Users className="h-5 w-5 text-primary" />
                        <span className="font-vietnam text-sm">
                          <strong>Sĩ số:</strong> {course.students}
                        </span>
                      </div>
                    </div>

                    <div className="mt-auto">
                      <div className="bg-gold/10 rounded-lg p-4 text-center">
                        <div className="font-quicksand font-bold text-xl text-gold-foreground">
                          Học phí:{" "}
                          <span className="gradient-text">{course.price}</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Course Content */}
                <Card className="border-2 hover:border-primary/20 transition-all duration-300 flex flex-col">
                  <CardContent className="p-8 flex flex-col flex-grow">
                    <div className="flex items-center space-x-3 mb-6">
                      <BookOpen className="h-6 w-6 text-primary" />
                      <h4 className="font-quicksand font-bold text-xl">
                        Nội Dung Học Tập
                      </h4>
                    </div>

                    <ul className="space-y-3 mb-8 flex-grow">
                      {course.content.map((item, index) => (
                        <li key={index} className="flex items-start space-x-3">
                          <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                            <span className="text-primary font-semibold text-sm">
                              {index + 1}
                            </span>
                          </div>
                          <span className="font-vietnam text-muted-foreground">
                            {item}
                          </span>
                        </li>
                      ))}
                    </ul>

                    <div className="mt-auto">
                      <Button
                        onClick={() =>
                          document
                            .getElementById("contact")
                            ?.scrollIntoView({ behavior: "smooth" })
                        }
                        className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-3 rounded-full"
                      >
                        Đăng Ký Ngay
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </section>
  );
};

export default CoursesSection;
