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