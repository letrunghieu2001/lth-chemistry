import { Button } from "@/components/ui/button";
import { Star } from "lucide-react";

const HeroSection = () => {
  const scrollToContact = () => {
    const element = document.getElementById("contact");
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section className="min-h-screen flex items-center hero-bg relative overflow-hidden">
      {/* Floating elements */}
      <div className="absolute top-20 left-10 animate-float">
        <Star className="h-6 w-6 text-gold" fill="currentColor" />
      </div>
      <div
        className="absolute top-32 right-20 animate-float"
        style={{ animationDelay: "1s" }}
      >
        <Star className="h-4 w-4 text-gold" fill="currentColor" />
      </div>
      <div
        className="absolute bottom-32 left-32 animate-float"
        style={{ animationDelay: "2s" }}
      >
        <Star className="h-5 w-5 text-gold" fill="currentColor" />
      </div>

      <div className="container mx-auto px-4 py-32">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
          {/* Left Content */}
          <div className="flex-1 text-center lg:text-left animate-fade-in">
            <h1 className="font-quicksand font-bold text-4xl md:text-5xl lg:text-6xl mb-6 leading-tight">
              <span className="gradient-text">LTH Chemistry</span>
              <br />
              <span className="text-foreground">Khơi Dậy Đam Mê Hóa Học</span>
              <br />
              <span className="text-primary-dark">Chinh Phục Điểm Số Chemistry</span>
            </h1>

            <p className="font-vietnam text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl">
              Học hóa học (chemistry) hiệu quả với phương pháp giảng dạy độc đáo của thầy Lê Trung Hiếu - LTH Chemistry. 6+ 
              năm kinh nghiệm giúp học sinh cấp 3 nắm vững kiến thức hóa học, tự tin 
              làm bài và đạt điểm cao trong các kỳ thi.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button
                onClick={scrollToContact}
                size="lg"
                className="gradient-bg hover:opacity-90 transition-all duration-300 font-vietnam font-semibold px-8 py-4 rounded-full shadow-xl transform hover:scale-105"
              >
                Kết Nối Tư Vấn
              </Button>

              <Button
                onClick={() =>
                  document
                    .getElementById("benefits")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
                variant="outline"
                size="lg"
                className="font-vietnam font-semibold px-8 py-4 rounded-full border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300"
              >
                Tìm Hiểu Thêm
              </Button>
            </div>

            {/* Stats Preview */}
            <div className="mt-12 grid grid-cols-2 md:grid-cols-3 gap-6 max-w-md mx-auto lg:mx-0">
              <div className="text-center">
                <div className="font-quicksand font-bold text-2xl gradient-text">
                  80%+
                </div>
                <div className="font-vietnam text-sm text-muted-foreground">
                  Học sinh đạt 9+
                </div>
              </div>
              <div className="text-center">
                <div className="font-quicksand font-bold text-2xl gradient-text">
                  5+
                </div>
                <div className="font-vietnam text-sm text-muted-foreground">
                  Năm kinh nghiệm
                </div>
              </div>
              <div className="text-center col-span-2 md:col-span-1">
                <div className="font-quicksand font-bold text-2xl gradient-text">
                  95%+
                </div>
                <div className="font-vietnam text-sm text-muted-foreground">
                  Học sinh đậu vào trường top
                </div>
              </div>
            </div>
          </div>

          {/* Right Content */}
          <div className="flex-1 flex justify-center lg:justify-end animate-slide-up">
            <div className="relative">
              <div className="w-80 h-80 md:w-96 md:h-96 rounded-full bg-gradient-to-br from-primary/20 to-primary-dark/20 flex items-center justify-center animate-float p-4">
                <div className="relative w-full h-full rounded-full overflow-hidden shadow-2xl border-4 border-white/10 backdrop-blur-sm">
                  <video
                    src="/lovable-uploads/Video_Ready_Add_a_Wave.mp4"
                    autoPlay
                    muted
                    loop
                    playsInline
                    className="w-full h-full object-cover rounded-full"
                    aria-label="LTH Chemistry - Video giới thiệu lớp học dạy Hóa học (chemistry) chất lượng cao với thầy Lê Trung Hiếu"
                    title="LTH Chemistry - Lớp học dạy Hóa học cấp 3 với phương pháp chemistry hiệu quả"
                  />
                  <div className="absolute inset-0 rounded-full bg-gradient-to-t from-black/5 to-transparent pointer-events-none"></div>
                  <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-primary/30 via-gold/30 to-primary-dark/30 opacity-50 blur-lg animate-pulse"></div>
                </div>
              </div>

              {/* Floating badges */}
              <div className="absolute -top-4 -right-4 bg-gold text-gold-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float">
                Chất lượng cao
              </div>
              <div
                className="absolute -bottom-4 -left-4 bg-primary text-primary-foreground px-4 py-2 rounded-full font-vietnam font-semibold shadow-lg animate-float"
                style={{ animationDelay: "1s" }}
              >
                Đội ngũ chuyên nghiệp
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
