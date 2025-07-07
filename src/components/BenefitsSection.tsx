import { Card, CardContent } from '@/components/ui/card';
import { Star } from 'lucide-react';

const BenefitsSection = () => {
  const benefits = [
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Phương Pháp Hiệu Quả",
      description: "Phương pháp giảng dạy được chứng minh hiệu quả, giúp học sinh nắm vững kiến thức và áp dụng thành thạo."
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Giảng Viên Chuyên Nghiệp", 
      description: "Thầy Lê Trung Hiếu với nhiều năm kinh nghiệm, am hiểu tâm lý học sinh và phương pháp truyền đạt hiệu quả."
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Kết Quả Xuất Sắc",
      description: "90% học sinh đạt điểm 8+ môn Hóa, nhiều em đậu vào các trường đại học top đầu trong cả nước."
    },
    {
      icon: <Star className="h-8 w-8 text-gold" fill="currentColor" />,
      title: "Theo Dõi Sát Sao",
      description: "Theo dõi tiến độ học tập của từng học sinh, đưa ra lộ trình học tập phù hợp với từng em."
    }
  ];

  return (
    <section id="benefits" className="py-20 bg-secondary/50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Tại Sao Nên Chọn <span className="gradient-text">LTH Chemistry?</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Những lợi ích cốt lõi giúp học sinh thành công và đạt được mục tiêu học tập
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