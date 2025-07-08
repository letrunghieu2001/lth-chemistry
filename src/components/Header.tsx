import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-background/95 backdrop-blur-sm shadow-lg"
          : "bg-transparent"
      }`}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <img
              src="/lovable-uploads/a9ca5b60-c7ef-4893-878f-1d0dc280940e.png"
              alt="LTH Chemistry Logo"
              className="h-12 w-auto animate-float"
            />
            <div className="hidden md:block">
              <h1 className="font-quicksand font-bold text-xl gradient-text">
                LTH Chemistry
              </h1>
              <p className="text-sm text-muted-foreground font-vietnam">
                Khơi dậy đam mê Hóa học
              </p>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="hidden lg:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection("benefits")}
              className="font-vietnam font-medium text-foreground hover:text-primary transition-colors"
            >
              Lợi Ích
            </button>
            <button
              onClick={() => scrollToSection("teacher")}
              className="font-vietnam font-medium text-foreground hover:text-primary transition-colors"
            >
              Giảng Viên
            </button>
            <button
              onClick={() => scrollToSection("achievements")}
              className="font-vietnam font-medium text-foreground hover:text-primary transition-colors"
            >
              Thành Tích
            </button>
            <button
              onClick={() => scrollToSection("courses")}
              className="font-vietnam font-medium text-foreground hover:text-primary transition-colors"
            >
              Khóa Học
            </button>
            <button
              onClick={() => scrollToSection("contact")}
              className="font-vietnam font-medium text-foreground hover:text-primary transition-colors"
            >
              Liên Hệ
            </button>
          </nav>

          {/* CTA Button */}
          <Button
            onClick={() => scrollToSection("contact")}
            className="gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold px-6 py-2 rounded-full shadow-lg"
          >
            Kết Nối Ngay
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
