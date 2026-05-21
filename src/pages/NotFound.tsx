import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Helmet } from "react-helmet-async";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <>
      <Helmet>
        <title>Không tìm thấy trang | LTH Chemistry</title>
        <meta name="description" content="Trang bạn tìm không tồn tại. Quay lại trang chủ LTH Chemistry để xem các khóa học Hóa cấp 3 và luyện thi THPTQG." />
        <meta name="robots" content="noindex, follow" />
        <link rel="canonical" href={`https://lthchemistry.lovable.app${location.pathname}`} />
        <meta property="og:title" content="Không tìm thấy trang | LTH Chemistry" />
        <meta property="og:description" content="Trang bạn tìm không tồn tại. Quay lại trang chủ LTH Chemistry." />
        <meta property="og:url" content={`https://lthchemistry.lovable.app${location.pathname}`} />
      </Helmet>
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center px-4">
          <h1 className="text-6xl font-bold mb-4 text-foreground">404</h1>
          <p className="text-xl text-muted-foreground mb-6">Rất tiếc! Không tìm thấy trang bạn yêu cầu.</p>
          <a href="/" className="text-primary hover:underline font-semibold">
            Quay lại trang chủ
          </a>
        </div>
      </div>
    </>
  );
};

export default NotFound;
