import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { MessageCircle, Phone, Calendar, MessagesSquare } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const ContactSection = () => {
  const [activeTab, setActiveTab] = useState("zalo");
  const { toast } = useToast();

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text).then(() => {
      toast({
        title: "Đã sao chép!",
        description: `${label} đã được sao chép vào bộ nhớ tạm`,
      });
    });
  };

  return (
    <section id="contact" className="py-20 bg-secondary/50">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
            Sẵn Sàng Bứt Phá?{" "}
            <span className="gradient-text">Kết Nối Với Thầy Ngay!</span>
          </h2>
          <p className="font-vietnam text-lg text-muted-foreground max-w-2xl mx-auto">
            Chọn kênh liên lạc phù hợp và bắt đầu hành trình chinh phục Hóa học
            cùng LTH Chemistry
          </p>
        </div>

        {/* Contact Tabs */}
        <div className="max-w-4xl mx-auto">
          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="w-full"
          >
            <TabsList className="grid w-full grid-cols-3 mb-8">
              <TabsTrigger
                value="zalo"
                className="font-vietnam font-semibold flex items-center space-x-2"
              >
                <MessageCircle className="h-4 w-4" />
                <span>Zalo</span>
              </TabsTrigger>
              <TabsTrigger
                value="messenger"
                className="font-vietnam font-semibold flex items-center space-x-2"
              >
                <MessagesSquare className="h-4 w-4" />
                <span>Messenger</span>
              </TabsTrigger>
              <TabsTrigger
                value="gmail"
                className="font-vietnam font-semibold flex items-center space-x-2"
              >
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
                      Quét mã QR hoặc tìm kiếm theo số điện thoại để liên lạc
                      nhanh chóng
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    {/* QR Code */}
                    <div className="flex flex-col items-center">
                      <div className="w-48 h-48 bg-gradient-to-br from-primary/10 to-primary-dark/10 rounded-2xl flex items-center justify-center mb-4">
                        <div className="text-center">
                          <div className="text-6xl mb-2">
                            {" "}
                            <img
                              src="/contacts/zaloqr.png"
                              alt="Thầy Lê Trung Hiếu"
                              className="w-full h-full rounded-2xl object-cover"
                            />{" "}
                          </div>
                        </div>
                      </div>
                      <p className="font-vietnam text-sm text-muted-foreground text-center">
                        Mở ứng dụng Zalo và quét mã QR để chat với thầy
                      </p>
                    </div>

                    {/* Contact Info */}
                    <div className="space-y-4">
                      <div 
                        className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-xl p-6 border border-primary/20 cursor-pointer hover:border-primary/40 transition-all duration-200"
                        onClick={() => copyToClipboard("0942225766", "Số điện thoại")}
                      >
                        <div className="flex items-center justify-center space-x-3 mb-3">
                          <div className="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center">
                            <Phone className="h-5 w-5 text-primary" />
                          </div>
                          <div className="text-center">
                            <div className="font-vietnam font-bold text-sm text-muted-foreground mb-1">
                              Số điện thoại
                            </div>
                            <div className="font-vietnam text-xl font-bold text-primary">
                              0942225766
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-xl p-6 border border-primary/20">
                        <div className="flex items-center justify-center space-x-3">
                          <div className="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center">
                            <Calendar className="h-5 w-5 text-primary" />
                          </div>
                          <div className="text-center">
                            <div className="font-vietnam font-bold text-sm text-muted-foreground mb-1">
                              Thời gian hỗ trợ
                            </div>
                            <div className="font-vietnam text-sm font-semibold text-primary">
                              Thứ 2 - Chủ nhật: 8:00 - 22:00
                            </div>
                          </div>
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
                      Chat trực tiếp qua Facebook Messenger để được tư vấn chi
                      tiết
                    </p>
                  </div>

                  <div className="max-w-md mx-auto space-y-6">
                    <div className="w-32 h-32 bg-gradient-to-br from-primary/10 to-primary-dark/10 rounded-full flex items-center justify-center mx-auto">
                      <div className="text-5xl">
                        <img
                          src="/contacts/messenger.png"
                          alt="Facebook Messenger - Liên hệ trực tiếp với thầy Lê Trung Hiếu LTH Chemistry"
                          className="w-full h-full rounded-2xl object-cover"
                          title="Chat Messenger với thầy Hiếu để được tư vấn khóa học Hóa học"
                        />
                      </div>
                    </div>

                    <div className="space-y-4">
                      <Button
                        className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-4 rounded-full text-lg"
                        onClick={() =>
                          window.open("https://m.me/thl.201", "_blank")
                        }
                      >
                        Liên hệ ngay
                      </Button>

                      <div 
                        className="bg-primary/10 rounded-lg p-4 cursor-pointer hover:bg-primary/20 transition-all duration-200"
                        onClick={() => copyToClipboard("https://www.facebook.com/lthchemistry/", "Link Facebook Page")}
                      >
                        <div className="font-vietnam font-semibold mb-1">
                          Facebook Page
                        </div>
                        <div className="font-vietnam text-sm text-muted-foreground">
                          https://www.facebook.com/lthchemistry/
                        </div>
                      </div>

                      <div 
                        className="bg-primary/10 rounded-lg p-4 cursor-pointer hover:bg-primary/20 transition-all duration-200"
                        onClick={() => copyToClipboard("https://www.facebook.com/trunghieule01/", "Link Facebook cá nhân")}
                      >
                        <div className="font-vietnam font-semibold mb-1">
                          Facebook cá nhân
                        </div>
                        <div className="font-vietnam text-sm text-muted-foreground">
                          https://www.facebook.com/trunghieule01/
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
                <CardContent className="p-8">
                  <div className="text-center mb-8">
                    <h3 className="font-quicksand font-bold text-2xl mb-2 gradient-text">
                      Kết Nối Qua Email
                    </h3>
                    <p className="font-vietnam text-muted-foreground">
                      Gửi email để được tư vấn chi tiết về khóa học và lộ trình
                      học tập
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Email Doanh Nghiệp */}
                    <div className="rounded-xl p-6 border-2 border-white bg-white hover:border-primary hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer">
                      <div className="text-center mb-4">
                        <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-3">
                          <MessageCircle className="h-6 w-6 text-primary" />
                        </div>
                        <h4 className="font-vietnam font-bold text-lg text-primary mb-1">
                          Email Doanh Nghiệp
                        </h4>
                        <p className="font-vietnam text-sm text-muted-foreground">
                          Liên hệ chính thức
                        </p>
                      </div>
                      
                      <div 
                        className="bg-gray-50 rounded-lg p-4 mb-4 border cursor-pointer hover:bg-gray-100 transition-all duration-200"
                        onClick={() => copyToClipboard("chemistrylth@gmail.com", "Email doanh nghiệp")}
                      >
                        <div className="font-vietnam text-center text-primary font-semibold break-all">
                          chemistrylth@gmail.com
                        </div>
                      </div>
                      
                      <Button
                        className="w-full gradient-bg hover:opacity-90 transition-opacity font-vietnam font-semibold py-3 rounded-full"
                        onClick={() =>
                          window.open(
                            "mailto:chemistrylth@gmail.com?subject=Tư vấn khóa học Hóa học&body=Xin chào thầy Hiếu,%0D%0A%0D%0ATôi muốn tìm hiểu về khóa học Hóa học tại LTH Chemistry.%0D%0A%0D%0AThông tin học sinh:%0D%0A- Họ tên:%0D%0A- Lớp:%0D%0A- Số điện thoại:%0D%0A- Mục tiêu học tập:%0D%0A%0D%0ACảm ơn thầy!",
                            "_blank"
                          )
                        }
                      >
                        Gửi Email Ngay
                      </Button>
                    </div>

                    {/* Email Cá Nhân */}
                    <div className="rounded-xl p-6 border-2 border-white bg-white hover:border-primary hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer">
                      <div className="text-center mb-4">
                        <div className="w-12 h-12 bg-secondary/20 rounded-full flex items-center justify-center mx-auto mb-3">
                          <MessageCircle className="h-6 w-6 text-secondary-foreground" />
                        </div>
                        <h4 className="font-vietnam font-bold text-lg text-secondary-foreground mb-1">
                          Email Cá Nhân
                        </h4>
                        <p className="font-vietnam text-sm text-muted-foreground">
                          Liên hệ trực tiếp
                        </p>
                      </div>
                      
                      <div 
                        className="bg-gray-50 rounded-lg p-4 mb-4 border cursor-pointer hover:bg-gray-100 transition-all duration-200"
                        onClick={() => copyToClipboard("letrunghieu2001@gmail.com", "Email cá nhân")}
                      >
                        <div className="font-vietnam text-center text-secondary-foreground font-semibold break-all">
                          letrunghieu2001@gmail.com
                        </div>
                      </div>
                      
                      <Button
                        variant="outline"
                        className="w-full font-vietnam font-semibold py-3 rounded-full border-2 hover:bg-secondary/10"
                        onClick={() =>
                          window.open(
                            "mailto:letrunghieu2001@gmail.com?subject=Tư vấn khóa học Hóa học&body=Xin chào thầy Hiếu,%0D%0A%0D%0ATôi muốn tìm hiểu về khóa học Hóa học tại LTH Chemistry.%0D%0A%0D%0AThông tin học sinh:%0D%0A- Họ tên:%0D%0A- Lớp:%0D%0A- Số điện thoại:%0D%0A- Mục tiêu học tập:%0D%0A%0D%0ACảm ơn thầy!",
                            "_blank"
                          )
                        }
                      >
                        Gửi Email Cá Nhân
                      </Button>
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
                  <strong>Cơ sở 1:</strong> Số 28, ngách 371/9 Kim Mã, P. Giảng
                  Võ, Hà Nội
                </div>
                <div className="font-vietnam">
                  <strong>Cơ sở 2:</strong> Số 44D, ngõ 66 Hồ Tùng Mậu, P. Phú
                  Diễn, Hà Nội
                </div>
                <div 
                  className="font-vietnam cursor-pointer hover:bg-primary/5 p-2 rounded transition-all duration-200"
                  onClick={() => copyToClipboard("0942225766", "Hotline")}
                >
                  <strong>Hotline:</strong>{" "}
                  <span className="text-primary font-semibold">0942225766</span>
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
