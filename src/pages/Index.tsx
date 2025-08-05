import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import BenefitsSection from '@/components/BenefitsSection';
import SEOContentSection from '@/components/SEOContentSection';
import TeacherSection from '@/components/TeacherSection';
import AchievementsSection from '@/components/AchievementsSection';
import CoursesSection from '@/components/CoursesSection';
import ContactSection from '@/components/ContactSection';
import Footer from '@/components/Footer';

const Index = () => {
  return (
    <div className="min-h-screen bg-background font-vietnam">
      <Header />
      <HeroSection />
      <BenefitsSection />
      <SEOContentSection />
      <TeacherSection />
      <AchievementsSection />
      <CoursesSection />
      <ContactSection />
      <Footer />
    </div>
  );
};

export default Index;