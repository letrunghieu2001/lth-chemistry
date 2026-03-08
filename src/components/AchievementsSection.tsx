import { Card, CardContent } from "@/components/ui/card";
import { Star } from "lucide-react";
import { useState, useRef, useEffect, useMemo } from "react";

const AchievementsSection = () => {
  // Student testimonials in custom order
  const testimonials = [
    {
      name: "Nguyễn Khánh Vân",
      school: "THPT Nguyễn Thị Minh Khai",
      schoolLogo: "/highschool-logos/ntmk-logo.png",
      score: "9.75 điểm Hóa Kỳ thi THPTQG 2025",
      university: "Đại học Y Hà Nội",
      universityLogo: "/university-logos/hmu-logo.png",
      content:
        "Từ một đứa sợ Hóa, em chưa bao giờ nghĩ mình có thể đạt 9.75 điểm. Phương pháp dạy của thầy không chỉ giúp em hiểu bài mà còn truyền cho em niềm yêu thích môn học này.",
    },
    {
      name: "Trần Minh Hiếu",
      school: "THPT Phạm Hồng Thái",
      schoolLogo: "/highschool-logos/pham-hong-thai-logo.png",
      score: "9.25 điểm Hóa Kỳ thi THPTQG 2025",
      university: "Đại học Y Hà Nội",
      universityLogo: "/university-logos/hmu-logo.png",
      content:
        "Đồng hành cùng thầy từ năm lớp 8, em đã được xây dựng một nền tảng Hóa học vững chắc từ con số 0. Sự tận tâm và kiên nhẫn của thầy là động lực lớn nhất giúp em đạt được kết quả hôm nay.",
    },
    {
      name: "Nguyễn Bá Minh",
      school: "THPT Đinh Tiên Hoàng",
      schoolLogo: "/highschool-logos/dth-logo.png",
      score: "9.0 điểm Hóa Kỳ thi THPTQG 2021",
      university: "Đại học Bách Khoa Hà Nội",
      universityLogo: "/university-logos/hust-logo.png",
      content:
        "Thầy Hiếu dạy em cách tư duy như một kỹ sư, hiểu sâu bản chất vấn đề thay vì học vẹt. Các bài giảng về hóa vô cơ và điện phân của thầy thực sự đỉnh cao.",
    },
    {
      name: "Nguyễn Phúc Minh",
      school: "THPT Phạm Hồng Thái",
      schoolLogo: "/highschool-logos/pham-hong-thai-logo.png",
      score: "8.5 điểm Hóa Kỳ thi THPTQG 2025",
      university: "Đại học Kinh tế Quốc dân",
      universityLogo: "/university-logos/neu-logo.png",
      content:
        "Em đã theo học thầy từ những ngày đầu tiên của lớp 8. Thầy đã dẫn dắt em từ một người hoàn toàn mất gốc trở nên yêu thích và chinh phục được môn Hóa. Em thực sự biết ơn thầy.",
    },
    {
      name: "Trần Thu Phương",
      school: "THPT Nguyễn Thị Minh Khai",
      schoolLogo: "/highschool-logos/ntmk-logo.png",
      score: "9.75 điểm Hóa Kỳ thi THPTQG 2025",
      university: "Đại học Y Thái Bình",
      universityLogo: "/lovable-uploads/0af2065a-5831-4955-a2cd-780295646c0f.png",
      content:
        "Bộ đề chuyên sâu và các phương pháp giải nhanh của thầy là chìa khóa giúp em tối ưu hóa điểm số từ 9 lên 9.75. Thầy luôn có những cách tiếp cận bài toán rất độc đáo và hiệu quả.",
    },
    {
      name: "Đỗ Trung Vĩnh",
      school: "THPT Chuyên Chu Văn An",
      schoolLogo: "/highschool-logos/chu-van-an-logo.png",
      score: "9.0 điểm Hóa Kỳ thi THPTQG 2023",
      university: "Đại học Kinh tế Quốc dân",
      universityLogo: "/university-logos/neu-logo.png",
      content:
        "Dù là học sinh chuyên Hóa, em vẫn học được rất nhiều từ hệ thống kiến thức và các dạng bài nâng cao của thầy. Thầy giúp em lấp đầy những lỗ hổng kiến thức nhỏ nhất.",
    },
    {
      name: "Lê Minh Trang",
      school: "THPT Đống Đa",
      schoolLogo: "/highschool-logos/dong-da-logo.png",
      score: "8.0 điểm Hóa Kỳ thi THPTQG 2021",
      university: "Đại học Kinh tế Quốc dân",
      universityLogo: "/university-logos/neu-logo.png",
      content:
        "Em bắt đầu học thầy với số điểm chỉ 5-6. Thầy đã kiên nhẫn dạy lại cho em từ những kiến thức nền tảng nhất. Đạt được 8.0 điểm là một kỳ tích và sự tiến bộ vượt bậc đối với em.",
    },
    {
      name: "Phạm Lê Minh Nhật",
      school: "THPT Nguyễn Trãi",
      schoolLogo: "/highschool-logos/nguyen-trai-logo.png",
      score: "9.0 điểm Hóa Kỳ thi THPTQG 2024",
      university: "Đại học Kinh Tế Quốc dân",
      universityLogo: "/university-logos/neu-logo.png",
      content:
        "Mỗi buổi học với thầy đều rất vui và nhiều năng lượng. Thầy biến những công thức khô khan trở nên thú vị, giúp em tiếp thu kiến thức một cách tự nhiên mà không hề áp lực.",
    },
    {
      name: "Ngô Quốc Khánh",
      school: "THPT Nguyễn Trãi",
      schoolLogo: "/highschool-logos/nguyen-trai-logo.png",
      score: "8.5 điểm Hóa Kỳ thi THPTQG 2024",
      university: "Đại học Khoa học tự nhiên",
      universityLogo: "/university-logos/vnu-hanoi-logo.png",
      content:
        "Thật không thể tin được! Chỉ trong 2 tháng học cấp tốc với thầy, em đã đi từ không biết gì về Hóa đến việc tự tin đạt 8.5 điểm. Lộ trình của thầy thực sự quá hiệu quả.",
    },
    {
      name: "Phạm Vũ Gia Huy",
      school: "THPT Đống Đa",
      schoolLogo: "/highschool-logos/dong-da-logo.png",
      score: "8.0 điểm Hóa Kỳ thi THPTQG 2022",
      university: "Đại học Khoa học tự nhiên",
      universityLogo: "/university-logos/vnu-hanoi-logo.png",
      content:
        "Nhờ có thầy, em đã vượt qua được nỗi sợ môn Hóa và đạt được kết quả 8.0 điểm. Cách giảng dạy sinh động và dễ hiểu của thầy đã giúp em xây dựng nền tảng vững chắc để theo đuổi ngành khoa học.",
    },
  ];
  
  // Statistics
  const stats = [
    { number: "80%+", label: "Học sinh đạt điểm 9+ môn Hóa" },
    { number: "95%+", label: "Học sinh đậu vào trường top" },
    { number: "5+", label: "Năm kinh nghiệm giảng dạy" },
    { number: "100%", label: "Tỷ lệ hài lòng của phụ huynh" },
  ];

  // Top universities with logos
  const universities = [
    {
      name: "Đại học Bách Khoa Hà Nội",
      logo: "/university-logos/hust-logo.png",
    },
    { name: "Đại học Y Hà Nội", logo: "/university-logos/hmu-logo.png" },
    {
      name: "Đại học Quốc gia Hà Nội",
      logo: "/university-logos/vnu-hanoi-logo.png",
    },
    {
      name: "Đại học Kinh tế Quốc dân",
      logo: "/university-logos/neu-logo.png",
    },
    { name: "Đại học Ngoại thương", logo: "/university-logos/ftu-logo.png" },
    { name: "Đại học Dược Hà Nội", logo: "/university-logos/hup-logo.png" },
    { name: "Đại học Xây Dựng", logo: "/university-logos/hau-logo.png" },
    { name: "Đại học Sư Phạm Hà Nội", logo: "/university-logos/hnue-logo.png" },
  ];
  
  // Start from center position with proper infinite scroll setup
  const totalSlides = testimonials.length;
  const [currentSlide, setCurrentSlide] = useState(3 + Math.floor(totalSlides / 2)); // Start at center of original items
  const slideInterval = useRef<NodeJS.Timeout | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState(0);
  const [dragOffset, setDragOffset] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  // Create infinite loop by adding duplicates at both ends
  const extendedTestimonials = [
    ...testimonials.slice(-3), // Last 3 items at the beginning
    ...testimonials,           // Original items
    ...testimonials.slice(0, 3) // First 3 items at the end
  ];

  // Drag handlers
  const handleDragStart = (clientX: number) => {
    setIsDragging(true);
    setDragStart(clientX);
    if (slideInterval.current) {
      clearInterval(slideInterval.current);
    }
  };

  const handleDragMove = (clientX: number) => {
    if (!isDragging) return;
    const offset = clientX - dragStart;
    setDragOffset(offset);
  };

  const handleDragEnd = () => {
    if (!isDragging) return;
    setIsDragging(false);
    
    const threshold = 100;
    if (Math.abs(dragOffset) > threshold) {
      if (dragOffset > 0) {
        // Drag right - previous slide
        setCurrentSlide(prev => prev - 1);
      } else {
        // Drag left - next slide  
        setCurrentSlide(prev => prev + 1);
      }
    }
    
    setDragOffset(0);
    
    // Restart auto-play
    slideInterval.current = setInterval(() => {
      setCurrentSlide(prev => prev + 1);
    }, 4000);
  };

  const goToSlide = (index: number) => {
    setCurrentSlide(index + 3); // Add offset for duplicates
  };

  useEffect(() => {
    if (!isDragging) {
      slideInterval.current = setInterval(() => {
        setCurrentSlide(prev => prev + 1);
      }, 4000);
    }

    return () => {
      if (slideInterval.current) {
        clearInterval(slideInterval.current);
      }
    };
  }, [isDragging]);

  // Handle infinite scroll reset
  useEffect(() => {
    if (currentSlide >= totalSlides + 3) {
      // Reset to beginning
      setTimeout(() => {
        setIsTransitioning(false);
        setCurrentSlide(3);
      }, 500);
      setIsTransitioning(true);
    } else if (currentSlide < 3) {
      // Reset to end
      setTimeout(() => {
        setIsTransitioning(false);
        setCurrentSlide(totalSlides + 2);
      }, 500);
      setIsTransitioning(true);
    }
  }, [currentSlide, totalSlides]);

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
                className="bg-background rounded-lg p-4 text-center border-2 border-transparent hover:border-primary/20 transition-all duration-300 animate-slide-up flex flex-col items-center"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <img
                  src={university.logo}
                  alt={`Logo đại học ${university.name} - Nơi học sinh LTH Chemistry đã đậu vào`}
                  className="w-12 h-12 object-contain mb-2"
                  title={`${university.name} - Một trong những trường đại học top mà học sinh LTH Chemistry đã trúng tuyển`}
                />
                <div className="font-vietnam font-medium text-sm text-foreground">
                  {university.name}
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
                className={`cursor-grab active:cursor-grabbing select-none ${
                  isDragging ? 'cursor-grabbing' : 'cursor-grab'
                }`}
                onMouseDown={(e) => {
                  e.preventDefault();
                  handleDragStart(e.clientX);
                }}
                onMouseMove={(e) => handleDragMove(e.clientX)}
                onMouseUp={handleDragEnd}
                onMouseLeave={handleDragEnd}
                onTouchStart={(e) => {
                  handleDragStart(e.touches[0].clientX);
                }}
                onTouchMove={(e) => {
                  e.preventDefault();
                  handleDragMove(e.touches[0].clientX);
                }}
                onTouchEnd={handleDragEnd}
              >
                <div
                  className={`flex transition-transform duration-500 ease-out ${
                    isTransitioning ? 'transition-none' : ''
                  }`}
                  style={{ 
                    transform: `translateX(calc(-${currentSlide * 100}% + ${dragOffset}px))` 
                  }}
                >
                  {extendedTestimonials.map((testimonial, index) => (
                    <div 
                      key={`${testimonial.name}-${index}`} 
                      className="w-full flex-shrink-0"
                    >
                      <Card className="mx-4 border-2 border-primary/20 hover:border-primary/30 transition-all duration-300 shadow-lg h-[320px]">
                        <CardContent className="p-6 text-center h-full flex flex-col">
                          {/* Stars */}
                          <div className="flex justify-center mb-2">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className="h-4 w-4 text-gold fill-current"
                              />
                            ))}
                          </div>

                          {/* Quote */}
                          <div className="flex-1 flex items-center justify-center mb-2">
                            <p className="font-vietnam text-base text-muted-foreground italic leading-snug">
                              "{testimonial.content}"
                            </p>
                          </div>

                          {/* User Info */}
                          <div className="space-y-1">
                            <div className="font-quicksand font-bold text-xl gradient-text">
                              {testimonial.name}
                            </div>
                            
                            <div className="w-12 h-px bg-gradient-to-r from-primary/60 to-primary/20 mx-auto my-1"></div>
                            
                            {/* University */}
                            <div className="flex items-center justify-center space-x-2">
                              <img
                                src={testimonial.universityLogo}
                                alt={`Logo ${testimonial.university}`}
                                className="w-6 h-6 object-contain"
                                title={`${testimonial.university} - ${testimonial.name} đạt ${testimonial.score}`}
                              />
                              <div className="font-vietnam text-sm font-medium text-primary">
                                {testimonial.university}
                              </div>
                            </div>
                            
                            {/* Score */}
                            <div className="font-vietnam font-medium text-sm text-muted-foreground">
                              {testimonial.score}
                            </div>
                            
                            {/* School */}
                            <div className="flex items-center justify-center space-x-1">
                              <img
                                src={testimonial.schoolLogo}
                                alt={`Logo trường THPT ${testimonial.school}`}
                                className="w-4 h-4 object-contain"
                                title={`${testimonial.school} - Trường cấp 3 của ${testimonial.name}`}
                              />
                              <span className="font-vietnam text-xs text-muted-foreground">Cựu học sinh {testimonial.school}</span>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Navigation dots */}
            <div className="flex justify-center mt-6 space-x-2">
              {testimonials.map((_, index) => {
                const actualCurrentIndex = (currentSlide - 3 + totalSlides) % totalSlides;
                return (
                  <button
                    key={index}
                    onClick={() => goToSlide(index)}
                    className={`w-2 h-2 rounded-full transition-all duration-300 ${
                      index === actualCurrentIndex ? "bg-primary w-6" : "bg-muted hover:bg-muted-foreground/50"
                    }`}
                  />
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AchievementsSection;
