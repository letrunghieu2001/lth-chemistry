import { Card, CardContent } from "@/components/ui/card";

const SEOContentSection = () => {
  return (
    <section className="py-16 bg-background/50">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="font-quicksand font-bold text-3xl md:text-4xl mb-4">
              Học Hóa Học Trực Tuyến <span className="gradient-text">Hiệu Quả</span> Cùng LTH Chemistry
            </h2>
            <p className="font-vietnam text-lg text-muted-foreground max-w-3xl mx-auto">
              Khám phá phương pháp học Hóa học hiện đại với công cụ tương tác, tài liệu phong phú và bảng tuần hoàn trực tuyến. 
              Nền tảng học tập toàn diện cho học sinh cấp 3 chuẩn bị thi THPT Quốc gia.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            <Card className="border-2 hover:border-primary/20 transition-all duration-300">
              <CardContent className="p-6">
                <h3 className="font-quicksand font-bold text-xl mb-4 text-primary">
                  Bảng Tuần Hoàn Tương Tác
                </h3>
                <p className="font-vietnam text-muted-foreground leading-relaxed">
                  Công cụ bảng tuần hoàn hóa học trực tuyến hiện đại giúp học sinh dễ dàng tra cứu thông tin các nguyên tố, 
                  tính chất hóa học và vật lý. Giao diện thân thiện, tương tác trực quan.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary/20 transition-all duration-300">
              <CardContent className="p-6">
                <h3 className="font-quicksand font-bold text-xl mb-4 text-primary">
                  Công Thức Hóa Học & Tính Toán
                </h3>
                <p className="font-vietnam text-muted-foreground leading-relaxed">
                  Bộ sưu tập công thức hóa học đầy đủ từ cơ bản đến nâng cao. Công cụ tính toán hóa học tự động 
                  giúp giải bài tập nhanh chóng và chính xác. Hỗ trợ cân bằng phương trình.
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary/20 transition-all duration-300">
              <CardContent className="p-6">
                <h3 className="font-quicksand font-bold text-xl mb-4 text-primary">
                  Tài Liệu Ôn Thi THPT
                </h3>
                <p className="font-vietnam text-muted-foreground leading-relaxed">
                  Kho tài liệu ôn thi THPT Quốc gia môn Hóa phong phú với đề thi thử, bài giảng chi tiết, 
                  video học tập và phương pháp giải bài tập từ cơ bản đến nâng cao.
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="bg-gradient-to-r from-primary/5 to-primary-dark/5 rounded-2xl p-8 border border-primary/20">
            <h3 className="font-quicksand font-bold text-2xl mb-6 text-center gradient-text">
              Phương Pháp Học Hóa Học Hiệu Quả
            </h3>
            <p className="text-center font-vietnam text-muted-foreground mb-6">
              Tìm hiểu thêm về <a href="#teacher" className="text-primary hover:underline">giảng viên chuyên nghiệp</a> và 
              <a href="#courses" className="text-primary hover:underline ml-1">các khóa học</a> tại LTH Chemistry
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h4 className="font-vietnam font-semibold text-lg mb-4 text-primary-dark">
                  Hóa Học Vô Cơ
                </h4>
                <ul className="space-y-2 font-vietnam text-muted-foreground">
                  <li>• Cấu tạo nguyên tử và bảng tuần hoàn các nguyên tố hóa học</li>
                  <li>• Liên kết hóa học: ion, cộng hóa trị, kim loại</li>
                  <li>• Phản ứng oxi hóa khử và điện phân</li>
                  <li>• Kim loại, phi kim và hợp chất</li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-vietnam font-semibold text-lg mb-4 text-primary-dark">
                  Hóa Học Hữu Cơ
                </h4>
                <ul className="space-y-2 font-vietnam text-muted-foreground">
                  <li>• Hydrocarbon: ankan, anken, ankin, benzen</li>
                  <li>• Dẫn xuất halogen, alcohol, phenol</li>
                  <li>• Aldehyde, ketone, carboxylic acid</li>
                  <li>• Ester, lipid, glucid, protein</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SEOContentSection;