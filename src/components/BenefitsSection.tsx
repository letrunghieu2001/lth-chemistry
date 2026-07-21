import { Card, CardContent } from "@/components/ui/card";
import { Star } from "lucide-react";

const BenefitsSection = () => {
  const benefits = [
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Phương Pháp Đã Được Kiểm Chứng",
      description:
        "Cách dạy của thầy Hiếu đi từ gốc, giúp các em thực sự hiểu bản chất thay vì học thuộc lòng. Kiến thức nắm chắc thì bài nào cũng giải được.",
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Thầy Giáo Tâm Huyết",
      description:
        "Thầy Lê Trung Hiếu – hơn 6 năm kinh nghiệm, cựu học sinh chuyên Hóa THPT Chuyên Khoa Học Tự Nhiên - ĐHQGHN. Thầy hiểu học sinh cần gì và biết cách truyền đạt sao cho dễ nhớ nhất.",
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Kết Quả Nói Lên Tất Cả",
      description:
        "75% học sinh đạt từ 8 điểm Hóa trở lên, 95% các em vượt qua mục tiêu điểm mà chính mình đặt ra từ đầu. Kết quả cụ thể, không cần nói nhiều.",
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Đồng Hành Từng Bước",
      description:
        "Mỗi em đều có lộ trình riêng phù hợp với trình độ và mục tiêu. Thầy theo sát từng bước tiến bộ, không em nào bị bỏ lại phía sau.",
    },
  ];

  return (
    <section id="benefits" className="py-20 bg-secondary/50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Tại Sao Chọn{" "}
            <span className="gradient-text">LTH Chemistry</span>?
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Những lý do giúp học sinh từ THCS đến THPT đều tin tưởng và đạt
            kết quả vượt mong đợi
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {benefits.map((benefit, index) => (
            <Card
              key={index}
              className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-primary/20 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6 text-center">
                <div className="mb-4 flex justify-center transform group-hover:scale-110 transition-transform duration-300">
                  {benefit.icon}
                </div>
                <h3 className="font-quicksand font-bold text-xl mb-3 text-foreground">
                  {benefit.title}
                </h3>
                <p className="font-vietnam text-muted-foreground leading-relaxed">
                  {benefit.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default BenefitsSection;
