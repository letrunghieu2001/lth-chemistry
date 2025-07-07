import { Card, CardContent } from '@/components/ui/card';
import { Star } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

const AchievementsSection = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const slideInterval = useRef<NodeJS.Timeout | null>(null);

  // Statistics
  const stats = [
    { number: "90%+", label: "Học sinh đạt điểm 8+ môn Hóa" },
    { number: "100+", label: "Học sinh đã thành công" },
    { number: "5+", label: "Năm kinh nghiệm giảng dạy" },
    { number: "95%+", label: "Tỷ lệ hài lòng của phụ huynh" }
  ];

  // Top universities
  const universities = [
    "Đại học Bách Khoa Hà Nội",
    "Đại học Y Hà Nội", 
    "Đại học Quốc gia Hà Nội",
    "Đại học Kinh tế Quốc dân",
    "Đại học Ngoại thương",
    "Học viện Ngân hàng",
    "Đại học Xây Dựng",
    "Đại học Công nghiệp Hà Nội"
  ];

  // Student testimonials
  const testimonials = [
    {
      name: "Nguyễn Minh Anh",
      grade: "Lớp 12A1",
      score: "9.2 điểm Hóa",
      university: "Đại học Bách Khoa Hà Nội",
      content: "Thầy Hiếu dạy rất dễ hiểu, luôn tạo không khí học tập vui vẻ. Nhờ thầy mà em đã từ sợ Hóa học thành yêu thích môn này."
    },
    {
      name: "Trần Việt Hoàng",
      grade: "Lớp 12A2", 
      score: "8.8 điểm Hóa",
      university: "Đại học Y Hà Nội",
      content: "Phương pháp của thầy giúp em hiểu bản chất các phản ứng, không cần học thuộc lòng mà vẫn nhớ lâu."
    },
    {
      name: "Lê Thị Mai",
      grade: "Lớp 12A3",
      score: "9.0 điểm Hóa", 
      university: "Đại học Quốc gia Hà Nội",
      content: "Thầy luôn nhiệt tình hỗ trợ, giải đáp mọi thắc mắc của học sinh. Cảm ơn thầy đã giúp em đạt được ước mơ."
    }
  ];

  useEffect(() => {
    slideInterval.current = setInterval(() => {
      setCurrentSlide(prev => (prev + 1) % testimonials.length);
    }, 4000);

    return () => {
      if (slideInterval.current) {
        clearInterval(slideInterval.current);
      }
    };
  }, [testimonials.length]);

  return (
    <section id="achievements" className="py-20 bg-secondary/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            <span className="gradient-text">Thành Quả</span> Nói Lên Tất Cả
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Những con số và câu chuyện thành công của các học sinh LTH Chemistry
          </p>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {stats.map((stat, index) => (
            <Card 
              key={index}
              className="text-center hover:shadow-lg transition-all duration-300 animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <CardContent className="p-6">
                <div className="font-quicksand font-bold text-3xl md:text-4xl gradient-text mb-2">
                  {stat.number}
                </div>
                <div className="font-vietnam text-sm text-muted-foreground">
                  {stat.label}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Universities Section */}
        <div className="mb-16 animate-fade-in">
          <h3 className="font-quicksand font-bold text-2xl text-center mb-8">
            Học Sinh Của Chúng Tôi Đã Đậu Vào
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {universities.map((university, index) => (
              <div 
                key={index}
                className="bg-background rounded-lg p-4 text-center border-2 border-transparent hover:border-primary/20 transition-all duration-300 animate-slide-up"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className="font-vietnam font-medium text-sm text-foreground">
                  {university}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Testimonials Carousel */}
        <div className="animate-fade-in">
          <h3 className="font-quicksand font-bold text-2xl text-center mb-8">
            Cảm Nhận Từ Học Sinh
          </h3>
          
          <div className="relative max-w-4xl mx-auto">
            <div className="overflow-hidden rounded-2xl">
              <div 
                className="flex transition-transform duration-500 ease-in-out"
                style={{ transform: `translateX(-${currentSlide * 100}%)` }}
              >
                {testimonials.map((testimonial, index) => (
                  <div key={index} className="w-full flex-shrink-0">
                    <Card className="mx-4 border-2 hover:border-primary/20 transition-all duration-300">
                      <CardContent className="p-8 text-center">
                        <div className="flex justify-center mb-4">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="h-5 w-5 text-gold fill-current" />
                          ))}
                        </div>
                        
                        <p className="font-vietnam text-lg text-muted-foreground mb-6 italic leading-relaxed">
                          "{testimonial.content}"
                        </p>
                        
                        <div className="space-y-2">
                          <div className="font-quicksand font-bold text-xl gradient-text">
                            {testimonial.name}
                          </div>
                          <div className="font-vietnam text-sm text-muted-foreground">
                            {testimonial.grade} • {testimonial.score}
                          </div>
                          <div className="font-vietnam text-sm font-medium text-primary">
                            {testimonial.university}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                ))}
              </div>
            </div>

            {/* Dots indicator */}
            <div className="flex justify-center mt-6 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentSlide ? 'bg-primary' : 'bg-muted'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AchievementsSection;