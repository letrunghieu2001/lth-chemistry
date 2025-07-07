import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { MessageCircle, Phone, Calendar } from 'lucide-react';

const ContactSection = () => {
  const [activeTab, setActiveTab] = useState('zalo');

  return (
    <section id="contact" className="py-20 bg-secondary/50">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Sẵn Sàng Bứt Phá? <span className="gradient-text">Kết Nối Với Thầy Ngay!</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Chọn kênh liên lạc phù hợp và bắt đầu hành trình chinh phục Hóa học cùng LTH Chemistry
          </p>
        </div>

        {/* Contact Tabs */}
        <div className="max-w-4xl mx-auto">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger value="zalo" className="font-vietnam font-semibold flex items-center space-x-2">
                <MessageCircle className="h-4 w-4" />
                <span>Zalo</span>
              </TabsTrigger>
              <TabsTrigger value="messenger" className="font-vietnam font-semibold flex items-center space-x-2">
                <MessageCircle className="h-4 w-4" />
                <span>Messenger</span>
              </TabsTrigger>
              <TabsTrigger value="gmail" className="font-vietnam font-semibold flex items-center space-x-2">
                <MessageCircle className="h-4 w-4" />
                <span>Gmail</span>
              </TabsTrigger>
            </TabsList>

            {/* Zalo Tab */}
            <TabsContent value="zalo" className="animate-fade-in">
              <Card className="border-2 hover:border-primary/20 transition-all duration-300">
                <CardContent className="p-8 text-center">
                  <div className="mb-6">
                    <h3 className="font-quicksand font-bold text-2xl mb-2 gradient-text">
                      Kết Nối Qua Zalo
                    </h3>
                    <p className="font-vietnam text-muted-foreground">
                      Quét mã QR hoặc tìm kiếm theo số điện thoại để liên lạc nhanh chóng
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    {/* QR Code */}
                    <div className="flex flex-col items-center">
                      <div className="w-48 h-48 bg-gradient-to-br from-primary/10 to-primary-dark/10 rounded-2xl flex items-center justify-center mb-4">
                        <div className="text-center">
                          <div className="text-6xl mb-2">📱</div>
                          <div className="font-vietnam text-sm text-muted-foreground">Mã QR Zalo</div>
                          <div className="font-vietnam text-xs text-muted-foreground mt-1">Quét để kết nối</div>
                        </div>
                      </div>
                      <p className="font-vietnam text-sm text-muted-foreground text-center">
                        Mở ứng dụng Zalo và quét mã QR để chat trực tiếp với thầy
                      </p>
                    </div>

                    {/* Contact Info */}
                    <div className="space-y-4">
                      <div className="bg-primary/10 rounded-lg p-4">
                        <div className="flex items-center space-x-3 mb-2">
                          <Phone className="h-5 w-5 text-primary" />
                          <span className="font-vietnam font-semibold">Số điện thoại</span>
                        </div>
                        <div className="font-vietnam text-lg font-bold text-primary">
                          0123 456 789
                        </div>
                        <div className="font-vietnam text-sm text-muted-foreground mt-1">
                          Tìm kiếm số này trên Zalo
                        </div>
                      </div>

                      <div className="bg-gold/10 rounded-lg p-4">
                        <div className="flex items-center space-x-3 mb-2">
                          <Calendar className="h-5 w-5 text-gold" />
                          <span className="font-vietnam font-semibold">Thời gian hỗ trợ</span>
                        </div>
                        <div className="font-vietnam text-sm">
                          <div>Thứ 2 - Chủ nhật: 8:00 - 22:00</div>
                          <div className="text-gold font-medium">Phản hồi trong 15 phút</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Messenger Tab */}
            <TabsContent value="messenger" className="animate-fade-in">
              <Card className="border-2 hover:border-primary/20 transition-all duration-300">
                <CardContent className="p-8 text-center">
                  <div className="mb-6">
                    <h3 className="font-quicksand font-bold text-2xl mb-2 gradient-text">
                      Kết Nối Qua Messenger
                    </h3>
                    <p className="font-vietnam text-muted-foreground">
                      Chat trực tiếp qua Facebook Messenger để được tư vấn chi tiết
                    </p>
                  </div>

                  <div className="max-w-md mx-auto space-y-6">
                    <div className="w-32 h-32 bg-gradient-to-br from-primary/10 to-primary-dark/10 rounded-full flex items-center justify-center mx-auto">
                      <div className="text-5xl">💬</div>
                    </div>

                    <div className="space-y-4">
                      <Button 
                        className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-4 rounded-full text-lg"
                        onClick={() => window.open('https://m.me/lthchemistry', '_blank')}
                      >
                        Mở Messenger Chat
                      </Button>
                      
                      <div className="bg-primary/10 rounded-lg p-4">
                        <div className="font-vietnam font-semibold mb-1">Facebook Page</div>
                        <div className="font-vietnam text-sm text-muted-foreground">
                          facebook.com/lthchemistry
                        </div>
                      </div>
                      
                      <div className="bg-gold/10 rounded-lg p-4">
                        <div className="font-vietnam font-semibold mb-1">Thời gian phản hồi</div>
                        <div className="font-vietnam text-sm text-gold">
                          Trung bình 10 phút
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Gmail Tab */}
            <TabsContent value="gmail" className="animate-fade-in">
              <Card className="border-2 hover:border-primary/20 transition-all duration-300">
                <CardContent className="p-8 text-center">
                  <div className="mb-6">
                    <h3 className="font-quicksand font-bold text-2xl mb-2 gradient-text">
                      Kết Nối Qua Email
                    </h3>
                    <p className="font-vietnam text-muted-foreground">
                      Gửi email để được tư vấn chi tiết về khóa học và lộ trình học tập
                    </p>
                  </div>

                  <div className="max-w-md mx-auto space-y-6">
                    <div className="w-32 h-32 bg-gradient-to-br from-primary/10 to-primary-dark/10 rounded-full flex items-center justify-center mx-auto">
                      <div className="text-5xl">📧</div>
                    </div>

                    <div className="space-y-4">
                      <Button 
                        className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-4 rounded-full text-lg"
                        onClick={() => window.open('mailto:contact@lthchemistry.vn?subject=Tư vấn khóa học Hóa học&body=Xin chào thầy Hiếu,%0D%0A%0D%0ATôi muốn tìm hiểu về khóa học Hóa học tại LTH Chemistry.%0D%0A%0D%0AThông tin học sinh:%0D%0A- Họ tên:%0D%0A- Lớp:%0D%0A- Số điện thoại:%0D%0A- Mục tiêu học tập:%0D%0A%0D%0ACảm ơn thầy!', '_blank')}
                      >
                        Gửi Email Ngay
                      </Button>
                      
                      <div className="bg-primary/10 rounded-lg p-4">
                        <div className="font-vietnam font-semibold mb-1">Email liên hệ</div>
                        <div className="font-vietnam text-lg font-bold text-primary">
                          contact@lthchemistry.vn
                        </div>
                      </div>
                      
                      <div className="bg-gold/10 rounded-lg p-4">
                        <div className="font-vietnam font-semibold mb-1">Thời gian phản hồi</div>
                        <div className="font-vietnam text-sm text-gold">
                          Trong vòng 24 giờ
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Additional Contact Info */}
        <div className="mt-16 text-center animate-fade-in">
          <Card className="max-w-2xl mx-auto border-2 border-primary/20">
            <CardContent className="p-8">
              <h3 className="font-quicksand font-bold text-xl mb-4 gradient-text">
                Thông Tin Liên Hệ Khác
              </h3>
              <div className="space-y-3">
                <div className="font-vietnam">
                  <strong>Địa chỉ:</strong> 123 Đường ABC, Quận XYZ, Hà Nội
                </div>
                <div className="font-vietnam">
                  <strong>Hotline:</strong> <span className="text-primary font-semibold">0123 456 789</span>
                </div>
                <div className="font-vietnam">
                  <strong>Giờ làm việc:</strong> Thứ 2 - Chủ nhật, 8:00 - 22:00
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;