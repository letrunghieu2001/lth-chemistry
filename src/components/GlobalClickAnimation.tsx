import { useEffect, useState } from 'react';

interface FlagAnimation {
  id: number;
  x: number;
  y: number;
}

const GlobalClickAnimation = () => {
  const [flags, setFlags] = useState<FlagAnimation[]>([]);

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const newFlag: FlagAnimation = {
        id: Date.now(),
        x: e.clientX,
        y: e.clientY,
      };

      setFlags(prev => [...prev, newFlag]);

      // Remove flag after animation completes
      setTimeout(() => {
        setFlags(prev => prev.filter(flag => flag.id !== newFlag.id));
      }, 1000);
    };

    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('click', handleClick);
    };
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      {flags.map(flag => (
        <div
          key={flag.id}
          className="absolute w-8 h-5 animate-[flag-fly-up_1s_ease-out_forwards]"
          style={{
            left: flag.x - 16,
            top: flag.y - 10,
          }}
        >
          <svg width="32" height="21" viewBox="0 0 32 21" xmlns="http://www.w3.org/2000/svg">
            <rect width="32" height="21" fill="#da020e"/>
            <path 
              d="M16 4.5l1.545 4.755h5l-4.045 2.94 1.545 4.755L16 14.01l-4.045 2.94 1.545-4.755L9.455 9.255h5L16 4.5z" 
              fill="#ffff00" 
              stroke="#ffff00" 
              strokeWidth="0.3"
            />
          </svg>
        </div>
      ))}
    </div>
  );
};

export default GlobalClickAnimation;