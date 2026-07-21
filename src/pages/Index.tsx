import { Helmet } from 'react-helmet-async';
import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import BenefitsSection from '@/components/BenefitsSection';
import TeacherSection from '@/components/TeacherSection';
import AchievementsSection from '@/components/AchievementsSection';
import CoursesSection from '@/components/CoursesSection';
import ContactSection from '@/components/ContactSection';
import Footer from '@/components/Footer';
import BackToTop from '@/components/BackToTop';

const Index = () => {
  return (
    <div className="min-h-screen bg-background font-vietnam">
      <Helmet>
        <title>LTH Chemistry — Dạy Hóa cấp 3, luyện thi THPTQG Hà Nội</title>
        <meta name="description" content="LTH Chemistry — Thầy Lê Trung Hiếu dạy Hóa cấp 3 tại Hà Nội. 75% học sinh đạt từ 8 điểm Hóa trở lên, 95% vượt mục tiêu điểm tự đề ra. Luyện thi THPTQG hiệu quả." />
        <link rel="canonical" href="https://lthchemistry.lovable.app/" />
        <meta property="og:url" content="https://lthchemistry.lovable.app/" />
      </Helmet>

      <Header />
      <main>
        <HeroSection />
        <BenefitsSection />
        <TeacherSection />
        <AchievementsSection />
        <CoursesSection />
        <ContactSection />
      </main>
      <Footer />
      <BackToTop />
    </div>
  );
};

export default Index;